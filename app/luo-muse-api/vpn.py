"""Touch VPN cho từng tài khoản Muse.

Touch VPN đặt proxy cho CẢ trình duyệt, nên muốn mỗi tài khoản một IP thì mỗi tài khoản phải là một trình duyệt riêng
(--user-data-dir riêng, cổng CDP riêng) có nạp tiện ích. Module này:
  * tự tải tiện ích từ Chrome Web Store một lần (data/touchvpn/), nạp bằng --load-extension;
  * giữ cho mỗi tài khoản MỘT vị trí cố định (chọn ngẫu nhiên theo vùng khi gặp lần đầu), để lúc đăng nhập, xem và gen
    cùng ra một nơi — Muse dễ đăng xuất phiên khi IP đổi liên tục; chỉ đổi khi người dùng bấm "Đổi IP";
  * bật kết nối bằng cách mở trang popup của tiện ích qua CDP, chọn vị trí, bấm Connect, rồi đo IP ra ngoài.

Google Chrome từ bản 137 bỏ qua --load-extension, nên ưu tiên Microsoft Edge (Windows) / Chromium (Linux).
"""
from __future__ import annotations

import io
import json
import logging
import os
import random
import shutil
import socket
import struct
import sys
import subprocess
import threading
import time
import zipfile

import requests

from cdp import CDP, http_json

log = logging.getLogger("muse2api")

EXT_ID = "bihmplhobchoageeokmgbdihknkjbknd"
CRX_URL = ("https://clients2.google.com/service/update2/crx?response=redirect&prodversion=131.0"
           "&acceptformat=crx2,crx3&x=id%3D" + EXT_ID + "%26uc")
PANEL = f"chrome-extension://{EXT_ID}/panel/index.html"
BEST = "Best Choice"
# Vùng chọn ngẫu nhiên: lọc theo tiền tố tên vị trí trong danh sách của Touch VPN ("United States - Miami"...).
REGIONS = {
    "us": ("United States",),
    "eu": ("Czechia", "Denmark", "France", "Germany", "Ireland", "Italy", "Netherlands", "Norway", "Romania", "Spain",
           "Sweden", "Switzerland", "United Kingdom"),
    "any": (),
    "best": None,   # dùng "Best Choice" của Touch VPN cho mọi tài khoản
}
REGION_LABELS = {"us": "Mỗi tài khoản 1 nơi ngẫu nhiên ở Mỹ", "eu": "Mỗi tài khoản 1 nơi ngẫu nhiên ở châu Âu",
                 "any": "Mỗi tài khoản 1 nơi ngẫu nhiên (mọi nước)", "best": "Best Choice (Touch VPN tự chọn)"}
# Danh sách vị trí đo được từ tiện ích 5.0.23; khi đọc được danh sách thật từ trang popup thì dùng danh sách thật.
KNOWN_LOCATIONS = [
    "Australia - Sydney", "Canada - Toronto", "Czechia - Prague", "Denmark - Copenhagen", "France - Paris",
    "Germany - Frankfurt am Main", "Hong Kong - Hong Kong", "Ireland - Dublin", "Italy - Milan", "Japan - Tokyo",
    "Mexico - Mexico City", "Netherlands - Amsterdam", "Norway - Oslo", "Romania - Bucharest", "Russia - Moscow",
    "Singapore - Singapore", "Spain - Madrid", "Sweden - Stockholm", "Switzerland - Zurich", "Turkey - Istanbul",
    "Ukraine - Kyiv", "United Kingdom - London", "United Kingdom - Manchester", "United States - Los Angeles",
    "United States - Miami", "United States - New York", "United States - Newark", "United States - San Jose",
]

_JS_STATE = r"""(()=>{const t=document.body?document.body.innerText:'';
const on=[...document.querySelectorAll('div,span,a,button')].some(e=>e.children.length==0&&e.innerText&&e.innerText.trim()=='Stop'&&e.getBoundingClientRect().width>0);
let loc='';const m=t.match(/You are browsing from\s*\n\s*([^\n]+)/);if(m)loc=m[1].trim();
const rows=[...document.querySelectorAll('#Locations .row:not(.center)')].map(e=>e.innerText.trim()).filter(Boolean);
return {ready:!!document.querySelector('.location')||on,on,loc,rows};})()"""


def _state(c: CDP) -> dict:
    """Trạng thái trang popup. Mở lại hồ sơ cũ thì tiện ích nạp sau trang (trang báo "blocked"): tự tải lại trang."""
    try:
        r = c.evaluate(_JS_STATE + " ", timeout=10)
        if isinstance(r, dict) and not r.get("ready"):
            href = c.evaluate("location.href", timeout=5) or ""
            if href.startswith("chrome-error") or href in ("", "about:blank"):
                c.send("Page.navigate", {"url": PANEL}, timeout=10)
        return r if isinstance(r, dict) else {}
    except Exception:  # noqa: BLE001
        return {}


def _kill_pidfile(prof: str):
    pf = os.path.join(prof, "luo.pid")
    try:
        with open(pf) as f:
            pid = int(f.read().strip() or 0)
    except (OSError, ValueError):
        return
    if pid > 0:
        try:
            if os.name == "nt":
                subprocess.run(["taskkill", "/PID", str(pid), "/T", "/F"], capture_output=True,
                               creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0), timeout=15)
            else:
                os.kill(pid, 9)
            time.sleep(1)
        except Exception:  # noqa: BLE001
            pass
    try:
        os.unlink(pf)
    except OSError:
        pass


def fresh_profile(base: str) -> str:
    """Hồ sơ MỚI cho mỗi lần mở: Edge tắt tiện ích nạp bằng --load-extension ở lần mở lại hồ sơ cũ
    (disable_reasons 1<<24), còn hồ sơ mới thì lần nạp đầu luôn chạy. Cookie Muse do engine bơm lại mỗi lần mở.
    Dọn các hồ sơ cũ của cùng `base` (tắt tiến trình còn giữ trước)."""
    parent, name = os.path.dirname(base), os.path.basename(base)
    os.makedirs(parent, exist_ok=True)
    for d in os.listdir(parent):
        if d == name or d.startswith(name + "~"):
            old = os.path.join(parent, d)
            _kill_pidfile(old)
            shutil.rmtree(old, ignore_errors=True)
    prof = os.path.join(parent, f"{name}~{int(time.time() * 1000)}")
    os.makedirs(prof, exist_ok=True)
    return prof


def _free_port() -> int:
    s = socket.socket()
    s.bind(("127.0.0.1", 0))
    p = s.getsockname()[1]
    s.close()
    return p


class VpnError(RuntimeError):
    pass


class Vpn:
    def __init__(self, cfg):
        self.cfg = cfg
        self.dir = os.path.join(cfg.data_dir, "touchvpn")
        self.ext_dir = os.path.join(self.dir, "ext")
        self.path = os.path.join(cfg.data_dir, "vpn.json")
        self._lock = threading.RLock()
        self._dl_lock = threading.Lock()
        self._data = self._load()
        self.ips: dict[str, dict] = {}   # khoá (tài khoản / cửa sổ) -> {"ip","loc","at"}: IP đo được lần kết nối gần nhất

    # ---------------- cài đặt ----------------
    def _load(self) -> dict:
        try:
            with open(self.path, encoding="utf-8") as f:
                d = json.load(f)
        except (OSError, ValueError):
            d = {}
        d.setdefault("enabled", False)
        d.setdefault("region", "us")
        d.setdefault("loc", {})
        d.setdefault("daily", False)       # tự đổi IP mọi tài khoản mỗi `daily_hours` giờ
        d.setdefault("daily_hours", 24)
        d.setdefault("last_daily", 0)
        d.setdefault("daily_result", {})
        return d

    def _save(self):
        tmp = self.path + ".tmp"
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(self._data, f, ensure_ascii=False, indent=1)
        os.replace(tmp, self.path)

    @property
    def enabled(self) -> bool:
        return bool(self._data.get("enabled"))

    @property
    def region(self) -> str:
        r = self._data.get("region") or "us"
        return r if r in REGIONS else "us"

    def settings(self) -> dict:
        with self._lock:
            return {"enabled": self.enabled, "region": self.region, "regions": REGION_LABELS,
                    "installed": self.installed(), "browser": self.browser_exe() or "",
                    "loc": dict(self._data.get("loc") or {}), "ips": dict(self.ips),
                    "daily": bool(self._data.get("daily")), "last_daily": int(self._data.get("last_daily") or 0),
                    "daily_hours": self._hours(),
                    "next_daily": int((self._data.get("last_daily") or 0) + self._hours() * 3600) if self._data.get("daily") else 0,
                    "daily_result": dict(self._data.get("daily_result") or {})}

    HOURS_MIN, HOURS_MAX = 1, 168   # chu kỳ tự đổi IP: 1 giờ .. 7 ngày (mặc định 24 giờ)

    def _hours(self) -> int:
        try:
            return max(self.HOURS_MIN, min(self.HOURS_MAX, int(self._data.get("daily_hours") or 24)))
        except (TypeError, ValueError):
            return 24

    def daily_due(self) -> bool:
        with self._lock:
            return (self.enabled and bool(self._data.get("daily"))
                    and time.time() - float(self._data.get("last_daily") or 0) >= self._hours() * 3600)

    def mark_daily(self, result: dict | None = None, start: bool = False):
        with self._lock:
            if start:
                self._data["last_daily"] = int(time.time())
            if result is not None:
                self._data["daily_result"] = result
            self._save()

    def set(self, enabled: bool | None = None, region: str | None = None, daily: bool | None = None,
            daily_hours: int | None = None) -> dict:
        with self._lock:
            if daily_hours is not None:   # đổi chu kỳ: lần đổi tiếp = lần đổi trước + số giờ mới
                self._data["daily_hours"] = max(self.HOURS_MIN, min(self.HOURS_MAX, int(daily_hours)))
            if daily is not None and bool(daily) != bool(self._data.get("daily")):
                self._data["daily"] = bool(daily)
                if daily:   # vừa bật: lần đổi đầu sau một chu kỳ (đổi ngay thì bấm "Đổi IP" từng tài khoản)
                    self._data["last_daily"] = int(time.time())
            if enabled is not None:
                self._data["enabled"] = bool(enabled)
            if region is not None and region in REGIONS and region != self._data.get("region"):
                self._data["region"] = region
                self._data["loc"] = {}   # đổi vùng: mọi tài khoản chọn lại vị trí trong vùng mới
            self._save()
        return self.settings()

    def _pool(self, rows: list[str] | None = None) -> list[str]:
        reg = REGIONS[self.region]
        if reg is None:
            return [BEST]
        rows = [r for r in (rows or []) if r != BEST]
        pick = [r for r in rows if not reg or r.startswith(reg)]
        if not pick:   # danh sách của trang chưa tải xong / không đọc được: dùng danh sách đã biết
            pick = [r for r in KNOWN_LOCATIONS if not reg or r.startswith(reg)]
        return pick or [BEST]

    def location(self, key: str, rows: list[str] | None = None) -> str:
        """Vị trí cố định của tài khoản; chưa có (hoặc không còn hợp vùng) thì chọn ngẫu nhiên, ưu tiên nơi ít tài khoản dùng."""
        with self._lock:
            locs = self._data.setdefault("loc", {})
            pool = self._pool(rows)
            cur = locs.get(key)
            if cur in pool:
                return cur
            used = {}
            for v in locs.values():
                used[v] = used.get(v, 0) + 1
            least = min(used.get(p, 0) for p in pool)
            cur = random.choice([p for p in pool if used.get(p, 0) == least])
            locs[key] = cur
            self._save()
            return cur

    def reroll(self, key: str, exclude: set | None = None) -> str:
        """Đổi sang một vị trí khác trong vùng (nút "Đổi IP"), tránh các nơi trong `exclude` (đã thử, ra IP trùng)."""
        with self._lock:
            locs = self._data.setdefault("loc", {})
            old = locs.get(key)
            skip = set(exclude or ()) | {old}
            pool = [p for p in self._pool() if p not in skip] or [p for p in self._pool() if p != old] or self._pool()
            locs[key] = random.choice(pool)
            self._save()
            return locs[key]

    def assign(self, key: str, loc: str):
        with self._lock:
            if loc:
                self._data.setdefault("loc", {})[key] = loc
                self._save()

    def forget(self, key: str):
        with self._lock:
            if self._data.get("loc", {}).pop(key, None) is not None:
                self._save()
            self.ips.pop(key, None)

    # ---------------- tiện ích ----------------
    def installed(self) -> bool:
        return os.path.isfile(os.path.join(self.ext_dir, "manifest.json"))

    def ensure_extension(self) -> str:
        """Tải Touch VPN từ Chrome Web Store (một lần) và giải nén vào data/touchvpn/ext."""
        if self.installed():
            return self.ext_dir
        with self._dl_lock:
            if self.installed():
                return self.ext_dir
            log.info("【vpn】tải Touch VPN từ Chrome Web Store")
            r = requests.get(CRX_URL, timeout=60, allow_redirects=True)
            b = r.content
            if r.status_code != 200 or b[:4] != b"Cr24":
                raise VpnError(f"Không tải được Touch VPN (HTTP {r.status_code})")
            ver = struct.unpack("<I", b[4:8])[0]
            if ver == 3:
                off = 12 + struct.unpack("<I", b[8:12])[0]
            else:   # crx2
                off = 16 + struct.unpack("<I", b[8:12])[0] + struct.unpack("<I", b[12:16])[0]
            tmp = self.ext_dir + ".tmp"
            shutil.rmtree(tmp, ignore_errors=True)
            with zipfile.ZipFile(io.BytesIO(b[off:])) as z:
                for n in z.namelist():   # không cho đường dẫn thoát ra ngoài thư mục
                    if n.startswith(("/", "\\")) or ".." in n.replace("\\", "/").split("/"):
                        raise VpnError("Gói Touch VPN có đường dẫn lạ, bỏ qua")
                z.extractall(tmp)
            with open(os.path.join(tmp, "manifest.json"), encoding="utf-8") as f:
                man = json.load(f)
            if "proxy" not in man.get("permissions", []):
                raise VpnError("Gói tải về không phải Touch VPN")
            shutil.rmtree(self.ext_dir, ignore_errors=True)
            os.replace(tmp, self.ext_dir)
            log.info("【vpn】đã cài Touch VPN %s", man.get("version"))
            return self.ext_dir

    # Chrome for Testing: bản Chrome chính thức của Google cho tự động hoá, VẪN nhận --load-extension (Chrome thường 137+
    # thì không). Máy Linux chỉ có Google Chrome (setup.sh cài .deb) thì tự tải bản này một lần vào data/chrome-for-testing.
    CFT_INDEX = "https://googlechromelabs.github.io/chrome-for-testing/last-known-good-versions-with-downloads.json"

    def _cft_platform(self) -> str | None:
        import platform
        m = platform.machine().lower()
        if sys.platform.startswith("linux") and m in ("x86_64", "amd64"):
            return "linux64"
        if os.name == "nt":
            return "win64" if m in ("amd64", "x86_64") else None
        if sys.platform == "darwin":
            return "mac-arm64" if m == "arm64" else "mac-x64"
        return None

    def _cft_exe(self) -> str | None:
        plat = self._cft_platform()
        if not plat:
            return None
        root = os.path.join(self.cfg.data_dir, "chrome-for-testing", f"chrome-{plat}")
        name = {"linux64": "chrome", "win64": "chrome.exe"}.get(plat,
               os.path.join("Google Chrome for Testing.app", "Contents", "MacOS", "Google Chrome for Testing"))
        p = os.path.join(root, name)
        return p if os.path.isfile(p) else None

    def browser_exe(self) -> str | None:
        """Trình duyệt còn nhận --load-extension: Edge (Windows), Chromium, Chrome for Testing đã tải; Google Chrome 137+ thì không."""
        env = os.environ.get("LUO_VPN_BROWSER", "").strip()
        if env and (os.path.isfile(env) or shutil.which(env)):
            return env
        if os.name == "nt":
            for r in (os.environ.get("ProgramFiles(x86)"), os.environ.get("ProgramFiles"), r"C:\Program Files (x86)",
                      r"C:\Program Files"):
                if r:
                    p = os.path.join(r, "Microsoft", "Edge", "Application", "msedge.exe")
                    if os.path.isfile(p):
                        return p
        for n in ("/usr/bin/chromium", "/usr/bin/chromium-browser", "/snap/bin/chromium", "chromium", "chromium-browser",
                  "microsoft-edge", "microsoft-edge-stable"):
            w = n if os.path.isfile(n) else shutil.which(n)
            if w:
                return w
        return self._cft_exe()

    def ensure_browser(self) -> str:
        """Trình duyệt cho Touch VPN; không có thì tải Chrome for Testing (~150 MB, một lần) từ kho chính thức của Google."""
        exe = self.browser_exe()
        if exe:
            return exe
        plat = self._cft_platform()
        if not plat:
            raise VpnError("Bật Touch VPN cần Microsoft Edge hoặc Chromium (Google Chrome 137+ không nạp được tiện ích)")
        with self._dl_lock:
            exe = self._cft_exe()
            if exe:
                return exe
            idx = requests.get(self.CFT_INDEX, timeout=30).json()
            st = idx["channels"]["Stable"]
            url = next((d["url"] for d in st["downloads"]["chrome"] if d.get("platform") == plat), None)
            if not url or not url.startswith("https://storage.googleapis.com/chrome-for-testing-public/"):
                raise VpnError(f"Không tìm thấy Chrome for Testing cho {plat}")
            log.info("【vpn】tải Chrome for Testing %s (%s) cho Touch VPN", st.get("version"), plat)
            base = os.path.join(self.cfg.data_dir, "chrome-for-testing")
            tmp = base + ".tmp"
            shutil.rmtree(tmp, ignore_errors=True)
            os.makedirs(tmp, exist_ok=True)
            zp = os.path.join(tmp, "chrome.zip")
            with requests.get(url, stream=True, timeout=60) as r:
                r.raise_for_status()
                with open(zp, "wb") as f:
                    for chunk in r.iter_content(1 << 20):
                        f.write(chunk)
            with zipfile.ZipFile(zp) as z:
                for info in z.infolist():
                    n = info.filename
                    if n.startswith(("/", "\\")) or ".." in n.replace("\\", "/").split("/"):
                        raise VpnError("Gói Chrome for Testing có đường dẫn lạ, bỏ qua")
                    z.extract(info, tmp)
                    mode = (info.external_attr >> 16) & 0o777   # zipfile bỏ quyền chạy: đặt lại theo gói
                    if mode and os.name != "nt":
                        os.chmod(os.path.join(tmp, n), mode)
            os.unlink(zp)
            shutil.rmtree(base, ignore_errors=True)
            os.replace(tmp, base)
            exe = self._cft_exe()
            if not exe:
                raise VpnError("Giải nén Chrome for Testing xong nhưng không thấy tệp chạy")
            log.info("【vpn】đã cài Chrome for Testing: %s", exe)
            return exe

    def ext_args(self) -> list[str]:
        ext = self.ensure_extension()
        return [f"--load-extension={ext}", f"--disable-extensions-except={ext}",
                "--disable-features=DisableLoadExtensionCommandLineSwitch"]

    # ---------------- kết nối ----------------
    @staticmethod
    def _open_page(browser: CDP, port: int, url: str) -> tuple[str, CDP]:
        res = browser.send("Target.createTarget", {"url": url}, timeout=30)
        tid = (res.get("result") or {}).get("targetId")
        if not tid:
            raise VpnError("Không mở được trang Touch VPN")
        return tid, CDP(f"ws://127.0.0.1:{port}/devtools/page/{tid}", timeout=60)

    def _measure_ip(self, browser: CDP, port: int) -> str:
        tid, c = self._open_page(browser, port, "https://api.ipify.org/?format=json")
        try:
            for _ in range(30):
                time.sleep(0.5)
                try:
                    txt = c.js("document.body ? document.body.innerText : ''", timeout=10) or ""
                    if txt.strip().startswith("{"):
                        return json.loads(txt).get("ip") or ""
                except Exception:  # noqa: BLE001
                    pass
            return ""
        finally:
            try:
                c.close()
                browser.send("Target.closeTarget", {"targetId": tid}, timeout=10)
            except Exception:  # noqa: BLE001
                pass

    def connect(self, browser: CDP, port: int, key: str, timeout: float = 60) -> dict:
        """Bật Touch VPN trong trình duyệt (cổng CDP `port`) ở vị trí cố định của `key`. Đã bật đúng vị trí thì giữ nguyên."""
        time.sleep(1.5)   # cho tiện ích nạp xong (profile mới cài lần đầu)
        tid, c = self._open_page(browser, port, PANEL)
        try:
            st = {}
            end = time.time() + 40
            while time.time() < end:
                time.sleep(1)
                try:
                    st = _state(c)
                except Exception:  # noqa: BLE001
                    st = {}
                if st.get("ready") and (st.get("on") or len(st.get("rows") or []) > 1):
                    break
            if not st.get("ready"):
                try:
                    log.warning("【vpn】trang Touch VPN chưa sẵn sàng: %s", c.evaluate("location.href+' | '+(document.body?document.body.innerText.slice(0,200):'')", timeout=5))
                except Exception:  # noqa: BLE001
                    pass
                raise VpnError("Trình duyệt không nạp được Touch VPN (Google Chrome 137+ chặn --load-extension; cần Edge hoặc Chromium)")
            loc = self.location(key, st.get("rows") or None)
            if st.get("on") and st.get("loc") == loc:
                pass
            else:
                if st.get("on"):   # đang nối nơi khác: ngắt trước rồi chọn lại
                    c.js("[...document.querySelectorAll('div,span,a,button')].find(e=>e.children.length==0&&e.innerText&&e.innerText.trim()=='Stop'&&e.getBoundingClientRect().width>0).click()", timeout=10)
                    for _ in range(30):
                        time.sleep(0.5)
                        if not (_state(c)).get("on"):
                            break
                ok = c.js("(n=>{const r=[...document.querySelectorAll('#Locations .row:not(.center)')].find(e=>e.innerText.trim()==n);"
                          "if(!r)return false;r.click();return true;})(" + json.dumps(loc) + ")", timeout=10)
                if not ok and loc != BEST:
                    log.warning("【vpn】không thấy vị trí %s trong Touch VPN, dùng Best Choice", loc)
                time.sleep(0.8)
                c.js("(()=>{const e=[...document.querySelectorAll('.title')].find(e=>e.innerText.trim()=='Connect');if(e)e.click();return !!e;})()", timeout=10)
                end = time.time() + timeout
                while time.time() < end:
                    time.sleep(1)
                    st = _state(c)
                    if st.get("on"):
                        break
                if not st.get("on"):
                    raise VpnError(f"Touch VPN không kết nối được ({loc})")
            ip = self._measure_ip(browser, port)
            info = {"ip": ip, "loc": st.get("loc") or loc, "at": int(time.time())}
            self.ips[key] = info
            log.info("【vpn】%s -> %s (%s)", key, info["loc"], ip or "?")
            return info
        finally:
            try:
                c.close()
                browser.send("Target.closeTarget", {"targetId": tid}, timeout=10)
            except Exception:  # noqa: BLE001
                pass

    def is_on(self, browser: CDP, port: int) -> bool:
        try:
            tid, c = self._open_page(browser, port, PANEL)
        except Exception:  # noqa: BLE001
            return False
        try:
            for _ in range(20):
                time.sleep(0.5)
                st = _state(c)
                if st.get("ready"):
                    return bool(st.get("on"))
            return False
        except Exception:  # noqa: BLE001
            return False
        finally:
            try:
                c.close()
                browser.send("Target.closeTarget", {"targetId": tid}, timeout=10)
            except Exception:  # noqa: BLE001
                pass


class _AccBrowser:
    __slots__ = ("acc", "proc", "port", "cdp", "profile", "checked", "started")

    def __init__(self, acc, proc, port, cdp, profile):
        self.acc, self.proc, self.port, self.cdp, self.profile = acc, proc, port, cdp, profile
        self.checked = self.started = time.time()

    def alive(self) -> bool:
        return bool(self.proc and self.proc.poll() is None and self.cdp and self.cdp.alive)


class AccountBrowsers:
    """Mỗi tài khoản một trình duyệt ẩn riêng có Touch VPN, dùng cho phần gen (engine)."""
    RECHECK = 300.0   # giây: kiểm lại VPN còn bật không trước khi mở tab mới

    def __init__(self, cfg, vpn: Vpn):
        self.cfg, self.vpn = cfg, vpn
        self._b: dict[str, _AccBrowser] = {}
        self._locks: dict[str, threading.Lock] = {}
        self._lock = threading.Lock()

    def profile(self, acc: str) -> str:
        return os.path.join(self.cfg.profile_root, "vpn", acc)

    def _acc_lock(self, acc: str) -> threading.Lock:
        with self._lock:
            return self._locks.setdefault(acc, threading.Lock())

    def peek(self, acc: str) -> _AccBrowser | None:
        b = self._b.get(acc)
        return b if b and b.alive() else None

    def get(self, acc: str) -> tuple[_AccBrowser, bool]:
        """Trình duyệt của tài khoản (mở + bật VPN khi chưa có). Trả (browser, mới_mở)."""
        with self._acc_lock(acc):
            b = self._b.get(acc)
            if b and b.alive():
                if time.time() - b.checked > self.RECHECK:
                    b.checked = time.time()
                    if not self.vpn.is_on(b.cdp, b.port):
                        log.warning("【vpn】Touch VPN của %s bị ngắt, nối lại", acc)
                        self.vpn.connect(b.cdp, b.port, acc)
                return b, False
            if b:
                self._kill(b)
            b = self._launch(acc)
            try:
                self.vpn.connect(b.cdp, b.port, acc)
            except Exception:
                self._kill(b)
                raise
            self._b[acc] = b
            return b, True

    def _launch(self, acc: str) -> _AccBrowser:
        exe = self.vpn.ensure_browser()
        prof = fresh_profile(self.profile(acc))
        port = _free_port()
        args = [exe, "--headless=new", "--no-sandbox", "--disable-gpu", "--disable-dev-shm-usage",
                "--no-first-run", "--no-default-browser-check", "--disable-sync",
                "--autoplay-policy=no-user-gesture-required",
                "--disable-backgrounding-occluded-windows", "--disable-renderer-backgrounding",
                "--disable-background-timer-throttling",
                "--disable-features=CalculateNativeWinOcclusion,IntensiveWakeUpThrottling,DisableLoadExtensionCommandLineSwitch",
                "--window-size=1440,2400", f"--remote-debugging-port={port}", "--remote-allow-origins=*",
                f"--user-data-dir={prof}"] + [a for a in self.vpn.ext_args() if not a.startswith("--disable-features")] + ["about:blank"]
        flags = getattr(subprocess, "CREATE_NO_WINDOW", 0)
        proc = subprocess.Popen(args, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, creationflags=flags)
        try:
            with open(os.path.join(prof, "luo.pid"), "w") as f:
                f.write(str(proc.pid))
        except OSError:
            pass
        last = None
        for _ in range(120):
            if proc.poll() is not None:
                raise VpnError("Trình duyệt VPN thoát ngay khi mở")
            try:
                v = http_json(f"http://127.0.0.1:{port}/json/version", timeout=2)
                log.info("【vpn】mở trình duyệt riêng cho tài khoản %s (cổng %d)", acc, port)
                return _AccBrowser(acc, proc, port, CDP(v["webSocketDebuggerUrl"], timeout=180), prof)
            except Exception as exc:  # noqa: BLE001
                last = exc
                time.sleep(0.5)
        proc.kill()
        raise VpnError(f"Không kết nối được trình duyệt VPN: {last}")

    @staticmethod
    def _kill(b: _AccBrowser):
        try:
            b.cdp.send("Browser.close", timeout=5)
        except Exception:  # noqa: BLE001
            pass
        try:
            b.cdp.close()
        except Exception:  # noqa: BLE001
            pass
        if b.proc and b.proc.poll() is None:
            b.proc.terminate()
            try:
                b.proc.wait(timeout=8)
            except Exception:  # noqa: BLE001
                b.proc.kill()

    def change_ip(self, acc: str, tries: int = 5) -> dict:
        """Nút "Đổi IP": chọn nơi khác trong vùng, nối lại và đo IP; IP trùng IP cũ (hoặc IP tài khoản khác đang dùng)
        thì thử nơi khác (vd. New York / Newark chung dải IP). Trình duyệt VPN chưa mở thì mở luôn để IP mới có hiệu lực ngay."""
        old_ip = (self.vpn.ips.get(acc) or {}).get("ip") or ""
        others = {v.get("ip") for k, v in self.vpn.ips.items() if k != acc and k in self._b and v.get("ip")}
        with self._acc_lock(acc):
            b = self._b.get(acc)
            if not b or not b.alive():
                if b:
                    self._kill(b)
                b = self._launch(acc)
                self._b[acc] = b
            tried: set = set()
            info: dict = {}
            fallback: dict | None = None
            for i in range(max(1, tries)):
                tried.add(self.vpn.reroll(acc, exclude=tried))
                info = self.vpn.connect(b.cdp, b.port, acc)
                ip = info.get("ip") or ""
                if ip and ip != old_ip and ip not in others:
                    break
                if ip and ip != old_ip and fallback is None:
                    fallback = dict(info)   # khác IP cũ nhưng trùng tài khoản khác: giữ làm phương án cuối
                log.info("【vpn】%s: %s ra IP %s trùng, thử nơi khác (%d/%d)", acc, info.get("loc"), ip or "?", i + 1, tries)
            else:
                if fallback:   # không tìm được IP "riêng": quay về nơi cho IP khác IP cũ
                    self.vpn.assign(acc, fallback["loc"])
                    info = self.vpn.connect(b.cdp, b.port, acc)
            b.checked = time.time()
            return dict(info, old_ip=old_ip, tries=len(tried), same=bool(old_ip) and info.get("ip") == old_ip)

    def idle_since(self, acc: str) -> float:
        b = self._b.get(acc)
        return max(b.started, b.checked) if b else 0.0

    def reconnect(self, acc: str) -> dict | None:
        """Nối lại VPN theo vị trí đang lưu (sau "Đổi IP"). Trình duyệt chưa mở thì vị trí mới dùng ở lần mở sau."""
        with self._acc_lock(acc):
            b = self._b.get(acc)
            if not b or not b.alive():
                return None
            b.checked = time.time()
            return self.vpn.connect(b.cdp, b.port, acc)

    def close(self, acc: str):
        with self._acc_lock(acc):
            b = self._b.pop(acc, None)
            if b:
                self._kill(b)

    def close_all(self):
        for acc in list(self._b):
            self.close(acc)

    def accounts(self) -> list[str]:
        return [a for a, b in self._b.items() if b.alive()]
