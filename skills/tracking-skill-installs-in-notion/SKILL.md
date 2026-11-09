---
name: tracking-skill-installs-in-notion
description: "Records which agent skills and Claude Code plugins are installed in which project or computer in Jeff's Notion database Skill Installs, via scripts/skills-inventory.py. Use when a skill was installed or removed, a project or computer joins the inventory, or auditing installs against vault status."
metadata:
  origin_type: "vault-operations"
  captured_at: "2026-11-09"
  vault_status: "draft"
---

# tracking-skill-installs-in-notion — one Notion database for every installed skill

## Overview

Jeff installs skills from this vault (and from other repositories) into many projects, with `npx skills add …` and with the
Claude Code plugin `skills-vault@tradecreditor-vault`, on more than one computer. Nothing records where each skill is installed:
the only traces are each project's `skills-lock.json` (written by the `skills` CLI), the agent skill folders
(`.claude/skills/`, `.agents/skills/`, …) and Claude Code's plugin records. This skill mirrors those traces into one private
Notion database, **Skill Installs** on the page **Skills HQ**, one row per skill × project × scope, so Jeff can see at a glance
what is installed where, which rows are vault skills, and whether an installed vault skill is still only a `draft`.

It is deliberately separate from Projects HQ (`tracking-projects-in-notion`): that board tracks workstreams, this database
tracks installations. They share the Notion integration and `NOTION_TOKEN`, nothing else.

Two access paths, as for Projects HQ:

| Path | Who | What it can do |
|---|---|---|
| Notion connector (MCP) | an interactive Claude Code session that has the connector | create the page, database and views once; read rows |
| Notion REST API with `NOTION_TOKEN` | `scripts/skills-inventory.py`, run by any session, any agent, or a cloud Routine | write rows (one run per project or computer), the vault's daily enrichment, the weekly audit |

## The database

Page **Skills HQ** (private, top level) holds the database **Skill Installs**. Views: **By project** (table grouped by Project,
Installed only), **By skill** (table sorted by Skill then Project), **Vault drafts installed** (Vault skill ✓ and Vault status
not reviewer-approved / verified), **Removed**.

| Property | Type | Written by |
|---|---|---|
| Skill | title | script: the skill name, or the plugin id `name@marketplace` for plugin rows |
| Project | select | script: `--project`, default the repo name; a `--global` run uses `global:<computer>` |
| Scope | select: project, global | script |
| Kind | select: skills-cli, claude-plugin, folder | script: a `skills-lock.json` entry, a Claude Code plugin, or a skill folder with no lock entry |
| Source repo | text | script: the lockfile `source` (`Tradecreditor/skills-vault`, `.`, a URL); a plugin's marketplace repo when known |
| Agents | multi-select: claude-code, codex, gemini-cli, cursor, openclaw, other | script: which `<agent>/skills/<name>` folders or links exist |
| Hash | text | script: the lockfile `computedHash`, or the plugin version |
| Status | select: Installed, Removed | script; a row this run's Source no longer sees becomes Removed (never deleted); seen again → Installed |
| Installed | date | script, on create only (first seen) |
| Last seen | date | script; only moves forward |
| Vault skill | checkbox | script: a skill folder whose source is `Tradecreditor/skills-vault` (or `.` inside the vault checkout). Never set on a plugin row: a plugin is a bundle, its provenance is the Source repo |
| Vault status | select: draft, reviewer-approved, verified, deprecated, unknown | **the vault's `--enrich` run only**, from `skills/README.md` |
| Link | url | script: `https://github.com/<owner>/<repo>/tree/main/skills/<name>` for a GitHub source |
| Source | select | script: the ownership key, `<repo>/skills-lock.json` or the global label; a run touches only its own Source |

Create it with the connector (DDL):

```
CREATE TABLE ("Skill" TITLE, "Project" SELECT('skills-vault':purple), "Scope" SELECT('project':blue, 'global':orange),
  "Kind" SELECT('skills-cli':green, 'claude-plugin':purple, 'folder':gray), "Source repo" RICH_TEXT,
  "Agents" MULTI_SELECT('claude-code':orange, 'codex':green, 'gemini-cli':blue, 'cursor':purple, 'openclaw':yellow, 'other':gray),
  "Hash" RICH_TEXT, "Status" SELECT('Installed':green, 'Removed':gray), "Installed" DATE, "Last seen" DATE,
  "Vault skill" CHECKBOX, "Vault status" SELECT('draft':gray, 'reviewer-approved':blue, 'verified':green, 'deprecated':red, 'unknown':yellow),
  "Link" URL, "Source" SELECT('skills-vault/skills-lock.json':purple))
```

Unlike the Projects HQ board, **Project, Source and Agents options are created on demand**: Notion adds a select option when a
row with a new value is written, so a new project needs no connector session first. Scope, Kind, Status and Vault status are a
fixed vocabulary; a value missing there stops the run with exit 2 before any write.

## What the script reads

Nothing on disk is ever written. Project scope (the default; `--root` picks the checkout, default is the script's repo root):

1. `skills-lock.json` → one row per `skills[<name>]` entry (`source`, `sourceType`, `computedHash`; extra keys are ignored).
2. The agent skill folders `.claude/skills/*`, `.agents/skills/*` (shared by Codex, Cursor, Gemini CLI, Copilot and others) and
   `skills/*` (OpenClaw; skipped inside the vault, whose `skills/` is the library) → the Agents column. A folder (or symlink)
   with a `SKILL.md` and no lock entry is a row of Kind `folder`.
3. Claude Code plugins enabled in `.claude/settings.json` and `.claude/settings.local.json` (`enabledPlugins` set to `true`;
   the local file wins) → Kind `claude-plugin`, Agents `claude-code`.

`--global` reads the computer instead (`--home` overrides the home directory): `~/.claude/skills`, `~/.agents/skills`,
`~/.gemini/skills`, `~/.cursor/skills`, `~/.openclaw/skills`, `~/.agents/skills-lock.json` when present,
`~/.claude/plugins/installed_plugins.json` (plugin version) and `~/.claude/settings.json`. Project defaults to
`global:<hostname>`; pass `--project "global:<a name you like>"` to choose the label. Hostnames go to Notion only.

Plan: fetch this Source's rows; create the missing ones (Installed = today); update changed fields (Kind, Agents, Hash, Source
repo, Link, Vault skill, Last seen); set Status `Removed` on rows no longer seen. `Installed` and `Vault status` are never
overwritten by a project run. One row per Skill title and Source: a second local copy of the same name only warns.

## Running it

```
python3 scripts/skills-inventory.py --dry-run        # collect and plan; with a token also read Notion; never writes
python3 scripts/skills-inventory.py                  # this project
python3 scripts/skills-inventory.py --global         # this computer's global installs (run once per computer)
python3 scripts/skills-inventory.py --json           # one JSON object instead of the summary line
python3 scripts/skills-inventory.py --enrich         # vault checkout only: fill Vault status from skills/README.md
python3 scripts/skills-inventory.py --audit          # read-only check of every row
```

| Flag | Default | Meaning |
|---|---|---|
| `--project LABEL` | `<repo>` (from `remote.origin.url`, else the folder name); `--global`: `global:<hostname>` | Project value |
| `--source LABEL` | `<project>/skills-lock.json`; `--global`: the Project label | Source value: the only rows this run may touch, the only rows an audit names |
| `--root DIR` | the script's repo root | project checkout to scan |
| `--global` / `--home DIR` | off / the user's home | scan the computer instead of a project |
| `--enrich` / `--vault DIR` | off / the script's repo root | the vault-only enrichment (needs `skills/README.md`) |
| `--data-source ID` | `NOTION_SKILLS_DS`, else search for the title `Skill Installs` | data source id (a database id with one data source is accepted and noted) |
| `--audit` | off | the audit instead of the sync; cannot be combined with `--dry-run` or `--enrich` (exit 4) |
| `--today YYYY-MM-DD` | current UTC date | tests; the audit's "today" |

stdout is one line (details on stderr):

- sync: `skills-inventory: created=<n> updated=<n> removed=<n> unchanged=<n> failed=<n> source=<label> data_source=<id8>`;
  dry run: `skills-inventory: dry-run rows=<n> created=…`, or `skills-inventory: dry-run rows=<n> project=<p> source=<s>` with no token;
- enrich: `skills-inventory: enriched=<n> unchanged=<n> failed=<n> vault_skills=<n> data_source=<id8>`;
- audit: `skills-audit: rows=<n> installed=<n> projects=<n> violations=<n> draft-installed=<n> stale=<n> unknown-vault=<n> removed=<n>`,
  then one `- [<rule>] <skill> @ <project> — <detail>` line per violation on this run's Source, and one closing count for rows of
  other projects (this repository is public, so other projects' rows are never named here);
- exit 2: `skills-inventory: off (<reason>)`; exits 3 and 4: `skills-inventory: error (<reason>)` on stderr.

| Exit | Meaning | What a Routine does |
|---|---|---|
| 0 | synced (also: dry run ok, enrich ok, audit ran with or without violations) | copy the line into the final message or report |
| 1 | some writes failed after retries, the rest are done | copy the line; do not retry more than once |
| 2 | off for this run: `NOTION_TOKEN` missing or malformed, 401/403, data source not found or page not shared with the integration, ambiguous search (set `NOTION_SKILLS_DS`), a schema property missing or of the wrong type, a fixed-vocabulary option missing, `api.notion.com` unreachable, any failed read | copy the `off (<reason>)` line; Jeff fixes the setup |
| 3 | local input unusable: `skills-lock.json` is not valid JSON, or `--root` / `--home` / `--vault` is not a directory | copy the line; fix the file |
| 4 | refused locally: bad flag, bad `--today`, bad `NOTION_VERSION`, `NOTION_API_BASE` not local, `--audit` with `--dry-run` or `--enrich` | copy the message; never expected in a Routine |

Audit rules: `draft-installed` (a vault skill whose Vault status is not reviewer-approved or verified is Installed somewhere:
only approved skills may be installed in other projects), `stale` (Installed but Last seen more than 30 days ago: that project
has not run the inventory lately), `unknown-vault` (Vault skill ✓ but no Vault status: the vault's `--enrich` has not run),
`removed` (a count of Removed rows; not a violation).

Behaviour: `Notion-Version` 2026-03-11 (`NOTION_VERSION` overrides); about 3 requests per second; 429 / 529 retried after
`Retry-After` (capped at 30 s), 409 / 5xx and timeouts retried after 1, 2, 4 s; a create is never blindly retried (the data
source is queried first, so a row that did land is not created twice); redirects never followed; the token goes only to
`api.notion.com` (`NOTION_API_BASE` accepts only a local test server); nothing is ever deleted or archived; the token is scrubbed
from every message and no traceback is ever printed. Python 3.9+, standard library only.

## Set up once

1. **Page and database** (done 2026-11-09 from a Claude Code session with the connector): private page **Skills HQ**, database
   **Skill Installs** with the DDL above, the four views. Without the connector, wait for a session that has it.
2. **Share the page with the integration**: the same internal integration Projects HQ uses (`routines/README.md` Step 0).
   On Skills HQ: ••• → Connections → add it. Until then every run prints `off (data source 'Skill Installs' not found …)`.
3. **Token**: `NOTION_TOKEN` is already set wherever Projects HQ syncs (the cloud environment "Skills Management", Jeff's
   computers). No new secret. Optional `NOTION_SKILLS_DS` = the data source id, only if the title search is ambiguous.
4. **First run**: `python3 scripts/skills-inventory.py --dry-run`, then without `--dry-run`; a second run must print `created=0`.

## Per project: after every install

Whenever a skill or plugin is added to or removed from a project (`npx skills add …`, `npx skills remove …`,
`/plugin install …`), run the inventory in that project before the session ends:

- A project with the vault plugin: `/skills-vault:skillsync` (it checks this skill's review, copies the script if the project
  lacks it, runs it and reports the line).
- Any project: copy `scripts/skills-inventory.py` from a **reviewed** clone of the vault (the same step-0 check as
  `tracking-projects-in-notion/references/joining-projects-hq.md`: `vault_status` reviewer-approved or verified and
  `static_scan.py --hash` equal to `review_hash`), commit it, then `python3 scripts/skills-inventory.py`. Record in the
  project's `handoff.md` "Environment facts": `skills-inventory.py copied from skills-vault <commit> (reviewed)`.
- Once per computer: `python3 scripts/skills-inventory.py --global --project "global:<name>"` from any checkout that has the
  script; repeat after a global install (`-g`).

`scripts/skills-inventory.py` in this skill is a byte-identical copy of the vault's `scripts/skills-inventory.py`, so the copy
other projects download is covered by this skill's review. Edit both together; `scripts/test_skills_inventory.py` fails when
they differ.

## Schedule (vault)

- `github-stars-sync` step 7b runs `python3 scripts/skills-inventory.py` (the vault's own installs) and then
  `python3 scripts/skills-inventory.py --enrich` daily; the Routine's final message carries both lines.
- `vault-lint` check 10 runs `python3 scripts/skills-inventory.py --audit --today <today>` every Monday and copies the output
  into the health report.

## Common mistakes

| Mistake | Fix |
|---|---|
| Editing a row in Notion | The next run of that project overwrites it. Change the install on disk, then rerun |
| Installing a `draft` vault skill in a project | The audit flags `draft-installed`; only reviewer-approved or verified skills belong in other projects (`skills/README.md`) |
| A project never runs the inventory again | Its rows go `stale` after 30 days: run the script there (or `/skills-vault:skillsync`) |
| Running `--enrich` outside the vault | It needs `skills/README.md`; exit 3. Only the vault runs it |
| Two repositories with the same name under different owners (`alice/app`, `bob/app`) | They would share the Source `app/skills-lock.json` and overwrite each other. Pass distinct `--project` labels (e.g. `alice-app`); the Source follows the Project label |
| Two computers with the same hostname | Their `--global` runs share one Source and overwrite each other's rows: pass distinct `--project "global:<name>"` labels |
| Pasting the database id as `NOTION_SKILLS_DS` | It must be the data source id; a database id with exactly one data source is accepted with a note |
| Forgetting to connect the integration to Skills HQ | Exit 2 "not found": Skills HQ → ••• → Connections → add it |
| Running the Notion connector from a Routine | Unavailable there (2026-10-06); the script with `NOTION_TOKEN` is the only path |

## Evidence

- 2026-11-09 — built in a Claude Code cloud session: page, database and views created through the connector;
  `scripts/skills-inventory.py` with 21 unit tests against a local fake Notion server
  (`python3 -m unittest discover -s scripts -p 'test_*.py'`): lockfile / folder / plugin collection, global scan, plan
  (create, update, Removed, return to Installed, Last seen forward only), other Sources untouched, enrich across Sources, audit
  naming only this Source's rows, 401 scrubbing, schema and option checks, exit codes. Dry run on the vault itself: 1 row
  (`scanning-agent-skills`, a local `draft` copy under `.claude/skills/`). Live run pending Jeff connecting the integration
  to Skills HQ.

## Source

- Jeff's request, 2026-11-09: keep track of which skills are installed across projects in Notion; decisions: a separate page and
  database (not under Projects HQ), each project runs its own script, all sources tracked with vault skills flagged.
- Files: `scripts/skills-inventory.py` (copy in this skill's `scripts/`), `scripts/test_skills_inventory.py`,
  `commands/skillsync.md`, `routines/github-stars-sync.md` step 7b, `routines/vault-lint.md` check 10, `CLAUDE.md` "Skill installs".
- Lockfile and install paths: the `skills` CLI docs (github.com/vercel-labs/skills, `docs/agents.md`); Claude Code plugin
  records: code.claude.com/docs/en/plugins/loading.
