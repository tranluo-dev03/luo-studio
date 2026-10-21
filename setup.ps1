# LUO Studio - cai dat mot lan tu ma nguon (Windows 10/11, 64-bit).
# Cach dung:  powershell -ExecutionPolicy Bypass -File setup.ps1
# Viec script lam:
#   1. Kiem tra Python 3.11 (neu thieu thi huong dan cai bang winget)
#   2. Tao moi truong ao .venv va cai thu vien tu requirements.txt
#   3. Tai ffmpeg ban chinh thuc (gyan.dev) vao bin\
#   4. Tao thu muc userdata\
$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot

function Find-Python {
  foreach ($v in "3.11", "3.12") {
    try {
      $p = & py "-$v" -c "import sys;print(sys.executable)" 2>$null
      if ($LASTEXITCODE -eq 0 -and $p) { return $p.Trim() }
    } catch {}
  }
  return $null
}

Write-Host "[1/4] Kiem tra Python..." -ForegroundColor Cyan
$python = Find-Python
if (-not $python) {
  Write-Host "Chua co Python 3.11/3.12. Cai bang lenh sau roi chay lai setup.ps1:" -ForegroundColor Yellow
  Write-Host "  winget install Python.Python.3.11"
  exit 1
}
Write-Host "  Dung: $python"

Write-Host "[2/4] Tao .venv va cai thu vien (co the mat vai phut)..." -ForegroundColor Cyan
if (-not (Test-Path ".venv\Scripts\python.exe")) { & $python -m venv .venv }
& .venv\Scripts\python.exe -m pip install --upgrade pip
& .venv\Scripts\python.exe -m pip install -r requirements.txt
if ($LASTEXITCODE -ne 0) { throw "Cai thu vien that bai." }

Write-Host "[3/4] Kiem tra ffmpeg..." -ForegroundColor Cyan
if ((Test-Path "bin\ffmpeg.exe") -and (Test-Path "bin\ffprobe.exe")) {
  Write-Host "  Da co ffmpeg trong bin\"
} else {
  $tmp = Join-Path $env:TEMP "luo-ffmpeg"
  if (Test-Path $tmp) { Remove-Item $tmp -Recurse -Force }
  New-Item -ItemType Directory -Path $tmp | Out-Null
  $zip = Join-Path $tmp "ffmpeg.zip"
  Invoke-WebRequest -Uri "https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip" -OutFile $zip
  Expand-Archive -Path $zip -DestinationPath $tmp -Force
  New-Item -ItemType Directory -Force -Path "bin" | Out-Null
  Get-ChildItem $tmp -Recurse -Include ffmpeg.exe, ffprobe.exe | Copy-Item -Destination "bin" -Force
  Remove-Item $tmp -Recurse -Force
  if (-not (Test-Path "bin\ffmpeg.exe")) { throw "Khong lay duoc ffmpeg.exe" }
  Write-Host "  Da cai ffmpeg vao bin\"
}

Write-Host "[4/4] Tao thu muc du lieu..." -ForegroundColor Cyan
New-Item -ItemType Directory -Force -Path "userdata" | Out-Null

Write-Host ""
Write-Host "Xong. Mo ung dung bang 'LUO Studio.bat' (hoac 'LUO Studio (xem loi).bat' de xem log)." -ForegroundColor Green
