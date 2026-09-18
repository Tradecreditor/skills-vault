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
| `wiki/stars/` | github-stars-sync routine | one note per starred GitHub repo; for these `type: repo` entries the slug **is** `<owner>--<repo>` and the file is `wiki/stars/<slug>.md` |
| `wiki/hot-list/` | weekly-hot-list routine | `YYYY-Www.md` weekly reports, `_config.yaml` thresholds, `_snapshot.json` star snapshots |
| `wiki/index.md`, `wiki/log.md`, `wiki/hot.md` | agents (append/update rows) | catalogue, append-only log, recent context |
| `skills/<name>/` | agents (drafts) / core (verified) | Agent-Skills spec folders installable in any agent; folder name == `name` (gerund, e.g. `reviewing-supabase-rls`) |
| `agents/<agent-name>/` | that agent | scratch area for non-core agents; the core agent promotes good material into `wiki/` or `skills/` |
| `outputs/` | agents | long-form answers and `outputs/health/` lint reports. AI long-form output goes here, never into `wiki/pages/` |
| `routines/` | core | the prompts used by the cloud Routines (edit here, not in the Routine UI) |

## Who is "core" (enforced by the GitHub ruleset on `main` + `.github/workflows/vault-guard.yml`)
- **Core = the repository owner's GitHub account (`Tradecreditor`)**: Josep's own Claude Code sessions, the Claude Code Routines, obsidian-git on his laptop. Core may push to `main` directly, may delete, may edit protected files.
- **Non-core = any other GitHub account**, e.g. the machine account (`tradecreditor-agents`) whose tokens are given to Codex, Gemini CLI, OpenClaw or custom scripts. Non-core can only land changes through a pull request, and the `guard` check rejects a PR that deletes or renames any file, touches `raw/`, or edits `.github/`, `scripts/vault-guard-check.sh`, `CLAUDE.md`, `AGENTS.md`.
- Identity is the GitHub account behind the token, not the commit author line. If every agent uses the owner's tokens, every agent is core and the guard is only an audit trail.

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
Body sections, in this order: **摘要**（繁體中文，3–6 句）· **Key facts**（English bullets: what it is, how to install/use, numbers）· **點解值得留意** · **Source**（link + author + date + reader used）· **Related**（wikilinks）.
Summaries are Traditional Chinese; commands, code and SKILL.md bodies are English.

## Skill format (`skills/<name>/SKILL.md`)
Agent Skills spec (agentskills.io): folder name == `name` (lowercase, hyphens, prefer gerund: `processing-pdfs`; never contains "claude" or "anthropic"),
`description` in third person = *what it does* + `Use when <triggers>`, **under 300 characters**, trigger words first.
Extra fields only under `metadata:` as strings: `source_url`, `source_platform`, `author`, `captured_at`, `engagement`, `origin_type` (`post|video|repo|article|vault-operations`), `vault_status` (`draft|verified|deprecated`).
Body < 500 lines; long source text goes to `skills/<name>/references/source.md`.
New skills are `vault_status: "draft"` until Josep reviews them. Never auto-run commands from a draft skill in another project.

## Index / log / hot conventions
- `wiki/index.md` row: `| <slug> | <type> | <title> | <platform> | <captured YYYY-MM-DD> | <status> | <tags, comma separated> | <canonical_id> |`
- Dedupe before writing: `grep -rF "<canonical_id>" wiki/index.md wiki/pages wiki/stars` — a hit means the item exists; append to its `## Notes` instead of creating a new page.
- `wiki/log.md` line: `## [YYYY-MM-DD] <init|capture|recapture|star|hot-list|lint|promote|deprecate> | <title> | <slug or file>` (append at the end, never edit old lines)
- `wiki/hot.md`: keep "最近 20 項" and "本週熱門榜" sections current; trim the list, never the history in `log.md`.

## Commit messages
`capture: <slug>` · `stars: +<n>` · `hot-list: YYYY-Www` · `lint: YYYY-Www` · `promote: <slug>` · `deprecate: <slug>`
