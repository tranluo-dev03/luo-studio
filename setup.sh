#!/usr/bin/env bash
# LUO Studio - cai dat mot lan tren Ubuntu/Debian (64-bit), tuong duong setup.ps1 cua Windows.
# Cach dung:   bash setup.sh            (tu hoi mat khau sudo de cai goi he thong)
# Tuy chon:    --no-apt     khong cai goi he thong (ban da cai san: ffmpeg, python3-venv, python3-tk, font, Chrome)
#              --no-chrome  khong cai Google Chrome (Muse API can Chrome/Chromium chay ngam de gen)
# Viec script lam:
#   1. Cai goi he thong: ffmpeg, python3-venv, python3-tk, font DejaVu/Liberation, thu vien do hoa cho opencv/mediapipe.
#   2. Tim Python 3.11-3.14 (Ubuntu 24.04 co san 3.12), tao .venv, cai thu vien tu requirements.txt.
#   3. Cai Google Chrome (ban .deb, khong dung snap) neu may chua co Chrome/Chromium.
#   4. Tao thu muc userdata/.
set -euo pipefail
cd "$(dirname "$(readlink -f "$0")")"
HERE="$PWD"

DO_APT=1; DO_CHROME=1
for a in "$@"; do
  case "$a" in
    --no-apt) DO_APT=0 ;;
    --no-chrome) DO_CHROME=0 ;;
    *) echo "Tuy chon khong hop le: $a"; exit 2 ;;
  esac
done

say() { printf '\n\033[36m%s\033[0m\n' "$*"; }
warn() { printf '\033[33m  CANH BAO: %s\033[0m\n' "$*"; }

if [ "$(uname -s)" != "Linux" ]; then echo "setup.sh chi danh cho Linux. Tren Windows dung setup.ps1."; exit 1; fi
if [ "$(uname -m)" != "x86_64" ]; then warn "CPU $(uname -m): mediapipe/onnxruntime co the khong co ban cai san. Khuyen dung may x86_64."; fi
case "$HERE" in *[!\ -~]*) warn "duong dan thu muc co ky tu co dau ($HERE): mediapipe/opencv khong mo duoc file o duong dan nhu vay. Nen dat o ~/LUO-Studio." ;; esac

SUDO=""
if [ "$(id -u)" -ne 0 ]; then
  if command -v sudo >/dev/null 2>&1; then SUDO="sudo"; elif [ "$DO_APT" = 1 ]; then
    echo "Can quyen root de cai goi he thong. Chay lai voi sudo, hoac them --no-apt neu da cai san."; exit 1
  fi
fi
if [ "$(id -u)" -eq 0 ]; then
  warn "dang chay bang root. Nen dung tai khoan thuong (vd. luo): Chrome chay ngam can --no-sandbox khi la root va profile trinh duyet thuoc ve root."
fi

free_gb=$(df -Pk "$HERE" | awk 'NR==2 {printf "%d", $4/1048576}')
[ "${free_gb:-0}" -lt 5 ] && warn "o dia chi con ${free_gb} GB trong; can it nhat ~5 GB (thu vien ~2 GB, mo hinh giong ~0,3 GB, video)."

# ---------------------------------------------------------------- 1. goi he thong
if [ "$DO_APT" = 1 ]; then
  say "[1/4] Cai goi he thong (apt)..."
  if ! command -v apt-get >/dev/null 2>&1; then
    warn "khong co apt-get (khong phai Ubuntu/Debian). Hay tu cai: ffmpeg, python3-venv, python3-tk, font DejaVu, libGL; roi chay lai voi --no-apt."
  else
    $SUDO apt-get update -y
    $SUDO apt-get install -y ffmpeg python3 python3-venv python3-pip python3-tk fonts-dejavu-core fonts-liberation curl ca-certificates unzip procps
    $SUDO apt-get install -y libgl1 || warn "khong cai duoc libgl1 (opencv/mediapipe co the bao thieu libGL.so.1)"
    $SUDO apt-get install -y libglib2.0-0t64 2>/dev/null || $SUDO apt-get install -y libglib2.0-0 || true
  fi
else
  say "[1/4] Bo qua cai goi he thong (--no-apt)."
fi
command -v ffmpeg >/dev/null && command -v ffprobe >/dev/null || { echo "Thieu ffmpeg/ffprobe: sudo apt install ffmpeg"; exit 1; }

# ---------------------------------------------------------------- 2. Python + .venv
say "[2/4] Kiem tra Python va tao .venv..."
pick_python() {
  for c in python3.12 python3.11 python3.13 python3.14 python3; do
    p=$(command -v "$c" 2>/dev/null) || continue
    if "$p" -c 'import sys,importlib.util as u; sys.exit(0 if (3,11) <= sys.version_info[:2] <= (3,14) and u.find_spec("venv") and u.find_spec("ensurepip") else 1)' 2>/dev/null; then
      echo "$p"; return 0
    fi
  done
  return 1
}
if [ -x .venv/bin/python ] && .venv/bin/python -c 'import sys; sys.exit(0 if (3,11) <= sys.version_info[:2] <= (3,14) else 1)' 2>/dev/null; then
  echo "  Dung .venv hien co ($(.venv/bin/python -V))."
else
  PY=$(pick_python) || { echo "Can Python 3.11-3.14 co venv. Ubuntu 24.04: sudo apt install python3 python3-venv. Ban cu hon: dung PPA deadsnakes cai python3.12."; exit 1; }
  echo "  Dung: $PY ($($PY -V))"
  rm -rf .venv
  "$PY" -m venv .venv
fi
.venv/bin/python -m pip install --upgrade pip
.venv/bin/python -m pip install --upgrade -r requirements.txt

# ---------------------------------------------------------------- 3. Chrome
say "[3/4] Kiem tra Chrome/Chromium (Muse API chay ngam de gen)..."
have_browser() { for b in google-chrome google-chrome-stable chromium chromium-browser; do command -v "$b" >/dev/null 2>&1 && return 0; done; [ -x /snap/bin/chromium ]; }
if have_browser; then
  echo "  Da co trinh duyet."
elif [ "$DO_CHROME" = 1 ] && [ "$DO_APT" = 1 ] && [ "$(uname -m)" = "x86_64" ]; then
  deb="$(mktemp --suffix=.deb)"
  echo "  Dang tai Google Chrome (.deb, khong dung snap)..."
  if curl -fL --retry 3 --connect-timeout 20 -o "$deb" https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb; then
    $SUDO apt-get install -y "$deb" || warn "khong cai duoc Chrome. Tu cai roi chay lai."
  else
    warn "khong tai duoc Chrome. Cai thu cong (xem HUONG-DAN-LINUX.md)."
  fi
  rm -f "$deb"
else
  warn "chua co Chrome/Chromium. Khong co no thi Muse API khong gen duoc. Xem HUONG-DAN-LINUX.md."
fi

# ---------------------------------------------------------------- 4. thu muc du lieu
say "[4/4] Tao thu muc du lieu..."
mkdir -p userdata/logs
chmod +x setup.sh update.sh luo-studio.sh chan-doan.sh 2>/dev/null || true

printf '\n\033[32mXong. Chay:  ./luo-studio.sh   (kiem tra may: ./chan-doan.sh)\033[0m\n'
if [ -z "${DISPLAY:-}${WAYLAND_DISPLAY:-}" ]; then
  echo "May nay khong co man hinh: Studio chay nen o cong 8765, xem HUONG-DAN-LINUX.md de mo tu may cua ban qua duong ham SSH."
fi
