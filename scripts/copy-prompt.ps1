# Copy one routine's prompt to the clipboard, intact, ready to paste into claude.ai.
#   .\scripts\copy-prompt.ps1 github-stars-sync
#
# Why this exists rather than a one-line Get-Content: Windows PowerShell 5.1 reads files in the system
# ANSI code page unless told otherwise, so a plain `Get-Content -Raw` turns 繁體中文 into mojibake before
# it ever reaches the clipboard. That is not cosmetic - it silently deleted the "write the summary in
# Traditional Chinese" rule from a live routine, and the routine then wrote English summaries for days.
# So: read as UTF-8, then read the clipboard back and refuse to report success unless it round-trips.
[CmdletBinding()]
param(
  [Parameter(Mandatory, Position = 0)]
  [ValidateSet('capture-link', 'github-stars-sync', 'weekly-hot-list', 'vault-lint')]
  [string]$Name
)

$path = Join-Path (Split-Path $PSScriptRoot -Parent) "routines/$Name.md"
if (-not (Test-Path $path)) { Write-Error "not found: $path"; exit 1 }

$marker = '## Prompt (paste verbatim)'
$text = Get-Content $path -Raw -Encoding UTF8
$i = $text.IndexOf($marker)
if ($i -lt 0) { Write-Error "$Name.md has no '$marker' section"; exit 1 }
$body = $text.Substring($i + $marker.Length).Trim()

Set-Clipboard -Value $body
$back = (Get-Clipboard -Raw)
if ($null -ne $back) { $back = $back.Trim() }

if ($back -ne $body) {
  Write-Error "Clipboard did not round-trip - do NOT paste this. Copy the prompt section out of $path by hand instead."
  exit 1
}
if ($body -match '[�]') {
  Write-Error "The file itself contains a replacement character - it was saved in the wrong encoding at some point."
  exit 1
}

$cjk = ([regex]::Matches($body, '[一-鿿]')).Count
Write-Host "copied $($body.Length) chars from $Name.md ($cjk Chinese characters, verified intact)" -ForegroundColor Green
Write-Host "Paste into claude.ai/code/routines -> $Name -> Instructions (select all, delete, Ctrl+V)."
