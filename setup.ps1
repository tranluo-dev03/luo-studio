# LUO Studio - cai dat mot lan tu ma nguon (Windows 10/11, 64-bit).
# Cach dung:  powershell -ExecutionPolicy Bypass -File setup.ps1
# Viec script lam:
#   1. Kiem tra Python: neu da co .venv dung duoc thi dung luon; neu khong thi tim Python 3.11/3.12 (64-bit) tren may
#      (py launcher, registry, thu muc mac dinh, PATH). Thieu thi TU DONG cai Python 3.11 tu python.org, cai song song
#      voi Python dang co (cho rieng nguoi dung, khong can quyen admin, khong sua PATH).
#   2. Tao moi truong ao .venv va cai thu vien tu requirements.txt
#   3. Tai ffmpeg ban chinh thuc (gyan.dev) vao bin\
#   4. Tao thu muc userdata\
# Tuy chon:  -NoInstallPython  chi bao thieu Python va in huong dan, khong tu cai.
#            -CheckOnly       chi kiem tra Python (in ra Python tim thay va ban se dung) roi thoat.
#            -PythonInstaller "C:\...\python-3.11.9-amd64.exe"  dung bo cai da tai san (may khong co mang toi python.org).
param([switch]$NoInstallPython, [switch]$CheckOnly, [string]$PythonInstaller = "")
$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot
# PowerShell 5.1 mac dinh dung TLS cu va tai file rat cham neu hien thanh tien do
[Net.ServicePointManager]::SecurityProtocol = [Net.ServicePointManager]::SecurityProtocol -bor [Net.SecurityProtocolType]::Tls12
$ProgressPreference = "SilentlyContinue"

# Studio can Python 3.11 hoac 3.12, 64-bit (numpy 1.26.4 va mediapipe 0.10.21 chua co ban cho 3.13 tro len)
$Supported = @("3.11", "3.12")

function Get-PythonInfo([string]$exe) {
  # Chay thu de biet phien ban va 32/64-bit; $null neu khong chay duoc
  try {
    $o = & $exe -c "import sys;print('%d.%d %d' % (sys.version_info[0], sys.version_info[1], 64 if sys.maxsize > 2**32 else 32))" 2>$null
    if ($LASTEXITCODE -ne 0 -or -not $o) { return $null }
    $t = ("$o").Trim().Split(" ")
    return [pscustomobject]@{ Path = $exe; Version = $t[0]; Bits = [int]$t[1] }
  } catch { return $null }
}

function Get-PythonCandidates {
  # Tim moi Python tren may bang nhieu cach: py launcher, registry (PEP 514, ke ca cai vao thu muc tuy y), thu muc mac dinh, PATH
  param([string[]]$RegRoots = @("HKCU:\Software\Python\PythonCore", "HKLM:\SOFTWARE\Python\PythonCore", "HKLM:\SOFTWARE\WOW6432Node\Python\PythonCore"))
  $paths = New-Object System.Collections.Generic.List[string]
  try { foreach ($l in (& py -0p 2>$null)) { if ("$l" -match '([A-Za-z]:\\.*python\.exe)\s*$') { $paths.Add($Matches[1]) } } } catch {}
  foreach ($root in $RegRoots) {
    if (-not (Test-Path $root)) { continue }
    foreach ($k in Get-ChildItem $root -ErrorAction SilentlyContinue) {
      $ip = Get-ItemProperty (Join-Path $k.PSPath "InstallPath") -ErrorAction SilentlyContinue
      if (-not $ip) { continue }
      $e = $ip.ExecutablePath
      if (-not $e -and $ip.'(default)') { $e = Join-Path $ip.'(default)' "python.exe" }
      if ($e) { $paths.Add($e) }
    }
  }
  foreach ($v in 39, 310, 311, 312, 313, 314) {
    foreach ($d in "$env:LOCALAPPDATA\Programs\Python\Python$v", "$env:ProgramFiles\Python$v") { $paths.Add((Join-Path $d "python.exe")) }
  }
  foreach ($n in "python", "python3") {
    foreach ($c in (Get-Command $n -All -ErrorAction SilentlyContinue)) {
      # bo loi tat Microsoft Store (python.exe trong WindowsApps): chay no se mo cua hang thay vi Python
      if ($c.Source -and $c.Source -notmatch '\\Microsoft\\WindowsApps\\') { $paths.Add($c.Source) }
    }
  }
  $seen = @{}; $out = @()
  foreach ($x in $paths) {
    if (-not $x -or -not (Test-Path $x)) { continue }
    $key = (Resolve-Path $x).Path.ToLower()
    if ($seen.ContainsKey($key)) { continue }
    $seen[$key] = 1
    $i = Get-PythonInfo $x
    if ($i) { $out += $i }
  }
  return $out
}

function Select-Python($infos) {
  # Ban dung duoc: 3.11 hoac 3.12, 64-bit; uu tien 3.11
  $ok = @($infos | Where-Object { $Supported -contains $_.Version -and $_.Bits -eq 64 } | Sort-Object { [array]::IndexOf($Supported, $_.Version) })
  if ($ok.Count) { return $ok[0].Path }
  return $null
}

function Find-Python { return Select-Python (Get-PythonCandidates) }

function Show-PythonSeen($infos) {
  if (-not $infos -or @($infos).Count -eq 0) { Write-Host "  Khong thay Python nao tren may." -ForegroundColor Yellow; return }
  Write-Host "  Python tim thay tren may:" -ForegroundColor Yellow
  foreach ($i in $infos) {
    $why = if ($Supported -contains $i.Version -and $i.Bits -eq 64) { "dung duoc" } elseif ($i.Bits -ne 64) { "khong dung duoc: ban 32-bit" } else { "khong dung duoc: Studio can 3.11 hoac 3.12" }
    Write-Host ("    Python {0} ({1}-bit)  {2}  [{3}]" -f $i.Version, $i.Bits, $i.Path, $why)
  }
}

function Install-Python {
  # Cai Python 3.11 SONG SONG voi Python san co: chi cho nguoi dung hien tai, khong sua PATH, khong cai py launcher, khong tao shortcut/lien ket file
  # (tranh xung dot voi ban Python/launcher dang co, nguyen nhan pho bien cua loi 1603).
  $exe = $PythonInstaller
  $own = $false
  if (-not $exe) {
    $exe = Join-Path $env:TEMP "python-3.11.9-amd64.exe"
    Write-Host "  Dang tai Python 3.11.9 tu python.org (khoang 26 MB)..."
    Invoke-WebRequest -Uri "https://www.python.org/ftp/python/3.11.9/python-3.11.9-amd64.exe" -OutFile $exe
    $own = $true
  }
  $log = Join-Path $env:TEMP "luo-python-install.log"
  if (Test-Path $log) { Remove-Item $log -Force -ErrorAction SilentlyContinue }
  Write-Host "  Dang cai Python 3.11 (tu dong, khong hien cua so, cai song song voi Python dang co)..."
  $proc = Start-Process -FilePath $exe -ArgumentList "/quiet", "/log", "`"$log`"", "InstallAllUsers=0", "PrependPath=0", "Include_launcher=0", "InstallLauncherAllUsers=0", "Shortcuts=0", "AssociateFiles=0", "Include_test=0", "Include_doc=0" -Wait -PassThru
  if ($own) { Remove-Item $exe -Force -ErrorAction SilentlyContinue }
  $code = $proc.ExitCode
  if ($code -eq 0 -or $code -eq 3010 -or $code -eq 1638) { return }   # 3010 = can khoi dong lai may (van dung duoc); 1638 = da co ban 3.11 khac
  $tail = @()
  if (Test-Path $log) { $tail = Get-Content $log -ErrorAction SilentlyContinue | Where-Object { $_ -match "Error|Failed|returned actual error|0x8" } | Select-Object -Last 4 }
  $msg = "Bo cai Python bao loi (ma $code)."
  if ($tail) { $msg += " Chi tiet trong $log :`n    " + ($tail -join "`n    ") }
  $msg += "`n  Cach xu ly: (1) khoi dong lai may roi chay lai; (2) cai thu cong Python 3.11 tu https://www.python.org/downloads/release/python-3119/ (chon Windows installer 64-bit) roi chay lai file nay."
  throw $msg
}

Write-Host "[1/4] Kiem tra Python..." -ForegroundColor Cyan
$python = $null
$venvOk = $false
if (Test-Path ".venv\Scripts\python.exe") {
  # Da co .venv (cap nhat): dung luon, khong can tim Python he thong
  $vi = Get-PythonInfo (Resolve-Path ".venv\Scripts\python.exe").Path
  if ($vi -and $Supported -contains $vi.Version -and $vi.Bits -eq 64) {
    $venvOk = $true
    Write-Host ("  Dung .venv hien co (Python {0}, {1}-bit): bo qua kiem tra Python he thong." -f $vi.Version, $vi.Bits)
  } else {
    Write-Host "  .venv hien co khong chay duoc (Python goc bi go hoac doi cho?) - se tao lai." -ForegroundColor Yellow
  }
}
if (-not $venvOk) {
  $infos = Get-PythonCandidates
  $python = Select-Python $infos
  if (-not $python) {
    Show-PythonSeen $infos
    if ($NoInstallPython -or $CheckOnly) {
      Write-Host "  Can Python 3.11 hoac 3.12 (64-bit). Cai tu https://www.python.org/downloads/ roi chay lai setup.ps1." -ForegroundColor Yellow
      if ($CheckOnly) { Write-Host "  (-CheckOnly: khong cai gi.)"; exit 1 }
      exit 1
    }
    Write-Host "  Chua co Python 3.11/3.12 (64-bit), tu dong cai dat..." -ForegroundColor Yellow
    Install-Python
    $infos = Get-PythonCandidates
    $python = Select-Python $infos
    if (-not $python) { Show-PythonSeen $infos; throw "Da cai Python nhung khong tim thay. Hay mo cua so PowerShell moi va chay lai setup.ps1." }
  }
  Write-Host "  Dung: $python"
}
if ($CheckOnly) { Write-Host "  (-CheckOnly: xong kiem tra Python.)"; exit 0 }

# Thu vien nhi phan (onnxruntime, mediapipe, opencv, ctranslate2) can Microsoft Visual C++ Redistributable x64; thieu thi bao loi DLL kho hieu luc chay
$vc = Get-ItemProperty "HKLM:\SOFTWARE\Microsoft\VisualStudio\14.0\VC\Runtimes\x64" -ErrorAction SilentlyContinue
if (-not $vc -or $vc.Installed -ne 1) {
  Write-Host "  CANH BAO: chua thay Microsoft Visual C++ Redistributable x64. Cai tai https://aka.ms/vs/17/release/vc_redist.x64.exe (hoac: winget install Microsoft.VCRedist.2015+.x64) neu sau nay gap loi 'DLL load failed'." -ForegroundColor Yellow
}

Write-Host "[2/4] Tao .venv va cai thu vien (co the mat vai phut)..." -ForegroundColor Cyan
if (-not $venvOk) {
  if (Test-Path ".venv") { Remove-Item ".venv" -Recurse -Force }
  & $python -m venv .venv
  if ($LASTEXITCODE -ne 0 -or -not (Test-Path ".venv\Scripts\python.exe")) { throw "Tao .venv that bai (Python: $python)." }
}
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
