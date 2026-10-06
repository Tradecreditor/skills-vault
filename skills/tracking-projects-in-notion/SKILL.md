---
name: tracking-projects-in-notion
description: "Keeps a cross-project status board in Notion (Project Status database, Board by Status) and mirrors each repo's handoff.md In flight table into it via scripts/notion-sync.py. Use when setting up a Notion project board, syncing handoff.md to Notion, or adding NOTION_TOKEN to a Routine."
metadata:
  origin_type: "vault-operations"
  captured_at: "2026-10-06"
  vault_status: "draft"
---

# tracking-projects-in-notion — one Notion board for every project

## Overview

One board shows all of Josep's projects: repo work and personal (non-repo) projects side by side. `handoff.md` stays the source of truth for repo work (`skills/keeping-handoff-docs/SKILL.md`); Notion is the overview, plus the home of the projects that have no repo.

Two access paths, because they have different limits:

| Path | Who | What it can do |
|---|---|---|
| Notion connector (MCP) | an interactive Claude Code session that has the connector | create the page, database and views; seed and edit rows by hand |
| Notion REST API with an internal integration token in `NOTION_TOKEN` | `scripts/notion-sync.py`, run by a cloud Routine or any session | the recurring one-way sync of `handoff.md` In flight into the board |

Josep's cloud Routines cannot use the Notion connector (his finding, 2026-10-06: Routines run headless, and a claude.ai connector that needs an interactive sign-in is not reliably there), so the daily sync never depends on it.

## The board

Private page **Projects HQ** holds the database **Project Status**. Views: a **Board** grouped by Status (the main one), a **Table**, and an inline Board on the HQ page.

| Property | Type | Written by |
|---|---|---|
| Project | title | sync (from the Workstream cell); manual rows by hand |
| Status | select: Backlog, In progress, Waiting on Josep, Blocked, Done | sync; manual rows by hand |
| Area | select, one option per project or area (e.g. `skills-vault`) | sync (`--area`, default the repo name) |
| Next step | text | sync (from the Next step cell) |
| Owner | select: Josep, Claude Code, Routine | sync |
| Link | url | sync (from the Detail cell) |
| Last update | date | sync |
| Source | select: `<repo>/handoff.md` or `manual` | sync sets its own label; `manual` rows by hand |

Create it with the connector (DDL as used for the first build):

```
CREATE TABLE ("Project" TITLE,
  "Status" SELECT('Backlog':gray, 'In progress':blue, 'Waiting on Josep':yellow, 'Blocked':red, 'Done':green),
  "Area" SELECT('skills-vault':purple),
  "Next step" RICH_TEXT,
  "Owner" SELECT('Josep':pink, 'Claude Code':orange, 'Routine':brown),
  "Link" URL, "Last update" DATE,
  "Source" SELECT('skills-vault/handoff.md':purple, 'manual':gray))
```

Board view configuration: `GROUP BY "Status"; SORT BY "Last update" DESC`.

## Who owns a row (the Source rule)

| Source value | Written by | What the sync does with it |
|---|---|---|
| `<repo>/handoff.md` | the sync only | overwrites it every run; sets Status `Done` when the Workstream leaves In flight; never deletes or archives |
| `manual` (or any other label) | Josep, or a session through the connector | never reads it for writing, never writes it (the query filters on the sync's own Source) |

- To change a sync card, **edit the handoff**, not the card: the next run overwrites Status, Area, Next step, Owner, Link and Last update.
- The script never changes the schema. Add a new Area, Source, Status or Owner option in Notion by hand **before** the first run that uses it. A run (a dry run too) whose plan needs a missing option stops with exit 2 naming it, before any write.
- Two cards with the same Project and Source: the oldest is the live one; the others are set to Done with a note and counted as `duplicates=<n>` in the summary. They are never deleted; delete them by hand.

## How a handoff row becomes a card

The script reads the first table under `## In flight`, matches columns by header (Workstream required; State, Next step, Detail optional), and turns each row into one card. Writers steer it like this.

**Project** is the Workstream cell with links, wikilinks, `**` and backticks removed, then ONE trailing balanced ` (…)` group removed (`Skill review by agent (Josep's ask …)` becomes `Skill review by agent`; a title ending in `"` is left alone), then trailing ` —`, `-`, `:` stripped, at most 200 characters. The project title is the key: **keep the Workstream text stable**. Renaming it closes the old card and opens a new one. Two rows with the same title: the first wins, the second is skipped with a warning.

**Status**: the first rule that matches, compared case-insensitively on the cleaned text.

| # | Write this | Status |
|---|---|---|
| a | Next step empty, or `none`, `—`, `-`, `n/a`, `nothing`, or starting with `done`, `fixed`, `closed` | Done |
| b | State starting with `done`, `closed`, `finished` (and Next step not starting with `Josep`) | Done |
| c | State or Next step starting with `Blocked` | Blocked |
| d | State starting with `Not started` | Backlog |
| e | Next step starting with `Josep` (`Josep:`, `Josep merges …`) | Waiting on Josep |
| f | anything else | In progress |

Because d comes before e, a `Not started` row whose Next step starts with `Josep` is Backlog with Owner Josep.

| Card field | Comes from |
|---|---|
| Owner | Next step starts with `Josep` → Josep; starts with `Routine` or `Next scheduled run` → Routine; anything else → Claude Code |
| Next step | the Next step cell, at most 1900 characters (longer is cut with `…`); for a Done row with an empty or `none` Next step: `Done — ` plus the first sentence of State |
| Last update | the newest `YYYY-MM-DD` anywhere in the row that is not later than the handoff's `Last updated:` date; none found → that date. Later dates are plans and ignored; a date right after `version` or `v` (`Notion-Version 2026-03-11`, `v2026-10-04`) is a version string and ignored |
| Link | Detail cell: first `http(s)` URL; else first backtick span that looks like a repo path (contains `/` or ends in `.md`, `.yaml`, `.yml`, `.py`, `.json`, `.sh`) → `<repo-url>/blob/main/<path>` (`/tree/main/` for a trailing `/`); else first `PR #<n>` in the row → `<repo-url>/pull/<n>`; else `<repo-url>/blob/main/handoff.md` |

Cells are split on `|` except inside backtick spans and `\|`, so a wikilink such as `[[page|alias]]` in backticks does not break a row.

## Set up once

1. **Create the page and database.** In a session with the Notion connector: create the private page "Projects HQ", create the database with the DDL above, add the Board view (config above), a Table view and an inline Board on the page. Without the connector, build the same by hand from the property table.
2. **Create an internal integration** in Notion's developer portal (https://www.notion.so/profile/integrations; Notion also calls these "connections"). A workspace owner is needed. Capabilities: Read content, Update content, Insert content. Copy the secret.
3. **Share the page with it**: on Projects HQ, ••• → Connections → add the integration. It then sees only that page and its database.
4. **Store the secret** as a plain environment variable `NOTION_TOKEN` on the cloud environment (here "Skills Management") and add `api.notion.com` to that environment's allowed domains (`routines/README.md` Step 0 lists the domains; its keys table has the `NOTION_TOKEN` row).
5. **First run**: `python3 scripts/notion-sync.py --dry-run` (reads Notion, prints the plan, writes nothing), then `python3 scripts/notion-sync.py`. If the board was seeded from the handoff, the first real run should report `created=0`.

Optional: `NOTION_PROJECTS_DS` = the **data source id** (not the database id in the page URL). Needed only when the search for a data source titled "Project Status" is ambiguous. Find it with the connector (fetch the database; its data source is listed with a `collection://` id) or in the database's data-source settings.

## Running the sync

```
python3 scripts/notion-sync.py --dry-run     # parse; with a token also read Notion and log the plan; never writes
python3 scripts/notion-sync.py               # sync
python3 scripts/notion-sync.py --json        # one JSON object (rows, plan, counts) instead of the summary line
```

| Flag | Default | Meaning |
|---|---|---|
| `--handoff PATH` | `handoff.md` at the repo root | file to mirror |
| `--source LABEL` | `<repo>/handoff.md` | Source value; the only rows the run may touch |
| `--area LABEL` | `<repo>` | Area value for every row |
| `--data-source ID` | `NOTION_PROJECTS_DS`, else search | data source id |
| `--repo-url URL` | derived from `git config remote.origin.url` | base for Link values |
| `--today YYYY-MM-DD` | current UTC date | tests only |

`<repo>` is the last two path components of `remote.origin.url` (HTTPS, SSH and proxy URLs all work); with no git remote it falls back to the checkout's folder name.

stdout is one line: `notion-sync: created=<n> updated=<n> closed=<n> unchanged=<n> failed=<n> source=<label> data_source=<id8>` (with ` duplicates=<n>` after `failed` when there are any). A dry run prints `notion-sync: dry-run rows=<n> …` (just rows and source when no token is set); exit 2 prints `notion-sync: off (<reason>)`; exits 3 and 4 print `notion-sync: error (<reason>)` on stderr. Per-row details go to stderr.

| Exit | Meaning | What a Routine does |
|---|---|---|
| 0 | synced (also: dry run ok) | copy the line into the final message |
| 1 | some writes failed after retries, the rest are done | copy the line; do not retry more than once |
| 2 | sync is off for this run: `NOTION_TOKEN` missing or malformed, 401/403 (on a write the run stops at once), data source not found or not shared, ambiguous search, schema property missing or wrong type, a needed select option missing, `api.notion.com` unreachable (for example not in the allowed domains), any failed read | copy the `off (<reason>)` line; Josep fixes the setup |
| 3 | `handoff.md` unusable: file missing, no `## In flight`, no table, no Workstream column | copy the line; the In flight table needs fixing |
| 4 | refused locally: bad flag, bad `--today`, bad `NOTION_VERSION`, `NOTION_API_BASE` not 127.0.0.1 or localhost | copy the message; never expected in a Routine |

A Routine never fails because of this script; it reports the line and carries on. Never print, echo or export `NOTION_TOKEN`.

Run it on a checkout of `main`. On a feature branch it mirrors unmerged state, and the next daily run overwrites that.

Behaviour: `Notion-Version` 2026-03-11 (override with `NOTION_VERSION`); about 3 requests per second (at least 0.34 s between requests); 429 and 529 retried after `Retry-After` (capped at 30 s), 409, 500, 502, 503, 504 and timeouts retried after 1, 2, 4 s (3 retries); 30 s socket timeout; a create is never blindly retried (after a timeout, 409 or 5xx the data source is queried first, so a page that did land is not created twice); redirects are never followed; the token goes only to `api.notion.com` (`NOTION_API_BASE` accepts only a local test server); nothing is ever deleted or archived. Python 3.9+, standard library only.

## Schedule

- `github-stars-sync` step 7 runs it daily, after the stars commit and also when there were no new stars; the Routine's final message carries the `notion-sync:` line.
- A session may run it once after its handoff change is merged to `main`, to refresh the board without waiting for the next run.

## Personal (manual) rows

Add them in Notion, or through the connector, with Source `manual`. The sync never reads or writes them. This vault is public: keep personal project names and details out of the repo, the handoff and this skill; they live only in Notion.

## Another repo

1. Copy `scripts/notion-sync.py` (standard library only) into that repo's `scripts/`.
2. In Notion add that repo's Area option and its Source option (`<repo>/handoff.md`) to the board by hand.
3. Run it with the defaults (it derives `<repo>/handoff.md` and the Area from `git remote`), or pass `--source` and `--area`. Same token, same board.
4. The repo needs a `handoff.md` with a `## In flight` table (`skills/keeping-handoff-docs`).

## Common mistakes

| Mistake | Fix |
|---|---|
| Editing a sync card in Notion | The next run overwrites it. Edit the handoff row; use a `manual` row for anything the handoff does not hold |
| Renaming a Workstream | It closes the old card and opens a new one. Keep the text stable; rename only when you want a fresh card |
| Pasting the database id from the page URL as `NOTION_PROJECTS_DS` | It must be the data source id. When the lookup 404s the script tries it as a database id and, if that database has exactly one data source, uses it and logs a note; otherwise exit 2. Set the data source id |
| Forgetting to add the integration to the page | Exit 2 "not shared". Projects HQ → ••• → Connections → add it |
| Using the Notion connector from a Routine | It is not available there. Use `scripts/notion-sync.py` with `NOTION_TOKEN` |
| Pasting `NOTION_TOKEN` with a line break or space inside it | Exit 2 "invalid characters". Re-enter the secret as one line; surrounding whitespace is stripped |
| `api.notion.com` missing from the allowed domains | Exit 2 "cannot reach". Add it to the environment (`routines/README.md` Step 0) |
| A new Area, Owner or Source value not yet in the board | Exit 2 naming the option. Add it in Notion by hand first (see the Source rule) |
| Running it from a feature branch | The board shows unmerged state until the next run on `main`. Run it on `main` |

## Evidence

- 2026-10-06 — skills-vault: board built and seeded (4 handoff rows plus Josep's manual rows). `scripts/notion-sync.py` was tested only against a local fake Notion server: 51 unit tests pass (`python3 -m unittest discover -s scripts -p 'test_*.py'`), and request shapes were checked against the official notion-sdk-js source. Not yet run against the live Notion API: that session had no token.

## Source

- Josep's request, 2026-10-06: a Projects HQ with a Project Status database and a Board view, seeded from the handoff In flight table and his personal projects; a Routine cannot use the connector, so `NOTION_TOKEN` plus `scripts/notion-sync.py`; draft this skill once the schema is stable.
- Files: `scripts/notion-sync.py`, `scripts/test_notion_sync.py`, `routines/github-stars-sync.md` step 7.
