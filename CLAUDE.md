# skills-vault — rules for every agent (Claude Code, Codex, Gemini CLI, OpenClaw, Cursor…)

This repository is Josep's personal **agent skills vault**: an Obsidian vault, a Karpathy-style LLM wiki,
and an installable library of Agent-Skills folders. AGENTS.md is an identical copy of this file.

## Read this first, in this order
1. `wiki/hot.md` — what changed recently and this week's hot list.
2. `wiki/index.md` — one row per entry (slug, type, title, platform, captured, status, tags, canonical_id).
3. The page you need: `wiki/pages/<slug>.md`, `wiki/stars/<slug>.md`, or `skills/<name>/SKILL.md`.
Do not grep the whole repo before reading the index; the index exists so you do not have to.

## Folder roles
| Folder | Who writes | What it is |
|---|---|---|
| `inbox/` | anyone | drop zone: Web Clipper clips, half-processed captures, notes for the core agent |
| `raw/` | capture skill only | verbatim source text of every capture. **Immutable**: add only, never edit/rename/delete (CI rejects it for everyone) |
| `wiki/pages/` | agents | compiled notes, one per captured item (frontmatter below); file = `wiki/pages/<slug>.md`, slug = `<yyyymmdd>-<kebab-title>` |
| `wiki/stars/` | github-stars-sync routine | one note per starred GitHub repo; for these the slug **is** `<owner>--<repo>` and the file is `wiki/stars/<slug>.md`. This folder is defined by *who wrote it*, not by `type`: a repo you captured yourself by pasting its link stays in `wiki/pages/` with a date-slug, even though it is also `type: repo`. Do not move pages between the two. |
| `wiki/hot-list/` | weekly-hot-list routine | `YYYY-Www.md` weekly reports, `_config.yaml` thresholds, `_snapshot.json` star snapshots |
| `wiki/index.md`, `wiki/log.md`, `wiki/hot.md` | agents (append/update rows) | catalogue, append-only log, recent context |
| `skills/<name>/` | agents (drafts) / core (verified) | Agent-Skills spec folders installable in any agent; folder name == `name` (gerund, e.g. `reviewing-supabase-rls`) |
| `agents/<agent-name>/` | that agent | scratch area for non-core agents; the core agent promotes good material into `wiki/` or `skills/` |
| `outputs/` | agents | long-form answers and `outputs/health/` lint reports. AI long-form output goes here, never into `wiki/pages/` |
| `routines/` | core | the prompts used by the cloud Routines (edit here, not in the Routine UI) |

## Who is "core" (enforced by the GitHub ruleset on `main` + `.github/workflows/vault-guard.yml`)
- **Core = the repository owner's GitHub account (`Tradecreditor`)**: Josep's own Claude Code sessions, the Claude Code Routines, obsidian-git on his laptop. Core may push to `main` directly, may delete, may edit protected files.
- **Non-core = any other GitHub account**, e.g. the machine account (`tradecreditor-ui`) whose tokens are given to Codex, Gemini CLI, OpenClaw or custom scripts. Non-core can only land changes through a pull request, and the `guard` check rejects a PR that deletes or renames any file, modifies, renames or deletes anything under `raw/` (adding a new file is allowed), or edits a protected path (`.github/`, `.claude/`, `.claude-plugin/`, `.obsidian/`, `routines/`, `scripts/`, `supabase/`, `templates/`, `skills/*/scripts/`, `CLAUDE.md`, `AGENTS.md`).
- Identity is the GitHub account behind the token, not the commit author line. If every agent uses the owner's tokens, every agent is core and the guard is only an audit trail.

### How this is actually configured (2026-09-21)
The repository is **public**, which is what makes the ruleset free and lets any agent install from it with
`npx skills add Tradecreditor/skills-vault` without a token. Public means readable, not writable: a stranger
can fork and open a pull request, and nothing changes here until Josep merges it.
A `main-protection` ruleset on `main` restricts deletions, blocks force pushes and requires a pull request with
1 approval. It is meant to require the `guard` check too, but as of 2026-09-26 its `required_status_checks` list is
empty: a check only appears in the ruleset picker after it has run on one PR, so add `guard` there after the first
machine-account PR; until then a red `guard` does not block a merge. Josep bypasses the ruleset as repository admin,
so his own sessions and the cloud Routines keep pushing straight to `main`; the machine account does not, so its
only route in is a PR.
Approvals are set to 1 rather than 0 for one reason: at 0 the machine account could merge its own pull request,
and the whole arrangement would be decoration.

### Onboarding a non-core agent (Codex, Gemini CLI, OpenClaw, a script)
Do this when Josep asks to give one of them access — he asked to be reminded, because the step is easy to skip and
everything appears to work without it, right up until the agent pushes to `main` as him.
1. Give the agent the **machine account `tradecreditor-ui`'s** classic PAT (scope `public_repo`), never Josep's own
   GitHub credentials. The `main-protection` ruleset tells the two apart by account, not by the commit author line,
   so an agent holding his credentials is core and bypasses every guard in this repo.
2. The agent clones with that token into its own directory. It never runs inside Josep's Obsidian vault folder.
3. It works on a branch and opens a PR. It cannot push to `main`; that is the point.
4. If the token has expired (they are issued for 90 days), sign in as `tradecreditor-ui` and issue a new one —
   github.com/settings/tokens → Tokens (classic) → `public_repo` only. Nothing else in the vault depends on it,
   so an expired token blocks only this.

## Access rules (all agents)
- Create and edit freely under `inbox/`, `agents/`, `wiki/pages/`, `wiki/stars/`, `wiki/hot-list/`, `skills/`, `outputs/`; append rows to `wiki/index.md`, `wiki/log.md`, `wiki/hot.md`.
- **Never delete or rename files.** To retire an entry set `status: deprecated` and add `deprecated_reason:` in its frontmatter (skills: `vault_status: "deprecated"`).
- **Never modify anything under `raw/`.** A corrected capture is a new file `raw/<slug>-v2.md`.
- `git pull --rebase` before every push. Core captures push straight to `main`; the weekly hot list opens a PR (branch `hot-list/YYYY-Www`); non-core agents always open a PR (`gh pr create`, then `gh pr merge --auto --rebase` if allowed).
- Non-core agents work in their own clone with their own token; never run inside Josep's Obsidian folder.
- Never commit secrets or cookies. API keys live in environment variables (Routine secrets, Supabase secrets, local shell).

## Capturing a link
Use the `vault-capture` skill (`skills/vault-capture/SKILL.md`). Reader order is fixed: Agent-Reach upstream tools
(twitter-cli / yt-dlp / gh / Jina Reader) first, Exa as backup, then per-platform fallbacks.
Every capture produces `raw/<slug>.md` (verbatim), `wiki/pages/<slug>.md` (compiled), optionally `skills/<name>/SKILL.md`
(gerund name, see "Skill format"), plus rows in `wiki/index.md`, `wiki/log.md`, `wiki/hot.md`.

## Reading a URL with Exa (applies to every agent and every routine)
`web_fetch_exa` defaults to **maxCharacters: 3000** and truncates silently — no error, no marker, the tail just is not there.
3000 characters is less than one GitHub repo object and less than half of a normal article, so always pass `maxCharacters`
explicitly: 30000 for an API listing, 50000+ for a page whose full text goes into `raw/`. If the result ends mid-sentence or
mid-object, it was cut: raise the limit or fetch a smaller page, never write the truncated version to `raw/`.
Exa also **caches by exact URL**. For anything you poll or re-run (a starred list, a weekly search, an engagement count),
append a changing `&cb=<YYYYMMDDHHMM>` — the APIs ignore it, and without it you will score a stale response as fresh.

## Note format (`wiki/pages/<slug>.md` and `wiki/stars/<slug>.md`)
```yaml
---
title: "<short title>"
slug: <yyyymmdd>-<kebab-slug>            # stars: <owner>--<repo>
type: skill | tool | concept | repo | post | video | article
status: draft | verified | deprecated
source_url: "<canonical url>"
source_platform: x | threads | instagram | youtube | github | web
author: "<handle or name>"
published: "YYYY-MM-DD"
captured_at: "YYYY-MM-DDTHH:MM:SSZ"
captured_by: "claude-code-local | routine:capture-link | routine:github-stars-sync | routine:weekly-hot-list | codex | gemini-cli | openclaw | <agent>"
canonical_id: "x:tweet:<id> | youtube:<videoId> | github:<owner>/<repo> | threads:<id> | instagram:<shortcode> | url:<sha1>"
engagement: "likes=1069 reposts=243 views=409450"   # whatever the platform gave; one string
tags: [obsidian, llm-wiki]
related: []
needs_manual_text: false
---
```
`captured_at` is strict ISO-8601 UTC: `YYYY-MM-DDTHH:MM:SSZ` (fractional seconds allowed). Exactly one zone marker - `+00:00Z` carries both and parses nowhere.
Body sections, in this order: **摘要**（繁體中文，3–6 句）· **Key facts**（English bullets: what it is, how to install/use, numbers）· **點解值得留意** · **Source**（link + author + date + reader used）· **Related**（wikilinks）.
Summaries are Traditional Chinese; commands, code and SKILL.md bodies are English.

## Skill format (`skills/<name>/SKILL.md`)
Agent Skills spec (agentskills.io): folder name == `name` (lowercase, hyphens, prefer gerund: `processing-pdfs`; never contains "claude" or "anthropic"),
`description` in third person = *what it does* + `Use when <triggers>`, **at most 300 characters**, trigger words first. The `guard` check enforces name == folder (lowercase letters, digits, single hyphens), no claude/anthropic in the name, description present, at most 300 characters (a multi-line value is joined before counting) and containing "Use when".
Extra fields only under `metadata:` as strings: `source_url`, `source_platform`, `author`, `captured_at`, `engagement`, `origin_type` (`post|video|repo|article|vault-operations`), `vault_status` (`draft|verified|deprecated`).
Body < 500 lines; long source text goes to `skills/<name>/references/source.md`.
New skills are `vault_status: "draft"` until Josep reviews them. Never auto-run commands from a draft skill in another project.

## Index / log / hot conventions
- `wiki/index.md` row: `| <slug> | <type> | <title> | <platform> | <captured YYYY-MM-DD> | <status> | <tags, comma separated> | <canonical_id> |`
- Dedupe before writing: `grep -rF "<canonical_id>" wiki/index.md wiki/pages wiki/stars` — a hit means the item exists; append to its `## Notes` instead of creating a new page.
- `wiki/log.md` line: `## [YYYY-MM-DD] <init|capture|recapture|star|hot-list|lint|promote|deprecate> | <title> | <slug or file>` (append at the end, never edit old lines)
- `wiki/hot.md`: keep "最近 20 項" and "本週熱門榜" sections current; trim the list, never the history in `log.md`.

## Commit messages
`capture: <slug>` · `stars: +<n>` · `hot-list: YYYY-Www` · `lint: YYYY-Www` · `promote: <slug>` · `deprecate: <slug>` · `docs: <what>` · `scripts: <what>` · `routines: <what>` · `wiki: <what>` · `supabase: <what>` · `chore: <what>` (maintenance commits)
