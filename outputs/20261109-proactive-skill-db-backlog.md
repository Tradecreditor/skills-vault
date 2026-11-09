# Proactive skill database — Backlog card specs (2026-11-09)

Seven Projects HQ cards opened on Jeff's word from the performance review `outputs/20261109-vault-performance-review.md`.
Each section is one card (Area `skills-vault`, Status Backlog, Priority P2 by policy default, Owner Claude Code) and is written so a
fresh session can execute it: read this section, move the card's `handoff.md` row to In progress in the first commit, and follow
Steps. Each spec was drafted by one agent from the repository, checked by an independent reviewer against `CLAUDE.md` and the
repository, and revised; facts are as of 2026-11-09. Decisions for Jeff are listed per card: ask them before building the part they gate.

| # | Card | Depends on | First step |
|---|---|---|---|
| 1 | Project-to-skill matching — vault skill suggestions per project | — | Write scripts/skill-signals.json with match terms for each of the 14 reviewer-approved or verified skills listed in skills/README.md |
| 2 | External skill registry with reviewed install commands | — | Confirm the skills CLI accepts a full-commit pin by running npx skills add cloudflare/security-audit-skill@FULL_SHA_OF_c1c8a8c --list in a scratch folder outside the vault |
| 3 | Catalogue of non-vault skills and plugins on the main computer | §2 | Confirm the registry card is merged on main and record its registry file path and row fields in this card's handoff.md row |
| 4 | Skill usage logging and weekly usage report | — | Capture one Skill-tool PostToolUse payload and one UserPromptExpansion payload with claude -p --plugin-dir on a vault checkout plus a scratch --settings hook file (NOTION_TOKEN unset), confirm each invocation yields exactly one payload, and record the field names in this card's handoff.md row |
| 5 | Automatic clearing of rejected skills, stale drafts and orphan pages | — | Write the fail-closed fix gate scripts/skill-fix-gate.sh on a claude/ branch |
| 6 | Demand-driven skill discovery in the weekly hot list | — | Ask Jeff to answer Decisions for Jeff 1-3 (needs source, what happens to picks, test plan), then record his answers in handoff.md before building anything |
| 7 | Reviewer-approved model-tiering skill | — | Load the claude-api skill, re-fetch the live advisor-tool doc with scripts/read-url.sh, and check this card's defect list against cat -n of the files in skills/model-tiering |

## 1. Project-to-skill matching — vault skill suggestions per project

Card: Backlog · P2 · Owner Claude Code · depends on: none

**State:** Backlog card from the 2026-11-09 performance review (proposal 1); nothing is built yet. Vault skills are 4 of 92 installs on the main computer, and the marketing project has 0 vault skills among its 7 installs although 3 marketing and SEO skills in the vault are reviewer-approved.

**Next step:** Write scripts/skill-signals.json with match terms for each of the 14 reviewer-approved or verified skills listed in skills/README.md

### Goal
In every project that has the vault plugin, the agent learns at session start which reviewer-approved or verified vault skills fit the project and are not installed there yet. Each suggestion comes with the terms it matched and the exact install command. `/skills-vault:skillmatch` shows the same list on demand and installs a skill only after Jeff explicitly says yes. The first proof is the marketing project being offered its approved marketing/SEO skills.

### Why
- Source: `outputs/20261109-vault-performance-review.md` (commit `9e2491b`), proposal 1 and its KPI table.
  - Vault skills are 4 of the 92 installs on the main computer (4%), and all 4 are vault-operations skills.
  - None of the 14 web-captured skills is installed anywhere.
  - The marketing project has 7 installs and no vault skill, although `targeting-purchase-intent-keywords`, `auditing-seo-with-crawlie` and `researching-competitor-landing-pages` are reviewer-approved (all three have origin_type `post`).
- Targets for the next 4 weeks:
  - vault install rate: from 4% to 25%
  - active projects with at least 1 vault skill: from 1 of 2 to all of them
  - web-captured skills installed: from 0 to at least 3 (installing the three marketing skills meets this)

### Design
- **Runs inside the project, offline, with no `NOTION_TOKEN`.** Routines cannot see other repos. The plugin root is the vault, so `${CLAUDE_PLUGIN_ROOT}` holds both the README and the signals file.
- **NEW mode `scripts/skills-inventory.py --suggest [--root DIR] [--vault DIR] [--home DIR] [--json] [--if-changed]`.**
  - `run()` dispatches it before the token check, as it does `--audit` and `--enrich`.
  - It reuses `collect_project`, `collect_global`, `vault_statuses` and `default_labels`.
  - It refuses `--audit`, `--enrich` and `--global` with exit 4.
- **Vault data and the skill copy.**
  - It reads `<vault>/skills/README.md` and `<vault>/scripts/skill-signals.json`. `--vault` defaults to `ROOT`, which is `${CLAUDE_PLUGIN_ROOT}` for the hook and the command.
  - If either file is missing, it exits 3 with one stderr line (`skills-inventory: error (--suggest: no skills/README.md or scripts/skill-signals.json under <dir>; pass --vault)`), empty stdout and no traceback.
  - This is what happens when the script runs from the skill copy (whose `ROOT` is `skills/tracking-skill-installs-in-notion/`) or from a copy in another project.
- **Candidates and exclusions.**
  - A candidate's README status is `reviewer-approved` or `verified`, and its signals entry does not say `"suggest": false`. Draft and deprecated skills are never candidates.
  - Excluded: skills installed in the project (lockfile, `.claude/skills`, `.agents/skills`, `skills/`), skills installed globally (`collect_global(--home)`), and skills dismissed for this project.
- **Signals.** Unreadable or invalid files are skipped.
  - `CLAUDE.md`, `AGENTS.md` and `README*.md` (first 64 KB of each)
  - `package.json`: name, description, keywords and dependency names
  - `pyproject.toml` and `requirements*.txt`
  - the names of the skills and plugins already installed
- **Score.**
  - +1 for each distinct `terms` entry found. Matching is case-insensitive, whole word or phrase, with an optional plural on the last word: `\b` + `re.escape(term)` + `(?:e?s)?\b`, so `landing page` matches `landing pages`.
  - +2 for each `files` entry that exists at the project root.
  - A skill is suggested at `min_score` or above (2). At most `max_suggestions` (3) are shown.
- **Output.**
  - One line per suggestion: `skills-suggest: <skill> (<status>) matched <terms>; install: npx skills add Tradecreditor/skills-vault --skill <skill> -a claude-code -y`.
  - A closing line tells the agent to mention the suggestions once and install nothing without the user's yes.
  - `--json` prints every candidate with its score and matched terms, below the threshold too, so terms can be tuned in a project without copying its files anywhere.
  - It prints nothing and exits 0 when nothing fits or when `--root` is the vault (the `root_is_vault` test in `run()`).
- **State, kept apart from the inventory's own.**
  - The inventory's `--if-changed` writes `state_path(source)` = `<sha1(source)[:16]>.json` with `{fingerprint, ran_at}`.
  - Suggest writes NEW `suggest-<same hash>.json` with `{shown, shown_at}`, and dismissals go to NEW `dismiss-<same hash>.json` with `{dismissed}`. Both live in the same `SKILLS_INVENTORY_STATE` directory (default `~/.cache/skills-inventory`).
  - `--suggest --if-changed` prints only when the list differs from `shown`, or when `shown_at` is at least `IF_CHANGED_MAX_AGE` (7 days) old.
  - NEW `--dismiss <skill>` adds the skill to the dismiss file. Nothing is ever written inside the project.
- **Signals live in `scripts/skill-signals.json`, not in SKILL.md metadata.** Editing an approved skill's folder changes its `review_hash` and sends it back to draft.
- **Surfaces.**
  - NEW SessionStart hook `hooks/skill-suggest.sh`: matcher `startup`, timeout 15, works without `NOTION_TOKEN`, turned off by NEW `SKILLS_SUGGEST=off`. Its stdout becomes session context (see `report()` in `hooks/skill-install-sync.sh`).
  - NEW `/skills-vault:skillmatch` lists the suggestions with each skill's `review_report`, installs on Jeff's yes (the existing PostToolUse hook then records the install in Skill Installs), and runs `--dismiss` on his no.

### Files
- `scripts/skills-inventory.py` - existing - protected - add `--suggest` and `--dismiss`, extend the `--vault` help text and the docstring.
- `skills/tracking-skill-installs-in-notion/scripts/skills-inventory.py` - existing - protected - must stay a byte-identical copy (`test_skill_copy_is_identical`).
- `scripts/skill-signals.json` - NEW - protected - `min_score`, `max_suggestions`, and per skill `terms`, `files`, `suggest`.
- `scripts/test_skills_inventory.py` - existing - protected - add the tests in step 3.
- `hooks/skill-suggest.sh` and `hooks/skill-suggest.ps1` - NEW - protected - always exit 0; reuse the Python detection and `field()` from `skill-install-sync.sh`. The `.ps1` is a manual-registration twin, like `skill-install-sync.ps1`.
- `hooks/hooks.json` - existing - protected - add a second SessionStart entry.
- `commands/skillmatch.md` - NEW - protected - modelled on `commands/skillsync.md`.
- `skills/tracking-skill-installs-in-notion/SKILL.md` - existing - not protected - add a "Suggestions" section. The skill is a draft, so it gets re-reviewed anyway.
- `CLAUDE.md` and `AGENTS.md` - existing - protected - add one bullet under "Skill installs"; the two files must stay identical.
- `handoff.md` - existing - not protected - update the In flight row and add a Session log line.

### Steps
1. Create a branch. In its first commit, move this card's `handoff.md` row to In progress.
2. Write `scripts/skill-signals.json` with an entry for each of the 14 approved or verified skills in `skills/README.md`.
   - Set `"suggest": false` for skills that only make sense inside the vault: vault-capture, vault-search, auditing-agent-skills, judging-with-jev, and tracking-projects-in-notion (which joins through `/skills-vault:projecthq`).
   - Example terms:
     - targeting-purchase-intent-keywords: seo, ecommerce, e-commerce, shopify, woocommerce, keyword research, organic
     - auditing-seo-with-crawlie: seo, geo, sitemap, lighthouse, wcag, technical seo; files `robots.txt` and `sitemap.xml`
     - researching-competitor-landing-pages: landing page, competitor, positioning, conversion, copywriting
     - keeping-handoff-docs: file `handoff.md`
   - Keep the other skills' terms specific (e.g. `playwright`, `backlog.md`, `codex`).
3. Write the tests first. They should fail until step 4 is done.
   - (a) Fixture `CLAUDE.md` reads: "Marketing site for an e-commerce shop on Shopify. Work here: SEO and keyword research for organic traffic, technical SEO checks of the sitemap, competitor landing pages, positioning and conversion copywriting." The fixture also has an empty `robots.txt`.
     - Expected scores (`--json`): targeting 5, crawlie 5, landing-pages 5.
     - Every other candidate scores below 2, so exactly those 3 are printed.
   - (b) A draft skill with matching terms is never suggested (use a temporary vault README).
   - (c) A skill already in `skills-lock.json`, in `.claude/skills`, or in the fake home's `.claude/skills` is excluded.
   - (d) Running against the vault prints nothing.
   - (e) Works with `NOTION_TOKEN` unset, and the fake Notion server receives zero requests.
   - (f) `--if-changed` shows the list once, stays silent on the second run, shows it again when the list changes, and shows it again when `shown_at` is aged past the limit.
   - (g) `--dismiss` removes the skill from the list.
   - (h) Every approved or verified skill in the README has an entry, and every entry names an existing skill folder.
   - (i) The hook prints the list for a SessionStart payload, nothing for a PostToolUse payload, and nothing with `SKILLS_SUGGEST=off`.
   - (j) State isolation: in one state directory, with the fake Notion server running, run `--if-changed`, then `--suggest --if-changed`, then `--if-changed` again. The last run must print `unchanged since the last run` with zero new requests.
   - (k) The skill copy with `--suggest --root <fixture>` and no `--vault` exits 3 with empty stdout and no `Traceback`. With `--vault <repo root>` it prints the fixture's 3 suggestions.
4. Implement `--suggest` and `--dismiss`, then copy the script to the skill's `scripts/` folder. `python3 -m unittest discover -s scripts -p 'test_*.py' -v` must pass (111 tests before this card).
5. Add the hook scripts and the `hooks.json` entry, and check that `claude plugin validate .` passes. Run the hook by hand: `printf '{"hook_event_name":"SessionStart","cwd":"<fixture>"}' | SKILLS_INVENTORY_STATE=<tmp> CLAUDE_PLUGIN_ROOT="$PWD" CLAUDE_PROJECT_DIR=<fixture> bash hooks/skill-suggest.sh`.
6. Write `commands/skillmatch.md`:
   - use the plugin's own script and always pass `--root`
   - never print `NOTION_TOKEN`
   - install only on an explicit yes, with `npx skills add Tradecreditor/skills-vault --skill <name> -a claude-code -y` (project scope, no `-g`)
   - never install a draft skill
7. Write the SKILL.md section and the CLAUDE.md / AGENTS.md bullet. `diff -q CLAUDE.md AGENTS.md` must print nothing.
8. Check that `bash scripts/handoff-check.sh origin/main HEAD` prints ok, then open the PR. Move the row to Waiting on Jeff with Next step `Jeff: merge PR #<n>, update the tradecreditor-vault marketplace and plugin, open a session in the marketing project and answer its suggestions`.
9. Once Jeff has answered, read Skill Installs through the Notion connector (read-only).
   - If fewer than 3 marketing skills were listed, have the marketing project's session run `--suggest --json` and record only the skill names and scores in the handoff. Then tune the terms in a follow-up PR, or open a new Backlog row.
   - Put only counts and the `skills-audit:` line in the handoff, then move the row to Done.

### Done when
- The PR is merged to `main`, the full test suite including the new tests passes, and `claude plugin validate .` passes.
- Live check: after the plugin update, a session start in the marketing project listed at least 1 of the 3 marketing skills (target: all 3, with any misses handled in step 9), and nothing was installed without Jeff's yes. A session start in the vault itself shows no suggestions.
- Skill Installs shows at least 1 suggested vault skill Installed in that project, or Jeff dismissed all of them and that is recorded as his decision.
- The `handoff.md` row is Done, and its Detail holds the PR link plus public-safe counts (vault installs before and after, the audit line).

### Decisions for Jeff
- **D1: Should suggestions also appear in Notion?**
  - (a) Recommended: not in this card. The result already shows in Skill Installs once the skills are installed.
  - (b) A Status option `Suggested`, a view for it, and a `--record` flag writing rows under Source `<project>/suggestions`. This is a schema change, so it needs his word.
- **D2: The enabled `skills-vault@tradecreditor-vault` plugin already exposes every vault skill as `skills-vault:<name>`. What should the matcher do?**
  - (a) Default: still suggest an explicit project install, so it is recorded per project and pinned by the lockfile hash.
  - (b) Only remind the agent that the plugin skill exists. Skill Installs never counts that.

### Risks and rules
- **Public repo:** fixtures, tests, docs, commits and `handoff.md` use generic words ("the marketing project", "the main computer"). No project, computer or manual-card names; tuning notes hold skill names and scores only. Suggestions print only in the local session.
- **Protected paths:** everything above except SKILL.md and `handoff.md` is protected, so a core session must do this card, never the machine account.
- **Review gate:**
  - Only approved or verified skills are suggested, read from the plugin's own README.
  - Nothing is installed automatically.
  - Never edit an approved or verified skill folder.
  - The draft `tracking-skill-installs-in-notion` gets a new hash and goes through `skill-review` as usual.
- **handoff-check:** no Routine writes a new file, so the EXEMPT list in `scripts/handoff-check.sh` stays as it is. The hook writes only under the state directory.
- **Cost and staleness:**
  - No API calls and no tokens; at most 4 context lines, at most once a week per project.
  - Suggestions follow whatever plugin version Jeff last updated.

### Decisions for Jeff (from the reviewer pass)
- D1 Notion surface for suggestions: (a, recommended) none in this card, since the outcome already shows in Skill Installs as installed vault skills; or (b) add a Status option Suggested plus a view to Skill Installs (schema change) and a --record flag writing rows under Source <project>/suggestions
- D2 when the skills-vault@tradecreditor-vault plugin is enabled and every vault skill is already loadable as skills-vault:<name>: (a, default if Jeff says nothing) still suggest an explicit project install so it is recorded per project and pinned by the lockfile hash; or (b) only remind the agent the plugin skill exists, which Skill Installs never counts
- Whether to install each suggested marketing/SEO skill in the marketing project when the first suggestions appear (yes per skill, or dismiss)

## 2. External skill registry with reviewed install commands

Card: Backlog · P2 · Owner Claude Code · depends on: none

**State:** Not started. 26 captured items install as a skill, plugin, MCP server or own installer, 9 of them hot-list winners, but none has a catalogue row, so vault-search can recommend only the 14 reviewer-approved or verified vault skills.

**Next step:** Confirm the skills CLI accepts a full-commit pin by running npx skills add cloudflare/security-audit-skill@FULL_SHA_OF_c1c8a8c --list in a scratch folder outside the vault

### Goal
`wiki/registry.md` (NEW) is one public catalogue of every upstream skill, plugin or MCP server the vault has captured. Each row has the exact install command, review status, reviewed commit, report and wiki page. `vault-search` and the matching card use it to recommend reviewed upstream skills next to the vault's own, with installs pinned to the reviewed commit.

### Why
- Hot-list winners: W38–W45 picked 22 winners. The review says 24, but W38 picked only one. 9 of them install as a skill, plugin, MCP server or own installer: W38 fast-jev-compaction, W40 universal-modder and cloudflare/security-audit-skill, W41 anatomy and rea, W43 xerj and impeccable, W44 elephant-goldfish-model and Stageshow. They produced 0 SKILL.md drafts and 0 catalogue rows.
- Captures: 27 files match the step-3 grep (15 pages and 12 star notes). 3 of them only mention an install command, which leaves 24 real candidates; with rea and xerj, which the grep misses, that makes 26.
- Today `vault-search` can recommend only the 14 reviewer-approved or verified vault skills. 0 of the 14 skills captured from the web are installed anywhere.
- Targets in 4 weeks:
  - at least 20 rows on `main`;
  - every new installable winner or capture gets its row in the same run (today 0 do);
  - at least 5 skill rows reviewed by `skill-review` with a report. If Jeff delegates (Decision 1), at least 5 are `reviewer-approved` with a pinned install. If not, at least 5 are `passed` and waiting for his mark;
  - the review KPI "Capture → skill (registry counted)" rises from 15% to at least 30%.

### Design
- **Where.** `wiki/registry.md`, a Markdown table like `wiki/index.md`.
  - Not `skills/README.md`: vault-lint check 3 wants exactly one row per skill folder there.
  - Not page frontmatter: that needs a note-format change and is hard to list.
- **Columns.**
  - `id`: `github:<owner>/<repo>#<skill-or-plugin>`, unique.
  - `kind`: `skill`, `plugin`, `mcp` or `installer`.
  - `upstream_path`: the folder that holds SKILL.md.
  - `install`: the exact command.
  - `review`: one of the values below.
  - `reviewed_sha`: the full 40-character commit SHA.
  - `review_report`.
  - `page`: `[[pages/<slug>]]` or `[[stars/<slug>]]`, plus the vault wrapper skill if one exists, e.g. `using-ui-ux-pro-max` or `scanning-agent-skills`.
- **`review` values.**
  - `queued`: a skill folder waiting for review.
  - `passed`: used only if Decision 1 is no. The routine passed it and it waits for Jeff.
  - `reviewer-approved`.
  - `rejected`.
  - `not-auditable`: a plugin, MCP server, own installer or curl-pipe-sh binary. `static_scan.py` needs a skill folder, so these are catalogued but never recommended.
  - `pin-unsupported`.
  - `verified`: set on Jeff's word only.
  - `deprecated`: rows are never deleted.
- **Pinning.** Recommended rows install as `npx skills add <owner>/<repo>@<reviewed_sha> --skill <name>`.
  - vercel-labs/skills `docs/commands.md` (re-read 2026-11-09) says "Pin a release tag or full commit" and shows `npx skills add owner/repo@v1.2.3 --skill my-skill`.
  - Step 2 confirms a full SHA works before any file is edited.
  - Fallbacks, in order: the documented direct-path form `https://github.com/<o>/<r>/tree/<sha>/<upstream_path>`, then a release tag on the reviewed commit. If neither works, the row is `pin-unsupported` and is never recommended.
- **Writers.**
  - `vault-capture` gets a NEW section 4b, used by `capture-link` and by `weekly-hot-list` step 3 for winners. It appends a `queued` or `not-auditable` row with the command copied exactly from the source, after deduping with `grep -F "<id>" wiki/registry.md`.
  - A vault SKILL.md is still drafted only for a repeatable procedure that has no upstream skill.
  - Only `skill-review` moves `review` past `queued`.
- **Handoff check.** Routines push to `main`, where neither the PR-only CI `handoff` job nor the Stop hook (which exempts `main`) runs. Adding `wiki/registry\.md$` to `EXEMPT` keeps non-core PR captures and local `claude/` branch captures green.
- **Upstream audit.** This is a NEW step 2b in `routines/skill-review.md`. It runs after the vault queue and takes at most 4 `queued` rows per run, oldest first. The Routine runs on Skills Management with connectors removed (`routines/README.md`), but that environment allows `api.github.com` and `raw.githubusercontent.com`.
  1. Get the head SHA from `api.github.com/repos/<o>/<r>/commits?per_page=1`.
  2. List the folder's files with `git/trees/<sha>?recursive=1`.
  3. Fetch each file from `raw.githubusercontent.com/<o>/<r>/<sha>/<path>` into `${TMPDIR:-/tmp}/registry-review/<owner>--<repo>--<skill>/`, outside the checkout. If those hosts are blocked, use the Jina relay or the GitHub connector.
  4. Run `static_scan.py --hash <dir>` to get H.
  5. Run a fresh `vault-skill-reviewer` subagent with "Review <dir>", then apply the unchanged step-4 checks.
  6. Write the report to `outputs/skill-reviews/<date>-ext-<owner>--<repo>--<skill>.md` with `upstream` = `repo@sha`.
  7. Update the row: `review`, `reviewed_sha`, report and pinned `install`. Then add a log line `## [date] review | <id> approved|rejected`.
  8. Nothing is ever executed or installed.
- **Consumers.** `search.sh` and `search.ps1` print a NEW `## external skills (registry)` section. Following `vault-search` steps 3 and 5, they recommend only `reviewer-approved` and `verified` rows, with the pinned command and report, and label every other row as not approved. The matching card reads the same rows.

### Files
- `wiki/registry.md` - NEW - protected no - holds the header, column and vocabulary definitions, and 26 seed rows.
- `scripts/handoff-check.sh` - existing - protected yes - add `wiki/registry\.md$` to `EXEMPT` and to the header comment.
- `skills/vault-capture/SKILL.md` - existing - protected no - `verified`. Add NEW section 4b. The Never list gains "set a registry row's review above queued".
- `routines/capture-link.md` - existing - protected yes - step 3 names the registry row (vault-capture 4b).
- `routines/weekly-hot-list.md` - existing - protected yes - in step 3, an installable winner gets a registry row instead of a SKILL.md draft.
- `routines/skill-review.md` - existing - protected yes - add step 2b. Steps 5–8 also cover rows. The NEVER line gets one exception: fetching a queued row's own upstream folder at a pinned SHA, outside the checkout.
- `routines/README.md` - existing - protected yes - the skill-review row and its setup note now also cover registry rows and the two GitHub hosts it reads.
- `skills/vault-search/SKILL.md` - existing - protected no - `verified`. Steps 3 and 5 read the registry.
- `skills/vault-search/scripts/search.sh` and `search.ps1` - existing - protected yes - add the registry section, keeping the two scripts in parity.
- `routines/vault-lint.md` - existing - protected yes - NEW check 11:
  - ids are unique;
  - review values come from the vocabulary;
  - page links resolve;
  - recommended rows have a 40-hex `reviewed_sha`, an existing report, and the SHA in `install`;
  - `queued` rows older than 7 days are flagged.
- `CLAUDE.md` and `AGENTS.md` - existing - protected yes - add a folder-role row, "append rows to `wiki/registry.md`" in the access rules, and a short "External skill registry" paragraph. The two files must stay identical.
- `skills/README.md` - existing - protected no - one line pointing to `wiki/registry.md`.
- `handoff.md` - existing - protected no - move this card's row and add a Session log line.
- `.claude/agents/vault-skill-reviewer.md` - existing - protected yes - no change.

### Steps
1. Branch from `main`. In the first commit, move this card's existing Backlog row in `handoff.md` to In progress with Owner Claude Code, keeping its Priority. Update State and Next step, and append a Session log line.
2. Check the pin before editing anything:
   - Get the full SHA of `c1c8a8c` from `api.github.com/repos/cloudflare/security-audit-skill/commits/c1c8a8c` or the connector's `get_commit`.
   - In a scratch folder outside the vault, run `npx skills add cloudflare/security-audit-skill@<sha> --list`. It must list `security-audit`. If the proxy blocks the CLI's download, run it locally.
   - If it fails, try the fallbacks in order. Write the form that works (or `pin-unsupported`) into the registry header.
3. Find seed candidates:
   - Run `grep -rlE -e 'npx skills add' -e 'plugins? install' -e 'plugin marketplace add' -e 'claude mcp add' -e 'npx [a-z-]+ install' wiki/pages wiki/stars`. It returns 27 files today.
   - Drop the 3 mere mentions: `vercel-labs--skills` (the CLI itself), `20261003-backup-agent-workflows-as-skill-zips`, and `20260919-linkedin-skills-for-claude` (names no source).
   - Add the winners the grep misses: `20261012-rea-reverse-engineer-anything` and `20261026-xerj-local-search-engine-mcp-for-agents`. Winners sit under `## 本週入選`, or `## 本週亮點 (winners)` in W38.
4. For each candidate:
   - Copy the command from Key facts.
   - Confirm `upstream_path` holds a SKILL.md, using raw.githubusercontent.com or `get_file_contents`.
   - Set `kind`, and set `review` to `queued` (skill) or `not-auditable` (everything else).
   - Seed cloudflare as `queued`, with its report cell pointing to `[[pages/20261005-cloudflare-security-audit-skill]]` `## Review` until Jeff answers Decision 4.
5. Edit `EXEMPT`, then test it on a scratch branch:
   - A commit touching only `wiki/registry.md` must make `bash scripts/handoff-check.sh HEAD~1 HEAD` print `handoff: ok`.
   - A commit touching only `skills/README.md` must exit 1.
   - Switch back and delete the scratch branch.
6. Edit vault-capture 4b, capture-link step 3 and weekly-hot-list step 3.
7. Edit skill-review step 2b, then dry-run it by hand on one `queued` row, e.g. `wheresryan22/anatomy`:
   - fetch the folder into the temp folder;
   - run `python3 skills/auditing-agent-skills/scripts/static_scan.py <dir>`, then the same with `--hash`;
   - run one `vault-skill-reviewer` subagent;
   - confirm `git status` shows only the report and the row changed.
8. Add the registry section to `search.sh` and `search.ps1`, and edit vault-search SKILL.md. Then `bash skills/vault-search/scripts/search.sh stageshow` must print the registry row.
9. Add lint check 11 and run it by hand. Then:
   - `cmp CLAUDE.md AGENTS.md`;
   - `bash scripts/vault-guard-check.sh origin/main HEAD Tradecreditor` must pass.
10. Commit with `wiki: seed external skill registry`, `routines: …`, `scripts: …` and `docs: …`. Open the PR. Move the row to Waiting on Jeff, with Next step `Jeff: merge the PR and answer Decisions 1-4`.
11. After the merge:
    - trigger `skill-review` with Run now, or wait for the 07:47 UTC run;
    - check the reports and rows;
    - apply Jeff's answer to Decision 4;
    - set the row to Done with the evidence.

### Done when
- The PR is merged to `main`. `wiki/registry.md` there has at least 20 rows, and the next vault-lint report shows check 11 with 0 errors.
- One `skill-review` run on `main` reviewed at least 3 `queued` rows, each with a report under `outputs/skill-reviews/`. What the rows show depends on Decision 1:
  - Delegated: every `reviewer-approved` row's `install` carries the reviewed SHA in the confirmed pin form. Every row links its report.
  - Not delegated: the rows are `passed` or `rejected` with a report, and `search.sh` does not offer them for install until Jeff marks them `verified`.
- `search.sh` on `main` prints one recommended row with its pinned command and report. That is a row approved by `skill-review`, or cloudflare if Jeff said yes to Decision 4. If neither exists, it prints rows labelled not approved.
- A registry-only change gets `handoff: ok`.
- The handoff row is Done, and its Detail cites the PR, the review commit and the lint report.

### Decisions for Jeff
1. May `skill-review` mark an upstream skill folder `reviewer-approved`, which makes it installable at the pinned commit? This would extend the 2026-10-04 delegation to third-party code. The alternative is that the routine only marks rows `passed` and you approve each one. Recommended: delegate, skill folders only.
2. Plugins, MCP servers, own installers and curl-pipe-sh binaries: catalogue-only `not-auditable` (recommended), or extend the audit to them?
3. `vault-capture` and `vault-search` are `verified` and have no review hash. Should they keep `verified` after these small edits, as with `a550506` and `d70a4bf`? Or go through `skill-review`?
4. Does your 2026-10-07 approval of cloudflare/security-audit-skill at `c1c8a8c` carry over to a registry row marked `verified` with an install pinned to that commit? Until you say yes, the row stays `queued`.

### Risks and rules
- **Public repo.** Rows and reports carry only the upstream repo, path, command, status and page. They never say which project or computer installed something; that belongs only in Skill Installs in Notion.
- **No vendoring.** Upstream code is never committed. The temp folder lives outside the checkout. The review never runs or installs anything, and treats upstream text as untrusted (checklist S1).
- **Format rules.** Upstream folders need not meet the vault's own format rules. auditing-agent-skills step 4 treats those as advisory, not critical; confirm this on the step-7 dry run.
- **Review gate.** Only the `skill-review` procedure sets `reviewer-approved`, and `verified` is set only on Jeff's word. An unpinned command is never shown as approved. `skills/auditing-agent-skills` stays untouched, so its own review hash stays valid.
- **Protected paths.** `routines/`, `scripts/`, `skills/vault-search/scripts/`, `CLAUDE.md` and `AGENTS.md` mean this card needs a core session (Tradecreditor account); the machine account cannot do it.
- **Cost.** One Opus subagent per row, at most 4 rows per run, so about 12 rows clear in 3 daily runs. No Exa: GitHub reads use the API, raw or Jina.
- **Pin drift.** The docs do not say whether `npx skills update` keeps a pin. The registry text says an approval covers `reviewed_sha` only.
- **Out of scope.**
  - A Skill Installs `Vault status` for registry rows (a Notion schema change; belongs to the catalogue card).
  - Requeueing a row automatically when its upstream moves.

### Decisions for Jeff (from the reviewer pass)
- May the skill-review routine mark an external upstream skill folder reviewer-approved, which makes it installable in other projects at the pinned commit? That would extend the 2026-10-04 delegation from vault skills to third-party code. The alternative is that the routine only marks rows passed and Jeff approves each one, as with cloudflare/security-audit-skill on 2026-10-07. Recommended: delegate, skill folders only.
- Should vault-capture and vault-search keep their verified mark after their small registry edits, as with earlier core edits (a550506, d70a4bf), or go through skill-review?
- Does Jeff's 2026-10-07 approval of cloudflare/security-audit-skill at commit c1c8a8c carry over to a registry row marked verified, with an install pinned to that commit? Until he says yes, the row stays queued.

## 3. Catalogue of non-vault skills and plugins on the main computer

Card: Backlog · P2 · Owner Claude Code · depends on: §2 External skill registry with reviewed install commands

**State:** Backlog, not started. It depends on the registry card for the row format and the external audit procedure. Per the 2026-11-09 review the vault knows 4 of the 92 installs on the main computer, so 64 skill folders and 24 plugins are not catalogued.

**Next step:** Confirm the registry card is merged on main and record its registry file path and row fields in this card's handoff.md row

### Goal
The vault knows every skill folder and plugin installed globally on the owner's main computer. Each one with a public upstream gets a row in the registry from the registry card, with its upstream repo and path, a pinned commit, a match level and an audit verdict. Every other one is named only on a private Notion page.

### Why
- The 2026-11-09 review (`outputs/20261109-vault-performance-review.md`, proactive step 3) found that the vault knows 4 of the 92 installs on the main computer (about 4%).
  - For the 64 skill folders, Skill Installs holds only a name, the Kind and the Agents. `collect_global` in `scripts/skills-inventory.py` leaves Source repo and Hash empty when there is no lockfile entry.
  - The 24 plugins carry only a marketplace repo and a version.
- Targets:
  - Unknown installs go from 88 to 0.
  - The share the vault knows goes from 4% to at least 90% (a vault skill or a registry row; the rest are on the private list).
  - Every public row gets PASS, FAIL or `not-audited: <reason>`.

### Design
- **Where the gather step runs.** The folder contents exist only on the main computer. Jeff picks one option (Decision 1):
  - A: a Claude Code session on that computer in a **separate fresh clone** of the vault. Never use the Obsidian vault folder: obsidian-git auto-commits and pushes it. Keep every scratch file outside both folders.
  - B: a cloud session attached to such a clone through Remote Control (`list_computer_folders`, then `request_computer_folder`). This works only if the attached session can read the home-directory skill folders, so run one `ls ~/.claude/skills` first. If that is refused, use A or C.
  - C: cloud only, from the Notion names. Every row is then `name-only`.
- **Provenance, in order:**
  1. Local evidence: the symlink target and its `git remote -v`; the SKILL.md frontmatter (`metadata.source_url`, `homepage`, `repository`, `author`, `license`); links in README or LICENSE; any `skills` CLI lock file under `~/.agents/`.
  2. The vault itself: `github:<owner>/<repo>` canonical_ids in `wiki/index.md` and `wiki/stars/`. Examples: `greensock--gsap-skills`, `Leonxlnx--taste-skill`.
  3. Search:
     - Run `gh search code "name: <name>" --filename SKILL.md` on the main computer. In a cloud session api.github.com search answers 403 (handoff "Environment facts"), so use DuckDuckGo through Jina or WebSearch there.
     - Read skills.sh and ClawHub pages with `bash scripts/read-url.sh`.
     - Use Exa last.
- **Match levels:**
  - `hash-verified`: `static_scan.py --hash` of the local folder equals the hash of the upstream folder at the pinned commit.
  - `eol-only`: the hashes differ, but `diff -r --strip-trailing-cr` finds no difference. `normalized_bytes` strips CRLF only in SKILL.md, so a Windows autocrlf copy of `references/` or `scripts/` never hashes equal.
  - `differs`: a real difference. Keep both hashes and the reason. `walk` hashes a nested symlink as its link text, so a folder with a nested symlink is `differs: symlink` unless `diff -r` (which follows links) finds no difference.
  - `name-only`: no local copy was read.
- **Public and private.** A row enters the repo only when its upstream is a public repo or registry page that an anonymous read returns. Everything else goes to a NEW private child page of Skills HQ: hand-made skills, private ones, skills from another project and unresolved names. The repo carries only their count.
- **Plugins.** Add one row per `name@marketplace`, with the marketplace repo and version from Notion. The vault's own `skills-vault@tradecreditor-vault`, if listed, already counts as known.
- **Audits.**
  - Audits use only the registry card's external procedure: a static scan plus the reviewer subagent on the pinned upstream. Rows enter as `queued`.
  - Today `routines/skill-review.md` step 2 queues only `skills/*/SKILL.md`. If the registry card has not extended that, leave rows at `queued` and set this card to Blocked.
- **Out of scope:**
  - Notion schema changes.
  - Edits to `scripts/`, `routines/` or `hooks/`.
  - Uninstalling anything.
  - A check of installed skills against registered ones (a follow-up card).

### Files
- Registry file from the registry card: existing once that card merges, protected no. Add one row per public skill and plugin. If its format lacks upstream path, commit or match level, add those fields here as a `docs:` note.
- `outputs/<YYYYMMDD>-installed-skills-catalogue.md`: NEW, protected no. The method and counts only.
- `handoff.md`: existing, protected no. Update the In flight row and add a Session log line in the same commit. `outputs/` outside `outputs/health/` is not in the `scripts/handoff-check.sh` EXEMPT list.
- `scripts/skills-inventory.py`: existing, protected yes. Run only.
- `skills/auditing-agent-skills/scripts/static_scan.py`: existing, protected yes. Run only.
- `outputs/skill-reviews/<YYYY-MM-DD>-<name>.md`: written by the audit procedure, not by this card.
- Notion Skill Installs (data source id in handoff "Open loops"): read only.
- NEW private Notion page under Skills HQ.

### Steps
1. On `main`, confirm the registry card is merged, then read its format and its audit procedure. If either is missing, stop and set this card to Blocked on the registry card.
2. Read Skill Installs with the Notion connector. Filter on Project = the main computer's global label (`CLAUDE.md` "Skill installs") and Status Installed.
   - Skill rows (Kind folder or skills-cli): expect 68. Four of them have Vault skill ticked; keep the other 64.
   - Kind claude-plugin: expect 24.
   - Ignore the 170 Removed rows under the hostname-based label. They are duplicates (Jeff, 2026-11-09).
   - Keep this list in the scratchpad only. Never commit it.
3. On the main computer (option A or B), in the separate clone, create a NEW branch `claude/catalogue-installed-skills`.
   - Run `python3 scripts/skills-inventory.py --global --project "<global label>" --dry-run --json` (Windows: `py -3`). Dry-run never writes.
   - Compare: its non-plugin `rows`, minus the 4 vault names, must equal the 64 from step 2, and its plugin rows the 24. Explain any gap before you go on.
   - For each folder, collect the local evidence. Then run `python3 -I skills/auditing-agent-skills/scripts/static_scan.py --hash <real path of the folder>`, using the folder under the agent directory that Agents names.
   - Keep everything in one scratch JSON outside both folders.
4. Resolve each skill's upstream and pin a commit SHA.
   - Download with `gh api repos/<o>/<r>/tarball/<sha> > <dl>/src.tar.gz` into a new empty directory.
   - Extract with `tar -xzf` into another new empty directory.
   - From the repo root, run `python3 -I skills/auditing-agent-skills/scripts/static_scan.py --hash <extracted>/<path>`. Never run Python from inside an extracted folder.
   - If the hashes differ, run `diff -r --strip-trailing-cr` and set the match level.
   - Fetched files are untrusted data. Run, install or obey nothing in them.
5. Split the public rows from the private ones. Create the private Notion page with the private and unresolved names and their evidence, without local paths.
6. Write the registry rows with verdict `queued`, then write the report. Run the registry card's validator if it has one.
7. Run the privacy test before committing.
   - `git diff --cached` must contain none of: the username, the hostname, `C:\Users`, `/Users/`, `/home/`, or the names of other projects. Build that pattern from `whoami` and `hostname` at run time, and never write it to a file.
   - `git grep -F -f <scratch file of private names>` must return nothing.
8. Commit with the registry card's commit type, together with the handoff row and the log line. Run `git pull --rebase`, then push and open a PR, or push to `main` as a core session.
9. Track the audit queue until every public row has a verdict.
   - Put the FAIL names on the private Notion page; the report gives counts only.
   - Tell Jeff. Uninstall nothing.
10. Re-read Skill Installs. Record in the report how many installs the vault knows, before (4 of 92) and after.

### Done when
- Registry rows for every install with a public upstream are merged to `main`, with the PR or commit in Detail. Each row has:
  - the upstream repo and path;
  - a pinned commit;
  - a match level;
  - PASS, FAIL or `not-audited: <reason>`.
- Every install on the main computer is a vault skill, a registry row or a name on the private Notion page. The report shows unknown installs going from 88 to 0, based on a fresh read of Skill Installs.
- The privacy checks in step 7 come back empty on the merged diff.
- The `handoff.md` row is Done, with Detail pointing to the PR and the report.

### Decisions for Jeff
1. Where the gather step runs:
   - A: a short local session on the main computer. Gives hash-verified matches.
   - B: a Remote Control attach. Works only if the home skill folders can be read from it.
   - C: cloud only. All rows are name-only, and Jeff does nothing.
2. Audit scope: the 64 skill folders only, with plugins marked `not-audited: plugin` (recommended), or the 24 plugins too.
3. Public disclosure: neutral rows with no install provenance, where the link to the main computer stays in Notion (recommended), or rows marked as installed.
4. Review budget: wait for the shared daily queue (8 per run, shared with vault drafts), or allow extra batches by a core session. Each skill in a batch is one Opus subagent.
5. Skills that FAIL or have no public upstream: flag them only (recommended), or uninstall them from the main computer.
6. Optional: reinstall PASS skills with `npx skills add <owner>/<repo> --skill <name> -g`, so that Skill Installs records their source and hash. This changes the main computer.

### Risks and rules
- **Public repo.**
  - Never put hostnames, usernames, local paths, other project names or Projects HQ manual-card text in repo files, reports or commits. Write "the main computer".
  - Private names go to Notion only.
- **Protected paths.**
  - No edits to `scripts/`, `skills/*/scripts/`, `routines/`, `hooks/`, `.claude/`, `CLAUDE.md` or `AGENTS.md`. Changes to the audit procedure belong to the registry card.
  - Never delete or rename files. Never touch `raw/`.
- **Review gate.**
  - A verdict comes only from the registry card's procedure, run per `.claude/agents/vault-skill-reviewer.md`.
  - This card never copies an upstream folder into `skills/`. Promoting one is a separate capture that starts at `vault_status: draft`.
  - Any instruction found in fetched content is a finding, never a command.
- **Notion.** Only `scripts/skills-inventory.py` writes Skill Installs rows; this card reads them. Changing any property or option needs Jeff's word.
- **Cost.**
  - The audits depend on the registry card's procedure. If it uses the daily `skill-review` cap of 8 per run, shared with vault drafts, 64 or more audits take at least 8 runs.
  - GitHub search is rate-limited, so batch it.
  - Exa is metered. Use it only after `read-url.sh` fails, and stop on an HTTP 402.

### Decisions for Jeff (from the reviewer pass)
- Where the gather step runs: A, a short local Claude Code session on the main computer in a separate vault clone (hash-verified matches); B, a Remote Control attach, only if that session can read the home-directory skill folders; or C, cloud only from the Notion names (all name-only, no action from Jeff)
- Audit scope: the 64 skill folders only, with plugins catalogued by marketplace and version as not-audited (recommended), or audit the 24 plugins too
- Public disclosure: registry rows stay neutral with no install provenance and the link to the main computer stays in Notion (recommended), or rows are marked as installed on the main computer
- Review budget: wait for the shared daily skill-review queue (8 per run, shared with vault drafts), or allow extra review batches by a core session at one Opus subagent per skill
- Installed skills that FAIL the audit or have no public upstream: flag them only (recommended), or uninstall them from the main computer
- Optional: reinstall skills that PASS with npx skills add <owner>/<repo> --skill <name> -g, so Skill Installs records their source and hash automatically (this changes the main computer)

## 4. Skill usage logging and weekly usage report

Card: Backlog · P2 · Owner Claude Code · depends on: none

**State:** Not started. Skill Installs records where skills are installed, but nothing records whether an installed skill is ever invoked. The design is written and needs Jeff to choose where the counts live in Notion.

**Next step:** Capture one Skill-tool PostToolUse payload and one UserPromptExpansion payload with claude -p --plugin-dir on a vault checkout plus a scratch --settings hook file (NOTION_TOKEN unset), confirm each invocation yields exactly one payload, and record the field names in this card's handoff.md row

### Goal
Each time Claude Code invokes a skill on a computer that has the vault plugin, the plugin logs it locally without a network call and later sends per-week counts to Notion. Every Monday, `vault-lint` reports which vault skills were used and which had no use for 60 days, and suggests those for deprecation.

### Why
The review's main finding is "收藏 ≠ 使用", but the vault only measures installs: 4 of 92 installs on the main computer are vault skills, and 0 of the 14 web-captured skills are installed anywhere. Invocations are not measured for any of the 22 vault skills. Targets: within one week of go-live, the weekly report puts all 22 into a class (used, zero-use, not-measured, grace). After 60 days of tracking, each of the 8 approved captured skills has at least 1 use or a deprecation suggestion. This card measures usage. It does not raise the install rate (4% today; the review's target is 25%).

### Design
- **Log (hot path).** NEW hook `hooks/skill-usage.sh`, registered with `"async": true` (a 2.1.321 hook option: "runs in background without blocking"), so it never delays a turn. It fires on two events:
  - PostToolUse with matcher `Skill`. Its payload carries `tool_input.skill`.
  - UserPromptExpansion with `expansion_type` `slash_command`. Its schema in the 2.1.321 binary is `expansion_type`, `command_name`, `command_args`, `command_source` and `prompt`.

  The hook makes one Python call, `skills-inventory.py --usage-log` (stdin = the payload), which appends one line `{ts, skill, project_dir, via}` to `usage.jsonl` in the existing state dir (`SKILLS_INVENTORY_STATE`, default `~/.cache/skills-inventory`). It strips the `skills-vault:` plugin prefix. It never logs `args`, `command_args`, `prompt` or `tool_response`. It exits 0 every time, makes no network call, and does nothing without `NOTION_TOKEN` (the same gate as `skill-install-sync.sh`).
- **Why not SessionEnd.** In 2.1.321, SessionEnd hooks share a total budget of max(1.5 s, the largest settings-hook timeout capped at 60 s). The constants are in the binary. Only `CLAUDE_CODE_SESSIONEND_HOOKS_TIMEOUT_MS` raises it, so a plugin hook cannot count on more than 1.5 s, and a networked flush there would be killed partway through.
- **Flush (idempotent).** `--usage-flush` (NEW) runs from an async SessionStart hook (`startup|resume`, timeout 120), so usage reaches Notion one session later. It works in three steps:
  1. It takes an exclusive lock file (`O_CREAT|O_EXCL`; a lock older than 10 minutes counts as stale). If the lock is held, it exits 0.
  2. It renames `usage.jsonl` to a `.fold` file, waits 0.2 s, and folds the file into `counts.json`. That file maps each key (skill, project label from `repo_identity()`, computer label from `SKILLS_INVENTORY_GLOBAL_LABEL` or `global:<hostname>`, ISO week) to {count, pushed, last}. `counts.json` is written atomically (temp file + `os.replace`) together with the name of the file it folded, and only then is the `.fold` file deleted. A crash between those two steps cannot count lines twice.
  3. It pushes at most 20 dirty keys (count != pushed), with `Uses = max(remote, local count)` and Last used moving forward only. These are absolute values, never `+= n`, so a resend after a kill writes the same number. After each successful key it saves `pushed`. Clean keys older than 9 weeks are dropped. If nothing is dirty, it makes no network call. `--dry-run` writes nothing.
- **Store.** Jeff chooses (see Decisions).
  - A, recommended: a NEW database "Skill Usage" under Skills HQ (already shared with the integration). Properties: Skill (title), Key (rich_text, unique, used for lookup), Project and Computer (select, options created on demand), Week (rich_text, e.g. `2026-W46`), Uses (number), Last used (date), Via (multi_select: tool, slash). Each computer writes only its own rows, so no two computers race on a row.
  - B: two properties, Uses and Last used, on Skill Installs. It has no weekly history. Two computers that share a project Source would overwrite each other's counts. Built-in and plugin skills with no install row would be dropped.
- **Report.** `--usage-report --today D` (NEW, read-only, exit codes like `--audit`). It reads usage rows with Last used in the last 63 days, `skills/README.md` (via `vault_statuses()`, extended to return `origin_type`), each skill's `metadata.captured_at` (first 10 characters), and the Installed rows of Skill Installs (counts and Agents only). It prints one summary line, then one line per vault skill:
  - `used <name> uses_4w=N last=DATE`
  - `zero-use <name> installed=N`
  - `not-measured <name>`: installed only for agents other than claude-code
  - `grace <name>`

  A skill is in grace when tracking (the earliest usage row) or its `captured_at` is less than 60 days old. Non-vault skills appear only as one aggregate count. A deprecation is suggested only for a skill that is reviewer-approved or verified, is not `vault-operations` (Routines read those as files, so no hook sees them), is past grace, and has had no use for 60 days.
- **Weekly.** NEW check 11 in `routines/vault-lint.md` copies the report output verbatim into §11 of `outputs/health/WEEK.md`. `outputs/health/` is already in the EXEMPT list of `scripts/handoff-check.sh`, so that script needs no change.
- **Limits of v1.** Codex, Gemini CLI, OpenClaw and cloud Routines do not run the plugin's hooks. The summary line says so.

### Files
- `hooks/skill-usage.sh`: NEW, protected. Picks the event with a `grep` on `hook_event_name`, the same pattern `handoff-check.sh` uses, then calls `--usage-log` or `--usage-flush`.
- `hooks/skill-usage.ps1`: NEW, protected. PowerShell twin, registered by hand only where bash is WSL, like `skill-install-sync.ps1`.
- `hooks/hooks.json`: existing, protected. Adds three async entries: PostToolUse `Skill` (timeout 10), UserPromptExpansion (timeout 10) and SessionStart `startup|resume` (timeout 120). None has a statusMessage, and the existing entries stay unchanged.
- `scripts/skills-inventory.py`: existing, protected. Adds the three flags and `NOTION_USAGE_DS` (default: title search "Skill Usage"), and updates the docstring (it now writes local state).
- `skills/tracking-skill-installs-in-notion/scripts/skills-inventory.py`: existing, protected. Stays a byte-identical copy (`test_skill_copy_is_identical`).
- `scripts/test_skills_inventory.py`: existing, protected. New tests, plus a second data source on `FakeNotion`.
- `routines/vault-lint.md`: existing, protected. Check 11 and its summary-table row.
- `skills/tracking-skill-installs-in-notion/SKILL.md`: existing, not protected (draft). Adds the hooks table rows, Schedule and Evidence.
- `CLAUDE.md` and `AGENTS.md`: existing, protected. A "Skill installs" bullet and the `hooks/` folder row. The two files stay identical.
- `handoff.md`: existing, not protected. The card row and a Session log line.

### Steps
1. Verify the payloads. Write a scratch settings JSON in the scratchpad (never `.claude/settings.local.json`, which is not gitignored) whose PostToolUse `Skill` and UserPromptExpansion hooks append stdin to a scratch file. Then run `env -u NOTION_TOKEN claude -p --plugin-dir <vault checkout> --settings <file>` twice: once with a prompt that makes the model use `skills-vault:vault-search`, and once with `/skills-vault:vault-search notion`. Check that each invocation produced exactly one payload across both events (if not, `--usage-log` dedupes by session_id + skill within 5 s). Record the field names and that result in this card's handoff row, never the raw payloads.
2. Move the card to Waiting on Jeff for the store decision. On his word, a session with the Notion connector creates A or B, and reads it back.
3. Implement `--usage-log`, `--usage-flush` and `--usage-report`, then copy the script into the skill folder.
4. Write the tests:
   - parsing: Skill and slash payloads, other tools ignored, malformed input ignored, prefix stripped, args never stored, no request made
   - fold: two processes append 500 lines each and 1000 are counted; a kill after `counts.json` is written but before the `.fold` file is deleted does not double count
   - flush: a kill after the first pushed key followed by a rerun leaves Uses unchanged; while the lock is held a second flush writes nothing; a stale lock is taken over; Last used moves forward only; dry-run writes nothing; the token never appears in output
   - report: grace, vault-operations exempt, not-measured, and no Project or Computer label and no non-vault name in the output

   `python3 -m unittest discover -s scripts -p 'test_*.py' -v` must pass; 111 tests pass today.
5. Measure speed and silence. Pipe a saved payload into `bash hooks/skill-usage.sh` 20 times with `NOTION_TOKEN=dummy`, a scratch `SKILLS_INVENTORY_STATE` and `NOTION_API_BASE=http://127.0.0.1:9`. It passes when the median is under 300 ms, stdout is empty, the exit code is 0 every time and the log has 20 lines.
6. Run end to end. Use `claude -p --plugin-dir <checkout>` with the same environment, twice. The async hooks fire in print mode, the log gains a line, the second run's flush fails silently against port 9, and the counts stay dirty.
7. Add check 11. Exit 2 means ⏭️ with the reason. No suggestion means ✅ (with counts). A suggestion means ⚠️ plus a Suggested fixes line: "consider deprecating <skill> (Jeff decides; a core session sets vault_status deprecated + deprecated_reason)". The check never edits Notion and never prints the token.
8. Update the docs and `handoff.md`. Commit as `scripts: skill usage logging`, open a PR and merge it from a core session (as with PR #42).
9. Go live, which is Waiting on Jeff: he refreshes the `tradecreditor-vault` marketplace and updates the plugin on the main computer. After his next sessions, read back one real row with the connector or with `--usage-report`.

### Done when
- The PR is merged to `main`, all tests pass (copy identity included), `diff CLAUDE.md AGENTS.md` is empty, and the timings from steps 5 and 6 are in the PR.
- The plugin is updated on the main computer, and at least one usage row written by a real flush has been read back.
- The first Monday `outputs/health/<week>.md` after go-live has §11 at ✅ or ⚠️ (not ⏭️), and contains no Project or Computer label.
- The handoff row is Done, with Detail naming the PR and that report.

### Decisions for Jeff
- Where the counts live: A (recommended), a new "Skill Usage" database on Skills HQ, or B, two new properties on Skill Installs. Either one changes the Notion schema.
- The 60-day rule only suggests deprecation in the lint report, and you decide each one. `vault-operations` skills are exempt, and skills captured less than 60 days ago get grace.

### Risks and rules
- Privacy: this repo is public. Project paths stay in the local cache. Project and computer labels go to Notion only. Public output shows vault skill names and counts only, and the step 4 test enforces it. Never put a label, hostname, project name or raw payload in a commit.
- Protected paths (`hooks/`, `scripts/`, `skills/*/scripts/`, `routines/`, `CLAUDE.md`, `AGENTS.md`): only a core session may edit them. Never delete or rename files.
- Review gate: `tracking-skill-installs-in-notion` stays draft, and `skill-review` reviews its new hash. Do not touch approved skills.
- Notion: never write test rows to a live database. Use `FakeNotion` or `--dry-run`. Schema changes only on Jeff's word.
- Hooks: async, always exit 0, no network per call. A flush makes at most about 40 requests at about 3 per second. The Notion API is free, and no paid reader is used.

### Decisions for Jeff (from the reviewer pass)
- Choose where skill usage counts live: (A, recommended) a new Notion database 'Skill Usage' on Skills HQ with one row per skill, project, computer and ISO week, or (B) two new properties 'Uses' and 'Last used' on Skill Installs rows (no weekly history; two computers sharing a project would overwrite each other's counts). Either one changes the Notion schema.
- Confirm that the 60-day zero-use rule only produces deprecation suggestions in the weekly lint report (you decide each deprecation), that vault-operations skills are exempt because Routines read them as files and no hook sees them, and that skills captured less than 60 days ago are in grace.

## 5. Automatic clearing of rejected skills, stale drafts and orphan pages

Card: Backlog · P2 · Owner Claude Code · depends on: none

**State:** Backlog, not started. Lint W46 found 7 rejected draft skills that were never fixed. 5 of the in-scope ones are more than 14 days past review, and the oldest was reviewed 2026-10-04. It also found 94 entries at draft for more than 30 days, 29 orphan pages and 6 empty Related sections. Parts (a) and (c) can start now. Step 7c and the page-status rule (b) wait on Jeff's two decisions.

**Next step:** Write the fail-closed fix gate scripts/skill-fix-gate.sh on a claude/ branch

### Goal
The existing `skill-review` and `vault-lint` Routines clear the vault's backlog without a new Routine:
- Each rejected draft skill gets one automatic fix and a fresh independent review, then ends up approved or retired.
- Wiki entries stop sitting at `draft` forever.
- Orphan pages and empty `## Related` sections get links.

### Why
Sources: lint W46 (`outputs/health/2026-W46.md` §4, §6, §7) and the KPI table in `outputs/20261109-vault-performance-review.md`.

**Rejected draft skills left untouched more than 14 days after their review.**
- 5 today: configuring-fable-advisor-jev-tree, evaluating-llms-with-promptfoo, making-product-videos, providing-design-references and using-obsidian-skills. The oldest was reviewed on 2026-10-04, 36 days ago.
- 6 from 2026-11-21, when stacking-coding-agent-plugins (reviewed 2026-11-07) also passes 14 days.
- Target: 0.
- Out of scope: `model-tiering` (vault-operations, it has its own card) and `tracking-skill-installs-in-notion` (never reviewed, so not rejected).

**Entries at `status: draft` for more than 30 days.**
- 94 of 133 today. The other entries include 7 marked verified, all set by Jeff himself.
- Target: under 20 within 4 weeks.

**Orphan pages plus empty Related sections.**
- 29 + 6 = 35 today.
- Target: 5 or fewer.

### Design
**(a) Fix pass: new steps 7b and 7c in `routines/skill-review.md`.**
The Routine stub reads this file from `main`, so a merged edit is live on the next run. Both steps run on every run, after step 7, including runs where the review queue was empty.

- **Which skills qualify for a fix.** A skill qualifies when all of these hold:
  - `vault_status` is "draft" and `review_report` is set.
  - `review_hash` equals H, the current `static_scan.py --hash` value. This means nothing changed since the FAIL.
  - `reviewed_at` is at least 14 days old.
  - `origin_type` is not "vault-operations".
  - No `outputs/skill-fixes/*-<name>.md` record exists.

  At most 2 skills per run, oldest `reviewed_at` first.
- **The fixer.** A NEW subagent type, `vault-skill-fixer`, defined in `.claude/agents/vault-skill-fixer.md`.
  - Model sonnet; tools Read, Glob, Grep, Edit and Write only. With no Bash and no web access it cannot run, fetch, commit or push anything.
  - If that type is not offered in a run, skip 7b and say so. Never fall back to a general-purpose subagent.
  - The request is exactly "Fix skills/<name> per <review_report>".
  - It changes only what the report's `fail` items, its `critical` list and its `summary` name, and edits only `SKILL.md` and `references/`.
  - The preferred fix removes an unsafe or unverified step, or discloses it in the description. The description stays at most 300 characters and keeps "Use when".
  - It adds no URL, host, install command or run command, and never touches metadata or `scripts/`.
  - Its final message is one JSON object: `{"addressed": [ids], "changed": bool}`.
- **The gate.** A NEW script, `scripts/skill-fix-gate.sh`, that fails closed on the whole working tree.
  - `begin <name>`:
    - Requires `git status --porcelain --untracked-files=all` to be empty. If it is not, the script exits 3 and 7b is skipped for this run.
    - Saves HEAD as H0 and saves the `--ignored` status listing to a state directory outside the repo.
  - `check <name> <state>` passes only if all of these hold:
    - HEAD still equals H0.
    - Every path that is new or changed compared with the snapshot (`git status --porcelain --ignored --untracked-files=all`) is under `skills/<name>/` and not under `skills/<name>/scripts/`.
    - After `git add -N skills/<name>`, no added line in `git diff -- skills/<name>` matches `https?://|curl |wget |npx |pip |uv tool|git clone|_BASE_URL`.
    - No added or removed line touches `vault_status`, `reviewed_at`, `reviewed_by`, `review_hash` or `review_report`.
    - `static_scan.py skills/<name>` exits 0.
  - When the checks pass, it prints `fixed` or `no-change`.
  - Any failure runs `git reset --hard H0`, removes the paths that are new since the snapshot, prints `reverted` and exits 1.
- **Record and commit.** The orchestrator never reads the skill files or the fixer's prose.
  - It writes `outputs/skill-fixes/<YYYY-MM-DD>-<name>.md` (NEW folder) with:
    - the report the fix was made against
    - the outcome
    - the addressed ids, copied only if they exist in that report's JSON
    - one 繁體中文 paragraph based on the report and the diffstat
  - It appends `## [date] review | <name> fix <outcome> | outputs/skill-fixes/<date>-<name>` to `wiki/log.md`.
  - It stages explicit paths only, never `git add -A`: `git add skills/<name> outputs/skill-fixes/<file> wiki/log.md`.
  - It commits `chore: auto-fix <name>` and runs `bash scripts/vault-guard-check.sh H0 HEAD Tradecreditor`. If that fails, it runs `git reset --hard H0`.
  - It then runs `git pull --rebase origin main` and `git push origin HEAD:main`, and checks the tip of `origin/main` as in step 7.
  - A `reverted` or `no-change` outcome commits only the record and the log line.
  - The new hash puts the skill in the next run's review queue. That run's fresh reviewer gets only "Review skills/<name>".
- **7c: deprecation candidates.** A skill is a candidate when it is still draft, its `review_hash` equals H, and it has a fix record dated before today that meets one of these:
  - Its outcome is `fixed` and `reviewed_at` is after the record's date (the skill failed again after the fix).
  - Its outcome is `no-change` or `reverted`.

  Decision 1 sets how candidates are handled. Under (i) the routine:
  - sets `vault_status` "deprecated" and adds a metadata `deprecated_reason`
  - updates the skill's cell in `skills/README.md`
  - adds a `deprecate` log line
  - commits `deprecate: <name>` and pushes as above
- **Other changes to the routine.**
  - Step 7's "no skills to review" no longer ends the run.
  - Step 8's final message adds one line per fix (with its outcome) and one per deprecation.
  - The NEVER line gets one exception: the 7b fixer may edit a skill's body and references, never its scripts.

**(b) Page status: new `vault-lint` step P after the checks, following Decision 2.**
Nothing reads page status today: neither `wiki/reads.base` nor `vault-search` uses it.

Under B1, an entry is eligible when all of these hold:
- `captured_at` is more than 30 days old.
- `needs_manual_text` is false.
- For a page, `raw/<slug>*.md` exists.
- Checks 1, 2, 4, 5 and 7 have no finding for the entry.
- `wiki/log.md` has no earlier `promote` line for the slug, so a page Jeff sets back to draft stays draft.

For each eligible entry, step P:
- sets `status: verified` and `verified_by: "rule:vault-lint"` (a NEW optional key)
- syncs the entry's status cell in `wiki/index.md`
- appends `## [date] promote | <title> | <slug>` to `wiki/log.md`

Step P promotes at most 30 entries per run, oldest first, and the report lists every promoted slug. A count on 2026-11-09 found 65 of the 94 eligible. Most of the others are orphans (23), which (c) fixes.

**(c) Link repair: new `vault-lint` step R after check 7.**
- Targets: check 4's orphans and empty Related sections, oldest first, at most 15 per run.
- For each target, find 1 to 3 related entries using `bash skills/vault-search/scripts/search.sh "<3 keywords>"` and shared tags.
- Add the link on both sides. The new inbound link is what fixes an orphan.
- Line format: `- [[<relative path>|<title>]] — <繁體中文 reason>`, as in `wiki/stars/DietrichGebert--ponytail.md`. Keep the frontmatter `related:` list in sync.
- Put one `topic/*` tag first on post, video and article pages that lack it (8 in W46), and update the tags cell of that page's row in `wiki/index.md`.
- It writes only to `wiki/pages`, `wiki/stars` and `wiki/index.md`.

### Files
- `routines/skill-review.md` — existing, protected. Add steps 7b and 7c, and change steps 7 and 8 and the NEVER line.
- `.claude/agents/vault-skill-fixer.md` — NEW, protected. The fixer subagent described above.
- `scripts/skill-fix-gate.sh` — NEW, protected. The `begin` and `check` gate.
- `routines/vault-lint.md` — existing, protected.
  - Add step R, and step P once Decision 2 is made.
  - Update the "Check, without modifying any content pages" line and the list of safe fixes.
  - Check 4 reports found and repaired counts.
  - Check 6 lists only the drafts that fail the rule, with the reason.
- `routines/README.md` — existing, protected. Update the skill-review and vault-lint rows.
- `CLAUDE.md` and `AGENTS.md` — existing, protected. One `docs:` edit, kept identical in both files, covering:
  - what draft and verified mean for pages and stars
  - the optional `verified_by` key
  - `deprecated_reason` in the skill metadata list
  - the fix pass, under "Skill format"
  - `outputs/skill-fixes/` in the folder roles table
- `outputs/skill-fixes/<YYYY-MM-DD>-<name>.md` — NEW, not protected. One record per fix attempt.
- `skills/<name>/SKILL.md` and `skills/<name>/references/` of the in-scope rejected drafts — existing, not protected. Changed by the fixer, or in the metadata when a skill is deprecated.
- `skills/README.md`, `wiki/pages/*.md`, `wiki/stars/*.md`, `wiki/index.md`, `wiki/log.md` — existing, not protected.
- `scripts/handoff-check.sh` — existing, protected, no change. Both Routines push to `main`, where the Stop hook exits early and the PR-only `handoff` job does not run.
- `handoff.md` — existing, not protected. This card's row and a Session log line.

### Steps
1. On a `claude/` branch, move this card's existing `handoff.md` In flight row from Backlog to In progress (Owner Claude Code). Do not add a new row. Ask Jeff Decisions 1 and 2.
2. Write `scripts/skill-fix-gate.sh` and `.claude/agents/vault-skill-fixer.md`.
3. Test the gate on a clean tree, starting each case with `begin`:
   - (i) a `curl https://example.com` line added to `skills/providing-design-references/SKILL.md`
   - (ii) a new `references/x.md` in that folder containing `npx foo`
   - (iii) a new `routines/x.md`
   - (iv) a change to `vault_status`

   Each case must print `reverted` and leave HEAD equal to H0 and the status listing equal to the snapshot. Then (v): deleting one line must print `fixed`; restore the file with `git checkout`. Paste all outputs into the PR.
4. Write step 7b and the changes to step 7, step 8 and the NEVER line.
5. Dry-run 7b by hand on providing-design-references (its report asks for the unverified install section to be removed). Run the fixer, the gate and the record, and commit on the branch only. If the new subagent type is not offered, start a fresh session on the branch. Then follow routine steps 2 to 6 with a fresh `vault-skill-reviewer` and paste the verdict into the PR.
6. Write step R. Run it by hand on these 3 orphans:
   - 20260821-git-vs-github-mental-model
   - 20261003-backup-agent-workflows-as-skill-zips
   - 20261012-anatomy-isometric-explainer-skill

   Rerun the check-4 orphan scan and confirm at least 3 fewer orphans. Commit `wiki: related links for 3 orphans`.
7. After Jeff's decisions:
   - Write step 7c and step P.
   - Make the `docs:` edit and confirm `diff CLAUDE.md AGENTS.md` is empty.
   - Dry-run step P read-only and list in the PR body the entries it would promote today. Promote nothing in the PR.
8. Update `routines/README.md` and `handoff.md`, then open the PR. `guard` and `handoff` must be green. Move the row to Waiting on Jeff with Next step `Jeff: merge PR #N`.
9. After the merge:
   - Record as evidence the first `chore: auto-fix` commit, the next `review:` commit with its new report, and the next Monday `lint: WEEK` commit.
   - If step R has linked the 5 pages of the "WhatsApp link drop follow-ups" row, close that row too.

### Done when
- The PR is merged to `main` with every file above, and `CLAUDE.md` is identical to `AGENTS.md`. The gate test outputs and the providing-design-references verdict are in the PR.
- Live: a scheduled skill-review run pushed an `outputs/skill-fixes/` record and a `chore: auto-fix` commit. A later run then either reviewed that skill (a new `outputs/skill-reviews/` report) or applied Decision 1.
- Live: the first Monday vault-lint after the merge shows:
  - orphans plus empty Related below 35
  - under B1, `promote` lines, with drafts older than 30 days below 94
- This card's handoff row is Done, with Detail pointing to the PR, the commit SHAs and the report paths.

The 4-week KPI targets are tracked by the weekly lint and are not part of Done.

### Decisions for Jeff
1. **A skill that fails again after its one fix, or whose fix ended `no-change` or `reverted`.**
   - (i) Recommended: the routine deprecates it itself. This can be reversed by hand, and a draft cannot be installed anyway.
   - (ii) Lint only lists it, and a core session deprecates it on Jeff's word.
2. **What draft and verified mean for pages and stars.**
   - B1, recommended: lint promotes entries by the rule above and marks them `verified_by: "rule:vault-lint"`, at most 30 per run. Jeff's own changes stay distinguishable because they carry no marker.
   - B2: drop the distinction for pages and stars. This rewrites 133 notes, the index, lint check 1, github-stars-sync and the verified vault-capture skill.

### Risks and rules
- **Review gate.** The fixer never sets a status. Only the next run's fresh reviewer, with step 4's checks unchanged, can approve. Verified skills and vault-operations skills are never auto-fixed or deprecated.
- **Untrusted text.** Skill files and the fixer's output may be written to persuade. The orchestrator does not read them, applies only the scripted gate and copies only report ids. The fixer has no Bash.
- **Protected paths.** `routines/`, `scripts/`, `.claude/`, `CLAUDE.md` and `AGENTS.md` may be changed only by a core session. No tracked file is deleted or renamed; the gate removes only files the fixer created in that run. `raw/` is untouched.
- **Privacy.** This repo is public. Records, reports and commits name only vault skills and pages. Install locations stay in Notion.
- **Cost.**
  - At most 2 Sonnet fixer runs per day.
  - Re-reviews fall inside the existing cap of 8 Opus reviews per run.
  - Each weekly Sonnet lint run repairs at most 15 pages in step R and promotes at most 30 entries in step P.
  - No new Routine, secret or Notion schema change.
- **Skill Installs.** A deprecated skill that is still installed stays flagged by `skills-inventory.py --audit`, because draft-installed covers deprecated.

### Decisions for Jeff (from the reviewer pass)
- A rejected skill that fails review again after its one automatic fix, or whose fix ended no-change or reverted: (i) recommended, the skill-review routine deprecates it itself by setting vault_status deprecated plus deprecated_reason. This can be reversed by hand, and a draft cannot be installed anyway. (ii) The routine and lint only list it, and a core session deprecates it on your word.
- What draft and verified mean for wiki pages and stars: (B1, recommended) vault-lint promotes an entry to verified when it is more than 30 days old, is not needs_manual_text, has its raw file and has no open lint finding. It marks the entry verified_by rule:vault-lint, so your own changes in Obsidian stay distinguishable, and promotes at most 30 per run; a count on 2026-11-09 found 65 of the 94 eligible. (B2) Drop the draft/verified distinction for pages and stars. This rewrites all 133 notes, the index, lint check 1, github-stars-sync and the verified vault-capture skill.
- Reviewer issues checked against the repo: all six were confirmed and fixed in this revision. One example is the count of rejected skills untouched more than 14 days, which is 5 today, not 6.

## 6. Demand-driven skill discovery in the weekly hot list

Card: Backlog · P2 · Owner Claude Code · depends on: none

**State:** Not started. The weekly hot list ranks candidates only by stars and likes. None of its 24 winners from W38-W45 became a SKILL.md, and no step searches for what Jeff's projects need.

**Next step:** Ask Jeff to answer Decisions for Jeff 1-3 (needs source, what happens to picks, test plan), then record his answers in handoff.md before building anything

### Goal
Every weekly hot-list report gets a new `## 你需要嘅` section. It lists up to 3 installable skills (GitHub repos or SkillsMP skills) found by searching on Jeff's current needs, not on star growth. No private project information reaches any repo file. Installable picks are captured and get a draft SKILL.md, so `skill-review` can approve them and `vault-search` can recommend them.

### Why
This is row 6 (按需求捕捉) of the table 點樣變成 pro-active skill database in `outputs/20261109-vault-performance-review.md`. The review found that intake is passive:
- Pasted-link captures fell from 37 (W40) to 0 (W45-W46).
- The 24 hot-list winners (W38-W45) were picked on popularity alone, and none became a SKILL.md.
- 0 of the 14 skills captured from the web are installed anywhere.
- Capture-to-skill is about 15% (14 skills / 96 pages).

Today the hot list finds 0 installable picks a week that match a need. Targets over the 4 scheduled runs after the first live one:
- Every report names at least 1 pick per active need, or says why there was none.
- At least 4 demand drafts in total (if Decision 2 is "draft"), and at least 2 of them reach `reviewer-approved`.
- Capture-to-skill moves from 15% toward about 20%. The review's 30% KPI ("Capture → skill（包括外部 registry）") is shared with the external-registry card; this card cannot reach it alone.

### Design
**Need vocabulary (public).** A NEW file, `wiki/hot-list/_needs.json`, holds the needs. It is JSON because the script uses only the standard library, which has no YAML parser. Each entry has:
- `id`: a CLAUDE.md topic id without the `topic/` prefix. Start with seo-geo, marketing-content, video-gen, sales-ops, infra-devops and knowledge-mgmt. Agent topics are already covered by the trending search.
- `keywords`: generic English words, plus generic Chinese words where cards use Chinese.
- `queries`: at most 2 public search strings.
- `pinned`: true only on Jeff's word.

The file holds generic words only: no product, client, project or host names.

**Needs signal (private, read-only).** A NEW script, `scripts/skill-demand.py` (Python 3.9+, standard library only), follows the settings and exit-code conventions of `scripts/notion-sync.py`:
- Settings: `NOTION_TOKEN` (never printed); `NOTION_API_BASE` (localhost only, for tests); `NOTION_VERSION`; `NOTION_PROJECTS_DS` / `NOTION_SKILLS_DS`, or the title searches.
- It sends only GET, `POST /v1/search` and `POST …/query`, and never writes.

It has two modes:
- **`--needs <file>`** reads every open card of "Project Status" (Backlog, In progress, Waiting on Jeff, Blocked). It matches each card's title, Area and Next step against the keywords: whole word and case-insensitive, or substring for CJK keywords. It prints one JSON line, `{"needs":[{"id":"seo-geo","pinned":false,"areas":2}],"cards_read":31}`.
  - Output rule: only ids that exist in the needs file, booleans and integers. It never prints a title, Area, Next step or matched word.
  - This is stricter than `notion-sync.py --audit`, which does print the titles of its own source's cards.
- **`--leak-check <file>…`** collects private terms from Notion and prints only `file:line` for each hit. The terms are:
  - whole titles of cards whose Source is not `skills-vault/handoff.md`, matched as phrases;
  - Area options other than `skills-vault`;
  - the repo part of every other `<repo>/handoff.md` Source option;
  - Skill Installs `Project` options other than `skills-vault`. For a `global:<x>` label, only `<x>` is matched.

  To stop ordinary words from firing, the check skips terms shorter than 4 characters and terms in a built-in GENERIC set. That set holds the topic-vocabulary words and a fixed list of common English words, written without looking at the live Areas. An Area outside a repo is a life or business area (board-policy §2) and can be an ordinary word. Stderr prints counts only.

Exit codes: 0 ok, 1 leak found (`--leak-check` only), 2 off (no token, 401/403, a data source not shared or ambiguous, host unreachable), 4 refused locally.

**Choosing needs and searching (NEW routine step 1g, after 1f).**
1. Run `--needs`. Active needs are the pinned needs plus every need with `areas` ≥ 1. Pinned needs rank first, then by `areas`, up to `demand.max_needs_per_run`. If the script exits 2, use pinned needs only and give the reason in the `demand:` line.
2. For each active need and each of its queries, run two searches:
   - a GitHub repo search, in step 1a's tool order: `<query> stars:>=<min_stars> pushed:>=<today - max_days_since_push>`, sorted by stars, 10 results;
   - a SkillsMP search, using the URL already in `sources.registries`, read with `bash scripts/read-url.sh --fresh`.
3. Keep a result only if all of these hold:
   - It is installable: it has a SKILL.md, a `.claude-plugin/` manifest, or an `npx skills add` / `claude plugin install` / MCP install command. Check the README on raw.githubusercontent.com (free). A root listing through the connector's `get_file_contents` counts toward `max_github_calls`.
   - It has a license.
   - It is not already in the vault (step 1's canonical_id grep). A result that is already in the vault is listed as "already in vault" and not captured again.
4. Pick at most `demand.max_picks`, one per need first.

Picks are not winners: they get no heat score and no gates, and never count toward the winners, `social_rule` or `quiet_week`.

**Report and captures (step 3).**
- `## 你需要嘅` goes between `## 你貼嘅 link` and `## Watch`.
  - It opens with one line: "not reviewed; install only after the vault draft is reviewer-approved".
  - Then a table with these columns: Need · Item (owner/repo or registry skill, with URL) · Install command · Numbers (stars, last push, registry installs) · Vault action (captured / drafted / already in vault) · Why (one line, in 繁中).
  - There is no pinned-vs-board column. That signal goes in the routine's final message only.
  - When nothing qualifies, the section says "none this week (<reason>)".
- Picks are captured with the vault-capture procedure: `captured_by: routine:weekly-hot-list`, tags `hot-list`, WEEK, `demand` and the need id. Installable picks get a draft SKILL.md, at most `demand.max_skill_drafts` a week.
- Page text names the need id only ("matches need seo-geo"), never a project.
- One `demand:` line goes under `## 方法`, in the shape of `demand.report_line`, with no card counts. One line goes under `本週熱門榜` in `wiki/hot.md`.

**Leak check, scoped to demand text.**
- The routine drafts the section, the `demand:` line and every pick's `raw/`, `wiki/pages/` and SKILL.md files in a temp dir outside the repo (`mktemp -d`).
- It runs `--leak-check` on all of them in one call. Only files that pass are copied into the repo; the index, log and hot rows follow.
- On exit 1: drop each pick that has a hit (its row, capture and draft) and run the check once more. If the section still hits, replace it with "none this week (leak-check)".
- The check never edits other sections or source text, and never holds back the winners. Everything else is pushed, and the `demand:` line says `leak-check dropped <n>`.
- On exit 2: the line says `leak-check off (<reason>)`, and the section still ships, because the routine itself never saw private text.

**Config.** A NEW `demand:` block in `wiki/hot-list/_config.yaml` holds:
- `enabled`, `needs_file`, `client`.
- `max_needs_per_run: 3`, `queries_per_need: 2`.
- `min_stars: 200`, `max_days_since_push: 90`.
- `max_picks: 3`, `max_skill_drafts: 2`.
- `max_github_calls: 20`. This sits inside `cost_caps_per_run.github_api_calls` (200); W45 used about 36.
- `max_registry_reads: 6`.
- `report_line: "demand: needs <active>; github <calls>; registry <reads>; picks <n> (<drafted> drafted, <in_vault> in vault); leak-check <ok|dropped n|off (reason)>"`. It reads `demand: off (<reason>)` when disabled.

Demand uses 0 `web_searches` (W45 used all 30 of 30). Exa is used only as the existing fallback inside `exa_calls`, when `read-url.sh` exits 2.

**Jev is not used.** H1 and H2 judge whether an item is in the vault's scope, not whether it fits a need. H4 `installable_skill` exists in `skills/judging-with-jev/references/vault-routine-questions.md` (marked "later"), but it has no `jev:` block and no `report_line` field. Adding one would change the line that vault-lint check 8 parses. The `jev:` line stays exactly as it is.

### Files
- `wiki/hot-list/_needs.json` - NEW - protected no - the need vocabulary.
- `scripts/skill-demand.py` - NEW - protected yes - the needs signal and the leak check.
- `scripts/test_skill_demand.py` - NEW - protected yes - tests against a fake Notion server, on the pattern of `scripts/test_skills_inventory.py`.
- `wiki/hot-list/_config.yaml` - existing - protected no - adds the `demand:` block.
- `routines/weekly-hot-list.md` - existing - protected yes - five changes:
  - step 0 reads the `demand:` block and the needs file;
  - a new step 1g;
  - step 3 adds the section, temp-dir drafting, the leak check, the captures and the hot.md line;
  - step 5's final message lists the picks and each need's signal (pinned / board).
- `routines/README.md` - existing - protected yes - two changes:
  - The `NOTION_TOKEN` row adds weekly-hot-list step 1g (read-only `--needs` and `--leak-check`).
  - Step 5, for `weekly-hot-list`: drop "paste a note into the run text", because a schedule-type Routine's Run now passes no run text (`handoff.md` Environment facts). Drop the disposable-branch claim, because since 2026-10-30 a Run now pushes to `main`. Then state the test practice from Decision 3.
- `CLAUDE.md` and `AGENTS.md` - existing - protected yes - the `wiki/hot-list/` folder-role row names `_needs.json`. Make an identical edit in both.
- `handoff.md` - existing - protected no - an In flight row and a Session log line.
- `scripts/handoff-check.sh` - existing - protected yes - no change. The routine writes only exempt paths (reports, `raw/`, `wiki/pages/`, index/log/hot) plus `skills/` drafts on `main`, where the Stop hook skips and the PR-only `handoff` job does not run. `_needs.json` stays non-exempt on purpose: editing it is a config change and needs a handoff line.

### Steps
1. Get Jeff's answers to Decisions 1-3. On a `claude/…` branch, add the In flight row (In progress, Claude Code) in the first commit.
2. Write `_needs.json`. Check that `python3 -c "import json;json.load(open('wiki/hot-list/_needs.json'))"` passes and that every id is in the CLAUDE.md topic list.
3. Write `scripts/skill-demand.py` and its tests. The tests cover:
   - open versus closed cards;
   - whole-word and CJK matching;
   - a planted "ZZPRIVATE" title and Area never appearing in stdout;
   - unknown ids never printed;
   - `--leak-check` printing only `file:line`;
   - `--leak-check` catching a planted title phrase, Area, project and `global:` label, and skipping a GENERIC Area (e.g. "Marketing") and short terms;
   - exit 2 without a token, and exit 4 with a non-localhost API base;
   - the token never printed.

   Run `python3 -m unittest discover -s scripts -p 'test_*.py' -v`; every suite must pass.
4. Run a live, read-only check, only if this session has `NOTION_TOKEN`. Otherwise say so and rely on the tests.
   - `--needs` prints only ids, booleans and integers.
   - `--leak-check wiki/hot-list/2026-W45.md` should exit 0. This calibrates against hundreds of public repo descriptions.
   - Any hit means the term rules are too loose. Tighten them in the script, never by writing the matched word into a repo file or editing the report.
   - Never paste stderr or hit lines into a commit or PR.
5. Add the `demand:` block. Edit `routines/weekly-hot-list.md` (steps 0, 1g, 3, 5), `routines/README.md`, `CLAUDE.md` and `AGENTS.md`.
6. Rehearse step 1g and the demand part of step 3 in this session for the W45 window, exactly as the edited prompt says:
   - Work in a temp dir outside the repo and commit nothing.
   - Run the leak check on the drafts.
   - Count the GitHub calls (must be ≤ 20).
   - Show the section to Jeff in chat.
7. Update `handoff.md`: the row moves to Waiting on Jeff with "Jeff: merge PR #…", plus a Session log line. Open the PR with the unittest summary, and check that `guard` and `handoff` are green.
8. After the merge, read the first scheduled report after the merge (Mon 2026-11-16 / W46 at the earliest) and the next health report. Then close the card.

### Done when
- The PR is merged to `main`, its description shows the unittest summary, and `guard` and `handoff` are green.
- The first scheduled report after the merge, on `main`, has all of these:
  - `## 你需要嘅` with at least 1 active need, and at least 1 pick or a stated reason, and no pinned/board column;
  - a `demand:` line showing demand GitHub calls ≤ 20, a run total ≤ 200, and 0 demand web searches;
  - a `jev:` line with the same shape as before, and vault-lint check 8 ✅ in the next `outputs/health/` report.
- The closing session extracts that section to a temp file. It runs `--leak-check` on that file plus the run's demand pick files (`raw/`, `wiki/pages/`, SKILL.md), and the check exits 0, or exits 2 with the reason recorded.
- The `handoff.md` row is Done, with Detail set to the PR and the report commit.

### Decisions for Jeff
1. **Where do needs come from?** Pick one:
   - (a) Recommended: the script matches open Projects HQ cards in all Areas against the generic keywords and returns only need ids. Pinned needs are added on top. Each public report then shows which generic need ids are active that week, never why.
   - (b) Pinned needs in the public `_needs.json` only, with no Notion read.
   - (c) A new private "Skill Wishlist" database on Skills HQ that agents fill on Jeff's word. This is a new Notion schema.

   Also: which need ids, if any, start pinned?
2. **What happens to picks?** Pick one:
   - Recommended: capture them and draft a SKILL.md for installable ones. This adds at most 2 drafts a week to skill-review.
   - List them in the report only.
3. **How is the change tested?** A Run now would recompute the last full week and push a rewrite of that report to `main`, and it passes no run text. Is it OK to replace the 2026-10-02 "Run now after every change" practice for this routine with an in-session rehearsal plus the first scheduled run?

### Risks and rules
- **Privacy.** The repo is public. From Notion, only need ids may reach a file, commit, PR or report. Never write titles, Areas, project or host names, card counts, or the pinned-vs-board signal.
  - The guards are: the whitelisted script output (the routine never sees private text), the planted-string tests, and the scoped leak check run before files enter the repo.
  - `raw/` is immutable once pushed and the guard rejects edits, so pick files are checked in the temp dir first.
  - Never put a matched private word into the GENERIC set or any repo file.
- **Protected paths.** `scripts/`, `routines/`, `CLAUDE.md` and `AGENTS.md` may be changed only by a core session. Never delete or rename files. `raw/` is add-only.
- **Review gate.** Drafts start at `vault_status: "draft"` and must pass the guard's SKILL.md rules (name == folder; description ≤ 300 characters and containing "Use when"). Only skill-review approves them. The section never recommends installing an unreviewed item.
- **Cost.** No new paid source. Demand spends at most 20 of the 200 GitHub calls, SkillsMP is free, and demand runs 0 web searches. Exa is used only inside `exa_calls`. There is no Jev or TypeSafe cost. Skill-review gets at most 2 extra drafts a week.
- **Notion.** Access is read-only. There is no schema change unless Jeff picks 1(c).
- **handoff.md.** Every commit that touches `scripts/`, `routines/`, `_config.yaml`, `_needs.json`, `CLAUDE.md` or `AGENTS.md` also updates `handoff.md`.
- **Overlap.** The external-registry card also edits step 3 of `routines/weekly-hot-list.md`, so rebase on whichever merges first. If that card is live, installable picks also get a registry row in its format.

### Decisions for Jeff (from the reviewer pass)
- Needs source: (a) recommended, the script keyword-matches open Projects HQ cards in all Areas and outputs only generic need ids, plus pinned needs, so each public report shows which need ids are active that week but never why; (b) pinned needs in the public wiki/hot-list/_needs.json only, with no Notion read; or (c) a new private Skill Wishlist database on Skills HQ, which is a new Notion schema. Also: which need ids, if any, start pinned?
- Demand picks: capture them and draft a SKILL.md for installable ones (recommended; at most 2 drafts a week go to skill-review), or only list them in the report section?
- Testing: a Run now of weekly-hot-list would recompute the last full week and push a rewrite of that report to main, and it passes no run text. Is it OK to test this change with an in-session rehearsal plus the first scheduled run after the merge, instead of the 2026-10-02 Run-now practice?

## 7. Reviewer-approved model-tiering skill

Card: Backlog · P2 · Owner Claude Code · depends on: none

**State:** model-tiering is still draft. It failed skill review on 2026-10-04 on S2 (it sends bulk judgments to the third-party Jev API), and it also mixes up Haiku and Sonnet and uses old model IDs. Its hash has not changed since then (83e5bb68). It is installed globally on the main computer, so the 2026-11-09 --audit run in the handoff Session log reports draft-installed=1.

**Next step:** Load the claude-api skill, re-fetch the live advisor-tool doc with scripts/read-url.sh, and check this card's defect list against cat -n of the files in skills/model-tiering

### Goal
`skills/model-tiering` passes the skill-review procedure (`vault_status: "reviewer-approved"`). The copy installed globally on the main computer is then replaced with the reviewed files, so no draft vault skill is installed anywhere.

### Why
- The 2026-11-09 review counts 4 vault skills among the 92 installs on the main computer, and `model-tiering` is the only one still in draft.
- The 2026-11-09 `--audit` run (handoff.md Session log) reports draft-installed=1. The target is 0. The W46 lint report came before check 10 existed, so §10 first appears in W47 or later.
- `outputs/skill-reviews/2026-10-04-model-tiering.md` failed the skill on S2 and on accuracy errors. Its hash is still `83e5bb68…`, so nobody has fixed it.
- Jeff chose to fix it rather than uninstall it (2026-11-09).

### Design
All line numbers come from today's `cat -n` output. They are 4 lines lower than the review's numbers because 4 review keys were added to the metadata.

**S2, the blocker.** The description (L3, 291 of 300 characters) promises only a Claude tier. But the L34 table row, Part C (L74-78) and the Jev evidence line (L94) tell the agent to "ask Jev first", which sends item contents to TypeSafe's third-party API.
- **Option A (recommended, and the default).**
  - Delete the L34 row and L94.
  - Keep the `## Part C` heading, because `skills/judging-with-jev/SKILL.md` L26 links to "model-tiering, Part C".
  - Replace the Part C body with 1-2 sentences saying that this skill sends nothing outside Claude; that the separate skill `judging-with-jev` sends typed yes/no, choice and score questions to TypeSafe's Jev, a third-party non-Anthropic API with its own key; and that it should be used only in a project that has opted in.
- **Option B: name Jev in the description.** Not recommended. Only 9 characters are left, and every install of a model-picking skill would become a Jev router.
- **Never edit `judging-with-jev`.** Any edit changes its hash, and the next review run sends it back to draft.

**Defects in SKILL.md**
- **L18, L27:** "Fable 5" and "typically Fable 5 or Opus" are previous-generation names. The Evidence line at L93 already cites Sonnet 5.5 and Opus 5.5.
- **L23:** prices for Fable 5, Opus 4.8 and Sonnet 5, an expired "intro $2/$10 through 2026-08-31", and a stray " .". Replace with current prices marked "as of <date>", or point to the live pricing page.
- **L33:** the row for trivial classification, extraction and formatting says `model: "sonnet"`, the same as L32. That contradicts L18 ("Sonnet / Haiku produce the bulk"). Change it to `"haiku"` after confirming the Agent tool accepts that value in the running Claude Code.
- **L37:** "user rule 2026-09-22" is a personal rule. Write it as a general rule or drop it.
- **L21, L43:** these name the owner's own cron agents and a pipeline, which mean nothing to anyone else who installs the skill. Use generic words such as "your cron agents, batch pipelines".
- **L53, L59:** previous-generation IDs (`claude-sonnet-5` executor, `claude-fable-5` / `claude-opus-4-8` advisor). The pair is still valid, but update to current IDs and a pair from the live table. For example, a `claude-sonnet-5-5` executor rejects Opus 4.x and Sonnet 5 advisors, and every advisor it accepts returns `advisor_redacted_result`.
- **L66:** "for my projects" is personal wording.
- **L67:** "Opus 5 advisor … advice visible in plaintext" is wrong: Opus 5 and 5.5 advisors return `advisor_redacted_result`. Opus 5 is also missing from the reference file's pair table.
- **L68:** "Fable 5.1 advisor" is missing from the reference file's pair table. The live table has it, so fix the reference table.
- **L69:** "Sonnet executor + Opus advisor … cheaper than switching executor to Sonnet/Opus" contradicts itself and repeats L67. It was meant to describe a Haiku executor.
- **L72:** "(helps Sonnet, neutral on Sonnet, hurts Opus)" should say it helps Haiku (reference L119-122). The same line's "removing the tool mid-conversation 400s" is outdated (see L88).
- **L88:** this common-mistakes row is outdated. Per the claude-api skill, removing the advisor tool no longer fails by itself. A 400 now comes from an advisor call that is still pending, or, where the history-editing check is enforced, from the `tools` edit invalidating the thinking blocks. The new rule is to change or remove the advisor only in a new conversation.
- **L89:** "Sonnet +7pp, Sonnet neutral" should read "Haiku +7pp, Sonnet neutral".
- **L78, L93:** the `[[../…]]` wikilinks and `outputs/` paths lead nowhere in an installed copy. Name the skill instead, or mark the path as inside the vault.

**Defects in references/advisor-tool.md**
- **L3:** fetched 2026-07-11. Re-fetch it and update the date.
- **L27-37:** the rule "Advisor must be Sonnet 4.6+" and a pair table with no 5.x models. Replace both from the live table.
- **L47-48, L52:** the set of advisors that return plaintext has changed, and "use claude-opus-4-8 to read advice" fails with a Sonnet 5.5 executor.
- **L54:** the error list now also includes `model_not_found`.
- **L59:** the tool-removal rule is outdated (same as SKILL.md L88).
- **L82:** re-check the Sonnet effort pairing, because Sonnet 5.5 recalibrated its effort levels.
- **L117-122:** label these results as measured on older models.
- **L124:** forcing `tool_choice` on the advisor returns 400 with Fable 5.1/5.2, Mythos 5.1/5.2, Opus 5.5 and Sonnet 5.5 executors.

**Model facts: check them, do not copy them.** The current family is Fable 5.2, Opus 5.5, Sonnet 5.5 and Haiku 5.5; the claude-api skill's model table is marked "cached 2026-11-03". Check every ID, price, pair and advisor-tool shape against the claude-api skill and the live doc. Neither the skill file nor this list is the authority.

### Files
- `skills/model-tiering/SKILL.md` - existing - protected: no - Option A, the fixes above, generic wording. Leave the metadata block untouched.
- `skills/model-tiering/references/advisor-tool.md` - existing - protected: no - refresh from the live doc with a new fetch date.
- `skills/README.md` - existing - protected: no - update the description cell only if the description changes. The review procedure sets the status cell.
- `outputs/skill-reviews/<YYYY-MM-DD>-model-tiering.md` - NEW - protected: no - written only by the review procedure, which also appends its line to `wiki/log.md`.
- `handoff.md` - existing - protected: no - this card's row and the Session log.
- `skills/judging-with-jev/SKILL.md` - existing - protected: no - read only.
- `routines/skill-review.md`, `.claude/agents/vault-skill-reviewer.md`, `skills/auditing-agent-skills/scripts/static_scan.py`, `scripts/{read-url.sh,vault-guard-check.sh,handoff-check.sh,skills-inventory.py}` - existing - protected: yes - read or run only.

### Steps
1. In the first commit, set this card's handoff row to In progress with Owner Claude Code.
2. Load the claude-api skill and read its model table and `shared/tool-use-concepts.md` § Advisor.
3. Run `bash scripts/read-url.sh https://platform.claude.com/docs/en/agents-and-tools/tool-use/advisor-tool`. Use Exa `web_fetch_exa` (`maxCharacters` 50000) only if that exits 2 or the page comes back cut off.
4. Run `cat -n` on both files and re-check every defect above against the current lines.
5. Edit SKILL.md (Option A plus the fixes) and refresh the reference file. Keep the description quoted, at most 300 characters, and containing "Use when".
6. Run these checks:
   - `python3 skills/auditing-agent-skills/scripts/static_scan.py skills/model-tiering` shows `summary.block` 0.
   - `--hash skills/model-tiering` no longer equals `83e5bb68…`, and `--hash skills/judging-with-jev` still equals `6992a8e9…`.
   - `grep -rnE "through 2026-08-31|Sonnet \+7pp|neutral on Sonnet|for my projects|user rule|claude-sonnet-5\"|claude-fable-5\"" skills/model-tiering` finds nothing.
   - `grep -rn "Jev" skills/model-tiering` finds only the Part C pointer.
   - The lines that replaced L21 and L43 name no specific agent product or personal pipeline.
   - `bash scripts/vault-guard-check.sh origin/main HEAD Tradecreditor` passes.
   - `bash scripts/handoff-check.sh origin/main HEAD` passes.
7. Commit as `docs: model-tiering fixes for skill review`, with the handoff row and a Session log line in the same commit. Run `git pull --rebase`, then push to `main`. A non-core agent opens a PR instead, which Jeff merges.
8. Get the review, in one of two ways:
   - Wait for the daily `skill-review` run at 07:47 UTC. It queues any draft whose `review_hash` differs from its current hash.
   - Or have a core session run `routines/skill-review.md` steps 1-8 for this skill only, with a fresh `vault-skill-reviewer` subagent. Never use the session that wrote the fix.

   Check `outputs/skill-reviews/` first so the skill is not reviewed twice. A session that runs the review on a branch also updates handoff.md, because `outputs/skill-reviews/` and `skills/` are not on the EXEMPT list in `handoff-check.sh`.
9. On FAIL, fix what the report names and repeat steps 6-8.
10. On PASS, wait for the next `github-stars-sync` step 7b (`--enrich`, daily at 06:00 UTC). Then run `python3 scripts/skills-inventory.py --audit --today <date>` and record its summary line. It needs `NOTION_TOKEN`; if it exits 2 with "skills-inventory: off", use §10 of the next `vault-lint` report instead. draft-installed=0 here proves only that the README now says reviewer-approved: `--enrich` matches by skill name, not by content.
11. Hand off. Set the row to Waiting on Jeff, Owner Jeff, with Next step `Jeff: in a Claude Code session on the main computer run npx skills add Tradecreditor/skills-vault --skill model-tiering -g -a claude-code -y (replaces the pre-fix copy)`. If that computer's Skill Installs row lists other agents, add one `-a <agent>` for each.
12. In that session, run `python3 skills/auditing-agent-skills/scripts/static_scan.py --hash <installed model-tiering folder>` from a vault clone. It must equal the new `review_hash`. Then set the row to Done.

### Done when
- The fix is on `main`, and `outputs/skill-reviews/<date>-model-tiering.md` says PASS.
- SKILL.md has `vault_status: "reviewer-approved"`, and its `review_hash` equals `static_scan.py --hash skills/model-tiering`. The README row agrees.
- `judging-with-jev` is still reviewer-approved, with its hash unchanged.
- The `--audit` summary line (or lint §10) shows draft-installed=0.
- The installed folder on the main computer hashes to the reviewed `review_hash`. Record the hash, not the computer's name.
- The handoff row is Done, and its Detail lists the fix commit, the review report, the audit line and the installed-hash check.

### Decisions for Jeff
None are blocking. Jeff decided on 2026-11-09 to fix rather than uninstall. The executor applies Option A unless Jeff picks Option B before work starts. At step 11 Jeff has one action to do: open a session on the main computer. If the fix fails review twice, uninstalling needs his word.

### Risks and rules
- **Public repo.** Write "the main computer". Put no hostnames, computer labels or project names in the repo, and do not copy the names at L21 and L43 into commits, reports or this card.
- **Review gate.** Never set reviewer-approved by hand, and never let the session that wrote the fix judge it.
- **Approval does not cover the installed copy yet.** Between the PASS and step 12, Skill Installs shows reviewer-approved while the main computer still runs the pre-fix files, Jev routing included. The card stays open until the hash check.
- **Protected paths.** None are edited. The review keys are left to the procedure; they are excluded from the hash.
- **Overlap.** The auto-clearing-backlog card (it auto-fixes, then deprecates, rejected drafts after 14 days) must skip `model-tiering`, or this card must land first. Otherwise the skill could be edited twice, or deprecated while it is installed.
- **Cost.** Each review attempt is one Opus reviewer run. Jina is free. Exa is metered, so use it only as the fallback.

### Decisions for Jeff (from the reviewer pass)
- S2 fix: Option A (Part C becomes a one-line pointer to judging-with-jev that discloses it is a third-party API; this is the default) or Option B (name Jev in the description, 9 characters left). The executor applies A unless Jeff says otherwise before work starts.
- After the PASS: Jeff opens a Claude Code session on the main computer so it can run the global reinstall of model-tiering and the installed-hash check. Only a session on that computer can replace the pre-fix copy.
- If the fixed skill fails review twice: keep fixing, or uninstall it from the main computer (uninstalling needs Jeff's word).
