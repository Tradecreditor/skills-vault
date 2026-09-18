# First push of this scaffold to GitHub (Windows / PowerShell). Run once from inside the scaffold folder:
#   cd C:\Users\<you>\skills-vault
#   powershell -ExecutionPolicy Bypass -File scripts\bootstrap-repo.ps1
param([string]$Repo = "Tradecreditor/skills-vault")
$ErrorActionPreference = "Stop"

if (-not (Test-Path "CLAUDE.md") -or -not (Test-Path "wiki/index.md")) {
  Write-Host "Run this from the scaffold folder (the one containing CLAUDE.md)." -ForegroundColor Red; exit 1
}
foreach ($t in @("git","gh")) {
  if (-not (Get-Command $t -ErrorAction SilentlyContinue)) {
    Write-Host "$t is not installed or not on PATH." -ForegroundColor Red
    Write-Host "  git: https://git-scm.com/download/win    gh: winget install GitHub.cli"; exit 1
  }
}
gh auth status 2>$null | Out-Null
if ($LASTEXITCODE -ne 0) { Write-Host "Run: gh auth login" -ForegroundColor Red; exit 1 }
gh auth setup-git | Out-Null

if (-not (Test-Path ".git")) { git init -q -b main }
git add -A
git -c user.name="skills-vault-core" -c user.email="skills-vault-core@users.noreply.github.com" commit -q -m "init: skills vault scaffold" 2>$null | Out-Null

gh repo view $Repo 2>$null | Out-Null
if ($LASTEXITCODE -eq 0) {
  if (-not (git remote get-url origin 2>$null)) { git remote add origin "https://github.com/$Repo.git" }
  git ls-remote --exit-code --heads origin main 2>$null | Out-Null
  if ($LASTEXITCODE -eq 0) {
    Write-Host "Remote main already has commits; rebasing on top of it."
    git pull --rebase --allow-unrelated-histories origin main
  }
  git push -u origin main
} else {
  gh repo create $Repo --private --source=. --remote=origin --push --description "Personal agent skills vault: Obsidian vault + LLM wiki + installable Agent Skills"
}
Write-Host ""
Write-Host "Done: https://github.com/$Repo" -ForegroundColor Green
Write-Host "Next: powershell -ExecutionPolicy Bypass -File scripts\setup-phase1.ps1"
