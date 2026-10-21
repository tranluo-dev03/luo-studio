@echo off
cd /d "%~dp0"
if exist ".venv\Scripts\python.exe" (
  ".venv\Scripts\python.exe" "app\launcher.py"
) else if exist "runtime\python.exe" (
  "runtime\python.exe" "app\launcher.py"
) else (
  echo Chua cai dat. Hay chay: powershell -ExecutionPolicy Bypass -File setup.ps1
)
pause
