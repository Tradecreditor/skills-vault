# Phase 1 helper for Windows / PowerShell. Idempotent; prints what it cannot do automatically.
#   powershell -ExecutionPolicy Bypass -File scripts\setup-phase1.ps1
$ErrorActionPreference = "Continue"
$VaultDir = (Get-Location).Path
$Repo = "Tradecreditor/skills-vault"
function Say($t) { Write-Host ""; Write-Host "== $t" -ForegroundColor Cyan }
function Have($n) { [bool](Get-Command $n -ErrorAction SilentlyContinue) }

Say "1/6 tools"
foreach ($p in @(@("git","https://git-scm.com/download/win"), @("gh","winget install GitHub.cli"),
                 @("node","winget install OpenJS.NodeJS.LTS"), @("python","winget install Python.Python.3.12"))) {
  if (Have $p[0]) { Write-Host "  ok: $($p[0])" } else { Write-Host "  MISSING: $($p[0])  ->  $($p[1])" -ForegroundColor Yellow }
}

Say "2/6 vault location"
if (Test-Path "wiki\index.md") {
  Write-Host "  vault: $VaultDir"
} else {
  Write-Host "vault not found: run this from your skills-vault folder" -ForegroundColor Yellow
  exit 2
}
if (Test-Path ".git") {
  git pull --rebase -q 2>$null
  if ($LASTEXITCODE -eq 0) { Write-Host "  updated" } else { Write-Host "  git pull failed (offline or uncommitted changes); continuing" -ForegroundColor Yellow }
} else {
  Write-Host "  not a git repo yet - run scripts\bootstrap-repo.ps1 first" -ForegroundColor Yellow
}

Say "3/6 Agent-Reach (reader toolbox; decision 1/4)"
if (Have "agent-reach") { agent-reach doctor } else {
  Write-Host "  run:  pipx install https://github.com/Panniantong/agent-reach/archive/main.zip"
  Write-Host "  then: agent-reach install --env=auto --system"
}

Say "4/6 Firecrawl CLI (generic web fallback)"
if (Have "firecrawl") { Write-Host "  already installed" } else {
  Write-Host "  run:  npx -y firecrawl-cli@latest init --all --browser   (uses your existing Firecrawl account)"
}

Say "5/6 Claude Code plugin marketplace"
if (Have "claude") {
  claude plugin marketplace add $Repo --scope user
  if ($LASTEXITCODE -eq 0) { Write-Host "  marketplace tradecreditor-vault added" } else { Write-Host "  (if it says already added, fine; otherwise in Claude Code run: /plugin marketplace add $Repo)" }
  claude plugin install "skills-vault@tradecreditor-vault" --scope user
  if ($LASTEXITCODE -eq 0) { Write-Host "  plugin skills-vault installed (user scope)" } else { Write-Host "  (if it says already installed, fine; otherwise in Claude Code run: /plugin install skills-vault@tradecreditor-vault)" }
  Write-Host "  repo is public, so the marketplace add needs no token"
} elseif (Have "npx") {
  Write-Host "  Claude Code CLI not found (install from https://code.claude.com); installing vault-capture/vault-search into ~\.claude\skills meanwhile" -ForegroundColor Yellow
  npx -y skills add $Repo --skill vault-capture --skill vault-search -a claude-code -g -y
  if ($LASTEXITCODE -ne 0) { Write-Host "  npx skills add failed; after installing Claude Code run: claude plugin marketplace add $Repo ; claude plugin install skills-vault@tradecreditor-vault" -ForegroundColor Yellow }
} else { Write-Host "  Claude Code CLI not found; install from https://code.claude.com, then: claude plugin marketplace add $Repo ; claude plugin install skills-vault@tradecreditor-vault" -ForegroundColor Yellow }

Say "6/6 manual steps"
@"
  a) Obsidian 1.12.7+ : "Open folder as vault"  ->  $VaultDir
     Settings > Community plugins > Browse "Git" > Install + Enable, then in its settings:
       Auto commit-and-sync interval: 10   Pull on startup: on   Auto pull interval: 10   Pull before push: on
  b) Session-start suggestions in every project:
     merge templates\claude-settings-user.windows.json into %USERPROFILE%\.claude\settings.json
  c) Smoke test:  cd "$VaultDir" ; claude
     paste  https://x.com/Jackywine/status/2095750518941659567  and say "save"
"@ | Write-Host
