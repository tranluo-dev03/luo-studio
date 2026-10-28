# LUO Studio - cai dat mot lan tu ma nguon (Windows 10/11, 64-bit).
# Cach dung:  powershell -ExecutionPolicy Bypass -File setup.ps1
# Viec script lam:
#   0. Canh bao thu muc cai dat co van de (co dau, OneDrive, qua dai, o day) va go dau "tai tu Internet" khoi cac file.
#   1. Kiem tra Python: neu da co .venv dung duoc thi dung luon; neu khong thi tim Python 3.11-3.14 (64-bit, ban day du co venv - bo qua ban
#      embeddable) tren may (py launcher, registry, thu muc mac dinh, PATH). Thieu thi TU DONG cai Python 3.11 tu python.org, cai song song
#      voi Python dang co (cho rieng nguoi dung, khong can quyen admin, khong sua PATH).
#      Kiem tra Visual C++ Redistributable x64: thieu hoac cu hon 14.40 thi tu tai va cai (hoi UAC).
#   2. Tat tien trinh LUO Studio con sot cua thu muc nay, tao moi truong ao .venv va cai thu vien tu requirements.txt
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

# Studio can Python 3.11 den 3.14, 64-bit (onnxruntime chua co ban cho 3.15; them vao day khi da co va da chay thu)
$Supported = @("3.11", "3.12", "3.13", "3.14")

function Get-PythonInfo([string]$exe) {
  # Chay thu de biet phien ban, 32/64-bit va co tao duoc .venv khong; $null neu khong chay duoc.
  # Full = co venv + ensurepip. Ban "embeddable" (thu muc runtime\ cua cac app khac, ke ca ban LUO Studio cu) chay duoc nhung co tinh bo venv/pip:
  # chon nham no thi buoc tao .venv bao "No module named venv".
  try {
    $o = & $exe -c "import sys,importlib.util as u;print('%d.%d %d %d' % (sys.version_info[0], sys.version_info[1], 64 if sys.maxsize > 2**32 else 32, all(u.find_spec(m) for m in ('venv','ensurepip'))))" 2>$null
    if ($LASTEXITCODE -ne 0 -or -not $o) { return $null }
    $t = ("$o").Trim().Split(" ")
    return [pscustomobject]@{ Path = $exe; Version = $t[0]; Bits = [int]$t[1]; Full = ($t[2] -eq "1") }
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
  # Ban dung duoc: 3.11-3.14, 64-bit, ban day du (co venv); uu tien theo thu tu trong $Supported (3.11 truoc), cung phien ban thi theo thu tu tim thay.
  # Khong dung Sort-Object: tren PowerShell 5.1 no khong giu thu tu cac phan tu bang nhau, nen nhieu Python cung "3.12" thi chon ngau nhien.
  foreach ($v in $Supported) {
    foreach ($i in @($infos)) {
      if ($i.Version -eq $v -and $i.Bits -eq 64 -and $i.Full) { return $i.Path }
    }
  }
  return $null
}

function Find-Python { return Select-Python (Get-PythonCandidates) }

function Show-PythonSeen($infos) {
  if (-not $infos -or @($infos).Count -eq 0) { Write-Host "  Khong thay Python nao tren may." -ForegroundColor Yellow; return }
  Write-Host "  Python tim thay tren may:" -ForegroundColor Yellow
  foreach ($i in $infos) {
    $why = if ($i.Bits -ne 64) { "khong dung duoc: ban 32-bit" } elseif ($Supported -notcontains $i.Version) { "khong dung duoc: Studio can 3.11 den 3.14" } elseif (-not $i.Full) { "khong dung duoc: ban rut gon (embeddable), khong co venv/pip" } else { "dung duoc" }
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

# Kiem tra thu muc cai dat: cac loi nay khong bao ro rang ma lam thu vien nhi phan hong am tham ve sau
$here = $PSScriptRoot
if ($here -match '[^\x00-\x7F]') {
  Write-Host "  CANH BAO: duong dan thu muc co ky tu co dau/khong phai ASCII ($here). mediapipe/opencv khong mo duoc file o duong dan nhu vay." -ForegroundColor Yellow
  Write-Host "  Nen chuyen ca thu muc sang duong dan khong dau, vd. D:\LUO-Studio, roi chay lai setup.ps1." -ForegroundColor Yellow
}
if ($here -match '\\OneDrive') {
  Write-Host "  CANH BAO: thu muc nam trong OneDrive ($here). OneDrive khoa/dong bo file luc dang chay gay loi ngau nhien; nen chuyen sang vd. D:\LUO-Studio." -ForegroundColor Yellow
}
if ($here.Length -gt 120) {
  Write-Host "  CANH BAO: duong dan thu muc qua dai ($($here.Length) ky tu); mot so thu vien vuot gioi han 260 ky tu cua Windows khi cai. Nen dat o thu muc ngan, vd. D:\LUO-Studio." -ForegroundColor Yellow
}
try {
  $free = (Get-PSDrive -Name $here.Substring(0, 1) -ErrorAction Stop).Free
  if ($free -lt 5GB) { Write-Host ("  CANH BAO: o dia chi con {0:N1} GB trong; can it nhat ~5 GB (thu vien ~2 GB, mo hinh giong ~0,3 GB, video)." -f ($free / 1GB)) -ForegroundColor Yellow }
} catch {}
# File tai tu Internet (ZIP) bi Windows danh dau: .bat bi SmartScreen chan, .ps1 bi canh bao. Go dau (bo qua .venv, .git, userdata cho nhanh).
Get-ChildItem $here -Recurse -File -ErrorAction SilentlyContinue | Where-Object { $_.FullName -notmatch '\\(\.venv|\.git|userdata|userdata-backup)\\' } | Unblock-File -ErrorAction SilentlyContinue

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
      Write-Host "  Can Python 3.11 den 3.14 (64-bit). Cai tu https://www.python.org/downloads/ roi chay lai setup.ps1." -ForegroundColor Yellow
      if ($CheckOnly) { Write-Host "  (-CheckOnly: khong cai gi.)"; exit 1 }
      exit 1
    }
    Write-Host "  Chua co Python 3.11-3.14 (64-bit), tu dong cai dat Python 3.11..." -ForegroundColor Yellow
    Install-Python
    $infos = Get-PythonCandidates
    $python = Select-Python $infos
    if (-not $python) { Show-PythonSeen $infos; throw "Da cai Python nhung khong tim thay. Hay mo cua so PowerShell moi va chay lai setup.ps1." }
  }
  Write-Host "  Dung: $python"
}
if ($CheckOnly) { Write-Host "  (-CheckOnly: xong kiem tra Python.)"; exit 0 }

# Thu vien nhi phan (onnxruntime, ctranslate2, mediapipe, opencv) can Microsoft Visual C++ Redistributable x64 TU 14.40 TRO LEN (Visual Studio 2022 17.10+).
# Thieu thi bao 'DLL load failed'; co nhung CU HON (vd. 14.29 nam 2021) con te hon: nap duoc nhung crash cung trong MSVCP140.dll luc chay
# (doi ABI cua std::mutex o 14.40), Studio chet giua chung va nguoi dung chi thay "mat ket noi API" khi bam Gen. Nen kiem tra PHIEN BAN va tu nang cap.
$VCMin = [version]"14.40"
$VCUrl = "https://aka.ms/vs/17/release/vc_redist.x64.exe"
$restartNeeded = $false

function Get-VCRuntimeVersion {
  # Phien ban cua chinh file DLL ma tien trinh se nap (registry co the con ghi ban cu/moi khong khop file that); $null neu khong co
  $v = $null
  foreach ($f in "msvcp140.dll", "vcruntime140.dll") {
    $p = Join-Path $env:SystemRoot "System32\$f"
    if (-not (Test-Path $p)) { return $null }
    $fv = (Get-Item $p).VersionInfo
    $x = [version]("{0}.{1}.{2}" -f $fv.FileMajorPart, $fv.FileMinorPart, $fv.FileBuildPart)
    if (-not $v -or $x -lt $v) { $v = $x }
  }
  return $v
}

$vcv = Get-VCRuntimeVersion
if ($vcv -and $vcv -ge $VCMin) {
  Write-Host "  Visual C++ Redistributable x64: $vcv (dat yeu cau)."
} else {
  if ($vcv) { Write-Host "  Visual C++ Redistributable x64 qua cu ($vcv, can tu $VCMin): thu vien nhan dang giong se crash. Dang cap nhat..." -ForegroundColor Yellow }
  else { Write-Host "  Chua co Visual C++ Redistributable x64. Dang cai..." -ForegroundColor Yellow }
  $vcExe = Join-Path $env:TEMP "vc_redist.x64.exe"
  try {
    $curl = Join-Path $env:SystemRoot "System32\curl.exe"
    if (Test-Path $curl) { & $curl -L --fail --retry 3 --connect-timeout 20 -s -o $vcExe $VCUrl; if ($LASTEXITCODE -ne 0) { throw "curl ma $LASTEXITCODE" } }
    else { Invoke-WebRequest -Uri $VCUrl -OutFile $vcExe -TimeoutSec 300 }
    # Can quyen admin: Windows se hien hop thoai UAC, bam "Yes"
    Write-Host "  Windows se hoi quyen quan tri (UAC) de cai Visual C++ Redistributable: hay bam 'Yes'."
    $p = Start-Process -FilePath $vcExe -ArgumentList "/install", "/quiet", "/norestart" -Verb RunAs -Wait -PassThru
    $code = $p.ExitCode
    if ($code -eq 3010 -or $code -eq 1641) { $restartNeeded = $true }
    elseif ($code -ne 0 -and $code -ne 1638) { throw "bo cai bao ma $code" }   # 1638 = da co ban moi hon
    $vcv = Get-VCRuntimeVersion
    Write-Host "  Da cai Visual C++ Redistributable x64 ($vcv)."
  } catch {
    Write-Host "  CANH BAO: khong cai duoc Visual C++ Redistributable tu dong ($($_.Exception.Message))." -ForegroundColor Red
    Write-Host "  Bat buoc phai cai thu cong truoc khi Gen video: tai $VCUrl , chuot phai > Run as administrator, cai xong KHOI DONG LAI MAY." -ForegroundColor Red
  } finally {
    Remove-Item $vcExe -Force -ErrorAction SilentlyContinue
  }
}

Write-Host "[2/4] Tao .venv va cai thu vien (co the mat vai phut)..." -ForegroundColor Cyan
# LUO Studio (hoac tien trinh con sot lai tu lan truoc) dang chay bang .venv nay thi file .pyd bi khoa: pip bao "Access is denied" va .venv hong nua chung
$mine = @(Get-CimInstance Win32_Process -ErrorAction SilentlyContinue | Where-Object {
  $_.ExecutablePath -and ($_.ExecutablePath.StartsWith("$here\.venv\", [StringComparison]::OrdinalIgnoreCase) -or $_.ExecutablePath.StartsWith("$here\runtime\", [StringComparison]::OrdinalIgnoreCase)) })
if ($mine.Count) {
  Write-Host "  Dang tat $($mine.Count) tien trinh LUO Studio con chay tu thu muc nay (de cap nhat thu vien)..." -ForegroundColor Yellow
  foreach ($p in $mine) { try { & taskkill /PID $p.ProcessId /T /F 2>$null | Out-Null } catch {} }   # tien trinh con co the da tat theo cha
  Start-Sleep -Seconds 1
}
if (-not $venvOk) {
  if (Test-Path ".venv") { Remove-Item ".venv" -Recurse -Force }
  & $python -m venv .venv
  if ($LASTEXITCODE -ne 0 -or -not (Test-Path ".venv\Scripts\python.exe")) { throw "Tao .venv that bai (Python: $python)." }
}
& .venv\Scripts\python.exe -m pip install --upgrade pip
& .venv\Scripts\python.exe -m pip install --upgrade -r requirements.txt
if ($LASTEXITCODE -ne 0) { throw "Cai thu vien that bai." }

Write-Host "[3/4] Kiem tra ffmpeg..." -ForegroundColor Cyan
if ((Test-Path "bin\ffmpeg.exe") -and (Test-Path "bin\ffprobe.exe")) {
  Write-Host "  Da co ffmpeg trong bin\"
} else {
  # ffmpeg ban essentials nang ~110 MB. Invoke-WebRequest trong Windows PowerShell 5.1 ve thanh tien do cuc cham (nhin nhu treo hang chuc phut)
  # va khong co timeout, nen dung curl.exe (co san tu Windows 10): co thanh tien do, tu thu lai, bo cuoc neu mang gan nhu dung.
  $tmp = Join-Path $env:TEMP "luo-ffmpeg"
  if (Test-Path $tmp) { Remove-Item $tmp -Recurse -Force }
  New-Item -ItemType Directory -Path $tmp | Out-Null
  $zip = Join-Path $tmp "ffmpeg.zip"
  $urls = @()
  try {
    [Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
    $rel = Invoke-RestMethod -Uri "https://api.github.com/repos/GyanD/codexffmpeg/releases/latest" -TimeoutSec 20 -UserAgent "luo-studio-setup"
    $asset = $rel.assets | Where-Object { $_.name -match 'essentials_build\.zip$' } | Select-Object -First 1
    if ($asset) { $urls += $asset.browser_download_url }   # ban sao chinh thuc cua gyan.dev tren GitHub: thuong nhanh hon nhieu (do thuc te ~16 lan)
  } catch {}
  $urls += "https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip"   # nguon goc, du phong khi khong goi duoc GitHub
  $got = $false
  foreach ($u in $urls) {
    Write-Host "  Dang tai ffmpeg (khoang 110 MB) tu $u"
    if (Test-Path $zip) { Remove-Item $zip -Force }
    $curl = Join-Path $env:SystemRoot "System32\curl.exe"
    if (Test-Path $curl) {
      & $curl -L --fail --retry 3 --retry-delay 3 --connect-timeout 20 --speed-limit 20000 --speed-time 60 -# -o $zip $u
      $ok = ($LASTEXITCODE -eq 0)
    } else {
      $pp = $ProgressPreference; $ProgressPreference = "SilentlyContinue"
      try { Invoke-WebRequest -Uri $u -OutFile $zip -TimeoutSec 600; $ok = $true } catch { $ok = $false }
      $ProgressPreference = $pp
    }
    if ($ok -and (Test-Path $zip)) { $got = $true; break }
    Write-Host "  Tai that bai tu nguon nay, thu nguon khac..." -ForegroundColor Yellow
  }
  if (-not $got) { throw "Khong tai duoc ffmpeg. Kiem tra mang, hoac tai thu cong ffmpeg-release-essentials.zip tu https://www.gyan.dev/ffmpeg/builds/ roi chep ffmpeg.exe va ffprobe.exe vao thu muc bin\." }
  Write-Host "  Dang giai nen ffmpeg.exe va ffprobe.exe..."
  # chi lay hai file can dung (Expand-Archive giai nen ca ~400 MB, rat cham)
  Add-Type -AssemblyName System.IO.Compression.FileSystem
  New-Item -ItemType Directory -Force -Path "bin" | Out-Null
  $za = [IO.Compression.ZipFile]::OpenRead($zip)
  try {
    foreach ($e in $za.Entries) {
      if (($e.Name -eq "ffmpeg.exe" -or $e.Name -eq "ffprobe.exe") -and $e.FullName -match '(^|/)bin/') {
        [IO.Compression.ZipFileExtensions]::ExtractToFile($e, (Join-Path (Resolve-Path "bin").Path $e.Name), $true)
      }
    }
  } finally { $za.Dispose() }
  Remove-Item $tmp -Recurse -Force
  if (-not (Test-Path "bin\ffmpeg.exe")) { throw "Khong lay duoc ffmpeg.exe" }
  Write-Host "  Da cai ffmpeg vao bin\"
}

Write-Host "[4/4] Tao thu muc du lieu..." -ForegroundColor Cyan
New-Item -ItemType Directory -Force -Path "userdata" | Out-Null

Write-Host ""
if ($restartNeeded) { Write-Host "Visual C++ Redistributable vua duoc cap nhat: KHOI DONG LAI MAY truoc khi mo LUO Studio." -ForegroundColor Yellow }
Write-Host "Xong. Mo ung dung bang 'LUO Studio.bat' (hoac 'LUO Studio (xem loi).bat' de xem log)." -ForegroundColor Green
