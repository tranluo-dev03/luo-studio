"""Cửa sổ Chrome thật (có giao diện) cho từng tài khoản Muse.

- Đăng nhập: mở Chrome với hồ sơ TRỐNG (cookie sạch) ở muse.ai. Người dùng tự nhập email / mã. Nếu tài khoản có hộp thư
  Outlook kèm refresh_token + client_id (tuỳ chọn), LUO tự điền email, tự đọc mã OTP trong hộp thư và điền vào; bước nào
  không tự làm được (captcha, trang khác thường) thì người dùng làm tiếp bằng tay trong cùng cửa sổ. Khi phiên Muse đã được cấp
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
BATCH_ITEM_TIMEOUT = 6 * 60      # thêm theo lô: mỗi tài khoản tối đa 6 phút rồi chuyển sang dòng kế
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
        self.mail: dict | None = None    # {"email","refresh_token","client_id"}: tự điền email + tự lấy OTP

    def public(self) -> dict:
        return {"token": self.token, "mode": self.mode, "label": self.label, "account_id": self.account_id,
                "state": self.state, "message": self.message, "elapsed": int(time.time() - self.created)}


class LoginBrowsers:
    def __init__(self, cfg, store, engine):
        self.cfg, self.store, self.engine = cfg, store, engine
        self._lock = threading.Lock()
        self._sess: dict[str, _Sess] = {}
        self._batches: dict[str, dict] = {}

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

    def start_login(self, label: str = "", account_id: str | None = None, mail: dict | None = None) -> dict:
        with self._lock:
            for s in self._sess.values():   # đang có cửa sổ đăng nhập cho tài khoản này thì đưa lên trước
                if s.mode == "login" and account_id and s.account_id == account_id and s.state in ("opening", "waiting"):
                    self._front(s)
                    return s.public()
            tmp = _Sess("login", label, account_id, "")
            tmp.profile = self._login_profile(tmp.token)
            tmp.mail = dict(mail) if mail and mail.get("refresh_token") else None
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
        if tmp.mail:
            tmp.message = f"Đã mở Chrome. Đang tự điền {tmp.mail['email']}…"
            threading.Thread(target=self._auto_login, args=(tmp,), daemon=True, name="muse-autologin").start()
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

    # ---------------- tự đăng nhập bằng hộp thư Outlook (tuỳ chọn) ----------------
    _JS_EMAIL = r"""(() => {
      const vis = e => { const r = e.getBoundingClientRect(); return r.width > 0 && r.height > 0 && !e.disabled; };
      const lab = i => ((i.labels && i.labels[0] && i.labels[0].textContent) || '') + ' ' + (i.getAttribute('aria-label') || '') + ' ' + (i.placeholder || '');
      const el = [...document.querySelectorAll('input')].filter(vis).find(i => i.type === 'email' || /email/i.test(lab(i)));
      if (!el) return false;
      el.focus(); if (el.select) el.select(); return true; })()"""
    _JS_SUBMIT = r"""(() => {
      const vis = e => { const r = e.getBoundingClientRect(); return r.width > 0 && r.height > 0; };
      const a = document.activeElement, f = a && a.form;
      let b = f && [...f.querySelectorAll('button')].find(x => vis(x) && !x.disabled && (x.type === 'submit' || /continue|next|verify|log ?in|submit/i.test(x.textContent)));
      if (!b) b = [...document.querySelectorAll('button')].find(x => vis(x) && !x.disabled && /^(continue|next|verify|submit|log in)$/i.test(x.textContent.trim()));
      if (b) { b.click(); return true; }
      if (f && f.requestSubmit) { f.requestSubmit(); return true; }
      return false; })()"""
    _JS_CODE = r"""(() => {
      const vis = e => { const r = e.getBoundingClientRect(); return r.width > 0 && r.height > 0 && !e.disabled; };
      const lab = i => (i.name || '') + ' ' + (i.id || '') + ' ' + (i.placeholder || '') + ' ' + (i.getAttribute('aria-label') || '') + ' ' + ((i.labels && i.labels[0] && i.labels[0].textContent) || '');
      const ins = [...document.querySelectorAll('input')].filter(vis).filter(i => i.type !== 'hidden' && i.type !== 'email' && !/email/i.test(lab(i)));
      const one = ins.filter(i => i.maxLength === 1);
      if (one.length >= 4) { one[0].focus(); return 'multi'; }
      const el = ins.find(i => i.autocomplete === 'one-time-code' || i.inputMode === 'numeric' || i.maxLength === 6 || /code|otp|verif/i.test(lab(i)));
      if (!el) return '';
      el.focus(); if (el.select) el.select(); return 'single'; })()"""

    # Trang đã nạp xong và form email đã "sống" (React đã gắn xử lý vào ô nhập) chưa
    _JS_READY = r"""(() => {
      if (document.readyState !== 'complete') return false;
      const vis = e => { const r = e.getBoundingClientRect(); return r.width > 0 && r.height > 0 && !e.disabled; };
      const lab = i => ((i.labels && i.labels[0] && i.labels[0].textContent) || '') + ' ' + (i.getAttribute('aria-label') || '') + ' ' + (i.placeholder || '');
      const el = [...document.querySelectorAll('input')].filter(vis).find(i => i.type === 'email' || /email/i.test(lab(i)));
      if (!el) return false;
      const react = Object.keys(el).some(k => k.startsWith('__reactProps') || k.startsWith('__reactFiber'));
      const btn = el.form && [...el.form.querySelectorAll('button')].find(x => x.type === 'submit' || /continue|next/i.test(x.textContent));
      return !!(react && btn); })()"""
    _JS_EMAIL_VALUE = r"""(() => {
      const vis = e => { const r = e.getBoundingClientRect(); return r.width > 0 && r.height > 0; };
      const lab = i => ((i.labels && i.labels[0] && i.labels[0].textContent) || '') + ' ' + (i.getAttribute('aria-label') || '') + ' ' + (i.placeholder || '');
      const el = [...document.querySelectorAll('input')].filter(vis).find(i => i.type === 'email' || /email/i.test(lab(i)));
      return el ? el.value : null; })()"""
    # Đã sang bước nhập mã (có ô mã) hoặc ô email đã biến mất -> Muse đã nhận email
    _JS_PAST_EMAIL = r"""(() => {
      const vis = e => { const r = e.getBoundingClientRect(); return r.width > 0 && r.height > 0 && !e.disabled; };
      const lab = i => ((i.labels && i.labels[0] && i.labels[0].textContent) || '') + ' ' + (i.getAttribute('aria-label') || '') + ' ' + (i.placeholder || '') + ' ' + (i.name || '') + ' ' + (i.id || '');
      const ins = [...document.querySelectorAll('input')].filter(vis);
      if (ins.filter(i => i.maxLength === 1).length >= 4) return true;
      if (ins.some(i => i.autocomplete === 'one-time-code' || (/code|otp|verif/i.test(lab(i)) && !/email/i.test(lab(i))))) return true;
      return !ins.some(i => i.type === 'email' || /email/i.test(lab(i))); })()"""

    def _wait_ready(self, s: _Sess, page: CDP, timeout: float = 40) -> bool:
        """Chờ trang Muse nạp xong và form email sẵn sàng. Quá hạn vẫn chưa thấy dấu hiệu thì đi tiếp (trả False)."""
        end = time.time() + timeout
        while time.time() < end and s.state == "waiting" and not s.cancel.is_set():
            try:
                if page.evaluate(self._JS_READY, timeout=10):
                    time.sleep(1.5)   # để các xử lý của trang gắn nốt
                    return True
            except Exception:  # noqa: BLE001
                pass
            time.sleep(0.8)
        return False

    def _fill_email(self, page: CDP, email: str) -> bool:
        """Gõ email vào ô và kiểm tra giá trị đã vào thật; không thì ép giá trị bằng setter gốc + sự kiện input."""
        page.evaluate(self._JS_EMAIL, timeout=10)           # focus + chọn hết nội dung cũ
        page.send("Input.insertText", {"text": email}, timeout=10)
        time.sleep(0.5)
        if (page.evaluate(self._JS_EMAIL_VALUE, timeout=10) or "").strip() == email:
            return True
        js = ("(() => { const vis = e => { const r = e.getBoundingClientRect(); return r.width > 0 && r.height > 0; };"
              "const el = [...document.querySelectorAll('input')].filter(vis).find(i => i.type === 'email' || /email/i.test((i.getAttribute('aria-label') || '') + (i.placeholder || '')));"
              "if (!el) return false; const set = Object.getOwnPropertyDescriptor(HTMLInputElement.prototype, 'value').set;"
              "set.call(el, " + json.dumps(email) + "); el.dispatchEvent(new Event('input', {bubbles: true})); "
              "el.dispatchEvent(new Event('change', {bubbles: true})); return true; })()")
        page.evaluate(js, timeout=10)
        time.sleep(0.5)
        return (page.evaluate(self._JS_EMAIL_VALUE, timeout=10) or "").strip() == email

    def _page(self, s: _Sess) -> CDP:
        targets = http_json(f"http://127.0.0.1:{s.port}/json/list", timeout=5)
        pages = [t for t in targets if t.get("type") == "page"]
        page = next((t for t in pages if "muse.ai" in t.get("url", "")), None) or (pages[0] if pages else None)
        if not page:
            raise RuntimeError("không thấy tab muse.ai")
        return CDP(page["webSocketDebuggerUrl"], timeout=30)

    def _wait_js(self, s: _Sess, page: CDP, expr: str, timeout: float):
        end = time.time() + timeout
        while time.time() < end and s.state == "waiting" and not s.cancel.is_set():
            try:
                v = page.evaluate(expr, timeout=10)
                if v:
                    return v
            except Exception:  # noqa: BLE001
                pass
            time.sleep(1)
        return None

    def _press_enter(self, page: CDP):
        for t in ("keyDown", "keyUp"):
            page.send("Input.dispatchKeyEvent", {"type": t, "key": "Enter", "code": "Enter", "windowsVirtualKeyCode": 13,
                                                 **({"text": "\r"} if t == "keyDown" else {})}, timeout=10)

    def _auto_login(self, s: _Sess):
        """Điền email -> bấm tiếp tục -> đọc OTP trong Outlook -> điền mã. Lỗi ở bước nào thì báo, người dùng làm tay tiếp."""
        import outlook_otp
        page = None
        manual = " Bạn làm tiếp bằng tay trong cửa sổ Chrome."

        def new_token(rt: str):   # Microsoft cấp refresh_token mới: giữ bản mới nhất để không hết hạn
            s.mail["refresh_token"] = rt
            if s.account_id:
                try:
                    self.store.update_account(s.account_id, mail=dict(s.mail))
                except Exception:  # noqa: BLE001
                    pass

        try:
            time.sleep(2)
            page = self._page(s)
            since = 0.0
            sent = False
            for attempt in range(1, 4):   # tối đa 3 lần: chưa sang bước nhập mã thì tải lại trang và điền lại
                if s.state != "waiting" or s.cancel.is_set():
                    return
                s.message = f"Đang chờ trang Muse tải xong… (lần {attempt}/3)"
                if not self._wait_js(s, page, self._JS_EMAIL, 60):
                    if s.state == "waiting":
                        s.message = "Không thấy ô email trên trang Muse." + manual
                    return
                self._wait_ready(s, page)
                s.message = f"Đang điền {s.mail['email']}… (lần {attempt}/3)"
                if not self._fill_email(page, s.mail["email"]):
                    s.message = f"Không điền được email vào ô (lần {attempt}/3), tải lại trang…"
                    page.evaluate("location.reload()", timeout=10)
                    time.sleep(3)
                    continue
                since = time.time()
                if not page.evaluate(self._JS_SUBMIT, timeout=10):
                    self._press_enter(page)
                # Xác nhận Muse thật sự đã nhận email (sang bước nhập mã) trước khi đi đợi thư
                end = time.time() + 20
                while time.time() < end and s.state == "waiting" and not s.cancel.is_set():
                    try:
                        if page.evaluate(self._JS_PAST_EMAIL, timeout=10):
                            sent = True
                            break
                    except Exception:  # noqa: BLE001
                        pass
                    time.sleep(1)
                if sent:
                    break
                s.message = f"Muse chưa nhận email (lần {attempt}/3), tải lại trang và thử lại…"
                page.evaluate("location.reload()", timeout=10)
                time.sleep(3)
            if not sent:
                if s.state == "waiting":
                    s.message = "Muse không chuyển sang bước nhập mã sau 3 lần thử (trang tải chậm hoặc có captcha)." + manual
                return
            s.message = f"Đã gửi mã tới {s.mail['email']}, đang đợi thư trong hộp Outlook…"
            try:
                code = outlook_otp.wait_code(s.mail, since, timeout=180, cancel=s.cancel, on_new_token=new_token)
            except outlook_otp.MailAuthError as exc:
                s.message = f"{exc}." + manual
                return
            if s.state != "waiting":
                return
            if not code:
                s.message = "Quá 3 phút chưa thấy thư mã của Muse (Hộp thư đến / Junk)." + manual
                return
            kind = self._wait_js(s, page, self._JS_CODE, 30)
            if not kind:
                s.message = f"Đã lấy được mã {code} nhưng không thấy ô nhập mã. Hãy tự nhập mã này vào cửa sổ Chrome."
                return
            if kind == "multi":
                for ch in code:
                    page.send("Input.insertText", {"text": ch}, timeout=10)
                    time.sleep(0.12)
            else:
                page.send("Input.insertText", {"text": code}, timeout=10)
            s.message = f"Đã điền mã {code}, đang chờ Muse xác nhận…"
            time.sleep(2.5)   # nhiều form tự gửi khi đủ 6 số; còn ô mã thì bấm nút / Enter
            if s.state == "waiting" and page.evaluate(self._JS_CODE, timeout=10):
                if not page.evaluate(self._JS_SUBMIT, timeout=10):
                    self._press_enter(page)
        except Exception as exc:  # noqa: BLE001
            log.info("tự đăng nhập Muse lỗi: %s", exc)
            if s.state == "waiting":
                s.message = f"Tự đăng nhập bị lỗi ({str(exc)[:120]})." + manual
        finally:
            if page:
                page.close()


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
                                            expiry_anchor=int(time.time()), cookies_exp=exp or None, mail=s.mail)
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
            if s.mail:
                self.store.update_account(acc["id"], mail=s.mail)
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

    # ---------------- thêm tài khoản theo lô (mỗi dòng email|password|refresh_token|client_id) ----------------
    def start_batch(self, lines: list[str], item_timeout: int = BATCH_ITEM_TIMEOUT) -> dict:
        """Đăng nhập lần lượt từng dòng (mỗi lần một cửa sổ Chrome, tự điền email + OTP). Email đã có trong LUO thì
        đăng nhập lại chính tài khoản đó thay vì thêm trùng."""
        import outlook_otp
        with self._lock:
            for b in self._batches.values():
                if b["state"] == "running":
                    raise RuntimeError("Đang có một lô khác chạy. Đợi xong hoặc huỷ lô đó trước.")
        items, seen = [], set()
        for n, raw in enumerate(lines, 1):
            line = raw.strip().lstrip("﻿")
            if not line or line.startswith("#"):
                continue
            mail = outlook_otp.parse_line(line)
            if not mail:
                items.append({"line": n, "email": line.split("|")[0][:60], "state": "skipped",
                              "message": "Sai định dạng (cần email|password|refresh_token|client_id)"})
                continue
            key = mail["email"].lower()
            if key in seen:
                items.append({"line": n, "email": mail["email"], "state": "skipped", "message": "Trùng dòng phía trên"})
                continue
            seen.add(key)
            items.append({"line": n, "email": mail["email"], "state": "pending", "message": "", "_mail": mail})
        if not any(i["state"] == "pending" for i in items):
            raise ValueError("Không có dòng hợp lệ nào")
        b = {"token": uuid.uuid4().hex[:16], "state": "running", "items": items, "created": time.time(),
             "cancel": threading.Event(), "current": None, "timeout": max(120, int(item_timeout))}
        with self._lock:
            self._batches[b["token"]] = b
        threading.Thread(target=self._run_batch, args=(b,), daemon=True, name="muse-login-batch").start()
        return self.get_batch(b["token"])

    def get_batch(self, token: str) -> dict | None:
        b = self._batches.get(token)
        if not b:
            return None
        items = [{k: v for k, v in i.items() if not k.startswith("_")} for i in b["items"]]
        cnt = {st: sum(1 for i in items if i["state"] == st) for st in ("pending", "running", "done", "failed", "skipped")}
        return {"token": b["token"], "state": b["state"], "items": items, "counts": cnt,
                "elapsed": int(time.time() - b["created"])}

    def cancel_batch(self, token: str) -> bool:
        b = self._batches.get(token)
        if not b:
            return False
        b["cancel"].set()
        if b.get("current"):
            self.cancel(b["current"])
        return True

    def _find_by_email(self, email: str) -> str | None:
        email = email.lower()
        for a in self.store.list_accounts():
            if (a.get("mail_email") or "").lower() == email or (a.get("label") or "").lower() == email:
                return a["id"]
        return None

    def _run_batch(self, b: dict):
        try:
            for it in b["items"]:
                if it["state"] != "pending":
                    continue
                if b["cancel"].is_set():
                    it["state"], it["message"] = "skipped", "Đã huỷ lô"
                    continue
                mail = it["_mail"]
                aid = self._find_by_email(mail["email"])
                it["state"] = "running"
                it["message"] = "Đăng nhập lại tài khoản đã có…" if aid else "Đang mở Chrome…"
                r = self.start_login(label=mail["email"], account_id=aid, mail=mail)
                if r["state"] == "error":
                    it["state"], it["message"] = "failed", r["message"]
                    continue
                b["current"] = r["token"]
                deadline = time.time() + b["timeout"]
                while True:
                    s = self._sess.get(r["token"])
                    if not s:
                        it["state"], it["message"] = "failed", "Mất phiên đăng nhập"
                        break
                    it["message"] = s.message
                    if s.state == "done":
                        it["state"], it["account_id"] = "done", s.account_id
                        break
                    if s.state in ("error", "closed", "cancelled"):
                        it["state"] = "failed"
                        break
                    if b["cancel"].is_set():
                        s.cancel.set()
                    elif time.time() > deadline and s.state == "waiting":
                        s.cancel.set()
                        it["message"] = f"Quá {b['timeout'] // 60} phút chưa đăng nhập xong, bỏ qua. ({s.message})"
                        it["state"] = "failed"
                        break
                    time.sleep(1.5)
                b["current"] = None
                time.sleep(3)   # đợi Chrome cũ thoát hẳn rồi mới mở cửa sổ kế
            b["state"] = "cancelled" if b["cancel"].is_set() else "done"
        except Exception as exc:  # noqa: BLE001
            log.exception("lô đăng nhập lỗi")
            b["state"] = "error"
            for it in b["items"]:
                if it["state"] in ("pending", "running"):
                    it["state"], it["message"] = "failed", str(exc)[:200]
        finally:
            for it in b["items"]:
                it.pop("_mail", None)   # không giữ refresh_token trong bộ nhớ sau khi xong

    def reap(self):
        """Bỏ các phiên đăng nhập đã kết thúc quá 10 phút (giao diện đã đọc xong kết quả)."""
        now = time.time()
        with self._lock:
            for t, s in list(self._sess.items()):
                if s.mode == "login" and s.state not in ("opening", "waiting", "saving") and now - s.created > 600:
                    self._sess.pop(t, None)

    def stop_all(self):
        for b in list(self._batches.values()):
            b["cancel"].set()
        for s in list(self._sess.values()):
            s.cancel.set()
            self._close(s)
