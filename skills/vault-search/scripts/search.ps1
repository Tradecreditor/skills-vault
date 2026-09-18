# Usage: powershell -ExecutionPolicy Bypass -File search.ps1 "<query words>"
# ORs the words (literal, case-insensitive); searches index rows, skill descriptions, page frontmatter, then full text.
param([Parameter(ValueFromRemainingArguments=$true)][string[]]$Query)
$ErrorActionPreference = "SilentlyContinue"

$here = Split-Path -Parent $MyInvocation.MyCommand.Path
$vault = Join-Path $here "..\..\.."
if (-not (Test-Path (Join-Path $vault "wiki/index.md"))) { $vault = $env:VAULT_DIR }
if (-not $vault -or -not (Test-Path (Join-Path $vault "wiki/index.md"))) { $vault = Join-Path $HOME "skills-vault" }
if (-not (Test-Path (Join-Path $vault "wiki/index.md"))) { Write-Host "vault not found (set VAULT_DIR)"; exit 2 }
$vault = (Resolve-Path $vault).Path

$words = @($Query) -join " " -split '\s+' | Where-Object { $_.Length -ge 2 }
if (-not $words) { Write-Host "usage: search.ps1 <query words>"; exit 1 }
$pat = ($words | ForEach-Object { [regex]::Escape($_) }) -join "|"

function Section($t) { Write-Host ""; Write-Host "## $t" }

Section "index rows matching: $($words -join ' ')"
$rows = Get-Content (Join-Path $vault "wiki/index.md") | Where-Object { $_ -match '^\| ' -and $_ -notmatch '^\| slug ' -and $_ -notmatch '^\|-' -and $_ -imatch $pat }
if ($rows) { $rows | ForEach-Object { Write-Host $_ } } else { Write-Host "(none)" }

Section "skills (description match)"
$hit = Get-ChildItem (Join-Path $vault "skills") -Directory | ForEach-Object {
  $sm = Join-Path $_.FullName "SKILL.md"
  if (Test-Path $sm) {
    $d = (Select-String -Path $sm -Pattern '^description:' | Select-Object -First 1).Line
    if ($d -and $d -imatch $pat) { "$($_.Name)  -- " + ($d -replace '^description:\s*','') }
  }
}
if ($hit) { $hit | ForEach-Object { Write-Host $_ } } else { Write-Host "(none)" }

Section "pages / stars (frontmatter match)"
$fm = Get-ChildItem (Join-Path $vault "wiki/pages"),(Join-Path $vault "wiki/stars") -Filter *.md |
  Where-Object { Select-String -Path $_.FullName -Pattern "^(title|tags|type|source_platform|author):.*($pat)" -Quiet }
if ($fm) { $fm | ForEach-Object { Write-Host $_.FullName.Replace("$vault\","") } } else { Write-Host "(none)" }

Section "full text (top 15 files)"
$ft = Get-ChildItem (Join-Path $vault "wiki/pages"),(Join-Path $vault "wiki/stars"),(Join-Path $vault "skills"),(Join-Path $vault "wiki/hot-list") -Recurse -File |
  Where-Object { Select-String -Path $_.FullName -Pattern $pat -Quiet } | Select-Object -First 15
if ($ft) { $ft | ForEach-Object { Write-Host $_.FullName.Replace("$vault\","") } } else { Write-Host "(none)" }
