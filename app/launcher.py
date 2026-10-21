"""LUO Studio - khởi động MỘT LẦN cho cả bộ: máy chủ API Muse (LUO-API) + ứng dụng LUO Studio.

Người dùng chỉ cần bấm "LUO Studio.bat". Trình khởi động này:
  1. tạo thư mục dữ liệu người dùng (userdata/) nếu chưa có, tách riêng khỏi mã nguồn để cập nhật không mất dữ liệu;
  2. tự sinh khoá API ngẫu nhiên lần đầu (người dùng không phải cấu hình gì);
  3. bật LUO-API ở nền (cổng trống đầu tiên từ 18610), chờ tới khi sẵn sàng;
  4. mở cửa sổ LUO Studio đã nối sẵn với API đó;
  5. khi đóng cửa sổ thì tắt API và trình duyệt con của nó.

Chạy khi phát triển:  python luo-suite/launcher.py [--no-window] [--selftest]
"""
import json, os, secrets, socket, subprocess, sys, time, urllib.request

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
HERE = os.path.dirname(os.path.abspath(__file__))
# bản đóng gói: app/launcher.py nằm cạnh app/luo-studio ...; khi phát triển: luo-suite/launcher.py, mã ở thư mục cha
APP = HERE if os.path.isdir(os.path.join(HERE, "luo-studio")) else os.path.dirname(HERE)
ROOT = os.path.dirname(APP) if os.path.basename(APP).lower() == "app" else APP
STUDIO_DIR, API_DIR = os.path.join(APP, "luo-studio"), os.path.join(APP, "luo-muse-api")
USER = os.environ.get("LUO_USERDATA") or os.path.join(ROOT, "userdata")
STUDIO_DATA, API_HOME, LOGS = os.path.join(USER, "studio"), os.path.join(USER, "api"), os.path.join(USER, "logs")
PREFERRED_PORT = int(os.environ.get("LUO_API_PORT", "18610"))
CREATE_NO_WINDOW = 0x08000000 if os.name == "nt" else 0


def say(msg):
    try:
        print(msg, flush=True)
    except Exception:  # pythonw không có stdout
        pass


def port_free(p):
    with socket.socket() as s:
        s.settimeout(0.3)
        return s.connect_ex(("127.0.0.1", p)) != 0


def pick_port(preferred):
    for p in range(preferred, preferred + 40):
        if port_free(p):
            return p
    raise RuntimeError("Không tìm được cổng trống cho API")


def http_ok(url, timeout=2):
    try:
        with urllib.request.urlopen(url, timeout=timeout) as r:
            return r.status == 200
    except Exception:
        return False


def write_env(port):
    """userdata/api/.env: khoá API sinh một lần, giữ nguyên các lần sau; cổng được cập nhật mỗi lần chạy."""
    os.makedirs(API_HOME, exist_ok=True)
    path = os.path.join(API_HOME, ".env")
    lines, key = [], ""
    if os.path.exists(path):
        for ln in open(path, encoding="utf-8").read().splitlines():
            if ln.startswith("MUSE2API_KEY="):
                key = ln.split("=", 1)[1].strip()
            if ln.split("=", 1)[0] not in ("MUSE2API_PORT", "MUSE2API_HOST") and ln.strip():
                lines.append(ln)
    if not key:
        key = secrets.token_hex(16)
        lines = [ln for ln in lines if not ln.startswith("MUSE2API_KEY=")] + [f"MUSE2API_KEY={key}"]
    lines += ["MUSE2API_HOST=127.0.0.1", f"MUSE2API_PORT={port}"]
    open(path, "w", encoding="utf-8").write("\n".join(lines) + "\n")
    return key


def prefetch_whisper(py):
    """Lần đầu: tải mô hình nhận dạng giọng (~250MB) ở nền để hậu kỳ dùng được sớm, người dùng không phải làm gì."""
    hub = os.path.join(os.environ.get("HF_HOME", ""), "hub", "models--Systran--faster-whisper-small.en")
    if os.path.isdir(hub):
        return
    try:
        log = open(os.path.join(LOGS, "model.log"), "ab")
        subprocess.Popen([py, "-c", "from faster_whisper import WhisperModel; WhisperModel('small.en', device='cpu', compute_type='int8')"],
                         stdout=log, stderr=log, creationflags=CREATE_NO_WINDOW)
    except Exception:
        pass


def kill_tree(proc):
    if proc is None or proc.poll() is not None:
        return
    try:
        if os.name == "nt":
            subprocess.run(["taskkill", "/PID", str(proc.pid), "/T", "/F"], capture_output=True, creationflags=CREATE_NO_WINDOW)
        else:
            proc.terminate()
    except Exception:
        pass


def already_running():
    """Chỉ cho một bản chạy: nếu bản trước còn sống thì chỉ mở lại cửa sổ vào đúng máy chủ đó."""
    p = os.path.join(USER, "running.json")
    try:
        d = json.load(open(p, encoding="utf-8"))
        if http_ok(d["studio_url"] + "api/health", 3) or http_ok(d["studio_url"], 3):
            return d["studio_url"]
    except Exception:
        pass
    return None


def main():
    selftest = "--selftest" in sys.argv
    os.makedirs(STUDIO_DATA, exist_ok=True)
    os.makedirs(LOGS, exist_ok=True)

    # ---- môi trường chung cho API, Studio và các tiến trình con (ffmpeg, Whisper...)
    bin_dir = os.path.join(ROOT, "bin")
    if os.path.isdir(bin_dir):
        os.environ["PATH"] = bin_dir + os.pathsep + os.environ.get("PATH", "")
    models = os.path.join(ROOT, "models", "hf")
    os.environ.setdefault("HF_HOME", models if os.path.isdir(models) else os.path.join(USER, "hf"))   # mô hình nhận dạng giọng đóng sẵn (nếu có)
    os.environ.setdefault("MUSE2API_PROFILE_ROOT", os.path.join(USER, "profiles"))   # hồ sơ trình duyệt của API nằm trong userdata
    for p in range(19210, 19250):   # cổng điều khiển trình duyệt (CDP) trống
        if port_free(p):
            os.environ.setdefault("MUSE2API_CDP_PORT", str(p))
            break
    os.environ["LUO_STUDIO_DATA"] = STUDIO_DATA
    os.environ["MUSE2API_HOME"] = API_HOME
    os.environ["MUSE2API_ENV_FILE"] = os.path.join(API_HOME, ".env")

    again = None if selftest else already_running()
    if again:
        say(f"LUO Studio đang chạy: {again}")
        open_window(again)
        return 0

    # ---- bật LUO-API
    port = pick_port(PREFERRED_PORT)
    key = write_env(port)
    os.environ["MUSE2API_KEY"] = key
    os.environ["LUO_API_URL"] = f"http://127.0.0.1:{port}"
    api_log = open(os.path.join(LOGS, "api.log"), "ab")
    py = sys.executable
    if os.name == "nt" and py.lower().endswith("pythonw.exe"):
        py = py[:-len("pythonw.exe")] + "python.exe"
    api = subprocess.Popen([py, "-m", "uvicorn", "app:app", "--host", "127.0.0.1", "--port", str(port), "--log-level", "warning"],
                           cwd=API_DIR, stdout=api_log, stderr=api_log, creationflags=CREATE_NO_WINDOW,
                           env=dict(os.environ, PYTHONIOENCODING="utf-8"))
    try:
        say(f"Đang bật LUO-API (cổng {port})…")
        for _ in range(120):
            if api.poll() is not None:
                raise RuntimeError("LUO-API tắt ngay khi khởi động. Xem userdata/logs/api.log")
            if http_ok(f"http://127.0.0.1:{port}/healthz"):
                break
            time.sleep(0.5)
        else:
            raise RuntimeError("LUO-API không phản hồi sau 60 giây. Xem userdata/logs/api.log")
        say("LUO-API sẵn sàng.")

        # ---- bật LUO Studio (cùng tiến trình)
        sys.path.insert(0, STUDIO_DIR)
        import server  # noqa: E402  (đọc biến môi trường ở trên khi import)
        server.seed()
        srv = server.make_server(int(os.environ.get("LUO_STUDIO_PORT", "0")))
        studio_port = srv.server_address[1]
        url = f"http://127.0.0.1:{studio_port}/"
        import threading
        threading.Thread(target=srv.serve_forever, daemon=True).start()
        json.dump({"studio_url": url, "api_port": port, "pid": os.getpid()}, open(os.path.join(USER, "running.json"), "w", encoding="utf-8"))
        say(f"LUO Studio: {url}")

        if not selftest:
            prefetch_whisper(py)
        if selftest:
            h = json.load(urllib.request.urlopen(url + "api/health", timeout=10))
            m = json.load(urllib.request.urlopen(url + "api/muse/status", timeout=30))
            say("SELFTEST " + json.dumps({"api_port": port, "studio": url, "health": h, "tai_khoan": len(m.get("accounts", []))}, ensure_ascii=False))
            return 0
        if "--no-window" in sys.argv:
            try:
                while True:
                    time.sleep(3600)
            except KeyboardInterrupt:
                return 0
        open_window(url)
        return 0
    finally:
        kill_tree(api)
        try:
            os.remove(os.path.join(USER, "running.json"))
        except OSError:
            pass


def open_window(url):
    sys.path.insert(0, STUDIO_DIR)
    import app as studio_app  # noqa: E402
    exe = studio_app.find_browser()
    if not exe:
        import webbrowser
        webbrowser.open(url)
        input("Đã mở trình duyệt. Nhấn Enter để thoát và tắt LUO Studio… ")
        return
    profile = os.path.join(STUDIO_DATA, "window-profile")
    proc = subprocess.Popen([exe, f"--app={url}", f"--user-data-dir={profile}", "--start-maximized", "--no-first-run",
                             "--disable-features=Translate,TranslateUI,EdgeTranslate,msEdgeTranslate", "--disable-sync", "--lang=vi"])
    proc.wait()


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as e:  # noqa: BLE001
        msg = f"LUO Studio không khởi động được: {e}"
        say(msg)
        try:
            os.makedirs(LOGS, exist_ok=True)
            open(os.path.join(LOGS, "launcher-error.txt"), "w", encoding="utf-8").write(msg + "\n")
            if os.name == "nt":
                import ctypes
                ctypes.windll.user32.MessageBoxW(0, msg, "LUO Studio", 0x10)
        except Exception:
            pass
        sys.exit(1)
