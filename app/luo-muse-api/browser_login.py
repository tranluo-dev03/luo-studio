"""Cửa sổ Chrome thật (có giao diện) cho từng tài khoản Muse.

- Đăng nhập: mở Chrome với hồ sơ TRỐNG (cookie sạch) ở muse.ai. Người dùng tự nhập email / mã. Khi phiên Muse đã được cấp
  (/api/session trả "assigned"), LUO đọc cookie (kể cả httpOnly, qua CDP), lưu vào tài khoản rồi tự đóng cửa sổ.
  Hồ sơ trình duyệt đó được giữ lại làm hồ sơ "xem" của tài khoản.
- Xem: mở Chrome bằng hồ sơ riêng của tài khoản, nạp cookie đang lưu trong LUO rồi mở muse.ai để xem trực tiếp các
  đoạn chat. Trong lúc cửa sổ mở, nếu Muse cấp cookie mới (gia hạn, hoặc người dùng đăng nhập lại ngay trong cửa sổ)
  thì LUO tự cập nhật cookie của tài khoản.

Mỗi cửa sổ là một tiến trình Chrome riêng (--user-data-dir riêng, cổng CDP riêng), không đụng Chrome thường của người
dùng và không đụng trình duyệt headless dùng để gen.
"""
from __future__ import annotations

import hashlib
import json
import logging
import os
import shutil
import socket
import subprocess
import threading
import time
import uuid

from cdp import CDP, http_json

log = logging.getLogger("muse2api.login")

LOGIN_TIMEOUT = 15 * 60          # chờ người dùng đăng nhập tối đa 15 phút
NEED = ("hatch_sess", "hatch_native_auth_device")


def _free_port() -> int:
    s = socket.socket()
    s.bind(("127.0.0.1", 0))
    p = s.getsockname()[1]
    s.close()
    return p


def _sig(cookies: dict) -> str:
    keep = {k: cookies.get(k) for k in ("hatch_sess", "hatch_gw", "hatch_vml", "hatch_native_auth_device")}
    return hashlib.sha1(json.dumps(keep, sort_keys=True).encode()).hexdigest()


def _browser_exe(cfg) -> str:
    """Ưu tiên Google Chrome (cửa sổ người dùng nhìn thấy), không có thì dùng trình duyệt API đang dùng (Edge / Chromium)."""
    if os.name == "nt":
        roots = [os.environ.get("ProgramFiles"), os.environ.get("ProgramFiles(x86)"), os.environ.get("LOCALAPPDATA"),
                 r"C:\Program Files", r"C:\Program Files (x86)"]
        for r in roots:
            if r:
                p = os.path.join(r, "Google", "Chrome", "Application", "chrome.exe")
                if os.path.isfile(p):
                    return p
    else:
        for n in ("google-chrome", "google-chrome-stable", "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"):
            w = n if os.path.isfile(n) else shutil.which(n)
            if w:
                return w
    return cfg.chromium


class _Sess:
    def __init__(self, mode: str, label: str, account_id: str | None, profile: str):
        self.token = uuid.uuid4().hex[:16]
        self.mode = mode                 # "login" | "view"
        self.label = label
        self.account_id = account_id
        self.profile = profile
        self.proc: subprocess.Popen | None = None
        self.port = 0
        self.browser: CDP | None = None
        self.state = "opening"           # opening | waiting | saving | done | open | closed | error | cancelled
        self.message = ""
        self.created = time.time()
        self.cancel = threading.Event()

    def public(self) -> dict:
        return {"token": self.token, "mode": self.mode, "label": self.label, "account_id": self.account_id,
                "state": self.state, "message": self.message, "elapsed": int(time.time() - self.created)}


class LoginBrowsers:
    def __init__(self, cfg, store, engine):
        self.cfg, self.store, self.engine = cfg, store, engine
        self._lock = threading.Lock()
        self._sess: dict[str, _Sess] = {}

    # ---------------- đường dẫn ----------------
    def account_profile(self, aid: str) -> str:
        return os.path.join(self.cfg.profile_root, "accounts", aid)

    def _login_profile(self, token: str) -> str:
        return os.path.join(self.cfg.profile_root, "login", token)

    # ---------------- Chrome ----------------
    def _launch(self, s: _Sess, url: str):
        os.makedirs(s.profile, exist_ok=True)
        for lock_name in ("SingletonLock", "SingletonSocket", "SingletonCookie"):
            try:
                os.unlink(os.path.join(s.profile, lock_name))
            except OSError:
                pass
        s.port = _free_port()
        args = [_browser_exe(self.cfg),
                f"--remote-debugging-port={s.port}", "--remote-allow-origins=*",
                f"--user-data-dir={s.profile}",
                "--no-first-run", "--no-default-browser-check", "--disable-sync",
                "--window-size=1280,900", "--new-window", url]
        flags = getattr(subprocess, "CREATE_NEW_PROCESS_GROUP", 0)
        s.proc = subprocess.Popen(args, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, creationflags=flags)
        last = None
        for _ in range(60):
            if s.proc.poll() is not None:
                raise RuntimeError("Chrome thoát ngay khi mở (hồ sơ có thể đang bị một cửa sổ Chrome khác giữ)")
            try:
                v = http_json(f"http://127.0.0.1:{s.port}/json/version", timeout=2)
                s.browser = CDP(v["webSocketDebuggerUrl"], timeout=30)
                return
            except Exception as exc:  # noqa: BLE001
                last = exc
                time.sleep(0.5)
        raise RuntimeError(f"Không kết nối được Chrome: {last}")

    def _alive(self, s: _Sess) -> bool:
        return bool(s.proc and s.proc.poll() is None and s.browser and s.browser.alive)

    def _read_cookies(self, s: _Sess) -> tuple[dict, dict]:
        msg = s.browser.send("Storage.getCookies", {}, timeout=15)
        cookies, exp = {}, {}
        for c in (msg.get("result", {}).get("cookies") or []):
            if not str(c.get("domain", "")).lstrip(".").endswith("muse.ai") or not c.get("name"):
                continue
            cookies[c["name"]] = c.get("value", "")
            try:
                e = int(float(c.get("expires", -1)))
            except (TypeError, ValueError):
                e = -1
            if e > 0:
                exp[c["name"]] = e
        return cookies, exp

    def _close(self, s: _Sess):
        if s.browser:
            try:
                s.browser.send("Browser.close", {}, timeout=5)
            except Exception:  # noqa: BLE001
                pass
            s.browser.close()
        if s.proc:
            try:
                s.proc.wait(timeout=10)
            except Exception:  # noqa: BLE001
                try:
                    s.proc.kill()
                    s.proc.wait(timeout=5)
                except Exception:  # noqa: BLE001
                    pass

    def _front(self, s: _Sess):
        try:
            targets = http_json(f"http://127.0.0.1:{s.port}/json/list", timeout=3)
            page = next((t for t in targets if t.get("type") == "page"), None)
            if page:
                s.browser.send("Target.activateTarget", {"targetId": page["id"]}, timeout=5)
        except Exception:  # noqa: BLE001
            pass

    # ---------------- API ----------------
    def get(self, token: str) -> dict | None:
        s = self._sess.get(token)
        return s.public() if s else None

    def cancel(self, token: str) -> bool:
        s = self._sess.get(token)
        if not s:
            return False
        s.cancel.set()
        return True

    def close_account(self, aid: str):
        """Đóng mọi cửa sổ của tài khoản (vd. trước khi xoá tài khoản)."""
        for s in list(self._sess.values()):
            if s.account_id == aid:
                s.cancel.set()

    def start_login(self, label: str = "", account_id: str | None = None) -> dict:
        with self._lock:
            for s in self._sess.values():   # đang có cửa sổ đăng nhập cho tài khoản này thì đưa lên trước
                if s.mode == "login" and account_id and s.account_id == account_id and s.state in ("opening", "waiting"):
                    self._front(s)
                    return s.public()
            tmp = _Sess("login", label, account_id, "")
            tmp.profile = self._login_profile(tmp.token)
            self._sess[tmp.token] = tmp
        shutil.rmtree(tmp.profile, ignore_errors=True)
        try:
            self._launch(tmp, self.cfg.site_url)
        except Exception as exc:  # noqa: BLE001
            tmp.state, tmp.message = "error", str(exc)[:300]
            shutil.rmtree(tmp.profile, ignore_errors=True)
            return tmp.public()
        tmp.state = "waiting"
        tmp.message = "Đã mở Chrome. Hãy đăng nhập Muse trong cửa sổ đó."
        threading.Thread(target=self._watch_login, args=(tmp,), daemon=True, name="muse-login").start()
        return tmp.public()

    def open_view(self, aid: str) -> dict:
        acc = self.store.get_account(aid)
        if not acc:
            raise KeyError(aid)
        with self._lock:
            for s in self._sess.values():
                if s.mode == "view" and s.account_id == aid and s.state == "open" and self._alive(s):
                    self._front(s)
                    return s.public()
            s = _Sess("view", acc.get("label") or aid, aid, self.account_profile(aid))
            self._sess[s.token] = s
        try:
            self._launch(s, "about:blank")
            from engine import MuseEngine
            cookies = acc.get("cookies") or {}
            if cookies:
                s.browser.send("Storage.setCookies",
                               {"cookies": MuseEngine._cookie_params(cookies, acc.get("cookies_exp"))}, timeout=15)
            blank = [t["id"] for t in http_json(f"http://127.0.0.1:{s.port}/json/list", timeout=3)
                     if t.get("type") == "page"]
            s.browser.send("Target.createTarget", {"url": self.cfg.site_url}, timeout=15)
            for tid in blank:
                try:
                    s.browser.send("Target.closeTarget", {"targetId": tid}, timeout=5)
                except Exception:  # noqa: BLE001
                    pass
        except Exception as exc:  # noqa: BLE001
            s.state, s.message = "error", str(exc)[:300]
            self._close(s)
            return s.public()
        s.state, s.message = "open", "Đang mở Muse của tài khoản."
        threading.Thread(target=self._watch_view, args=(s, _sig(cookies)), daemon=True, name="muse-view").start()
        return s.public()

    # ---------------- theo dõi ----------------
    def _verify(self, cookies: dict, exp: dict) -> dict | None:
        """Phiên đã được Muse cấp chưa. Trả cookie (đã gộp cookie Muse vừa gia hạn) hoặc None nếu chưa đăng nhập."""
        from engine import MuseAuthError, MuseEngine
        try:
            r = MuseEngine.renew_session_http(cookies, exp, wake_vm=False)
        except MuseAuthError:
            return None
        except Exception as exc:  # noqa: BLE001  (mạng / 403...): không kết luận được, đủ cookie chính thì vẫn nhận
            log.info("kiểm tra phiên khi đăng nhập không xác nhận được: %s", exc)
            return {"cookies": cookies, "cookies_exp": exp} if cookies.get("hatch_vml") else None
        return r if r.get("ok") else None

    def _watch_login(self, s: _Sess):
        deadline = time.time() + LOGIN_TIMEOUT
        last_try = ""
        try:
            while True:
                if s.cancel.is_set():
                    s.state, s.message = "cancelled", "Đã huỷ đăng nhập."
                    return
                if not self._alive(s):
                    s.state, s.message = "closed", "Cửa sổ Chrome đã đóng trước khi đăng nhập xong."
                    return
                if time.time() > deadline:
                    s.state, s.message = "error", "Quá 15 phút chưa đăng nhập xong."
                    return
                try:
                    cookies, exp = self._read_cookies(s)
                except Exception:  # noqa: BLE001
                    time.sleep(2)
                    continue
                sig = _sig(cookies)
                if all(cookies.get(n) for n in NEED) and sig != last_try:
                    last_try = sig
                    ok = self._verify(cookies, exp)
                    if ok:
                        s.state, s.message = "saving", "Đã đăng nhập, đang lưu tài khoản…"
                        time.sleep(3)   # để trang Muse nhận nốt cookie (hatch_vml...)
                        try:
                            c2, e2 = self._read_cookies(s)
                            cookies, exp = {**c2, **ok["cookies"]}, {**e2, **(ok.get("cookies_exp") or {})}
                        except Exception:  # noqa: BLE001
                            cookies, exp = ok["cookies"], ok.get("cookies_exp") or exp
                        self._save_login(s, cookies, exp)
                        return
                time.sleep(2)
        except Exception as exc:  # noqa: BLE001
            log.exception("đăng nhập Muse lỗi")
            s.state, s.message = "error", str(exc)[:300]
        finally:
            self._close(s)
            if s.state == "done" and s.account_id:
                dst = self.account_profile(s.account_id)
                for _ in range(10):   # Chrome có thể còn giữ file vài giây sau khi thoát
                    try:
                        shutil.rmtree(dst, ignore_errors=True)
                        os.makedirs(os.path.dirname(dst), exist_ok=True)
                        os.replace(s.profile, dst)
                        break
                    except OSError:
                        time.sleep(1)
            shutil.rmtree(s.profile, ignore_errors=True)

    def _save_login(self, s: _Sess, cookies: dict, exp: dict):
        exp = {k: int(v) for k, v in exp.items() if v and int(v) > 0}
        if s.account_id:
            acc = self.store.update_account(s.account_id, cookies=cookies, ok=True, note="Đăng nhập lại bằng Chrome",
                                            expiry_anchor=int(time.time()), cookies_exp=exp or None)
            if not acc:
                raise RuntimeError("Tài khoản đã bị xoá trong lúc đăng nhập")
            try:
                self.engine.update_cookies(s.account_id, cookies, exp)
            except Exception:  # noqa: BLE001
                pass
            s.message = f"Đã đăng nhập lại tài khoản {acc.get('label') or s.account_id}."
        else:
            acc = self.store.add_account(cookies, s.label, cookies_exp=exp)
            self.store.mark(acc["id"], True, "Đăng nhập bằng Chrome")
            s.account_id = acc["id"]
            s.message = f"Đã thêm tài khoản {acc.get('label') or acc['id']}."
        s.state = "done"

    def _watch_view(self, s: _Sess, base_sig: str):
        last = base_sig
        try:
            while self._alive(s) and not s.cancel.is_set():
                for _ in range(10):
                    if s.cancel.is_set() or not self._alive(s):
                        break
                    time.sleep(1)
                if s.cancel.is_set() or not self._alive(s):
                    break
                try:
                    cookies, exp = self._read_cookies(s)
                except Exception:  # noqa: BLE001
                    continue
                sig = _sig(cookies)
                # Chỉ ghi khi chính cửa sổ này nhận cookie mới từ Muse (gia hạn / đăng nhập lại), không ghi đè bằng cookie cũ.
                if sig != last and all(cookies.get(n) for n in NEED):
                    last = sig
                    acc = self.store.get_account(s.account_id)
                    if not acc:
                        break
                    merged = {**(acc.get("cookies") or {}), **cookies}
                    relogin = cookies.get("hatch_sess") != (acc.get("cookies") or {}).get("hatch_sess")
                    self.store.update_account(s.account_id, cookies=merged, cookies_exp={**(acc.get("cookies_exp") or {}), **exp},
                                              **({"ok": True, "note": "Đăng nhập lại trong cửa sổ Xem",
                                                  "expiry_anchor": int(time.time())} if relogin else {}))
                    try:
                        self.engine.update_cookies(s.account_id, merged, exp)
                    except Exception:  # noqa: BLE001
                        pass
        finally:
            if s.cancel.is_set():
                self._close(s)
            elif s.browser:
                s.browser.close()
            s.state, s.message = "closed", "Đã đóng cửa sổ."
            with self._lock:
                self._sess.pop(s.token, None)

    def reap(self):
        """Bỏ các phiên đăng nhập đã kết thúc quá 10 phút (giao diện đã đọc xong kết quả)."""
        now = time.time()
        with self._lock:
            for t, s in list(self._sess.items()):
                if s.mode == "login" and s.state not in ("opening", "waiting", "saving") and now - s.created > 600:
                    self._sess.pop(t, None)

    def stop_all(self):
        for s in list(self._sess.values()):
            s.cancel.set()
            self._close(s)
