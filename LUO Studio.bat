@echo off
cd /d "%~dp0"
if exist ".venv\Scripts\pythonw.exe" (
  start "" ".venv\Scripts\pythonw.exe" "app\launcher.py"
) else if exist "runtime\pythonw.exe" (
  start "" "runtime\pythonw.exe" "app\launcher.py"
) else (
  echo Chua cai dat. Hay chay: powershell -ExecutionPolicy Bypass -File setup.ps1
  pause
)
