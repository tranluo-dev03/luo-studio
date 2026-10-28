"""Chan doan may: kiem tra cac dieu kien thuong gay loi nhi phan (DLL, crash, thieu lenh CPU) cho LUO Studio.

Chay bang "Chan doan.bat" (hoac: .venv\\Scripts\\python.exe app\\chan_doan.py). Ket qua in ra man hinh va luu vao userdata\\logs\\chan-doan.txt;
gui file nay khi bao loi. Moi thu vien nhi phan duoc thu trong mot tien trinh rieng nen neu no crash thi cong cu van chay tiep.
"""
import ctypes, importlib.metadata as md, os, platform, subprocess, sys

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "app", "luo-studio"))
import face_mesh as FM  # noqa: E402  (chi lay ma thu mediapipe; ban than module khong nap mediapipe)
lines = []


def out(s=""):
    print(s)
    lines.append(s)


def cpu_features():
    """AVX / AVX2 / AVX-512 theo Windows (IsProcessorFeaturePresent). mediapipe can AVX; may ao (VM) khong cap AVX thuong gay loi DLL init hoac crash."""
    if os.name != "nt":
        return {}
    k = ctypes.windll.kernel32
    return {name: bool(k.IsProcessorFeaturePresent(code)) for name, code in (("AVX", 39), ("AVX2", 40), ("AVX-512F", 41))}


def cpu_name():
    try:
        import winreg
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"HARDWARE\DESCRIPTION\System\CentralProcessor\0") as k:
            return winreg.QueryValueEx(k, "ProcessorNameString")[0].strip()
    except Exception:
        return platform.processor() or "?"


def machine_model():
    try:
        r = subprocess.run(["powershell", "-NoProfile", "-Command", "(Get-CimInstance Win32_ComputerSystem | ForEach-Object { $_.Manufacturer + ' / ' + $_.Model })"],
                           capture_output=True, text=True, timeout=30)
        return r.stdout.strip() or "?"
    except Exception:
        return "?"


def vcredist():
    """Microsoft Visual C++ Redistributable x64 (2015-2022): onnxruntime, mediapipe, opencv, ctranslate2 deu can."""
    try:
        import winreg
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\VisualStudio\14.0\VC\Runtimes\x64") as k:
            installed = winreg.QueryValueEx(k, "Installed")[0]
            ver = winreg.QueryValueEx(k, "Version")[0]
            return bool(installed), str(ver)
    except Exception:
        return False, ""


def try_import(mod, code=None):
    """Thu import trong tien trinh rieng. Tra ve (ket qua, ma thoat, thong bao)."""
    code = code or f"import {mod}; print(getattr({mod}, '__version__', 'ok'))"
    r = subprocess.run([sys.executable, "-I", "-W", "ignore", "-c", code], capture_output=True, text=True, timeout=180)
    msg = (r.stdout.strip() or r.stderr.strip().splitlines()[-1:] and r.stderr.strip().splitlines()[-1] or "").strip()
    rc = r.returncode & 0xFFFFFFFF if r.returncode < 0 else r.returncode
    return r.returncode == 0, rc, msg


out("=== LUO Studio: chan doan may ===")
try:
    ver = open(os.path.join(ROOT, "version.txt"), encoding="utf-8-sig").readline().strip()
except OSError:
    ver = "?"
out(f"Phien ban: {ver}")
out(f"He dieu hanh: {platform.platform()}")
out(f"Python: {sys.version.split()[0]} ({sys.executable})")
out(f"May: {machine_model()}")
out(f"CPU: {cpu_name()}")
feat = cpu_features()
if feat:
    out("Lenh CPU: " + ", ".join(f"{k}={'co' if v else 'KHONG'}" for k, v in feat.items()))
ok_vc, vcver = vcredist()
try:   # v14.29.30133.00 -> (14, 29)
    vc_old = ok_vc and tuple(int(x) for x in vcver.lstrip("v").split(".")[:2]) < (14, 40)
except ValueError:
    vc_old = False
out(f"Microsoft Visual C++ Redistributable x64: {'co (' + vcver + ')' if ok_vc else 'KHONG THAY'}" + ("  -> QUA CU, can tu 14.40" if vc_old else ""))
out("")
out("Phien ban thu vien:")
for p in ("faster-whisper", "ctranslate2", "onnxruntime", "numpy", "mediapipe", "opencv-contrib-python", "av", "pillow", "fastapi", "uvicorn"):
    try:
        out(f"  {p} {md.version(p)}")
    except md.PackageNotFoundError:
        out(f"  {p} CHUA CAI")
out("")
out("Thu nap thu vien nhi phan (moi cai trong tien trinh rieng):")
problems = []
for label, mod, code in (("mediapipe (do mieng nguoi nghe)", "mediapipe", FM.probe_code()),
                         ("onnxruntime (VAD cua Hau ky)", "onnxruntime", None),
                         ("ctranslate2 (nhan dang giong)", "ctranslate2", None),
                         ("opencv (cv2)", "cv2", None),
                         ("av (PyAV)", "av", None)):
    try:
        good, rc, msg = try_import(mod, code)
    except subprocess.TimeoutExpired:
        good, rc, msg = False, -1, "qua thoi gian"
    out(f"  {'OK  ' if good else 'LOI '} {label}" + ("" if good else f"  (ma thoat 0x{rc & 0xFFFFFFFF:08X}) {msg[:140]}"))
    if not good:
        problems.append(mod)
out("")
out("=== Nhan xet ===")
if not problems:
    out("Cac thu vien nhi phan deu nap duoc.")
if not ok_vc or vc_old:
    out(f"- Microsoft Visual C++ Redistributable x64 {'qua cu (' + vcver + ')' if vc_old else 'chua cai'}: onnxruntime/ctranslate2 se loi DLL hoac crash cung trong MSVCP140.dll "
        "(Studio chet giua chung, bao 'mat ket noi API' khi Gen). Chay lai setup.ps1 (tu cai), hoac cai ban x64 tu https://aka.ms/vs/17/release/vc_redist.x64.exe "
        "bang quyen Administrator roi KHOI DONG LAI MAY.")
if problems and feat and not feat.get("AVX", True):
    out("- CPU/may ao KHONG bao cao lenh AVX: mediapipe (va mot so ban onnxruntime) can AVX. Neu day la may ao, bat 'AVX passthrough' / chon loai CPU 'host' trong cau hinh may ao.")
if "mediapipe" in problems:
    out("- mediapipe loi: Studio van gen va Hau ky binh thuong, chi tat tinh nang kiem tra 'nguoi nghe khong mam may mieng'.")
if "onnxruntime" in problems:
    out("- onnxruntime loi: Hau ky tu bo VAD va dung nhan dang giong khong VAD (khong anh huong ket qua).")
log_dir = os.path.join(ROOT, "userdata", "logs")
try:   # stack Python luc tien trinh crash cung (launcher ghi bang faulthandler)
    crash = open(os.path.join(log_dir, "crash.log"), encoding="utf-8", errors="replace").read().strip().splitlines()
    if crash:
        out("")
        out("Crash gan nhat (userdata\logs\crash.log, 15 dong cuoi):")
        for ln in crash[-15:]:
            out("  " + ln)
except OSError:
    pass
try:
    os.makedirs(log_dir, exist_ok=True)
    path = os.path.join(log_dir, "chan-doan.txt")
    open(path, "w", encoding="utf-8").write("\n".join(lines) + "\n")
    out("")
    out(f"Da luu bao cao: {path}")
except OSError:
    pass
