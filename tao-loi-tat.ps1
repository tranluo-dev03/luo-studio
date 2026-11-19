# Tao loi tat "LUO Studio" tren Desktop (co icon rieng). Bam dup de mo; chuot phai > "Pin to taskbar" de ghim len thanh tac vu.
# Dung: powershell -ExecutionPolicy Bypass -File tao-loi-tat.ps1     (hoac bam dup "Tao loi tat.bat")
$ErrorActionPreference = "Stop"
$root = $PSScriptRoot
$py = @((Join-Path $root ".venv\Scripts\pythonw.exe"), (Join-Path $root "runtime\pythonw.exe")) | Where-Object { Test-Path $_ } | Select-Object -First 1
if (-not $py) { Write-Host "Chua cai dat. Hay chay setup.ps1 truoc." -ForegroundColor Red; exit 1 }

# Icon: tao luo-studio.ico tu logo cua ung dung (can Pillow trong moi truong Python cua Studio); khong tao duoc thi dung icon cua Python
$ico = Join-Path $root "app\luo-studio\ui\luo-studio.ico"
$png = Join-Path $root "app\luo-studio\ui\favicon.png"
if (-not (Test-Path $ico)) {
  $code = "import sys; from PIL import Image; im = Image.open(sys.argv[1]).convert('RGBA'); s = max(im.size); bg = Image.new('RGBA', (s, s), (0, 0, 0, 0)); bg.paste(im, ((s - im.width) // 2, (s - im.height) // 2)); bg.save(sys.argv[2], sizes=[(16, 16), (24, 24), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)])"
  $pyc = Join-Path (Split-Path $py) "python.exe"
  try { & $pyc -c $code $png $ico } catch { }
}
$icon = if (Test-Path $ico) { $ico } else { "$py,0" }

$desktop = [Environment]::GetFolderPath("Desktop")
$lnk = Join-Path $desktop "LUO Studio.lnk"
$sh = New-Object -ComObject WScript.Shell
$s = $sh.CreateShortcut($lnk)
$s.TargetPath = $py
$s.Arguments = '"' + (Join-Path $root "app\launcher.py") + '"'
$s.WorkingDirectory = $root
$s.IconLocation = $icon
$s.Description = "LUO Studio"
$s.Save()
Write-Host "Da tao loi tat: $lnk" -ForegroundColor Green
Write-Host "Ghim len thanh tac vu: chuot phai vao loi tat > Pin to taskbar (Windows 11: Show more options > Pin to taskbar)."
