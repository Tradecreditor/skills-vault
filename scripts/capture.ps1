# Fire the capture-link Routine with one URL, so pasting a link into the vault is one command.
#   .\scripts\capture.ps1 https://x.com/someone/status/123
# Needs two environment variables, set once (see the bottom of this file).
[CmdletBinding()]
param([Parameter(Mandatory, Position = 0)][string]$Url)

$fire  = $env:VAULT_FIRE_URL
$token = $env:VAULT_FIRE_TOKEN
if (-not $fire -or -not $token) {
  Write-Error "VAULT_FIRE_URL / VAULT_FIRE_TOKEN not set - see the comment at the bottom of scripts/capture.ps1."
  exit 1
}
if ($fire -notmatch '/fire$') {
  Write-Error "VAULT_FIRE_URL must end in /fire - a stray character there returns 404, which reads like a broken routine."
  exit 1
}

try {
  Invoke-RestMethod -Method Post -Uri $fire -ContentType 'application/json' -Headers @{
    'Authorization'     = "Bearer $token"
    'anthropic-version' = '2023-06-01'
    'anthropic-beta'    = 'experimental-cc-routine-2026-04-01'
  } -Body (@{ text = $Url } | ConvertTo-Json -Compress) | Out-Null
  Write-Host "fired: $Url" -ForegroundColor Green
  Write-Host "The routine runs in the cloud; watch it at https://claude.ai/code/routines"
} catch {
  Write-Error "fire failed: $($_.Exception.Message)"
  exit 1
}

# One-time setup (User scope, survives reboots). The token is a secret: it can start runs on your account.
#   [Environment]::SetEnvironmentVariable("VAULT_FIRE_URL",  "https://api.anthropic.com/v1/claude_code/routines/trig_XXXX/fire", "User")
#   [Environment]::SetEnvironmentVariable("VAULT_FIRE_TOKEN","<the token shown once when the API trigger was created>", "User")
# Open a new terminal afterwards. Optional shortcut, add to $PROFILE:
#   function vault { param([string]$u) & "$HOME\skills-vault\scripts\capture.ps1" $u }
