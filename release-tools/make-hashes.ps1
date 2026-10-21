# Tao file SHA256SUMS.txt cho goi phat hanh.
# Cach dung:  powershell -ExecutionPolicy Bypass -File make-hashes.ps1 -Zip "D:\path\LUO-Studio.zip"
param(
  [string]$Zip,
  [string]$PackageDir = (Split-Path $PSScriptRoot -Parent),
  [string]$Out = (Join-Path $PSScriptRoot "SHA256SUMS.txt")
)

$lines = @()
if ($Zip) {
  if (-not (Test-Path $Zip)) { throw "Khong thay file zip: $Zip" }
  $lines += "{0}  {1}" -f (Get-FileHash $Zip -Algorithm SHA256).Hash.ToLower(), (Split-Path $Zip -Leaf)
}

# Cac file thuong bi antivirus nghi ngo, de nguoi dung doi chieu
$keyFiles = "runtime\pythonw.exe","runtime\python.exe","runtime\python311.dll","bin\ffmpeg.exe","bin\ffprobe.exe","app\launcher.py","LUO Studio.bat"
foreach ($f in $keyFiles) {
  $full = Join-Path $PackageDir $f
  if (Test-Path $full) {
    $lines += "{0}  {1}" -f (Get-FileHash $full -Algorithm SHA256).Hash.ToLower(), ($f -replace '\\','/')
  } else { Write-Warning "Bo qua (khong co): $f" }
}

$lines | Set-Content -Path $Out -Encoding utf8
"Da ghi $Out"
$lines
