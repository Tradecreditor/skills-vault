# SessionStart hook (Windows): suggest vault entries relevant to the current project.
# Register in C:/Users/<you>/.claude/settings.json - see templates/claude-settings-user.windows.json (note: %USERPROFILE% is NOT expanded in a hook command).
# Prints nothing and exits 0 when there is no vault or no match.
$ErrorActionPreference = "SilentlyContinue"
# Windows PowerShell 5.1 reads files and writes stdout in the system ANSI code page, not UTF-8, so a
# Traditional Chinese title comes back as mojibake ("2026 ?? Obsidian ..."). Force UTF-8 on both sides:
# every Get-Content/Select-String below passes -Encoding UTF8, and this fixes what we hand back to the host.
try { [Console]::OutputEncoding = [System.Text.Encoding]::UTF8 } catch { }

$raw = [Console]::In.ReadToEnd()
$cwd = $null
try { $cwd = ($raw | ConvertFrom-Json).cwd } catch { }
if (-not $cwd) { $cwd = (Get-Location).Path }

$vault = $null
if ($PSScriptRoot) {
  $scriptVault = Join-Path $PSScriptRoot "../.."
  if (Test-Path (Join-Path $scriptVault "wiki/index.md")) { $vault = $scriptVault }
}
if (-not $vault) { $vault = $env:VAULT_DIR }
if (-not $vault -or -not (Test-Path (Join-Path $vault "wiki/index.md"))) {
  $vault = Join-Path $HOME "skills-vault"
}
if (-not (Test-Path (Join-Path $vault "wiki/index.md"))) { exit 0 }
$vault = (Resolve-Path $vault).Path
$vaultSep = $vault + [IO.Path]::DirectorySeparatorChar
if ($cwd.Equals($vault, [StringComparison]::OrdinalIgnoreCase) -or $cwd.StartsWith($vaultSep, [StringComparison]::OrdinalIgnoreCase)) { exit 0 }   # inside the vault itself (exact match or a real subdirectory - "skills-vault-foo" must NOT match "skills-vault")

# GIT_TERMINAL_PROMPT=0 matters: without it a repo whose credentials have expired blocks on a username
# prompt until the hook's 30s timeout, on every single session start, with nothing on screen to explain it.
$env:GIT_TERMINAL_PROMPT = "0"
# Bounded like the .sh's `timeout 20`: a hung pull (bad remote, a prompt that snuck past
# GIT_TERMINAL_PROMPT) must not eat the hook's whole 30s budget. Kill it at 20s and move on.
try {
  # Start-Process refuses the same target for both redirects, so use two scratch files (not NUL twice).
  $gitOut = Join-Path $env:TEMP "vault-suggest-git.out"; $gitErr = Join-Path $env:TEMP "vault-suggest-git.err"
  $gitPull = Start-Process -FilePath "git" -ArgumentList @("pull","-q","--rebase","--autostash") -WorkingDirectory $vault -NoNewWindow -PassThru -RedirectStandardOutput $gitOut -RedirectStandardError $gitErr
  if (-not $gitPull.WaitForExit(20000)) {
    try { Stop-Process -Id $gitPull.Id -Force -ErrorAction SilentlyContinue } catch { }
  }
  Remove-Item $gitOut, $gitErr -Force -ErrorAction SilentlyContinue
} catch { }

$stop = @('dependencies','devdependencies','peerdependencies','version','scripts','name','description','license','private','type','main','true','false','null','import','from','const','function','return','http','https','github','readme','project','this','that','with','your','have','will','when','then','file','files','using','used','make','sure','also','into','about','should','other','more','than','each','only','does','which','what','node_modules','package','packages','build','start','test','tests','testing','lint','dev','prod','src','dist','latest','index','config','default','example','json','yaml','yml','todo','note','notes','user','users','data','app','apps','api','web','site','page','pages','list','item','items','value','values','key','keys','new','old','add','set','get','run','runs','open','close','read','write','create','update','delete','remove','install','npm','npx','yarn','pnpm','pip','python','node','shell','bash','code','codes','tool','tools','skill','skills','repo','repos','post','posts','video','videos','article','concept','draft','verified','deprecated','threads','youtube','instagram','twitter','small','internal','simple','basic','module','modules','library','support','feature','features','require','requires','engines','author','email','homepage','bugs','keywords','workspaces','resolutions','overrides','typescript','javascript','react','next','vite')

$text = ""
foreach ($f in @("package.json","pyproject.toml","go.mod","Cargo.toml","Gemfile","README.md","CLAUDE.md")) {
  $p = Join-Path $cwd $f
  if (Test-Path $p) { $text += (Get-Content $p -Raw -Encoding UTF8 -ErrorAction SilentlyContinue) + "`n" }
}
foreach ($rf in (Get-ChildItem -Path $cwd -Filter "requirements*.txt" -File -ErrorAction SilentlyContinue)) {
  $text += (Get-Content $rf.FullName -Raw -Encoding UTF8 -ErrorAction SilentlyContinue) + "`n"
}
if (-not $text) { exit 0 }

$words = [regex]::Matches($text.ToLower(), '[a-z][a-z0-9._-]{3,30}') | ForEach-Object { $_.Value.Trim('._-') } |
  Where-Object { $_.Length -ge 4 -and $stop -notcontains $_ } |
  Group-Object | Sort-Object Count -Descending | Select-Object -First 60 -ExpandProperty Name
if (-not $words) { exit 0 }
$pat = ($words | ForEach-Object { [regex]::Escape($_) }) -join "|"

# $hits, not $matches: $matches is a PowerShell automatic variable that every -imatch below overwrites with its
# capture groups, so accumulating into it silently produced one "System.Collections.Hashtable" line.
$hits = @()
foreach ($line in (Get-Content (Join-Path $vault "wiki/index.md") -Encoding UTF8 -ErrorAction SilentlyContinue)) {
  if ($line -notmatch '^\| ' -or $line -match '^\| slug ' -or $line -match '^\|-') { continue }
  $c = $line.Split('|')
  if ($c.Count -lt 8) { continue }
  $title = $c[3].Trim(); $tags = $c[7].Trim(); $slug = $c[1].Trim()
  if ("$title $tags" -imatch $pat) { $hits += "$title ($slug)" }
}
foreach ($sk in (Get-ChildItem (Join-Path $vault "skills") -Directory -ErrorAction SilentlyContinue)) {
  $sm = Join-Path $sk.FullName "SKILL.md"
  if (-not (Test-Path $sm)) { continue }
  $desc = (Select-String -Path $sm -Pattern '^description:' -Encoding UTF8 -ErrorAction SilentlyContinue | Select-Object -First 1).Line
  if ($desc -and $desc -imatch $pat) { $hits += "skill: $($sk.Name)" }
}
$hits = $hits | Select-Object -Unique | Select-Object -First 6
if (-not $hits) { exit 0 }

$ctx = "Skills vault (Tradecreditor/skills-vault) entries that look relevant to this project:`n" +
       (($hits | ForEach-Object { "- $_" }) -join "`n") +
       "`nInstall a skill: npx skills add Tradecreditor/skills-vault --skill <name>  (Claude Code: /plugin install skills-vault@tradecreditor-vault). For more, read $vault\wiki\hot.md then wiki\index.md, or run the vault-search skill."
@{ hookSpecificOutput = @{ hookEventName = "SessionStart"; additionalContext = $ctx } } | ConvertTo-Json -Compress -Depth 5
