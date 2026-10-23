# LUO Studio - cap nhat len ban moi nhat, GIU NGUYEN du lieu (userdata\).
# Cach dung:  powershell -ExecutionPolicy Bypass -File update.ps1      (hoac bam dup "Cap nhat.bat")
# Viec script lam:
#   1. Tu choi chay neu LUO Studio dang mo (dong ung dung truoc).
#   2. Sao luu nhe du lieu quan trong vao userdata-backup\<ngay-gio>\ (tai khoan Muse, du an, loai du an, cai dat); giu 3 ban gan nhat.
#   3. Cap nhat ma nguon: thu muc co .git thi "git pull"; con lai tai ZIP ban moi roi chep de len
#      (KHONG dong vao userdata\, .venv\, bin\, runtime\).
#   4. Chay lai setup.ps1 de cap nhat thu vien (nhanh neu khong co gi moi).
# Tuy chon:  -Branch main   nhanh can lay (mac dinh main)
#            -ZipFile "C:\...\luo-studio-main.zip"   dung file ZIP da tai san (may khong co git / mang han che)
#            -SkipSetup   khong chay lai setup.ps1
#            -Force       bo qua kiem tra "ung dung dang chay"
param([string]$Branch = "main", [string]$ZipFile = "", [switch]$SkipSetup, [switch]$Force)
$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot
[Net.ServicePointManager]::SecurityProtocol = [Net.ServicePointManager]::SecurityProtocol -bor [Net.SecurityProtocolType]::Tls12
$ProgressPreference = "SilentlyContinue"
$Repo = "tranluo-dev03/luo-studio"

function Get-Version([string]$path) {
  if (-not (Test-Path $path)) { return "?" }
  $first = (Get-Content $path -TotalCount 1)
  if ($first -match "\d+\.\d+\.\d+") { return $Matches[0] }
  return "?"
}
$old = Get-Version "version.txt"
Write-Host "LUO Studio dang o ban $old." -ForegroundColor Cyan

# 1. Khong cap nhat khi ung dung dang chay
if (-not $Force -and (Test-Path "userdata\running.json")) {
  try {
    $run = Get-Content "userdata\running.json" -Raw | ConvertFrom-Json
    if ($run.pid -and (Get-Process -Id $run.pid -ErrorAction SilentlyContinue)) {
      throw "LUO Studio dang chay. Hay dong cua so ung dung roi chay lai update.ps1."
    }
  } catch [System.Management.Automation.RuntimeException] { throw }
  catch {}
}

# 2. Sao luu nhe (khong chep video, mo hinh giong noi, ho so trinh duyet: rat nang va co the tao lai)
Write-Host "[1/3] Sao luu du lieu quan trong..." -ForegroundColor Cyan
$bk = Join-Path "userdata-backup" (Get-Date -Format "yyyyMMdd-HHmmss")
New-Item -ItemType Directory -Force -Path $bk | Out-Null
foreach ($item in "userdata\api", "userdata\studio\projects", "userdata\studio\types", "userdata\studio\settings.json", "userdata\studio\queue.json") {
  if (Test-Path $item) { Copy-Item $item -Destination $bk -Recurse -Force }
}
Get-ChildItem "userdata-backup" -Directory | Sort-Object Name -Descending | Select-Object -Skip 3 | Remove-Item -Recurse -Force
Write-Host "  Da sao luu vao $bk"

# 3. Cap nhat ma nguon
Write-Host "[2/3] Cap nhat ma nguon..." -ForegroundColor Cyan
$tmp = $null
try {
  if ((Test-Path ".git") -and -not $ZipFile) {
    if (-not (Get-Command git -ErrorAction SilentlyContinue)) { throw "Thu muc co .git nhung may chua cai git. Cai git, hoac tai ZIP roi chay: update.ps1 -ZipFile duong-dan-file.zip" }
    & git pull --ff-only origin $Branch
    if ($LASTEXITCODE -ne 0) { throw "git pull that bai (co the ban da sua file trong thu muc nay). Xem lenh 'git status'. Du lieu cua ban khong bi anh huong." }
  } else {
    $tmp = Join-Path $env:TEMP "luo-update"
    if (Test-Path $tmp) { Remove-Item $tmp -Recurse -Force }
    New-Item -ItemType Directory -Path $tmp | Out-Null
    if ($ZipFile) {
      if (-not (Test-Path $ZipFile)) { throw "Khong thay file ZIP: $ZipFile" }
      $zip = $ZipFile
    } else {
      $zip = Join-Path $tmp "luo.zip"
      Write-Host "  Dang tai ban moi tu GitHub..."
      Invoke-WebRequest -Uri "https://github.com/$Repo/archive/refs/heads/$Branch.zip" -OutFile $zip
    }
    Expand-Archive -Path $zip -DestinationPath (Join-Path $tmp "x") -Force
    $src = Get-ChildItem (Join-Path $tmp "x") -Directory | Select-Object -First 1
    if (-not $src -or -not (Test-Path (Join-Path $src.FullName "app\launcher.py"))) { throw "File ZIP khong phai ma nguon LUO Studio." }
    # Chep de len; khong dung /MIR nen khong xoa gi; bo qua du lieu va thu vien. update.ps1 chep sau cung vi dang chay.
    & robocopy $src.FullName "." /E /XD userdata userdata-backup .venv bin runtime .git /XF update.ps1 /NFL /NDL /NJH /NJS /NP | Out-Null
    if ($LASTEXITCODE -ge 8) { throw "Chep file that bai (robocopy ma $LASTEXITCODE)." }
  }

  # 4. Cap nhat thu vien
  if (-not $SkipSetup) {
    Write-Host "[3/3] Cap nhat thu vien (chay setup.ps1)..." -ForegroundColor Cyan
    & (Join-Path $PSScriptRoot "setup.ps1")
  } else {
    Write-Host "[3/3] Bo qua setup.ps1 (-SkipSetup)." -ForegroundColor Yellow
  }
  if ($src) { Copy-Item (Join-Path $src.FullName "update.ps1") -Destination "update.ps1" -Force -ErrorAction SilentlyContinue }
} finally {
  if ($tmp -and (Test-Path $tmp)) { Remove-Item $tmp -Recurse -Force -ErrorAction SilentlyContinue }
}

$new = Get-Version "version.txt"
Write-Host ""
if ($new -eq $old) { Write-Host "Xong. Da o ban moi nhat ($new) hoac chua co ban moi hon." -ForegroundColor Green }
else { Write-Host "Xong. Da cap nhat $old -> $new. Du lieu trong userdata\ duoc giu nguyen. Xem CHANGELOG.md de biet co gi moi." -ForegroundColor Green }
Write-Host "Mo ung dung bang 'LUO Studio.bat'."
