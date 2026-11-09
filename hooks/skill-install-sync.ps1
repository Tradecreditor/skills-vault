# Plugin hook (Windows, PowerShell twin of skill-install-sync.sh): keep Jeff's Notion database "Skill Installs" current.
# Use it in place of the .sh when bash on this computer points at WSL: in ~/.claude/settings.json register
#   powershell -NoProfile -ExecutionPolicy Bypass -File "<plugin cache>/hooks/skill-install-sync.ps1"
# for PostToolUse (matcher Bash) and SessionStart. Same behaviour: records installs after an install / remove / update
# command, and on session start only what changed (--if-changed). Always exits 0; silent without NOTION_TOKEN.
$ErrorActionPreference = "SilentlyContinue"
if (-not $env:NOTION_TOKEN) { exit 0 }
$root = $env:CLAUDE_PLUGIN_ROOT
if (-not $root) { $root = Split-Path -Parent $PSScriptRoot }
$script = Join-Path $root "scripts\skills-inventory.py"
if (-not (Test-Path $script)) { exit 0 }
$raw = [Console]::In.ReadToEnd()
if (-not $raw) { exit 0 }
$payload = $null
try { $payload = $raw | ConvertFrom-Json } catch { exit 0 }

$py = $null
foreach ($cand in @(@("py", "-3"), @("python3"), @("python"))) {
  try { & $cand[0] @($cand[1..($cand.Length - 1)]) -c "import sys; sys.exit(0 if sys.version_info >= (3, 9) else 1)" 2>$null | Out-Null
        if ($LASTEXITCODE -eq 0) { $py = $cand; break } } catch { }
}
if (-not $py) { exit 0 }

$event = $payload.hook_event_name
$project = $env:CLAUDE_PROJECT_DIR
if (-not $project) { $project = $payload.cwd }
if (-not $project -or -not (Test-Path $project)) { $project = (Get-Location).Path }
$global = $false
switch ($event) {
  "PostToolUse" {
    $cmd = $payload.tool_input.command
    if (-not $cmd) { exit 0 }
    if ($cmd -notmatch '(^|[^A-Za-z0-9_-])(skills\s+(add|remove|rm|update|experimental_install|experimental_sync)|claude\s+plugin\s+(install|uninstall|update|enable|disable))(\s|$)') { exit 0 }
    if ($cmd -match '(^|\s)(-g|--global)(\s|$)|claude\s+plugin') { $global = $true }
  }
  "SessionStart" { $global = $true }
  default { exit 0 }
}

function Report($line) {
  if (-not $line) { return }
  $quiet = ($line -like "*unchanged since the last run*") -or ($line -like "*created=0 updated=0 removed=0*")
  if (-not $quiet -or $event -eq "PostToolUse") { Write-Output $line }
}
$exe = $py[0]; $pre = @(); if ($py.Length -gt 1) { $pre = $py[1..($py.Length - 1)] }
Report (& $exe @pre $script --root $project --if-changed 2>$null)
if ($global) { Report (& $exe @pre $script --global --if-changed 2>$null) }
exit 0
