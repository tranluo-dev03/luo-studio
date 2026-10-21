# Ky so cac file .exe/.dll/.pyd do BAN tu build hoac dong goi (khong ky lai file cua Python/FFmpeg goc).
# Can: Windows SDK (signtool.exe) va chung chi code signing (file .pfx hoac token EV).
# Cach dung:
#   $env:PFX_PASSWORD = "mat-khau-pfx"      # dat trong phien, KHONG ghi vao file
#   powershell -ExecutionPolicy Bypass -File sign-files.ps1 -Pfx "D:\cert\luo.pfx" -Files "D:\path\LUO-Setup.exe"
param(
  [Parameter(Mandatory)] [string]$Pfx,
  [Parameter(Mandatory)] [string[]]$Files,
  [string]$Timestamp = "http://timestamp.digicert.com"
)

$signtool = Get-ChildItem "${env:ProgramFiles(x86)}\Windows Kits\10\bin\*\x64\signtool.exe" -ErrorAction SilentlyContinue |
  Sort-Object FullName -Descending | Select-Object -First 1 -ExpandProperty FullName
if (-not $signtool) { throw "Khong thay signtool.exe. Cai Windows SDK (Signing Tools)." }
if (-not $env:PFX_PASSWORD) { throw "Chua dat bien moi truong PFX_PASSWORD." }

foreach ($f in $Files) {
  & $signtool sign /fd SHA256 /tr $Timestamp /td SHA256 /f $Pfx /p $env:PFX_PASSWORD $f
  if ($LASTEXITCODE -ne 0) { throw "Ky that bai: $f" }
  & $signtool verify /pa $f
}
