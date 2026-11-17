# Commit + push kem tang "version code" (dong `code N` trong version.txt).
# Dung: .\push.ps1 "noi dung commit" [-Files a,b,c]   (mac dinh: chi cac file da git add san; -All de them moi thay doi)
# Neu remote co version code moi hon: pull --rebase truoc, tang tren so cao nhat, roi push (thu lai neu bi day truoc).
param([Parameter(Mandatory)][string]$Message, [string[]]$Files, [switch]$All)
$ErrorActionPreference = "Continue"
Set-Location $PSScriptRoot
function Get-Code([string]$text) { if ($text -match "(?m)^code\s+(\d+)") { return [int]$Matches[1] } return 0 }
function Set-Code([int]$n) {
  $t = [IO.File]::ReadAllText("version.txt")
  if ($t -match "(?m)^code\s+\d+") { $t = [regex]::Replace($t, "(?m)^code\s+\d+", "code $n") } else { $t = $t.TrimEnd() + "`r`ncode $n`r`n" }
  [IO.File]::WriteAllText("version.txt", $t, (New-Object Text.UTF8Encoding($true)))
}
if ($All) { git add -A } elseif ($Files) { git add -- $Files }
if (-not (git diff --cached --name-only)) { Write-Host "Khong co gi de commit (git add truoc, hoac dung -Files / -All)." -ForegroundColor Yellow; exit 1 }
for ($try = 1; $try -le 5; $try++) {
  git fetch origin main --quiet
  $remote = Get-Code (git show origin/main:version.txt 2>$null | Out-String)
  $local = Get-Code ([IO.File]::ReadAllText("version.txt"))
  $new = [Math]::Max($remote, $local) + 1
  Set-Code $new
  git add version.txt
  git commit -q -m "$Message`n`n[code $new]"
  git pull --rebase --autostash origin main | Out-Null
  if ($LASTEXITCODE -ne 0) { Write-Host "Pull --rebase loi (xung dot?). Xu ly tay roi chay lai." -ForegroundColor Red; exit 1 }
  $after = Get-Code (git show origin/main:version.txt 2>$null | Out-String)
  if ($after -ge $new) {   # remote vua co code moi hon: bo commit nay, tang lai tren so moi
    git reset -q --soft HEAD~1; git reset -q version.txt; git checkout -- version.txt; continue
  }
  git push origin main
  if ($LASTEXITCODE -eq 0) { Write-Host "Da push, version code = $new" -ForegroundColor Green; exit 0 }
  git reset -q --soft HEAD~1; git reset -q version.txt; git checkout -- version.txt
}
Write-Host "Khong push duoc sau 5 lan thu." -ForegroundColor Red; exit 1
