# Phase 1 helper for Windows / PowerShell. Idempotent; prints what it cannot do automatically.
#   powershell -ExecutionPolicy Bypass -File scripts\setup-phase1.ps1
$ErrorActionPreference = "Continue"
$VaultDir = (Get-Location).Path
$Repo = "Tradecreditor/skills-vault"
function Say($t) { Write-Host ""; Write-Host "== $t" -ForegroundColor Cyan }
function Have($n) { [bool](Get-Command $n -ErrorAction SilentlyContinue) }

Say "1/5 tools"
foreach ($p in @(@("git","https://git-scm.com/download/win"), @("gh","winget install GitHub.cli"),
                 @("node","winget install OpenJS.NodeJS.LTS"), @("python","winget install Python.Python.3.12"))) {
  if (Have $p[0]) { Write-Host "  ok: $($p[0])" } else { Write-Host "  MISSING: $($p[0])  ->  $($p[1])" -ForegroundColor Yellow }
}

Say "2/5 this folder is the vault"
if (Test-Path ".git") {
  git pull --rebase -q 2>$null
  Write-Host "  vault repo: $VaultDir"
} else {
  Write-Host "  not a git repo yet - run scripts\bootstrap-repo.ps1 first" -ForegroundColor Yellow
}

Say "3/5 Agent-Reach (reader toolbox)"
if (Have "agent-reach") { agent-reach doctor } else {
  Write-Host "  run:  pipx install https://github.com/Panniantong/agent-reach/archive/main.zip"
  Write-Host "  then: agent-reach install --env=auto --system"
}

Say "4/5 install the vault's own skills for every local agent"
if (Have "npx") {
  Write-Host "  running: npx -y skills add $Repo --skill vault-capture --skill vault-search -a claude-code -g -y"
  npx -y skills add $Repo --skill vault-capture --skill vault-search -a claude-code -g -y
} else { Write-Host "  Node.js missing; install it, then run the npx command above" -ForegroundColor Yellow }

Say "5/5 manual steps"
@"
  a) Obsidian 1.12.7+ : "Open folder as vault"  ->  $VaultDir
     Settings > Community plugins > Browse "Git" > Install + Enable, then in its settings:
       Auto commit-and-sync interval: 10   Pull on startup: on   Auto pull interval: 10   Pull before push: on
  b) Session-start suggestions in every project:
     merge templates\claude-settings-user.windows.json into %USERPROFILE%\.claude\settings.json
  c) Smoke test:  cd "$VaultDir" ; claude
     paste  https://x.com/Jackywine/status/2095750518941659567  and say "save"
"@ | Write-Host
