#!/usr/bin/env bash
# Chay LUO Studio tren Linux (tuong duong "LUO Studio.bat").
#   Co man hinh (RDP/VNC/desktop): mo cua so ung dung Chrome.
#   Khong man hinh (SSH): chay nen o cong 8765 (doi bang LUO_STUDIO_PORT), mo qua duong ham SSH.
# Tuy chon them: --no-window (khong mo cua so), --selftest.
cd "$(dirname "$(readlink -f "$0")")" || exit 1
if [ ! -x .venv/bin/python ]; then echo "Chua cai dat. Hay chay: bash setup.sh"; exit 1; fi
export PYTHONIOENCODING=utf-8
exec .venv/bin/python app/launcher.py "$@"
