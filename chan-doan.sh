#!/usr/bin/env bash
# Chan doan may Linux (tuong duong "Chan doan.bat"): ket qua o userdata/logs/chan-doan.txt
cd "$(dirname "$(readlink -f "$0")")" || exit 1
exec .venv/bin/python app/chan_doan.py "$@"
