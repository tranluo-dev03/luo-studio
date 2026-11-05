"""Muse 生成引擎：dùng phiên web thật của muse.ai (Chromium + CDP) để tạo ảnh / video / chat.

LUO 1.2.0 — cách chạy:
  * Một Chromium; mỗi tài khoản MỘT browser context (kho cookie riêng, bơm cookie một lần) chứa tối đa
    `account_parallel` tab. Mỗi tab mở trong cửa sổ riêng + giả lập focus: Chromium bóp tốc tab nền của cùng một
    cửa sổ nên trước đây các việc song song trên một tài khoản chạy lần lượt.
  * Tab được giữ ấm giữa các request (checkout / checkin), không tạo context + tải lại muse.ai mỗi lần.
  * Mở hội thoại mới qua router Next.js của trang (1–4 s), chỉ tải lại trang khi router không dùng được.
  * Gửi tin qua ô soạn tin của trang; ảnh/video tham chiếu gắn bằng DOM.setFileInputFiles (không bơm base64 qua JS).
  * Theo dõi kết quả và tải file qua RPC nội bộ của trang (page helper `window.__luo`, xem dom.py):
    sessions.get + chat.history cho biết file nào trợ lý vừa tạo (đường dẫn trên VM), fs.raw tải đúng file gốc.
    Không phụ thuộc việc trang đã vẽ <video>/<img> hay chưa, không phải cuộn danh sách ảo.
  * Đường DOM cũ (đợi phần tử đính kèm xuất hiện, fetch blob) vẫn giữ làm dự phòng khi RPC không dùng được.
"""
from __future__ import annotations

import base64
import hashlib
import json
import logging
import mimetypes
import os
import re
import shutil
import subprocess
import threading
import time
import urllib.request
import uuid

import dom
from cdp import CDP, CDPError, http_json

log = logging.getLogger("muse2api")

ATT_SEL = dom.ATTACHMENT

# Cookie bắt buộc của một phiên đăng nhập. Từ 10/2026 Muse không còn đặt hatch_gw / hatch_vml cho mọi tài khoản:
# có thì chuyển tiếp, không có không coi là hỏng.
ESSENTIAL_COOKIES = ("hatch_sess", "hatch_native_auth_device")
OPTIONAL_SESSION_COOKIES = ("hatch_gw", "hatch_vml")

NEW_THREAD_URL = "https://muse.ai/thread/new"
TERMINAL_STATUS = {"completed", "complete", "idle", "done", "failed", "error", "errored", "cancelled", "canceled",
                   "stopped", "interrupted"}
QUOTA_TEXT_RE = re.compile(r"额度不足|积分不足|out of credits|usage limit|limit reached|token limit|24-hour limit|"
                           r"budget is (?:still )?exhausted|video budget|quota (?:is )?exhausted|"
                           r"limit for the (?:last|past) 24 hours|(?:video|daily|generation) limit (?:is |has been )?reached", re.I)
REFUSAL_TEXT_RE = re.compile(r"isn.t available|not available for|can.t (?:help|create|generate|make|do)|cannot (?:help|create|generate|make)|"
                             r"unable to (?:create|generate|make|help)|against (?:my|our|the) (?:policy|policies|guidelines)|"
                             r"not able to (?:create|generate|make)|i won.t|violat", re.I)
MEDIA_REPORT_RE = re.compile(r"\.(?:webp|png|jpe?g|mp4|webm|mov)|imagine_media|deliverable|generated\s+.*(?:image|video)|"
                             r"here(?:'s| is) (?:your|the)|artifact", re.I)


class MuseAuthError(RuntimeError):
    pass


class MuseGenerationError(RuntimeError):
    pass


class _RpcUnavailable(Exception):
    """RPC nội bộ của trang không dùng được -> chuyển sang đường DOM."""


class _Tab:
    __slots__ = ("acc", "ctx", "target", "cdp", "busy", "session", "thread", "last", "broken", "owner", "stale", "uses")

    def __init__(self, acc: str, ctx: str, target: str, cdp: CDP):
        self.acc, self.ctx, self.target, self.cdp = acc, ctx, target, cdp
        self.busy = False
        self.uses = 0        # số lượt gen đã phục vụ; đủ RECYCLE_AFTER thì đóng tab, mở tab mới (trang SPA phình bộ nhớ)
        self.stale = False   # cookie của tài khoản vừa đổi: tải lại trang trước khi dùng
        self.session: str | None = None   # session của LUO (một chat Muse giữ cho nhiều request)
        self.thread: str | None = None    # mã hội thoại Muse đang mở trên tab
        self.last = time.time()
        self.broken = False
        self.owner = None


def _acc_key(account_id: str | None, cookies: dict | None) -> str:
    if account_id:
        return account_id
    sess = (cookies or {}).get("hatch_sess") or json.dumps(sorted((cookies or {}).items()))
    return "anon-" + hashlib.sha1(sess.encode()).hexdigest()[:10]


class MuseEngine:
    SESSION_TTL = 1800.0
    RECYCLE_AFTER = 40
    POLL_RPC = 1.0           # giây giữa hai lần hỏi trạng thái qua RPC (rẻ, không quét DOM)
    CHUNK = 6 << 20          # bytes mỗi lần chuyển file từ trang về (base64 ~8 MB)

    def __init__(self, cfg):
        self.cfg = cfg
        self.proc: subprocess.Popen | None = None
        self.browser: CDP | None = None
        self._log = None
        self._start_lock = threading.Lock()
        self._cond = threading.Condition()
        self._tabs: dict[str, list[_Tab]] = {}
        self._opening: dict[str, int] = {}
        self._ctx: dict[str, str] = {}
        self._ctx_sig: dict[str, str] = {}
        self._ctx_lock = threading.Lock()
        self._sessions: dict[str, _Tab] = {}
        self._local = threading.local()
        self._last_http_renew: dict[str, float] = {}
        os.makedirs(cfg.profile_dir, exist_ok=True)

    # ---------------- thread-local: tab mà luồng hiện tại đang giữ ----------------
    @property
    def _tab(self) -> _Tab | None:
        return getattr(self._local, "tab", None)

    @_tab.setter
    def _tab(self, t: _Tab | None):
        self._local.tab = t

    @property
    def page(self) -> CDP | None:
        t = self._tab
        return t.cdp if t else None

    @property
    def current_acc_id(self) -> str | None:
        t = self._tab
        return t.acc if t else None

    @property
    def per_account(self) -> int:
        return max(1, int(getattr(self.cfg, "account_parallel", 2) or 2))

    # ---------------- vòng đời trình duyệt ----------------
    def _debug_url(self):
        return f"http://127.0.0.1:{self.cfg.cdp_port}/json/version"

    def _browser_alive(self) -> bool:
        b = self.browser
        if not b or not b.alive:
            return False
        if self.proc is not None and self.proc.poll() is not None:
            return False
        return True

    def start(self):
        with self._start_lock:
            if self._browser_alive():
                return
            # Trình duyệt chết: mọi tab/context cũ vô dụng.
            self._reset_pool()
            if self.proc is None:
                try:   # dùng lại CDP còn sống (vd. API khởi động lại khi trình duyệt vẫn chạy)
                    v = http_json(self._debug_url(), timeout=1)
                    if v and "webSocketDebuggerUrl" in v:
                        self.browser = CDP(v["webSocketDebuggerUrl"], timeout=180)
                        return
                except Exception:  # noqa: BLE001
                    pass
            env = dict(os.environ)
            env.setdefault("HOME", self.cfg.home_dir)
            if self.cfg.extra_path:
                env["PATH"] = self.cfg.extra_path + os.pathsep + env.get("PATH", "")
            args = [
                self.cfg.chromium,
                "--headless=new", "--no-sandbox", "--disable-gpu",
                "--disable-dev-shm-usage", "--disable-background-networking",
                "--no-first-run", "--no-default-browser-check",
                "--autoplay-policy=no-user-gesture-required",
                # Không cho Chromium bóp tốc tab/cửa sổ nền: các việc song song trên cùng tài khoản chạy song song thật.
                "--disable-backgrounding-occluded-windows", "--disable-renderer-backgrounding",
                "--disable-background-timer-throttling",
                "--disable-features=CalculateNativeWinOcclusion,IntensiveWakeUpThrottling",
                "--window-size=1440,2400",
                f"--remote-debugging-port={self.cfg.cdp_port}",
                "--remote-allow-origins=*",
                f"--user-data-dir={self.cfg.profile_dir}",
                "about:blank",
            ]
            for lock_name in ("SingletonLock", "SingletonSocket", "SingletonCookie"):
                lp = os.path.join(self.cfg.profile_dir, lock_name)
                if os.path.exists(lp) or os.path.islink(lp):
                    try:
                        os.unlink(lp)
                    except Exception:  # noqa: BLE001
                        pass
            os.makedirs(self.cfg.data_dir, exist_ok=True)
            if self._log is None:
                self._log = open(os.path.join(self.cfg.data_dir, "chromium.log"), "ab", buffering=0)
            cwd_dir = self.cfg.home_dir if (self.cfg.home_dir and os.path.isdir(self.cfg.home_dir)) else None
            self.proc = subprocess.Popen(args, stdout=self._log, stderr=subprocess.STDOUT, env=env, cwd=cwd_dir)
            last = None
            for _ in range(180):
                try:
                    v = http_json(self._debug_url(), timeout=2)
                    self.browser = CDP(v["webSocketDebuggerUrl"], timeout=180)
                    return
                except Exception as exc:  # noqa: BLE001
                    last = exc
                    if self.proc.poll() is not None:
                        break
                    time.sleep(0.5)
            raise MuseGenerationError(f"Chromium 启动失败: {last}")

    def _reset_pool(self):
        with self._cond:
            tabs = [t for ts in self._tabs.values() for t in ts]
            self._tabs.clear()
            self._opening.clear()
            self._sessions.clear()
            self._cond.notify_all()
        with self._ctx_lock:
            self._ctx.clear()
            self._ctx_sig.clear()
        for t in tabs:
            t.broken = True
            try:
                t.cdp.close()
            except Exception:  # noqa: BLE001
                pass
        if self.browser:
            try:
                self.browser.close()
            except Exception:  # noqa: BLE001
                pass
        self.browser = None

    def stop(self):
        with self._start_lock:
            if self.browser and self.browser.alive:
                for ctx in list(self._ctx.values()):
                    try:
                        self.browser.send("Target.disposeBrowserContext", {"browserContextId": ctx}, timeout=10)
                    except Exception:  # noqa: BLE001
                        pass
            self._reset_pool()
            if self.proc and self.proc.poll() is None:
                self.proc.terminate()
                try:
                    self.proc.wait(timeout=10)
                except Exception:  # noqa: BLE001
                    self.proc.kill()
            self.proc = None

    # ---------------- context + cookie ----------------
    @staticmethod
    def _cookie_params(cookies: dict, expires: dict | None, ctx: str | None = None) -> list[dict]:
        """Không bao giờ đưa Chromium thời hạn đã qua (nó lặng lẽ bỏ cookie, mất hatch_vml)."""
        now = time.time()
        out = []
        for name, value in (cookies or {}).items():
            if not value:
                continue
            exp = (expires or {}).get(name)
            try:
                exp_val = float(exp) if exp and float(exp) > now + 3600 else now + 7 * 86400
            except (TypeError, ValueError):
                exp_val = now + 7 * 86400
            p = {"name": name, "value": value, "path": "/", "secure": True, "expires": exp_val}
            if name.startswith("__Host-"):
                p["url"] = "https://muse.ai/"   # Chromium từ chối cookie __Host- có Domain
            else:
                p["domain"] = ".muse.ai"
            out.append(p)
        return out

    def _context(self, acc: str, cookies: dict, expires: dict | None) -> str:
        sig = hashlib.sha1(json.dumps(cookies or {}, sort_keys=True).encode()).hexdigest()
        with self._ctx_lock:
            ctx = self._ctx.get(acc)
            if not ctx:
                res = self.browser.send("Target.createBrowserContext", {"disposeOnDetach": False})
                ctx = res.get("result", {}).get("browserContextId")
                if not ctx:
                    raise MuseGenerationError("Target.createBrowserContext 失败")
                self._ctx[acc] = ctx
            if self._ctx_sig.get(acc) != sig and cookies:
                self.browser.send("Storage.setCookies", {"cookies": self._cookie_params(cookies, expires),
                                                         "browserContextId": ctx}, timeout=30)
                renewed = acc in self._ctx_sig
                self._ctx_sig[acc] = sig
                if renewed and self._session_cookie_changed(acc, cookies):
                    with self._cond:
                        for t in self._tabs.get(acc, []):
                            t.stale = True
            return ctx

    def _session_cookie_changed(self, acc: str, cookies: dict) -> bool:
        """Đăng nhập lại (hatch_sess đổi) thì tab cũ có thể đang ở trang đăng nhập; gia hạn thường thì không."""
        key = "_sess_" + acc
        cur = (cookies or {}).get("hatch_sess") or ""
        prev = getattr(self, key, None)
        setattr(self, key, cur)
        return prev is not None and prev != cur

    def update_cookies(self, account_id: str, cookies: dict, expires: dict | None = None):
        """Cookie mới (gia hạn phiên) ghi thẳng vào context đang mở: tab nóng giữ nguyên, không phải đóng."""
        if not account_id or not cookies or not self._browser_alive():
            return
        with self._ctx_lock:
            has = account_id in self._ctx
        if has:
            try:
                self._context(account_id, cookies, expires)
            except Exception as exc:  # noqa: BLE001
                log.warning("cập nhật cookie vào context %s lỗi: %s", account_id, exc)

    # ---------------- tab pool ----------------
    def _open_tab(self, acc: str, ctx: str) -> _Tab:
        res = self.browser.send("Target.createTarget", {"url": "about:blank", "browserContextId": ctx, "newWindow": True})
        target = res.get("result", {}).get("targetId")
        if not target:
            raise MuseGenerationError("Target.createTarget 失败")
        cdp = CDP(f"ws://127.0.0.1:{self.cfg.cdp_port}/devtools/page/{target}", timeout=180)
        # Không bật Network/Runtime/Page domain: kênh Noise bắn hàng nghìn sự kiện WebSocket mà mỗi lệnh CDP phải đọc bỏ.
        for method, params in (("Emulation.setFocusEmulationEnabled", {"enabled": True}),
                               ("Page.setWebLifecycleState", {"state": "active"}),
                               ("Browser.setDownloadBehavior", {"behavior": "allow", "downloadPath": self.cfg.download_dir})):
            try:
                cdp.send(method, params, timeout=10)
            except Exception:  # noqa: BLE001
                pass
        return _Tab(acc, ctx, target, cdp)

    def _dispose_tab(self, t: _Tab):
        t.broken = True
        try:
            t.cdp.close()
        except Exception:  # noqa: BLE001
            pass
        if self.browser and self.browser.alive:
            try:
                self.browser.send("Target.closeTarget", {"targetId": t.target}, timeout=10)
            except Exception:  # noqa: BLE001
                pass

    def _checkout(self, acc: str, cookies: dict, expires: dict | None, session: str | None = None,
                  wait: float = 120.0) -> _Tab:
        """Mượn một tab của tài khoản: ưu tiên tab đang giữ đúng session, rồi tab rảnh không giữ chat, rồi mở tab mới
        (dưới giới hạn), cuối cùng lấy tab rảnh đang giữ chat cũ nhất. Luôn trả bằng _checkin."""
        self.start()
        ctx = self._context(acc, cookies, expires)
        deadline = time.time() + wait
        limit = self.per_account
        dead: list[_Tab] = []
        tab = None
        with self._cond:
            while True:
                tabs = self._tabs.setdefault(acc, [])
                for t in [t for t in tabs if t.broken or (not t.busy and not t.cdp.alive)]:
                    tabs.remove(t)
                    dead.append(t)
                    if t.session and self._sessions.get(t.session) is t:
                        self._sessions.pop(t.session, None)
                idle = [t for t in tabs if not t.busy]
                pick = None
                if session:
                    pick = next((t for t in idle if t.session == session), None)
                if pick is None:
                    pick = next((t for t in sorted(idle, key=lambda x: -x.last) if not t.session), None)
                can_open = len(tabs) + self._opening.get(acc, 0) < limit
                if pick is None and not can_open and idle:
                    pick = min(idle, key=lambda x: x.last)   # tab giữ chat cũ nhất: bỏ chat đó
                if pick is not None:
                    if pick.session and pick.session != session:
                        self._sessions.pop(pick.session, None)
                        pick.session = None
                    pick.busy = True
                    pick.owner = threading.current_thread().name
                    tab = pick
                    break
                if can_open:
                    self._opening[acc] = self._opening.get(acc, 0) + 1
                    break
                left = deadline - time.time()
                if left <= 0:
                    raise MuseGenerationError("等待空闲标签页超时（tài khoản đang bận hết tab）")
                self._cond.wait(timeout=min(left, 1.0))
        for t in dead:
            self._dispose_tab(t)
        if tab is None:
            try:
                tab = self._open_tab(acc, ctx)
            finally:
                with self._cond:
                    self._opening[acc] = max(0, self._opening.get(acc, 0) - 1)
                    if tab is not None:
                        tab.busy = True
                        tab.owner = threading.current_thread().name
                        self._tabs.setdefault(acc, []).append(tab)
                    self._cond.notify_all()
            log.info("【tab】mở tab %d cho tài khoản %s", len(self._tabs.get(acc, [])), acc)
        self._tab = tab
        return tab

    def _checkin(self, tab: _Tab | None = None, session: str | None = None, dispose: bool = False):
        tab = tab or self._tab
        if tab is None:
            return
        if self._tab is tab:
            self._tab = None
        if not session and tab.uses >= self.RECYCLE_AFTER:
            dispose = True
        if dispose or tab.broken or not tab.cdp.alive:
            with self._cond:
                lst = self._tabs.get(tab.acc, [])
                if tab in lst:
                    lst.remove(tab)
                if tab.session and self._sessions.get(tab.session) is tab:
                    self._sessions.pop(tab.session, None)
                self._cond.notify_all()
            self._dispose_tab(tab)
            return
        with self._cond:
            if session:
                old = self._sessions.get(session)
                if old is not None and old is not tab:
                    old.session = None
                tab.session = session
                self._sessions[session] = tab
            elif tab.session and self._sessions.get(tab.session) is tab:
                self._sessions.pop(tab.session, None)
                tab.session = None
            tab.busy = False
            tab.owner = None
            tab.last = time.time()
            self._cond.notify_all()

    def _close_page(self):
        """Tương thích: trả tab đang giữ về pool (không đóng)."""
        self._checkin(self._tab)

    def close_current_page(self, dispose: bool = False):
        """Trả tab đang giữ về pool; dispose=True khi phiên hỏng (lỗi đăng nhập...)."""
        t = self._tab
        if t is not None:
            self._checkin(t, dispose=dispose)

    # ---------------- session: giữ một chat Muse cho nhiều request ----------------
    def _reap_sessions(self):
        now = time.time()
        with self._cond:
            for sid, t in list(self._sessions.items()):
                if not t.busy and now - t.last > self.SESSION_TTL:
                    self._sessions.pop(sid, None)
                    t.session = None

    def session_account(self, sid: str | None) -> str | None:
        if not sid:
            return None
        with self._cond:
            t = self._sessions.get(sid)
            return t.acc if t else None

    def attach_session(self, sid: str, account_id: str | None = None) -> bool:
        """Có tab đang giữ session này (đúng tài khoản) và còn sống không. Việc mượn tab do generate() làm."""
        self._reap_sessions()
        with self._cond:
            t = self._sessions.get(sid)
            return bool(t and not t.broken and (not account_id or t.acc == account_id))

    def finish_session(self, sid: str, keep: bool):
        """keep=True: tab giữ chat cho request sau của cùng session; keep=False: bỏ chat (tab vẫn về pool)."""
        t = self._tab
        if t is None:
            if not keep:
                self.drop_session(sid)
            return
        self._checkin(t, session=sid if keep else None)

    def drop_session(self, sid: str) -> bool:
        with self._cond:
            t = self._sessions.pop(sid, None)
            if t is not None:
                t.session = None
                t.last = time.time()
                self._cond.notify_all()
        return t is not None

    def drop_all_sessions(self):
        with self._cond:
            for t in self._sessions.values():
                t.session = None
            self._sessions.clear()

    def pool_status(self) -> dict:
        with self._cond:
            return {acc: {"tabs": len(ts), "busy": sum(t.busy for t in ts), "sessions": sum(bool(t.session) for t in ts)}
                    for acc, ts in self._tabs.items()}

    # ---------------- trang ----------------
    def _ready(self, tab: _Tab) -> dict:
        try:
            tab.cdp.js(dom.PAGE_HELPER, timeout=20)
            return tab.cdp.js("window.__luo ? window.__luo.ready() : null", timeout=20) or {}
        except (CDPError, TimeoutError):
            raise
        except Exception:  # noqa: BLE001
            return {}

    def _wait_ready(self, tab: _Tab, timeout: float) -> bool:
        deadline = time.time() + timeout
        st: dict = {}
        while time.time() < deadline:
            try:
                st = self._ready(tab)
            except (CDPError, TimeoutError):
                if not tab.cdp.alive:
                    raise
                st = {}
            if st.get("login"):
                raise MuseAuthError("会话已被 muse.ai 登出（可能被其它登录挤掉或触发风控），请用浏览器扩展重新导入 cookie")
            if st.get("ta") and st.get("rs") == "complete" and st.get("hyd") in (None, "hydrated") and not st.get("conn"):
                return True
            time.sleep(0.1)
        return False

    def _navigate_new(self, tab: _Tab):
        tab.thread = None
        tab.cdp.send("Page.navigate", {"url": NEW_THREAD_URL}, timeout=60)
        if self._wait_ready(tab, max(20, self.cfg.login_wait)):
            return
        try:
            body = (tab.cdp.js("document.body ? document.body.innerText.slice(0,1500) : ''") or "").lower()
        except Exception:  # noqa: BLE001
            body = ""
        if re.search(r"log in|sign in|create an account|登录|use another account", body):
            raise MuseAuthError("会话已被 muse.ai 登出（可能被其它登录挤掉或触发风控），请用浏览器扩展重新导入 cookie")
        raise MuseGenerationError("muse.ai 页面加载超时（未出现聊天输入框），请检查网络后重试；未确认会话失效")

    def _new_thread(self, tab: _Tab):
        """Hội thoại trống: qua router của trang nếu đang ở muse.ai, không thì tải trang."""
        tab.thread = None
        try:
            on_muse = "muse.ai" in (tab.cdp.js("location.hostname", timeout=10) or "")
        except (CDPError, TimeoutError):
            raise
        except Exception:  # noqa: BLE001
            on_muse = False
        if on_muse:
            try:
                if tab.cdp.js(dom.FRESH_THREAD, timeout=10) is True:
                    return
                if tab.cdp.js(dom.SOFT_NEW_THREAD, timeout=10) is True:
                    end = time.time() + 8.0
                    while time.time() < end:
                        time.sleep(0.15)
                        if tab.cdp.js(dom.FRESH_THREAD, timeout=10) is True:
                            return
            except (CDPError, TimeoutError):
                if not tab.cdp.alive:
                    raise
        self._navigate_new(tab)

    def _on_thread(self, tab: _Tab, thread: str | None) -> bool:
        if not thread:
            return False
        try:
            st = self._ready(tab)
        except Exception:  # noqa: BLE001
            return False
        return bool(st.get("ta") and not st.get("conn") and (st.get("path") or "").rstrip("/") == f"/thread/{thread}")

    def ensure_page(self, cookies: dict, expires: dict | None = None, account_id: str | None = None):
        """Tab của tài khoản, đã ở muse.ai và sẵn sàng (giữ tab cho luồng hiện tại tới khi trả)."""
        acc = _acc_key(account_id, cookies)
        t = self._tab
        if t is not None and t.acc == acc and not t.broken and t.cdp.alive:
            try:
                if self._wait_ready(t, 1.5):
                    return t.cdp
            except MuseAuthError:
                raise
            except Exception:  # noqa: BLE001
                pass
        if t is not None:
            self._checkin(t)
        t = self._checkout(acc, cookies, expires)
        try:
            fresh = t.stale
            if not fresh:
                try:
                    fresh = not self._wait_ready(t, 2.0)
                except MuseAuthError:
                    fresh = True
            if fresh:
                t.stale = False
                self._navigate_new(t)
        except MuseAuthError:
            self._checkin(t, dispose=True)
            raise
        except Exception:
            self._checkin(t, dispose=not t.cdp.alive)
            raise
        return t.cdp

    def refresh(self, cookies: dict, expires: dict | None = None, account_id: str | None = None):
        acc = _acc_key(account_id, cookies)
        try:
            renewed = self.renew_session_http(cookies, expires, wake_vm=True)
            cookies = renewed.get("cookies") or cookies
            expires = renewed.get("cookies_exp") or expires
        except MuseAuthError:
            raise
        except Exception as exc:  # noqa: BLE001
            log.warning("预续签 /api/session 失败（继续尝试浏览器加载）: %s", exc)
        self.close_current_page()
        t = self._checkout(acc, cookies, expires)
        try:
            self._navigate_new(t)
        except Exception:
            self._checkin(t, dispose=True)
            raise
        return t.cdp

    def warm(self, account_id: str, cookies: dict, expires: dict | None = None) -> bool:
        """Mở sẵn một tab ấm cho tài khoản (đã tải muse.ai, đã nối VM) để request đầu không phải chờ."""
        try:
            t = self._checkout(account_id, cookies, expires, wait=5)
        except Exception as exc:  # noqa: BLE001
            log.info("【预热】bỏ qua %s: %s", account_id, exc)
            return False
        try:
            if not self._wait_ready(t, 1.0):
                self._navigate_new(t)
            return True
        except Exception as exc:  # noqa: BLE001
            log.warning("【预热】tài khoản %s lỗi: %s", account_id, exc)
            self._checkin(t, dispose=True)
            return False
        finally:
            if self._tab is t:
                self._checkin(t)

    def cleanup_account(self, account_id: str, cookies: dict, expires: dict | None = None, *, keep_threads: int = 20,
                        min_age_s: float = 1800.0, media_days: float = 2.0, dry_run: bool = False) -> dict:
        """Dọn tài khoản trên VM Muse: hội thoại cũ và file media cũ trong workspace/imagine_media.

        Tài khoản dùng lâu tích hàng trăm hội thoại (đo 2026-11-06: 180–303/tài khoản) và 400–700 file media (300–570 MB);
        mỗi lần tải trang phải nạp danh sách hội thoại, trợ lý của Muse duyệt workspace khi tìm file. Giữ lại:
        `keep_threads` hội thoại mới nhất, hội thoại trẻ hơn `min_age_s`, hội thoại đang chạy / ghim / hội thoại chính /
        đang được tab của LUO giữ. Media: chỉ file (không thư mục) trong imagine_media cũ hơn `media_days` ngày
        (Studio đã tải bản sao về máy). media_days <= 0 thì không xoá media."""
        t0 = time.time()
        try:
            t = self._checkout(account_id, cookies, expires, wait=10)
        except Exception as exc:  # noqa: BLE001
            return {"ok": False, "error": f"không mượn được tab: {exc}"}
        out: dict = {"ok": True, "dry_run": dry_run}
        try:
            if not self._wait_ready(t, 2.0):
                self._navigate_new(t)
            p = t.cdp
            p.js(dom.PAGE_HELPER, timeout=20)
            sessions = p.js("window.__luo.listSessions(30)", await_promise=True, timeout=120) or []
            if not isinstance(sessions, list):
                raise MuseGenerationError(f"sessions.list lỗi: {sessions}")
            with self._cond:
                protect = {x.thread for x in self._tabs.get(account_id, []) if x.thread}
            now_ms = time.time() * 1000
            ordered = sorted(sessions, key=lambda s: max(s.get("updated") or 0, s.get("created") or 0), reverse=True)
            victims = []
            for i, s in enumerate(ordered):
                if i < keep_threads or s.get("pinned") or s.get("primary") or s["id"] in protect:
                    continue
                if (s.get("status") or "").lower() not in TERMINAL_STATUS:
                    continue
                if now_ms - max(s.get("updated") or 0, s.get("created") or 0) < min_age_s * 1000:
                    continue
                victims.append(s["id"])
            out.update(threads_total=len(sessions), threads_delete=len(victims))
            files = []
            if media_days and media_days > 0:
                entries = p.js("window.__luo.listDir('workspace/imagine_media')", await_promise=True, timeout=120) or []
                cutoff = now_ms - media_days * 86400 * 1000
                old = [e for e in entries if isinstance(e, dict) and not e.get("dir") and e.get("mtime") and e["mtime"] < cutoff]
                files = [f"workspace/imagine_media/{e['name']}" for e in old]
                out.update(media_total=sum(1 for e in entries if isinstance(e, dict) and not e.get("dir")),
                           media_delete=len(files), media_delete_mb=round(sum(e.get("size") or 0 for e in old) / 1e6, 1))
            if not dry_run:
                done_t = done_f = 0
                for i in range(0, len(victims), 100):
                    r = p.js(f"window.__luo.deleteSessions({dom.q(victims[i:i + 100])})", await_promise=True, timeout=300) or []
                    done_t += sum(1 for x in r if isinstance(x, dict) and x.get("ok"))
                for i in range(0, len(files), 100):
                    r = p.js(f"window.__luo.deleteFiles({dom.q(files[i:i + 100])})", await_promise=True, timeout=300) or []
                    done_f += sum(1 for x in r if isinstance(x, dict) and x.get("ok"))
                out.update(threads_deleted=done_t, media_deleted=done_f)
                # Trang đang hiện danh sách cũ: lần sau mở hội thoại mới qua router, không cần tải lại.
        except MuseAuthError as exc:
            out = {"ok": False, "error": str(exc)}
        except Exception as exc:  # noqa: BLE001
            out.update(ok=False, error=f"{type(exc).__name__}: {str(exc)[:200]}")
        finally:
            self._checkin(t)
        out["seconds"] = round(time.time() - t0, 1)
        return out

    def reset_thread(self, for_chat: bool = False):
        t = self._tab
        if not t:
            return
        try:
            if for_chat:
                st = t.cdp.js(dom.CHAT_STATE_DOM, timeout=20) or {}
                if not st.get("stop") and not st.get("atts") and (st.get("agentCount") or 0) < 24 \
                        and not any(h in (st.get("tail") or "") for h in dom.STALL_HINTS):
                    return
            if t.cdp.js(dom.NEEDS_NEW_THREAD, timeout=20):
                self._new_thread(t)
        except MuseAuthError:
            raise
        except Exception:  # noqa: BLE001
            pass

    # ---------------- cookie / phiên ----------------
    @staticmethod
    def renew_session_http(cookies: dict, expires: dict | None = None, wake_vm: bool = True) -> dict:
        """Gọi muse.ai/api/session để gia hạn cookie (hatch_vml +48h, hatch_sess +30d...) và đánh thức VM.
        Sau lệnh wake, hỏi lại /api/session tối đa ~20 s để biết VM đã RUNNING thật chưa (403 cho lệnh wake khi VM
        đang chạy là bình thường)."""
        import requests
        cur_cookies = dict(cookies or {})
        cur_exp = dict(expires or {})
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36",
            "Origin": "https://muse.ai", "Referer": "https://muse.ai/thread/new", "Accept": "application/json",
            "Sec-Fetch-Site": "same-origin", "Sec-Fetch-Mode": "cors", "Sec-Fetch-Dest": "empty",
        }

        def ck():
            return "; ".join(f"{k}={v}" for k, v in cur_cookies.items() if v)

        def merge(r):
            for c in r.cookies:
                if c.value:
                    cur_cookies[c.name] = c.value
                if c.expires:
                    cur_exp[c.name] = int(float(c.expires))
        try:
            r = requests.get("https://muse.ai/api/session", headers={**headers, "Cookie": ck()}, timeout=12, allow_redirects=False)
        except requests.RequestException as exc:
            raise MuseGenerationError(f"/api/session 网络请求失败 ({type(exc).__name__})；请检查网络/代理后重试") from None
        if r.status_code == 401:
            raise MuseAuthError("会话认证失败 (/api/session HTTP 401)，请在官网确认登录后重新导入 cookie")
        if r.status_code != 200:
            hint = ("访问被拒绝，请检查出口/地区/访问限制；不能据此判定 Cookie 失效" if r.status_code == 403
                    else "上游请求未成功，请稍后重试并检查网络")
            raise MuseGenerationError(f"/api/session HTTP {r.status_code}：{hint}")
        try:
            sj = r.json()
        except ValueError:
            raise MuseGenerationError("/api/session HTTP 200 返回非 JSON；会话状态未确认") from None
        if not isinstance(sj, dict) or sj.get("status") != "assigned":
            raise MuseGenerationError("/api/session HTTP 200 未返回 assigned 会话；请在官网检查账号/工作区状态")
        merge(r)
        vm_id, vm_state = sj.get("vm_id"), sj.get("vm_state")
        wake_ok = None
        if wake_vm and vm_id and vm_state != "DISABLED":
            if vm_state == "RUNNING":
                wake_ok = True
            else:
                try:
                    requests.post("https://muse.ai/api/hatch/vm/wake", headers={**headers, "Cookie": ck()},
                                  json={"vm_id": vm_id, "retry_count": 0, "connect_attempt_id": str(uuid.uuid4())}, timeout=8)
                except Exception:  # noqa: BLE001
                    pass
                end = time.time() + 20
                while time.time() < end:
                    time.sleep(2)
                    try:
                        r2 = requests.get("https://muse.ai/api/session", headers={**headers, "Cookie": ck()}, timeout=8,
                                          allow_redirects=False)
                        if r2.status_code == 200:
                            merge(r2)
                            vm_state = (r2.json() or {}).get("vm_state") or vm_state
                            if vm_state == "RUNNING":
                                wake_ok = True
                                break
                    except Exception:  # noqa: BLE001
                        pass
                if wake_ok is None:
                    wake_ok = False
        return {"ok": sj.get("status") == "assigned", "status": sj.get("status"), "vm_id": vm_id, "vm_state": vm_state,
                "wake_ok": wake_ok, "cookies": cur_cookies, "cookies_exp": cur_exp}

    def read_cookies(self) -> dict[str, dict]:
        """Cookie hiện tại của context tài khoản đang giữ (gồm cả httpOnly)."""
        t = self._tab
        if not t or not self.browser:
            return {}
        try:
            msg = self.browser.send("Storage.getCookies", {"browserContextId": t.ctx}, timeout=20)
        except Exception:  # noqa: BLE001
            return {}
        out: dict[str, dict] = {}
        for c in (msg.get("result", {}).get("cookies") or []):
            if not str(c.get("domain", "")).endswith("muse.ai"):
                continue
            name = c.get("name")
            if not name:
                continue
            try:
                exp = int(float(c.get("expires", -1)))
            except (TypeError, ValueError):
                exp = -1
            out[name] = {"value": c.get("value", ""), "expires": exp}
        return out

    # ---------------- hạn mức (Settings -> Usage) ----------------
    def _click_point(self, x: int, y: int):
        for t in ("mousePressed", "mouseReleased"):
            self.page.send("Input.dispatchMouseEvent", {"type": t, "x": x, "y": y, "button": "left", "clickCount": 1})

    def _escape(self):
        for _ in range(2):
            for t in ("keyDown", "keyUp"):
                self.page.send("Input.dispatchKeyEvent", {"type": t, "key": "Escape", "code": "Escape",
                                                          "windowsVirtualKeyCode": 27, "nativeVirtualKeyCode": 27})
            time.sleep(0.1)

    def _quota_click(self, expr: str, timeout: float = 8.0) -> bool:
        end = time.time() + timeout
        while time.time() < end:
            raw = self.page.js(expr)
            if isinstance(raw, str) and raw.startswith("{"):
                pt = json.loads(raw)
                self._click_point(pt["x"], pt["y"])
                return True
            time.sleep(0.15)
        return False

    def quota(self, cookies: dict, expires: dict | None = None, account_id: str | None = None) -> dict:
        """Đọc Settings -> Usage trên một tab rảnh của tài khoản; tự trả tab khi xong."""
        held = self._tab is not None
        self.ensure_page(cookies, expires, account_id=account_id)
        try:
            self._escape()
            if not self._quota_click(dom.QUOTA_SETTINGS_ENTRY):
                raise MuseGenerationError("找不到 Settings 按钮")
            if not self._quota_click(dom.QUOTA_MENU_ITEM):
                raise MuseGenerationError("Settings 菜单未弹出")
            txt = ""
            end = time.time() + 12
            while time.time() < end:
                txt = self.page.js(dom.QUOTA_DIALOG_TEXT) or ""
                if "used" in txt or "Usage" in txt or "已用" in txt or "使用" in txt:
                    break
                time.sleep(0.25)
            return self._parse_quota(txt)
        finally:
            try:
                self._escape()
            except Exception:  # noqa: BLE001
                pass
            if not held:
                self.close_current_page()

    @staticmethod
    def _parse_quota(txt: str) -> dict:
        lines = [ln.strip() for ln in (txt or "").split("\n") if ln.strip()]
        out: dict = {"raw": "\n".join(lines[:40])}
        for ln in lines:
            if re.match(r"^(.+?)\s*plan$", ln, re.I):
                out["plan"] = ln
                break
        m = re.search(r"Weekly limit resets? on (.+)", txt or "")
        if m:
            out["weekly_reset"] = m.group(1).strip()
        m = re.search(r"(\d+)%\s*used", txt or "")
        if m:
            out["weekly_used_pct"] = int(m.group(1))
        m = re.search(r"(\d+)%\s*used\s*\(([^)]+)\)", txt or "")
        if m:
            out["extra_used_pct"] = int(m.group(1))
            out["extra_left"] = m.group(2).strip()
        if "Never expires" in (txt or ""):
            out["extra_expires"] = "never"
        out["found"] = bool(out.get("plan") or "weekly_used_pct" in out)
        return out

    # ---------------- gửi tin ----------------
    def _send(self, prompt: str) -> str:
        p = self.page
        try:
            rect = p.js("(function(){var t=document.querySelector('textarea');if(!t)return null;t.scrollIntoView({block:'center'});"
                        "t.focus();var r=t.getBoundingClientRect();return JSON.stringify({x:Math.round(r.left+r.width/2),"
                        "y:Math.round(r.top+r.height/2)});})()")
        except Exception:  # noqa: BLE001
            rect = None
        if not rect:
            raise MuseGenerationError("找不到聊天输入框")
        c = json.loads(rect)
        for t in ("mousePressed", "mouseReleased"):
            p.send("Input.dispatchMouseEvent", {"type": t, "x": c["x"], "y": c["y"], "button": "left", "clickCount": 1})
        val_len = p.js(dom.fill_input(prompt)) or 0
        if not val_len and len(prompt) < 500:
            p.send("Input.insertText", {"text": prompt})
            p.js(dom.fill_input(prompt))
        clicked = "no-button"
        end = time.time() + 3.0
        while time.time() < end:
            res = p.js(dom.CLICK_SEND)
            if res == "clicked":
                clicked = "clicked"
                break
            time.sleep(0.06)
        if clicked != "clicked":
            for combo in (1, 0):
                for t in ("keyDown", "char", "keyUp"):
                    params = {"type": t, "key": "Enter", "code": "Enter", "windowsVirtualKeyCode": 13,
                              "nativeVirtualKeyCode": 13, "modifiers": combo}
                    if t == "char":
                        params["text"] = params["unmodifiedText"] = "\r"
                    p.send("Input.dispatchKeyEvent", params)
                time.sleep(0.8)
                if self._textarea_len() == 0:
                    clicked = "enter-sent"
                    break
        return clicked

    def _textarea_len(self) -> int:
        try:
            return int(self.page.js(dom.INPUT_LEN) or 0)
        except Exception:  # noqa: BLE001
            return 0

    # ---------------- tham chiếu ----------------
    @staticmethod
    def _sniff_image_mime(b64: str, declared: str) -> str:
        """Nhận loại file theo nội dung (Muse không nhận 'reference_image.octet-stream')."""
        d = (declared or "").lower()
        try:
            head = base64.b64decode((b64 or "")[:64] + "=" * (-len((b64 or "")[:64]) % 4))[:16]
        except Exception:  # noqa: BLE001
            return declared if d.startswith(("image/", "video/", "audio/")) else "image/png"
        return MuseEngine._sniff_bytes(head, declared)

    @staticmethod
    def _sniff_bytes(head: bytes, declared: str = "") -> str:
        d = (declared or "").lower()
        if head[4:8] == b"ftyp":
            brand = head[8:12]
            if brand in (b"M4A ", b"M4B ", b"M4P "):
                return "audio/mp4"
            if brand == b"qt  ":
                return "video/quicktime"
            if brand in (b"avif", b"avis"):
                return "image/avif"
            if brand not in (b"heic", b"heix", b"mif1", b"msf1"):
                return "video/mp4"
        if head[:4] == b"\x1a\x45\xdf\xa3":
            return "video/webm"
        if head[:4] == b"RIFF" and head[8:12] == b"WAVE":
            return "audio/wav"
        if head[:3] == b"ID3" or (len(head) > 1 and head[0] == 0xFF and (head[1] & 0xE0) == 0xE0):
            return "audio/mpeg"
        if head[:4] == b"OggS":
            return "audio/ogg"
        if head[:4] == b"fLaC":
            return "audio/flac"
        if head.startswith(b"\x89PNG"):
            return "image/png"
        if head.startswith(b"\xff\xd8\xff"):
            return "image/jpeg"
        if head[:4] == b"RIFF" and head[8:12] == b"WEBP":
            return "image/webp"
        if head[:4] == b"GIF8":
            return "image/gif"
        return declared if d.startswith(("image/", "video/", "audio/")) else "image/png"

    @staticmethod
    def _normalize_image(img: str) -> tuple[str, str]:
        b64, mime = MuseEngine._normalize_image_raw(img)
        return b64, MuseEngine._sniff_image_mime(b64, mime)

    @staticmethod
    def _normalize_image_raw(img: str) -> tuple[str, str]:
        """data URL / http(s) URL / đường dẫn file / base64 trần -> (base64, mime)."""
        if not img:
            return "", "image/png"
        img = str(img).strip()
        if img.startswith("data:"):
            parts = img.split(",", 1)
            mime = "image/png"
            if ";" in parts[0]:
                mime = parts[0].split(";")[0].replace("data:", "").strip()
            return (parts[1].strip() if len(parts) > 1 else ""), mime
        if img.startswith("http://") or img.startswith("https://"):
            try:
                req = urllib.request.Request(img, headers={"User-Agent": "Mozilla/5.0"})
                with urllib.request.urlopen(req, timeout=20) as resp:
                    data = resp.read()
                    return base64.b64encode(data).decode("ascii"), resp.headers.get_content_type() or "image/png"
            except Exception as e:  # noqa: BLE001
                log.warning("下载远程参考图失败: %s", e)
                return "", "image/png"
        if os.path.isfile(img):
            try:
                with open(img, "rb") as f:
                    data = f.read()
                return base64.b64encode(data).decode("ascii"), mimetypes.guess_type(img)[0] or "image/png"
            except Exception as e:  # noqa: BLE001
                log.warning("读取本地参考图失败: %s", e)
                return "", "image/png"
        return img, "image/png"

    def _clear_attachments(self):
        try:
            if self.page.js(dom.CLEAR_ATTACHMENTS):
                time.sleep(0.2)
        except Exception:  # noqa: BLE001
            pass

    def _attach_image(self, image_data) -> set[str]:
        """Gắn một hoặc nhiều tham chiếu (theo thứ tự) vào ô soạn tin. Trả sha256 các file đã gắn (để không bao giờ
        trả lại chính tham chiếu như kết quả)."""
        if not image_data:
            return set()
        sources = [x for x in (list(image_data) if isinstance(image_data, (list, tuple)) else [image_data]) if x]
        items, shas, paths = [], set(), []
        up_dir = os.path.join(self.cfg.data_dir, "uploads")
        os.makedirs(up_dir, exist_ok=True)
        for idx, src in enumerate(sources):
            b64, mime = self._normalize_image(src)
            if not b64:
                raise MuseGenerationError("参考图读取失败，已停止生成")
            try:
                raw = base64.b64decode(b64 + "=" * (-len(b64) % 4))
            except Exception:  # noqa: BLE001
                raise MuseGenerationError("参考图读取失败（base64 无效），已停止生成") from None
            shas.add(hashlib.sha256(raw).hexdigest())
            ext = {"image/jpeg": "jpg", "video/quicktime": "mov", "audio/mpeg": "mp3", "audio/mp4": "m4a"}.get(mime) \
                or (mime.split("/")[-1] if "/" in mime else "png")
            kind = "video" if mime.startswith("video/") else ("audio" if mime.startswith("audio/") else "image")
            name = f"reference_{kind}_{idx + 1}.{ext}" if len(sources) > 1 else f"reference_{kind}.{ext}"
            fdir = os.path.join(up_dir, uuid.uuid4().hex[:12])
            os.makedirs(fdir, exist_ok=True)
            fpath = os.path.join(fdir, name)
            with open(fpath, "wb") as f:
                f.write(raw)
            paths.append(os.path.abspath(fpath))
            items.append({"b64": b64, "mime": mime, "name": name})
        self._local.upload_dirs = [os.path.dirname(p) for p in paths]
        self._clear_attachments()
        expected = len(items)
        ok = False
        try:   # đường chính: như người dùng chọn file (không bơm hàng chục MB base64 qua Runtime.evaluate)
            r = self.page.send("Runtime.evaluate", {"expression": dom.FILE_INPUT_EXPR, "returnByValue": False}, timeout=20)
            obj = ((r.get("result") or {}).get("result") or {}).get("objectId")
            if obj:
                # setFileInputFiles chỉ có tác dụng khi DOM domain đang bật (kiểm chứng trên trang thật).
                self.page.send("DOM.enable", timeout=20)
                try:
                    self.page.send("DOM.setFileInputFiles", {"objectId": obj, "files": paths}, timeout=60)
                finally:
                    try:
                        self.page.send("DOM.disable", timeout=10)
                    except Exception:  # noqa: BLE001
                        pass
                ok = self._wait_attached(expected, 15.0)
        except Exception as exc:  # noqa: BLE001
            log.info("DOM.setFileInputFiles không dùng được (%s) — gắn bằng DataTransfer", exc)
        if not ok:
            self._clear_attachments()
            res = self.page.js(dom.inject_files(items))
            if not (isinstance(res, dict) and res.get("ok")):
                raise MuseGenerationError("附加参考图失败，已停止生成")
            ok = self._wait_attached(expected, 15.0)
        if not ok:
            n = 0
            try:
                n = int(self.page.js(dom.ATTACHED_COUNT) or 0)
            except Exception:  # noqa: BLE001
                pass
            if n:
                raise MuseGenerationError(f"参考图上传未全部确认（{n}/{expected}），已停止生成")
            raise MuseGenerationError("参考图上传未确认，已停止生成")
        return shas

    def _wait_attached(self, expected: int, timeout: float) -> bool:
        end = time.time() + timeout
        while time.time() < end:
            try:
                n = int(self.page.js(dom.ATTACHED_COUNT) or 0)
                up = int(self.page.js(dom.UPLOADING) or 0)
            except Exception:  # noqa: BLE001
                n, up = 0, 0
            if n >= expected and up <= 0:
                time.sleep(0.3)
                return True
            time.sleep(0.2)
        return False

    def _cleanup_uploads(self):
        for d in getattr(self._local, "upload_dirs", None) or []:
            shutil.rmtree(d, ignore_errors=True)
        self._local.upload_dirs = []

    # ---------------- RPC trong trang ----------------
    def _rpc_state(self, thread: str, after: int, limit: int = 40) -> dict:
        self.page.js(dom.PAGE_HELPER, timeout=20)
        r = self.page.js(f"window.__luo.state({dom.q(thread)}, {int(after)}, {int(limit)})", await_promise=True, timeout=45)
        if not isinstance(r, dict):
            raise _RpcUnavailable(f"state trả về {type(r).__name__}")
        if not r.get("ok"):
            raise _RpcUnavailable(r.get("err") or "state lỗi")
        return r

    def _rpc_ready(self) -> bool:
        try:
            self.page.js(dom.PAGE_HELPER, timeout=20)
            return bool(self.page.js("window.__luo.rpcReady()", timeout=10))
        except Exception:  # noqa: BLE001
            return False

    def _thread_id(self, timeout: float) -> str | None:
        end = time.time() + timeout
        while time.time() < end:
            try:
                tid = self.page.js("window.__luo ? window.__luo.thread() : null", timeout=10)
                if not tid:
                    self.page.js(dom.PAGE_HELPER, timeout=10)
                    tid = self.page.js("window.__luo.thread()", timeout=10)
            except Exception:  # noqa: BLE001
                tid = None
            if tid:
                return tid
            time.sleep(0.15)
        return None

    def _deny_approvals(self) -> list:
        try:
            self.page.js(dom.PAGE_HELPER, timeout=20)
            denied = self.page.js("window.__luo.denyApprovals()", await_promise=True, timeout=30) or []
        except Exception:  # noqa: BLE001
            return []
        for what in denied:
            log.info("【approval】đã tự từ chối yêu cầu phê duyệt của Muse: %s", what)
        return denied

    def _wait_media_rpc(self, thread: str, base_seq: int, expect: str, timeout: float, *, on_progress=None,
                        stop_event=None, exclude: set[str] | None = None, timing: dict | None = None) -> dict | None:
        """Đợi trợ lý tạo file `expect` trong hội thoại `thread` (chỉ xét sự kiện có seq > base_seq).

        Timeout mềm: còn đang chạy thì chờ thêm tới 1,5 lần (tối đa +5 phút) — bỏ cuộc lúc đó làm mất kết quả về sau
        và lần thử lại phải tạo lại từ đầu. Trả lời chỉ có chữ: hỏi xin file đúng 1 lần trước khi báo lỗi."""
        exclude = set(exclude or ())
        t0 = time.time()
        hard = timeout + min(300.0, timeout * 0.5)
        grace = 8.0 if expect == "video" else 4.0
        first_seen: dict[str, float] = {}
        text_done_at = None
        asked = False
        errors = 0
        polls = 0
        status = None
        last_any = t0
        seen_assistant = False
        while True:
            elapsed = time.time() - t0
            running = status is not None and status not in TERMINAL_STATUS
            if elapsed >= timeout and not (running and elapsed < hard):
                if running:
                    log.warning("%s vẫn đang tạo sau %.0fs; bỏ cuộc", expect, elapsed)
                return None
            if stop_event is not None and stop_event.is_set():
                raise MuseGenerationError("客户端已断开连接，终止生成任务")
            try:
                st = self._rpc_state(thread, base_seq, 40)
                errors = 0
            except _RpcUnavailable:
                errors += 1
                if errors >= 6:
                    raise
                time.sleep(self.POLL_RPC)
                continue
            polls += 1
            status = (st.get("status") or "").lower() or None
            events = st.get("events") or []
            if events:
                last_any = time.time()
            exclude.update(p for p in (st.get("uploads") or []) if p)
            cands = []
            for ev in events:
                if ev.get("role") == "user":
                    continue
                if ev.get("role") == "assistant" or ev.get("media"):
                    seen_assistant = True
                for m in ev.get("media") or []:
                    if m.get("kind") == expect and m.get("path") not in exclude:
                        cands.append((ev, m))
            now = time.time()
            if cands:
                ev, m = cands[-1]
                first_seen.setdefault(m["path"], now)
                if timing is not None:
                    timing.setdefault("media_seen", now)
                    timing.setdefault("muse_media_ms", ev.get("at"))
                settle = 0.0 if expect == "video" else 1.5
                if status in TERMINAL_STATUS or now - first_seen[m["path"]] >= settle:
                    m["event_at"] = ev.get("at")
                    return m
            if on_progress:
                try:
                    on_progress(min(92, int(25 + (now - t0) / max(timeout, 1) * 70)))
                except Exception:  # noqa: BLE001
                    pass
            if polls % 4 == 0 and status not in TERMINAL_STATUS:
                self._deny_approvals()
            texts = [ev.get("text") or "" for ev in events if ev.get("role") == "assistant" and ev.get("text")]
            last_text = texts[-1] if texts else ""
            if status in TERMINAL_STATUS and not cands and seen_assistant:
                if QUOTA_TEXT_RE.search(last_text):
                    raise MuseGenerationError(f"账号额度不足 / Muse báo hết hạn mức: {last_text[:400]}")
                if text_done_at is None:
                    text_done_at = now
                elif now - text_done_at >= grace:
                    if REFUSAL_TEXT_RE.search(last_text) and not MEDIA_REPORT_RE.search(last_text):
                        raise MuseGenerationError(f"模型未生成媒体，仅返回文本: {last_text[:400]}")
                    if not asked:
                        # Trợ lý hay để file trong workspace (sau khi xử lý hậu kỳ, hoặc khi nhận ra yêu cầu lặp lại):
                        # xin gắn file một lần rẻ hơn nhiều so với tạo lại.
                        log.info("【media】%s chưa được gắn (chỉ có chữ) — hỏi xin file trong chat: %.120s", expect, last_text)
                        self._clear_attachments()
                        self._send(f"Please attach the final {expect} file here in the chat, as a single attachment.")
                        asked, text_done_at, status = True, None, None
                        base_seq = max(base_seq, int(st.get("maxSeq") or base_seq))
                        time.sleep(1.0)
                        continue
                    raise MuseGenerationError(f"模型未生成媒体，仅返回文本: {last_text[:400]}")
            else:
                text_done_at = None
            # Gửi rồi mà không có gì xảy ra (không trợ lý, không chạy): thường do tin chưa tới VM.
            if not seen_assistant and status in TERMINAL_STATUS | {None} and now - last_any > 60 and now - t0 > 60:
                tail = ""
                try:
                    tail = self.page.js("document.body ? document.body.innerText.slice(-600) : ''") or ""
                except Exception:  # noqa: BLE001
                    pass
                if any(h in tail for h in dom.STALL_HINTS):
                    raise MuseGenerationError("提示词未发出（Still sending / Delivery not confirmed），在新对话中重试")
            time.sleep(self.POLL_RPC)

    def _download_media(self, path: str) -> tuple[bytes, str]:
        p = self.page
        p.js(dom.PAGE_HELPER, timeout=20)
        last = None
        for attempt in range(3):
            info = p.js(f"window.__luo.fetchRaw({dom.q(path)})", await_promise=True, timeout=600)
            if isinstance(info, dict) and info.get("ok"):
                size, rid = int(info["size"]), info["id"]
                try:
                    parts = []
                    for start in range(0, size, self.CHUNK):
                        b64 = p.js(f"window.__luo.chunk({dom.q(rid)}, {start}, {self.CHUNK})", timeout=120)
                        if not isinstance(b64, str):
                            raise MuseGenerationError("Tải file bị thiếu dữ liệu")
                        parts.append(base64.b64decode(b64))
                    data = b"".join(parts)
                finally:
                    try:
                        p.js(f"window.__luo.free({dom.q(rid)})", timeout=20)
                    except Exception:  # noqa: BLE001
                        pass
                if len(data) == size and size > 0:
                    return data, info.get("mime") or ""
                last = f"thiếu dữ liệu {len(data)}/{size}"
            else:
                last = (info or {}).get("err") if isinstance(info, dict) else str(info)
            time.sleep(1.5 * (attempt + 1))
        raise MuseGenerationError(f"未能取回生成结果 (fs.raw): {last}")

    # ---------------- đường DOM (dự phòng) ----------------
    def attachments(self) -> list[dict]:
        try:
            st = self.page.js(dom.CHAT_STATE_DOM) or {}
            return st.get("atts") or []
        except Exception:  # noqa: BLE001
            return []

    def _wait_attachment(self, baseline_sources: set, timeout: float, expect: str, on_progress=None,
                         base_agent_cnt: int = 0, base_att_cnt: int = 0, stop_event=None, **_kw) -> dict | None:
        t0 = time.time()
        hard = timeout + min(300.0, timeout * 0.5)
        stable_src, stable_n = "", 0
        last_txt, txt_stable = "", 0
        while True:
            elapsed = time.time() - t0
            st = {}
            try:
                st = self.page.js(dom.CHAT_STATE_DOM) or {}
            except Exception:  # noqa: BLE001
                pass
            busy = bool(st.get("stop"))
            if elapsed >= timeout and not (busy and elapsed < hard):
                return None
            if stop_event is not None and stop_event.is_set():
                raise MuseGenerationError("客户端已断开连接，终止生成任务")
            if st.get("approval"):
                self._deny_approvals()
            atts = st.get("atts") or []
            match = []
            for a in atts:
                src, v = a.get("src") or "", a.get("vSrc") or ""
                if expect == "video":
                    ok = bool(a.get("hasVideo") or v or src.endswith((".mp4", ".webm", ".mov")))
                else:
                    ok = ("image" in (a.get("tid") or "").lower()) or (not a.get("hasVideo") and not src.endswith((".mp4", ".webm", ".mov")))
                if ok:
                    match.append(a)
            att = match[-1] if match else None
            if att:
                check = (att.get("vSrc") or (att.get("src") if (att.get("src") or "").endswith((".mp4", ".webm", ".mov")) else "")) \
                    if expect == "video" else att.get("src")
                if check and check not in baseline_sources:
                    if (att.get("w") or 0) > 0 and (att.get("h") or 0) > 0:
                        return att
                    if check == stable_src:
                        stable_n += 1
                    else:
                        stable_src, stable_n = check, 0
                    if stable_n >= 1:
                        return att
            if on_progress:
                try:
                    on_progress(min(92, int(25 + elapsed)))
                except Exception:  # noqa: BLE001
                    pass
            tail = st.get("tail") or ""
            if QUOTA_TEXT_RE.search(tail) and not busy:
                raise MuseGenerationError(f"账号额度不足: {tail[-300:]}")
            cnt, txt = st.get("agentCount") or 0, st.get("lastText") or ""
            if cnt > base_agent_cnt and txt and not busy and len(atts) <= base_att_cnt and not MEDIA_REPORT_RE.search(txt):
                if txt == last_txt:
                    txt_stable += 1
                else:
                    last_txt, txt_stable = txt, 0
                if txt_stable >= 15 and elapsed > 8.0:
                    raise MuseGenerationError(f"模型未生成媒体，仅返回文本: {txt[:400]}")
            else:
                txt_stable = 0
            time.sleep(0.6)

    def extract_bytes(self, src: str, expect: str = "image", retries: int = 4):
        last = "未知"
        for _ in range(retries):
            raw = self.page.js(dom.fetch_blob_b64(src), await_promise=True, timeout=600)
            try:
                info = json.loads(raw) if isinstance(raw, str) else (raw or {})
            except Exception:  # noqa: BLE001
                info = {"ok": False, "err": f"解析失败 {str(raw)[:150]}"}
            if info.get("ok"):
                return base64.b64decode(info["b64"]), info.get("mime", ""), src
            last = info.get("err", "未知")
            time.sleep(2)
        raise MuseGenerationError(f"未能取回生成结果: {last}")

    def _confirm_sent_dom(self, base_user: int, base_agent: int, timeout: float) -> bool:
        end = time.time() + timeout
        while time.time() < end:
            try:
                st = self.page.js(dom.CHAT_STATE_DOM) or {}
            except Exception:  # noqa: BLE001
                st = {}
            if st.get("stop") or (st.get("users") or 0) > base_user or (st.get("agentCount") or 0) > base_agent:
                return True
            time.sleep(0.4)
        return False

    # ---------------- luồng chính ----------------
    def generate(self, cookies: dict, prompt: str, expect: str = "image",
                 timeout: int = 240, expires: dict | None = None, account_id: str | None = None,
                 on_progress=None, reference_image=None, stop_event=None, session: str | None = None) -> dict:
        """Tạo một ảnh/video. Giữ tab cho luồng hiện tại khi trả về (app gọi finish_session / close_current_page)."""
        T: dict = {"t0": time.time()}
        acc = _acc_key(account_id, cookies)
        held = self._tab
        if held is not None and (held.acc != acc or (session and held.session != session)):
            self._checkin(held)
        tab = self._tab or self._checkout(acc, cookies, expires, session=session)
        tab.uses += 1
        T["checkout"] = time.time()
        reused = bool(session) and not tab.stale and tab.session == session and tab.thread and self._on_thread(tab, tab.thread)
        if not reused:
            fresh = tab.stale
            if not fresh:
                try:
                    fresh = not self._wait_ready(tab, 1.0)
                except MuseAuthError:
                    fresh = True   # tab cũ còn ở trang đăng nhập: tải lại với cookie hiện tại rồi mới kết luận
            if fresh:
                tab.stale = False
                self._navigate_new(tab)
            else:
                self._new_thread(tab)
        T["thread_ready"] = time.time()
        use_rpc = self._rpc_ready()
        base_seq = 0
        known: set[str] = set()
        if reused and use_rpc:
            try:
                st = self._rpc_state(tab.thread, 0, 80)
                base_seq = int(st.get("maxSeq") or 0)
                for ev in st.get("events") or []:
                    for m in ev.get("media") or []:
                        known.add(m.get("path"))
            except _RpcUnavailable:
                use_rpc = False
        dom_base = {}
        try:
            dom_base = self.page.js(dom.CHAT_STATE_DOM) or {}
        except Exception:  # noqa: BLE001
            pass
        baseline_sources = {a.get(k) for a in (dom_base.get("atts") or []) for k in ("src", "vSrc") if a.get(k)}
        ref_shas: set[str] = set()
        try:
            if reference_image:
                ref_shas = self._attach_image(reference_image)
            else:
                self._clear_attachments()
            T["attached"] = time.time()
            how = self._send(prompt)
            if how not in ("clicked", "enter-sent"):
                raise MuseGenerationError("提示词发送未确认，已停止生成")
            T["sent"] = time.time()
            thread = tab.thread if reused else self._thread_id(12.0)
            confirmed = False
            if use_rpc and thread:
                end = time.time() + 25
                while time.time() < end:
                    try:
                        st = self._rpc_state(thread, base_seq, 10)
                        if any(ev.get("role") == "user" for ev in st.get("events") or []) or (st.get("status") or "") \
                                not in TERMINAL_STATUS | {""}:
                            confirmed = True
                            for ev in st.get("events") or []:
                                if ev.get("role") == "user":
                                    T.setdefault("muse_user_ms", ev.get("at"))
                            break
                    except _RpcUnavailable:
                        use_rpc = False
                        break
                    time.sleep(0.4)
            if not confirmed:
                confirmed = self._confirm_sent_dom(dom_base.get("users") or 0, dom_base.get("agentCount") or 0,
                                                   8.0 if thread else 25.0)
            if not confirmed:
                log.warning("【发送确认】提示词未出现在对话中，重新发送一次")
                if self._textarea_len() and self._send(prompt) in ("clicked", "enter-sent") \
                        and self._confirm_sent_dom(dom_base.get("users") or 0, dom_base.get("agentCount") or 0, 20.0):
                    thread = thread or self._thread_id(8.0)
                else:
                    self._debug_dump("not-sent")
                    raise MuseGenerationError("提示词未发出（对话中没有出现该消息），在新对话中重试")
            T["confirmed"] = time.time()
            tab.thread = thread or tab.thread
            media = None
            if use_rpc and tab.thread:
                remaining = max(30.0, timeout - (time.time() - T["t0"]))
                try:
                    media = self._wait_media_rpc(tab.thread, base_seq, expect, remaining, on_progress=on_progress,
                                                 stop_event=stop_event, exclude=known, timing=T)
                    if media is None:
                        self._debug_dump("no-attachment")
                        raise MuseGenerationError("等待生成超时，未出现新的生成结果")
                except _RpcUnavailable as exc:
                    log.warning("RPC trang không dùng được (%s) — chuyển sang đường DOM", exc)
                    use_rpc = False
            if media is not None:
                for _ in range(3):
                    data, mime = self._download_media(media["path"])
                    if hashlib.sha256(data).hexdigest() not in ref_shas:
                        break
                    # Chính file tham chiếu vừa tải lên: không phải kết quả. Bỏ đường dẫn đó, đợi tiếp.
                    log.warning("【media】file nhận được trùng tham chiếu đã gửi — bỏ qua, đợi kết quả thật")
                    known.add(media["path"])
                    remaining = max(30.0, timeout - (time.time() - T["t0"]))
                    media = self._wait_media_rpc(tab.thread, base_seq, expect, remaining, on_progress=on_progress,
                                                 stop_event=stop_event, exclude=known, timing=T)
                    if media is None:
                        raise MuseGenerationError("等待生成超时，未出现新的生成结果")
                else:
                    raise MuseGenerationError("Muse chỉ trả lại tham chiếu đã gửi, không có kết quả mới")
                T["downloaded"] = time.time()
                return self._save(data, mime or media.get("mime") or "", media["path"], expect, via="rpc",
                                  w=media.get("w"), h=media.get("h"), thread=tab.thread, timing=T, event_at=media.get("event_at"))
            # ---- dự phòng: DOM ----
            remaining = max(30.0, timeout - (time.time() - T["t0"]))
            att = self._wait_attachment(baseline_sources, remaining, expect, on_progress=on_progress,
                                        base_agent_cnt=dom_base.get("agentCount") or 0,
                                        base_att_cnt=len(dom_base.get("atts") or []), stop_event=stop_event)
            if not att:
                self._debug_dump("no-attachment")
                raise MuseGenerationError("等待生成超时，未出现新的生成结果")
            T["media_seen"] = time.time()
            src = (att.get("vSrc") if expect == "video" else None) or att.get("src") or ""
            data, mime, url = self.extract_bytes(src, expect=expect)
            if hashlib.sha256(data).hexdigest() in ref_shas:
                raise MuseGenerationError("Muse chỉ trả lại tham chiếu đã gửi, không có kết quả mới")
            T["downloaded"] = time.time()
            return self._save(data, mime, url, expect, via="dom", w=att.get("w"), h=att.get("h"), thread=tab.thread, timing=T)
        finally:
            self._cleanup_uploads()

    def _save(self, data: bytes, mime: str, hint: str, expect: str, *, via: str, w=None, h=None, thread=None,
              timing: dict | None = None, event_at=None) -> dict:
        os.makedirs(self.cfg.media_dir, exist_ok=True)
        real = self._sniff_bytes(data[:16], mime)
        ext = self._pick_ext(real or mime, hint, expect)
        kind = "video" if ext in (".mp4", ".webm", ".mov", ".m4v") else "image"
        if expect == "video" and kind != "video":
            raise MuseGenerationError(f"期望生成视频，但提取成品类型为图片 ({ext})，拒绝以图片冒充视频交付")
        name = f"{uuid.uuid4().hex}{ext}"
        dst = os.path.join(self.cfg.media_dir, name)
        with open(dst, "wb") as f:
            f.write(data)
        tm = {}
        if timing:
            t0 = timing["t0"]
            for k, v in timing.items():
                if k in ("t0", "muse_user_ms", "muse_media_ms"):
                    continue
                tm[k] = round(v - t0, 2)
            if timing.get("muse_user_ms") and (event_at or timing.get("muse_media_ms")):
                tm["muse_render"] = round(((event_at or timing["muse_media_ms"]) - timing["muse_user_ms"]) / 1000.0, 2)
        return {"path": dst, "filename": name, "size": len(data), "ext": ext, "mime": real or mime, "kind": kind,
                "via": via, "attachment": hint, "w": w, "h": h, "muse_thread": thread, "timing": tm}

    @staticmethod
    def _pick_ext(mime: str, url: str, expect: str) -> str:
        m = (mime or "").lower()
        for key, ext in (("mp4", ".mp4"), ("webm", ".webm"), ("quicktime", ".mov"), ("png", ".png"), ("jpeg", ".jpg"),
                         ("jpg", ".jpg"), ("webp", ".webp"), ("gif", ".gif"), ("avif", ".avif")):
            if key in m:
                return ext
        for e in (".mp4", ".webm", ".mov", ".png", ".jpg", ".jpeg", ".webp"):
            if e in (url or "").lower():
                return ".jpg" if e == ".jpeg" else e
        return ".mp4" if expect == "video" else ".png"

    def _debug_dump(self, tag: str):
        try:
            info = self.page.js(dom.CHAT_STATE_DOM)
            info = dict(info or {})
            info["path"] = self.page.js("location.pathname")
            with open(os.path.join(self.cfg.data_dir, f"debug-{tag}.json"), "w", encoding="utf-8") as f:
                f.write(json.dumps(info, ensure_ascii=False)[:20000])
        except Exception:  # noqa: BLE001
            pass

    # ---------------- chat văn bản ----------------
    def _poll_chat(self) -> tuple[int, str, bool]:
        try:
            st = self.page.js(dom.CHAT_STATE_DOM) or {}
            return int(st.get("agentCount") or 0), (st.get("lastText") or "").strip(), bool(st.get("stop"))
        except Exception:  # noqa: BLE001
            return 0, "", False

    def chat_stream(self, cookies: dict, prompt: str, expires: dict | None = None,
                    timeout: int | None = None, account_id: str | None = None, stop_event=None):
        """Gửi một tin, yield phần chữ mới (stream)."""
        timeout = int(timeout or getattr(self.cfg, "chat_timeout", 300))
        self.ensure_page(cookies, expires, account_id=account_id)
        self.reset_thread(for_chat=True)
        base_agent, base_text, _ = self._poll_chat()
        self._send(prompt)
        t_sent = time.time()
        deadline = t_sent + timeout
        first_deadline = min(deadline, t_sent + 75.0)
        sent, last, stable, got_first = "", None, 0, False
        while time.time() < first_deadline:
            if stop_event is not None and stop_event.is_set():
                return
            time.sleep(0.1)
            cnt, cur, _stop = self._poll_chat()
            if not cur or (cnt <= base_agent and cur == base_text):
                if time.time() - t_sent > 45.0:
                    try:
                        tail = self.page.js("document.body.innerText.slice(-500)") or ""
                    except Exception:  # noqa: BLE001
                        tail = ""
                    if "Still sending" in tail or "Connecting..." in tail:
                        raise MuseGenerationError("云端 VM 连接超时 (Still sending)")
                continue
            delta = cur[len(sent):] if cur.startswith(sent) else cur
            if delta:
                sent = cur
                yield delta
                last = cur
                got_first = True
                break
        if not got_first:
            raise MuseGenerationError("等待助手首字响应超时")
        while time.time() < deadline:
            if stop_event is not None and stop_event.is_set():
                return
            time.sleep(0.1)
            cnt, cur, has_stop = self._poll_chat()
            if not cur:
                continue
            if cur != last:
                delta = cur[len(sent):] if cur.startswith(sent) else cur
                if delta:
                    sent = cur
                    yield delta
                last, stable = cur, 0
            else:
                stable += 1
                if not has_stop and stable >= 3:
                    return
                if has_stop and stable >= 50:
                    return
        raise MuseGenerationError("等待助手回复超时")

    def chat(self, cookies: dict, prompt: str, expires: dict | None = None,
             timeout: int | None = None, account_id: str | None = None) -> str:
        out = ""
        for chunk in self.chat_stream(cookies, prompt, expires, timeout, account_id=account_id):
            out += chunk
        return out
