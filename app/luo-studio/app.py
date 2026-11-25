"""LUO Studio - khởi chạy: mở máy chủ cục bộ và hiển thị trong cửa sổ ứng dụng (Edge/Chrome --app, hoặc pywebview nếu có)."""
import os, shutil, subprocess, sys, threading, time, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import server  # noqa: E402


def has_display():
    """Windows/macOS luôn có màn hình; Linux cần X11/Wayland (VPS không giao diện thì không mở được cửa sổ)."""
    return os.name == "nt" or sys.platform == "darwin" or bool(os.environ.get("DISPLAY") or os.environ.get("WAYLAND_DISPLAY"))


def find_browser():
    if os.name != "nt":
        for n in ("google-chrome", "google-chrome-stable", "chromium", "chromium-browser", "microsoft-edge", "microsoft-edge-stable"):
            w = shutil.which(n)
            if w:
                return w
        return None
    for p in (r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe", r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
              r"C:\Program Files\Google\Chrome\Application\chrome.exe", r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"):
        if os.path.exists(p):
            return p
    return shutil.which("msedge") or shutil.which("chrome")


def main():
    server.seed()
    srv = server.make_server(int(os.environ.get("LUO_STUDIO_PORT", "0")))
    port = srv.server_address[1]
    url = f"http://127.0.0.1:{port}/"
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    print(f"LUO Studio: {url}")
    if "--no-window" in sys.argv or not has_display():
        try:
            while True:
                time.sleep(3600)
        except KeyboardInterrupt:
            return
    try:
        import webview  # type: ignore
        webview.create_window("LUO Studio", url, width=1320, height=860, min_size=(1000, 680), maximized=True, background_color="#0e1015")
        webview.start()
        return
    except ImportError:
        pass
    exe = find_browser()
    if not exe:
        import webbrowser
        webbrowser.open(url)
        input("Đã mở trình duyệt. Nhấn Enter để thoát…")
        return
    profile = os.path.join(server.DATA, "window-profile")
    proc = subprocess.Popen([exe, f"--app={url}", f"--user-data-dir={profile}", "--start-maximized", "--no-first-run", "--password-store=basic",
                             "--disable-features=Translate,TranslateUI,EdgeTranslate,msEdgeTranslate", "--disable-sync", "--lang=vi"])
    proc.wait()


if __name__ == "__main__":
    main()
