# SessionStart hook (Windows): suggest vault entries relevant to the current project.
# Register in %USERPROFILE%\.claude\settings.json - see templates\claude-settings-user.windows.json.
# Prints nothing and exits 0 when there is no vault or no match.
$ErrorActionPreference = "SilentlyContinue"

$raw = [Console]::In.ReadToEnd()
$cwd = $null
try { $cwd = ($raw | ConvertFrom-Json).cwd } catch { }
if (-not $cwd) { $cwd = (Get-Location).Path }

$vault = $env:VAULT_DIR
if (-not $vault -or -not (Test-Path (Join-Path $vault "wiki/index.md"))) {
  $vault = Join-Path $HOME "skills-vault"
}
if (-not (Test-Path (Join-Path $vault "wiki/index.md"))) { exit 0 }
$vault = (Resolve-Path $vault).Path
if ($cwd.StartsWith($vault, [StringComparison]::OrdinalIgnoreCase)) { exit 0 }   # inside the vault

Push-Location $vault; git pull -q --rebase --autostash 2>$null | Out-Null; Pop-Location

$stop = @('dependencies','devdependencies','peerdependencies','version','scripts','name','description','license','private','type','main','true','false','null','import','from','const','function','return','http','https','github','readme','project','this','that','with','your','have','will','when','then','file','files','using','used','make','sure','also','into','about','should','other','more','than','each','only','does','which','what','node_modules','package','packages','build','start','test','tests','testing','lint','dev','prod','src','dist','latest','index','config','default','example','json','yaml','yml','todo','note','notes','user','users','data','app','apps','api','web','site','page','pages','list','item','items','value','values','key','keys','new','old','add','set','get','run','runs','open','close','read','write','create','update','delete','remove','install','npm','npx','yarn','pnpm','pip','python','node','shell','bash','code','codes','tool','tools','skill','skills','repo','repos','post','posts','video','videos','article','concept','draft','verified','deprecated','threads','youtube','instagram','twitter','small','internal','simple','basic','module','modules','library','support','feature','features','require','requires','engines','author','email','homepage','bugs','keywords','typescript','javascript','react','next','vite')

$text = ""
foreach ($f in @("package.json","requirements.txt","pyproject.toml","go.mod","Cargo.toml","Gemfile","README.md","CLAUDE.md")) {
  $p = Join-Path $cwd $f
  if (Test-Path $p) { $text += (Get-Content $p -Raw -ErrorAction SilentlyContinue) + "`n" }
}
if (-not $text) { exit 0 }

$words = [regex]::Matches($text.ToLower(), '[a-z][a-z0-9._-]{3,30}') | ForEach-Object { $_.Value.Trim('._-') } |
  Where-Object { $_.Length -ge 4 -and $stop -notcontains $_ } |
  Group-Object | Sort-Object Count -Descending | Select-Object -First 60 -ExpandProperty Name
if (-not $words) { exit 0 }
$pat = ($words | ForEach-Object { [regex]::Escape($_) }) -join "|"

$matches = @()
foreach ($line in (Get-Content (Join-Path $vault "wiki/index.md") -ErrorAction SilentlyContinue)) {
  if ($line -notmatch '^\| ' -or $line -match '^\| slug ' -or $line -match '^\|-') { continue }
  $c = $line.Split('|')
  if ($c.Count -lt 8) { continue }
  $title = $c[3].Trim(); $tags = $c[7].Trim(); $slug = $c[1].Trim()
  if ("$title $tags" -imatch $pat) { $matches += "$title ($slug)" }
}
foreach ($sk in (Get-ChildItem (Join-Path $vault "skills") -Directory -ErrorAction SilentlyContinue)) {
  $sm = Join-Path $sk.FullName "SKILL.md"
  if (-not (Test-Path $sm)) { continue }
  $desc = (Select-String -Path $sm -Pattern '^description:' -ErrorAction SilentlyContinue | Select-Object -First 1).Line
  if ($desc -and $desc -imatch $pat) { $matches += "skill: $($sk.Name)" }
}
$matches = $matches | Select-Object -Unique | Select-Object -First 6
if (-not $matches) { exit 0 }

$ctx = "Skills vault (Tradecreditor/skills-vault) entries that look relevant to this project:`n" +
       (($matches | ForEach-Object { "- $_" }) -join "`n") +
       "`nInstall a skill: npx skills add Tradecreditor/skills-vault --skill <name>  (Claude Code: /plugin install skills-vault@tradecreditor-vault). For more, read $vault\wiki\hot.md then wiki\index.md, or run the vault-search skill."
@{ hookSpecificOutput = @{ hookEventName = "SessionStart"; additionalContext = $ctx } } | ConvertTo-Json -Compress -Depth 5
