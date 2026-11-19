#!/usr/bin/env bash
# Cap nhat LUO Studio len ban moi, GIU NGUYEN du lieu (userdata/), tuong duong update.ps1.
# Cach dung:  bash update.sh [--branch main] [--force]
#   1. Tu choi neu LUO Studio dang chay (tru khi --force).
#   2. git pull --ff-only (khong dong vao userdata/).
#   3. Chay lai setup.sh --no-apt de cap nhat thu vien.
set -euo pipefail
cd "$(dirname "$(readlink -f "$0")")"
BRANCH=main; FORCE=0
while [ $# -gt 0 ]; do
  case "$1" in
    --branch) BRANCH="$2"; shift ;;
    --force) FORCE=1 ;;
    *) echo "Tuy chon khong hop le: $1"; exit 2 ;;
  esac
  shift
done

echo "LUO Studio dang o ban $(head -n1 version.txt 2>/dev/null || echo '?')."
if [ "$FORCE" = 0 ] && [ -f userdata/running.json ]; then
  pid=$(.venv/bin/python -c 'import json;print(json.load(open("userdata/running.json")).get("pid",""))' 2>/dev/null || true)
  if [ -n "$pid" ] && kill -0 "$pid" 2>/dev/null; then echo "LUO Studio dang chay (pid $pid). Hay tat roi chay lai update.sh."; exit 1; fi
fi

echo "[1/2] Cap nhat ma nguon..."
[ -d .git ] || { echo "Thu muc khong co .git. Tai ban moi bang 'git clone' roi chep userdata/ sang."; exit 1; }
git pull --ff-only origin "$BRANCH"

echo "[2/2] Cap nhat thu vien..."
bash setup.sh --no-apt --no-chrome
echo "Xong. Chay lai: ./luo-studio.sh"
