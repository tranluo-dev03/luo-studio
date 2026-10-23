# LUO Studio - cai dat mot lan tu ma nguon (Windows 10/11, 64-bit).
# Cach dung:  powershell -ExecutionPolicy Bypass -File setup.ps1
# Viec script lam:
#   1. Kiem tra Python 3.11/3.12; neu thieu thi TU DONG cai Python 3.11 (winget, neu khong duoc thi tai
#      bo cai chinh thuc tu python.org), khong can thao tac. Cai cho rieng nguoi dung, khong can quyen admin.
#   2. Tao moi truong ao .venv va cai thu vien tu requirements.txt
#   3. Tai ffmpeg ban chinh thuc (gyan.dev) vao bin\
#   4. Tao thu muc userdata\
# Tuy chon:  -NoInstallPython  chi bao thieu Python va in huong dan, khong tu cai.
param([switch]$NoInstallPython)
$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot
# PowerShell 5.1 mac dinh dung TLS cu va tai file rat cham neu hien thanh tien do
[Net.ServicePointManager]::SecurityProtocol = [Net.ServicePointManager]::SecurityProtocol -bor [Net.SecurityProtocolType]::Tls12
$ProgressPreference = "SilentlyContinue"

function Find-Python {
  foreach ($v in "3.11", "3.12") {
    try {
      $p = & py "-$v" -c "import sys;print(sys.executable)" 2>$null
      if ($LASTEXITCODE -eq 0 -and $p) { return $p.Trim() }
    } catch {}
  }
  # Moi cai xong thi PATH cua phien nay chua cap nhat, nen tim truc tiep o cac thu muc cai mac dinh
  foreach ($d in "$env:LOCALAPPDATA\Programs\Python\Python311", "$env:LOCALAPPDATA\Programs\Python\Python312",
                 "$env:ProgramFiles\Python311", "$env:ProgramFiles\Python312") {
    $exe = Join-Path $d "python.exe"
    if (Test-Path $exe) { return $exe }
  }
  return $null
}

function Install-Python {
  if (Get-Command winget -ErrorAction SilentlyContinue) {
    Write-Host "  Dang cai Python 3.11 bang winget (tu dong, co the mat vai phut)..."
    try {
      & winget install --id Python.Python.3.11 -e --scope user --silent --accept-package-agreements --accept-source-agreements
    } catch { Write-Host "  winget loi: $($_.Exception.Message)" -ForegroundColor Yellow }
    if (Find-Python) { return }
    Write-Host "  winget khong cai duoc, chuyen sang bo cai chinh thuc tu python.org..." -ForegroundColor Yellow
  }
  $url = "https://www.python.org/ftp/python/3.11.9/python-3.11.9-amd64.exe"
  $exe = Join-Path $env:TEMP "python-3.11.9-amd64.exe"
  Write-Host "  Dang tai Python 3.11.9 tu python.org (khoang 26 MB)..."
  Invoke-WebRequest -Uri $url -OutFile $exe
  Write-Host "  Dang cai Python (tu dong, khong hien cua so)..."
  $proc = Start-Process -FilePath $exe -ArgumentList "/quiet", "InstallAllUsers=0", "PrependPath=1", "Include_launcher=1", "Include_test=0", "Include_doc=0" -Wait -PassThru
  Remove-Item $exe -Force -ErrorAction SilentlyContinue
  if ($proc.ExitCode -ne 0) { throw "Bo cai Python bao loi (ma $($proc.ExitCode))." }
}

Write-Host "[1/4] Kiem tra Python..." -ForegroundColor Cyan
$python = Find-Python
if (-not $python) {
  if ($NoInstallPython) {
    Write-Host "Chua co Python 3.11/3.12. Cai bang lenh sau roi chay lai setup.ps1:" -ForegroundColor Yellow
    Write-Host "  winget install Python.Python.3.11"
    exit 1
  }
  Write-Host "  Chua co Python 3.11/3.12, tu dong cai dat..." -ForegroundColor Yellow
  Install-Python
  $python = Find-Python
  if (-not $python) { throw "Da cai Python nhung khong tim thay. Hay mo cua so PowerShell moi va chay lai setup.ps1." }
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
