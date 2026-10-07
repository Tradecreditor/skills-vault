# skills-vault — rules for every agent (Claude Code, Codex, Gemini CLI, OpenClaw, Cursor…)

This repository is Jeff's personal **agent skills vault**: an Obsidian vault, a Karpathy-style LLM wiki,
and an installable library of Agent-Skills folders. AGENTS.md is an identical copy of this file.

## Read this first, in this order
1. `handoff.md` — where the project stands, what is in flight, what to do next (one per project; SOP in `skills/keeping-handoff-docs/SKILL.md`).
   Its "In flight" rows are this repo's cards on Jeff's cross-project kanban (Projects HQ, see that section below).
2. `wiki/hot.md` — what changed recently and this week's hot list.
3. `wiki/index.md` — one row per entry (slug, type, title, platform, captured, status, tags, canonical_id).
4. The page you need: `wiki/pages/<slug>.md`, `wiki/stars/<slug>.md`, or `skills/<name>/SKILL.md`.
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
| `wiki/reads.base` | core (rarely) | Obsidian Bases view of every `post` / `video` / `article` page, grouped by `topic/*` tag. A live query over `wiki/pages`: nothing to append, a page appears by having the right `type` and a topic tag |
| `skills/<name>/` | agents (drafts) / skill-review routine (reviewer-approved) / core (verified) | Agent-Skills spec folders installable in any agent; folder name == `name` (gerund, e.g. `reviewing-supabase-rls`) |
| `agents/<agent-name>/` | that agent | scratch area for non-core agents; the core agent promotes good material into `wiki/` or `skills/` |
| `outputs/` | agents | long-form answers and `outputs/health/` lint reports. AI long-form output goes here, never into `wiki/pages/` |
| `routines/` | core | the prompts used by the cloud Routines (edit here, not in the Routine UI) |

## Who is "core" (enforced by the GitHub ruleset on `main` + `.github/workflows/vault-guard.yml`)
- **Core = the repository owner's GitHub account (`Tradecreditor`)**: Jeff's own Claude Code sessions, the Claude Code Routines, obsidian-git on his laptop. Core may push to `main` directly, may delete, may edit protected files.
- **Non-core = any other GitHub account**, e.g. the machine account (`tradecreditor-ui`) whose tokens are given to Codex, Gemini CLI, OpenClaw or custom scripts. Non-core can only land changes through a pull request, and the `guard` check rejects a PR that deletes or renames any file, modifies, renames or deletes anything under `raw/` (adding a new file is allowed), or edits a protected path (`.github/`, `.claude/`, `.claude-plugin/`, `.obsidian/`, `routines/`, `scripts/`, `supabase/`, `templates/`, `skills/*/scripts/`, `CLAUDE.md`, `AGENTS.md`).
- Identity is the GitHub account behind the token, not the commit author line. If every agent uses the owner's tokens, every agent is core and the guard is only an audit trail.

### How this is actually configured (2026-09-21)
The repository is **public**, which is what makes the ruleset free and lets any agent install from it with
`npx skills add Tradecreditor/skills-vault` without a token. Public means readable, not writable: a stranger
can fork and open a pull request, and nothing changes here until Jeff merges it.
A `main-protection` ruleset on `main` restricts deletions, blocks force pushes and requires a pull request with
1 approval. It is meant to require the `guard` check too, but as of 2026-09-26 its `required_status_checks` list is
empty: a check only appears in the ruleset picker after it has run on one PR, so add `guard` there after the first
machine-account PR; until then a red `guard` does not block a merge. Jeff bypasses the ruleset as repository admin,
so his own sessions and the cloud Routines keep pushing straight to `main`; the machine account does not, so its
only route in is a PR.
Approvals are set to 1 rather than 0 for one reason: at 0 the machine account could merge its own pull request,
and the whole arrangement would be decoration.

### Onboarding a non-core agent (Codex, Gemini CLI, OpenClaw, a script)
Do this when Jeff asks to give one of them access — he asked to be reminded, because the step is easy to skip and
everything appears to work without it, right up until the agent pushes to `main` as him.
1. Give the agent the **machine account `tradecreditor-ui`'s** classic PAT (scope `public_repo`), never Jeff's own
   GitHub credentials. The `main-protection` ruleset tells the two apart by account, not by the commit author line,
   so an agent holding his credentials is core and bypasses every guard in this repo.
2. The agent clones with that token into its own directory. It never runs inside Jeff's Obsidian vault folder.
3. It works on a branch and opens a PR. It cannot push to `main`; that is the point.
4. If the token has expired (they are issued for 90 days), sign in as `tradecreditor-ui` and issue a new one —
   github.com/settings/tokens → Tokens (classic) → `public_repo` only. Nothing else in the vault depends on it,
   so an expired token blocks only this.

## Access rules (all agents)
- Create and edit freely under `inbox/`, `agents/`, `wiki/pages/`, `wiki/stars/`, `wiki/hot-list/`, `skills/`, `outputs/`; append rows to `wiki/index.md`, `wiki/log.md`, `wiki/hot.md`.
- **Never delete or rename files.** To retire an entry set `status: deprecated` and add `deprecated_reason:` in its frontmatter (skills: `vault_status: "deprecated"`).
- **Never modify anything under `raw/`.** A corrected capture is a new file `raw/<slug>-v2.md`.
- `git pull --rebase` before every push. Core captures push straight to `main`; the weekly hot list opens a PR (branch `hot-list/YYYY-Www`); non-core agents always open a PR (`gh pr create`, then `gh pr merge --auto --rebase` if allowed).
- Non-core agents work in their own clone with their own token; never run inside Jeff's Obsidian folder.
- Never commit secrets or cookies. API keys live in environment variables (Routine secrets, Supabase secrets, local shell).
- **Keep `handoff.md` current.** Any session or agent that changes code, prompts, config, skills, data or the plan updates it before ending and appends one line to its Session log, in the same commit or PR. Routines read it and never edit it; their output goes to `wiki/log.md`, `wiki/hot.md` and `outputs/health/`. Enforced by `scripts/handoff-check.sh`: a Claude Code Stop hook (`.claude/settings.json`) will not let a session end while its branch changed state without touching `handoff.md`, and the PR check `handoff` turns red for any agent that skips it. Captures and Routine output (`raw/`, `wiki/pages/`, `wiki/stars/`, index / log / hot, hot-list reports, `outputs/health/`) are exempt.

## Projects HQ — the kanban for every project (all agents, every session)
Jeff runs ALL his projects (this vault, his other repos, non-repo work) on one board: private Notion page **Projects HQ**,
database **Project Status**, Board view by Status, plus one Board view per project (a tab filtered by its Area; never a
separate database or board per project). The working agreement is `skills/tracking-projects-in-notion/references/board-policy.md`
(card definition, fields, column entry rules, Definition of Done, P0–P3, WIP limits, cadence); the mechanics are in
`skills/tracking-projects-in-notion/SKILL.md`. Rules every session follows:
- **Columns**: Backlog → In progress → Waiting on Jeff → Blocked → Done, plus Dropped. One card = one workstream with an
  observable outcome (2–6 weeks), title stable for life. Priority P0 (urgent, this week, Target date required) · P1 (current focus)
  · P2 (default) · P3 (someday). WIP limit In progress: Jeff 3, Claude Code 5.
- **Start**: after `handoff.md`, read this project's cards (Area) when you have the Notion connector. Work only on something that
  has a card; open one first. Say so if you must exceed the WIP limit.
- **Open**: repo work → add a row to `handoff.md` "In flight" (`| Workstream | Status | Priority | Owner | State | Next step | Detail |`)
  in the same commit as the first piece of work; non-repo work → a `manual` card in Notion with every required field.
- **Move**: change the row's Status / Owner / Next step in the same commit as the work that caused it. Waiting on Jeff → Next step
  starts `Jeff:` and names the decision; Blocked → names the blocker and what unblocks it. Every move updates Next step and Last update.
- **Close**: Status `Done` only when the Definition of Done holds (merged to `main` and live / shipped / decided, checked, Detail =
  the evidence: PR, commit, report); `Dropped` with `Dropped: <reason>` when abandoned. Move the row to "Recently done" in a later
  update. Never delete a card; follow-up work is a new card.
- **End**: update the rows you touched; your final message names the cards you opened, moved or closed.
- Never edit a card whose Source is a `handoff.md` in Notion (the sync overwrites it); edit the handoff. Never copy a `manual`
  card's title or details into this public repo. Only Jeff changes columns, priorities, Owners, Areas or the policy.
- Machinery: `scripts/notion-sync.py` mirrors In flight to the board (daily, `github-stars-sync` step 7; any session may run it on
  `main` when `NOTION_TOKEN` is set); `--audit` checks the policy weekly (`vault-lint` check 9). Another repo joins by copying the
  script and the "Projects HQ" lines from `skills/tracking-projects-in-notion/SKILL.md` into its own CLAUDE.md / AGENTS.md.

## Capturing a link
Use the `vault-capture` skill (`skills/vault-capture/SKILL.md`). Reader order is fixed: Agent-Reach upstream tools
(twitter-cli / yt-dlp / gh / Jina Reader) first, Exa as backup, then per-platform fallbacks. Readers are no-login by design (no cookies,
no logged-in browsers); the only paid-tier key, `SUPADATA_KEY`, is used solely for Instagram and Facebook video audio.
Every capture produces `raw/<slug>.md` (verbatim), `wiki/pages/<slug>.md` (compiled), optionally `skills/<name>/SKILL.md`
(gerund name, see "Skill format"), plus rows in `wiki/index.md`, `wiki/log.md`, `wiki/hot.md`.

## Reading a URL with Exa (applies to every agent and every routine)
`web_fetch_exa` defaults to **maxCharacters: 3000** and truncates silently — no error, no marker, the tail just is not there.
3000 characters is less than one GitHub repo object and less than half of a normal article, so always pass `maxCharacters`
explicitly: 30000 for an API listing, 50000+ for a page whose full text goes into `raw/`. If the result ends mid-sentence or
mid-object, it was cut: raise the limit or fetch a smaller page, never write the truncated version to `raw/`.
Exa also **caches by exact URL**. For anything you poll or re-run (a starred list, a weekly search, an engagement count),
append a changing `&cb=<YYYYMMDDHHMM>` — the APIs ignore it, and without it you will score a stale response as fresh.
A 402 from Exa means the credits are exhausted: skip the Exa tier for the rest of the run instead of retrying.

## Note format (`wiki/pages/<slug>.md` and `wiki/stars/<slug>.md`)
```yaml
---
title: "<short title>"
slug: <yyyymmdd>-<kebab-slug>            # stars: <owner>--<repo>
type: skill | tool | concept | repo | post | video | article
status: draft | verified | deprecated
source_url: "<canonical url>"
source_platform: x | threads | instagram | facebook | youtube | github | web
author: "<handle or name>"
published: "YYYY-MM-DD"
captured_at: "YYYY-MM-DDTHH:MM:SSZ"
captured_by: "claude-code-local | claude-code-cloud | routine:capture-link | routine:github-stars-sync | routine:weekly-hot-list | codex | gemini-cli | openclaw | <agent>"
canonical_id: "x:tweet:<id> | youtube:<videoId> | github:<owner>/<repo> | threads:<id> | instagram:<shortcode> | facebook:<id> | url:<sha1>"
engagement: "likes=1069 reposts=243 views=409450"   # whatever the platform gave; one string
tags: [topic/knowledge-mgmt, obsidian, llm-wiki]   # post/video/article: first tag is one topic/* from the list below
related: []
needs_manual_text: false
---
```
`captured_at` is strict ISO-8601 UTC: `YYYY-MM-DDTHH:MM:SSZ` (fractional seconds allowed). Exactly one zone marker - `+00:00Z` carries both and parses nowhere.
Body sections, in this order: **摘要**（繁體中文，3–6 句）· **Key facts**（English bullets: what it is, how to install/use, numbers）· **點解值得留意** · **Source**（link + author + date + reader used）· **Related**（wikilinks）.
Summaries are Traditional Chinese; commands, code and SKILL.md bodies are English.

Topic vocabulary (fixed; `tags[0]` of every `post` / `video` / `article`, prefix `topic/` so Obsidian nests them and `wiki/reads.base` can group on them):
`topic/model-comparison` · `topic/agent-platforms` · `topic/agent-tooling` · `topic/repo-picks` · `topic/seo-geo` · `topic/marketing-content` · `topic/video-gen` · `topic/infra-devops` · `topic/knowledge-mgmt` · `topic/sales-ops` · `topic/ai-news`.
Free-form tags follow the topic. Adding a topic is a `docs:` edit to this list (and AGENTS.md), never an ad-hoc tag.

## Skill format (`skills/<name>/SKILL.md`)
Agent Skills spec (agentskills.io): folder name == `name` (lowercase, hyphens, prefer gerund: `processing-pdfs`; never contains "claude" or "anthropic"),
`description` in third person = *what it does* + `Use when <triggers>`, **at most 300 characters**, trigger words first. The `guard` check enforces name == folder (lowercase letters, digits, single hyphens), no claude/anthropic in the name, description present, at most 300 characters (a multi-line value is joined before counting) and containing "Use when".
Extra fields only under `metadata:` as strings: `source_url`, `source_platform`, `author`, `captured_at`, `engagement`, `origin_type` (`post|video|repo|article|vault-operations`), `vault_status` (`draft|reviewer-approved|verified|deprecated`),
and the review record the `skill-review` routine writes: `reviewed_at`, `reviewed_by`, `review_hash`, `review_report`.
Body < 500 lines; long source text goes to `skills/<name>/references/source.md`.
New skills are `vault_status: "draft"`. The daily `skill-review` routine (`routines/skill-review.md`) audits every draft with an
independent reviewer subagent (`.claude/agents/vault-skill-reviewer.md`) following `skills/auditing-agent-skills`; a PASS sets
`"reviewer-approved"` plus the review record, a FAIL leaves it `draft` with a report in `outputs/skill-reviews/`. Jeff delegated
this decision on 2026-10-04 and no longer reviews skills himself. Only that review procedure sets `reviewer-approved` (the routine, or a core session running `routines/skill-review.md` step by step); only Jeff sets `verified`.
`reviewer-approved` and `verified` skills may be installed and used in other projects; never auto-run commands from a draft skill there.
An approval covers the files as reviewed: `static_scan.py --hash skills/<name>` must equal `review_hash`, so any later edit to an
approved skill sends it back to `draft` and through review again. Captures may add `## Evidence` to draft skills only.

## Index / log / hot conventions
- `wiki/index.md` row: `| <slug> | <type> | <title> | <platform> | <captured YYYY-MM-DD> | <status> | <tags, comma separated> | <canonical_id> |`
- Dedupe before writing: `grep -rF "<canonical_id>" wiki/index.md wiki/pages wiki/stars` — a hit means the item exists; append to its `## Notes` instead of creating a new page.
- `wiki/log.md` line: `## [YYYY-MM-DD] <init|capture|recapture|star|hot-list|lint|review|promote|deprecate> | <title> | <slug or file>` (append at the end, never edit old lines)
- `wiki/hot.md`: keep "最近 20 項" and "本週熱門榜" sections current; trim the list, never the history in `log.md`.

## Commit messages
`capture: <slug>` · `stars: +<n>` · `stars: enrich <n>` · `hot-list: YYYY-Www` · `lint: YYYY-Www` · `review: <a> approved, <r> rejected` · `promote: <slug>` · `deprecate: <slug>` · `docs: <what>` · `scripts: <what>` · `routines: <what>` · `wiki: <what>` · `supabase: <what>` · `chore: <what>` (maintenance commits)
