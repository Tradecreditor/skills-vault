---
name: tracking-projects-in-notion
description: "Runs Jeff's cross-project kanban in Notion under one board policy, mirrors each repo's handoff.md In flight rows via scripts/notion-sync.py, audits the board weekly. Use when opening, moving or closing cards, setting up the board or sync, onboarding a repo, or adding NOTION_TOKEN to a Routine."
metadata:
  origin_type: "vault-operations"
  captured_at: "2026-10-06"
  vault_status: "draft"
---

# tracking-projects-in-notion — one Notion board for every project

## Overview

This is the system for ALL of Jeff's projects. Each repository is one **Area** on one board; work without a repo is tracked as manual cards. The standard is the board policy, [`references/board-policy.md`](references/board-policy.md) (card definition, fields, column entry rules, Definition of Done, P0–P3, WIP limits, cadence): this skill links it and does not repeat it. `CLAUDE.md` / `AGENTS.md` ("Projects HQ" section) carry the per-session rules. `handoff.md` stays the source of truth for repo work (`skills/keeping-handoff-docs/SKILL.md`); Notion is the overview, plus the home of projects that have no repo.

Two access paths, because they have different limits:

| Path | Who | What it can do |
|---|---|---|
| Notion connector (MCP) | an interactive Claude Code session that has the connector | create the page, database and views; read cards; create and edit manual cards |
| Notion REST API with an internal integration token in `NOTION_TOKEN` | `scripts/notion-sync.py`, run by a cloud Routine or any session | the daily one-way sync of `handoff.md` In flight into the board, and the weekly read-only audit |

Jeff found the Notion connector unavailable in his cloud Routines (2026-10-06), so the daily sync and the weekly audit never depend on it.

## The board

Private page **Projects HQ** holds the database **Project Status**. Views: **Board** (GROUP BY Status, the main one), **Table**, **Waiting on Jeff** (filter Status = Waiting on Jeff), **Active** (Status is not Done and not Dropped, sorted by Priority), plus an inline Board on the HQ page and one filtered Board view per Area (below).

| Property | Type | Written by |
|---|---|---|
| Project | title | sync (from the Workstream cell); manual cards by a session with the connector |
| Status | select: Backlog, In progress, Waiting on Jeff, Blocked, Done, Dropped | sync; manual cards by a session with the connector |
| Priority | select: P0, P1, P2, P3; default P2 on create | sync-owned on synced cards when the handoff has a Priority column; manual cards by a session with the connector |
| Area | select, one option per repo or life/business area (e.g. `skills-vault`) | sync (`--area`, default the repo name) |
| Next step | text | sync (from the Next step cell) |
| Owner | select: Jeff, Claude Code, Routine | sync |
| Link | url | sync (from the Detail cell) |
| Last update | date | sync |
| Target date | date, optional | never written by the sync; set in Notion on any card; required for P0 |
| Source | select: `<repo>/handoff.md` or `manual` | sync sets its own label; `manual` cards by a session with the connector |

Create it with the connector (DDL):

```
CREATE TABLE ("Project" TITLE,
  "Status" SELECT('Backlog':gray, 'In progress':blue, 'Waiting on Jeff':yellow, 'Blocked':red, 'Done':green, 'Dropped':brown),
  "Priority" SELECT('P0':red, 'P1':orange, 'P2':blue, 'P3':gray),
  "Area" SELECT('skills-vault':purple),
  "Next step" RICH_TEXT,
  "Owner" SELECT('Jeff':pink, 'Claude Code':orange, 'Routine':brown),
  "Link" URL, "Last update" DATE, "Target date" DATE,
  "Source" SELECT('skills-vault/handoff.md':purple, 'manual':gray))
```

Board view configuration: `GROUP BY "Status"; SORT BY "Last update" DESC`.

**Per-Area board views.** Every project's board is a Board view of this one database filtered by its Area, a tab named after the Area (for example **skills-vault**). A new Area gets a new filtered Board view: `GROUP BY "Status"; FILTER "Area" = "<area>"`, added by a session with the connector on Jeff's word (the sync never changes views or the schema). Never create a separate database or board per project; the policy explains why ([section 1](references/board-policy.md)).

## Working the board (session protocol)

Every session, for repo work and for manual work alike. Column entry rules, the Definition of Done and the cadence are in the [policy](references/board-policy.md) (sections 3, 6 and 7); this is the short form.

1. **Start**: read `handoff.md`; with the Notion connector, also read this Area's cards. Work only on something that has a card, so open one first. Check the Owner's WIP (In progress: Jeff 3, Claude Code 5); say so in your summary if you must exceed it.
2. **Open**: repo work → add a row to `handoff.md` "In flight" (`| Workstream | Status | Priority | Owner | State | Next step | Detail |`) in the same commit as the first piece of work; the next sync creates the card. Manual work → create the card in Notion with every required field and Source `manual`.
3. **Move**: change the row's Status, Owner, Next step (and State) in the same commit as the work that caused the move; manual card → edit it and update Next step and Last update in the same edit. Waiting on Jeff: Next step starts `Jeff:` and names the decision. Blocked: Next step names the blocker and what unblocks it.
4. **Close**: `Done` only when the Definition of Done holds (merged to `main` and live, shipped or decided; checked; the evidence recorded). Repo row: Status `Done`, Next step `none`, Detail = the evidence, and move the row to "Recently done" in a later update. Manual card: Status `Done` and Link = the evidence. Abandoned work is `Dropped` with `Dropped: <reason>`. Never delete a card; follow-up work is a new card.
5. **End**: update the rows and manual cards you touched; your final message names the cards you opened, moved or closed.

Never edit a synced card in Notion: the next sync overwrites it. Never copy a manual card's title or details into a public repo.

**The board is view-only for Jeff** (decided 2026-10-07): he reads it, he never drags, edits or creates cards. Every change is made by an agent on his word — repo cards through `handoff.md`, manual cards through the Notion connector. Never ask him to edit the board.

## Who owns a row (the Source rule)

| Source value | Written by | What the sync does with it |
|---|---|---|
| `<repo>/handoff.md` | the sync only | overwrites it every run; sets Status `Done` when the Workstream leaves In flight (a card already Done or Dropped is left alone); never deletes or archives |
| `manual` (or any other label) | a session through the connector, on Jeff's word | never reads it for writing, never writes it (the query filters on the sync's own Source) |

- To change a sync card, **edit the handoff**, not the card: the next run overwrites Status, Priority, Area, Next step, Owner, Link and Last update. Target date is never written, so it can be set in Notion on any card.
- The script never changes the schema. Add a new Area, Source, Status, Priority or Owner option in Notion (a session with the connector, on Jeff's word) **before** the first run that uses it. The connector sets a select property's options only by restating the whole list, and an option left out is removed from every card: send every existing option with its exact name and colour plus the new one, then fetch again and check that the count rose by exactly one (`references/joining-projects-hq.md` step 3). A run (a dry run too) whose plan needs a missing option stops with exit 2 naming it, before any write.
- Two cards with the same Project and Source: the oldest is the live one; the others are set to Done with a note pointing at the live card and counted as `duplicates=<n>` in the summary (copies already Done or Dropped are skipped). Cards are never deleted, by the script or by hand. A duplicate manual card is set to Dropped through the connector with a pointer to the live card (policy section 5).

## How a handoff row becomes a card

The script reads the first table under `## In flight` and matches columns by header, case-insensitively and in any order: Workstream is required; Status, Priority, Owner, State, Next step, Detail are optional. The standard header is `| Workstream | Status | Priority | Owner | State | Next step | Detail |` (template: `skills/keeping-handoff-docs/references/handoff-template.md`). Each row becomes one card.

**Project** is the Workstream cell with links, wikilinks, `**` and backticks removed, then ONE trailing balanced ` (…)` group removed (`Skill review by agent (Jeff's ask …)` becomes `Skill review by agent`; a title ending in `"` is left alone), then trailing ` —`, `-`, `:` stripped, at most 200 characters. The project title is the key: **keep the Workstream text stable**. Renaming it closes the old card and opens a new one. Two rows with the same title: the first wins, the second is skipped with a warning.

**Explicit columns win; the rules below apply only when a cell is empty (or holds an unknown value).**

| Column | Accepted values | Empty | Unknown |
|---|---|---|---|
| Status | Backlog, In progress, Waiting on Jeff (or `Waiting`), Blocked, Done, Dropped | fallback rules a–f | warns on stderr, uses the rules |
| Owner | Jeff, Claude Code, Routine | derived from Next step | warns, derived from Next step |
| Priority | P0, P1, P2, P3 | not written on an update (Notion's value stays); a new card gets P2 | warns, same as empty |

**Fallback: rules a–f**, for old 4-column handoffs (Workstream, State, Next step, Detail) and for an empty Status cell. The first rule that matches, compared case-insensitively on the cleaned text:

| # | Write this | Status |
|---|---|---|
| a | Next step empty, or `none`, `—`, `-`, `n/a`, `nothing`, or starting with `done`, `fixed`, `closed` | Done |
| b | State starting with `done`, `closed`, `finished` (and Next step not starting with `Jeff`) | Done |
| c | State or Next step starting with `Blocked` | Blocked |
| d | State starting with `Not started` | Backlog |
| e | Next step starting with `Jeff` (`Jeff:`, `Jeff merges …`) | Waiting on Jeff |
| f | anything else | In progress |

Because d comes before e, a `Not started` row whose Next step starts with `Jeff` is Backlog with Owner Jeff.

| Card field | Comes from |
|---|---|
| Owner | the Owner cell; empty → Next step starts with `Jeff` → Jeff; starts with `Routine` or `Next scheduled run` → Routine; anything else → Claude Code |
| Next step | the Next step cell, at most 1900 characters (longer is cut with `…`); a Done row with an empty or `none` Next step gets `Done — ` plus the first sentence of State; a Dropped one gets `Dropped: ` plus the first sentence of State |
| Last update | the newest `YYYY-MM-DD` anywhere in the row that is not later than the handoff's `Last updated:` date; none found → that date. Later dates are plans and ignored; a date right after `version` or `v` (`Notion-Version 2026-03-11`, `v2026-10-04`) is a version string and ignored. A status change bumps it to the handoff date (it only moves forward) |
| Link | Detail cell: first `http(s)` URL; else first backtick span that looks like a repo path (contains `/` or ends in `.md`, `.yaml`, `.yml`, `.py`, `.json`, `.sh`) → `<repo-url>/blob/main/<path>` (`/tree/main/` for a trailing `/`); else first `PR #<n>` in the row → `<repo-url>/pull/<n>`; else `<repo-url>/blob/main/handoff.md` (a fallback the audit does not accept as evidence) |

Closing rules:

- **Done and Dropped cards never leave their column.** A row whose Status differs from its closed card only warns on stderr and the card is counted unchanged. Follow-up work is a new card: use a new Workstream title.
- A **Dropped** row gets `Dropped: <reason>` in Next step (or a first sentence in State); without a reason the sync warns and the audit flags `dropped`.
- A row that just disappears from In flight is closed as Done with `Left <source> In flight; last seen <date>.` and no evidence; the audit flags `evidence`. Set the row to Done with its evidence in Detail instead.

Cells are split on `|` except inside backtick spans and `\|`, so a wikilink such as `[[page|alias]]` in backticks does not break a row.

## Set up once

1. **Create the page and database.** In a session with the Notion connector: create the private page "Projects HQ", create the database with the DDL above, add the Board, Table, Waiting on Jeff and Active views and an inline Board on the page. Without the connector, wait for a session that has it (Jeff does not edit the board). Adding an option means restating the whole option list (see the Source rule above). A board built before the policy (no Priority or Target date property, no Dropped option) needs them added by a session with the connector, on Jeff's word; until Priority exists the sync stops with exit 2.
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
python3 scripts/notion-sync.py --audit       # read-only policy audit (next subsection)
```

| Flag | Default | Meaning |
|---|---|---|
| `--handoff PATH` | `handoff.md` at the repo root | file to mirror |
| `--source LABEL` | `<repo>/handoff.md` | Source value; the only rows a sync may touch, and the only cards an audit names |
| `--area LABEL` | `<repo>` | Area value for every row |
| `--data-source ID` | `NOTION_PROJECTS_DS`, else search | data source id |
| `--repo-url URL` | derived from `git config remote.origin.url` | base for Link values |
| `--audit` | off | the audit instead of the sync; cannot be combined with `--dry-run` (exit 4) |
| `--today YYYY-MM-DD` | current UTC date | tests; the audit's "today" |

`<repo>` is the last path component of `remote.origin.url` without `.git`, and the owner is the one before it (HTTPS, SSH and proxy URLs all work). With no remote, or a remote that is a local path, it is the checkout's folder name. Path, PR and fallback links are built as `<repo-url>/blob/main/…`, `<repo-url>/pull/<n>` and `<repo-url>/blob/main/handoff.md`, with `<repo-url>` defaulting to `https://github.com/<owner>/<repo>`: `--repo-url` changes only that base, so for a default branch other than `main` put full URLs in Detail.

stdout is one line (details go to stderr):

- sync: `notion-sync: created=<n> updated=<n> closed=<n> unchanged=<n> failed=<n> source=<label> data_source=<id8>`, with ` duplicates=<n>` after `failed` when there are any;
- dry run: `notion-sync: dry-run rows=<n> created=<n> … data_source=<id8>`, or just `notion-sync: dry-run rows=<n> source=<label>` when no token is set;
- audit: `notion-audit: cards=<n> open=<n> violations=<n> wip=<n> p0=<n> missing=<n> stale=<n> waiting=<n> blocked=<n> target=<n|n/a> overdue=<n|n/a> evidence=<n> dropped=<n> dup=<n>`, then one `- [<rule>] <card> — <detail>` line per violation on this repo's cards;
- exit 2: `notion-sync: off (<reason>)`; exits 3 and 4: `notion-sync: error (<reason>)` on stderr.

| Exit | Meaning | What a Routine does |
|---|---|---|
| 0 | synced (also: dry run ok, audit ran with or without violations) | copy the output into the final message or report |
| 1 | some writes failed after retries, the rest are done | copy the line; do not retry more than once |
| 2 | off for this run: `NOTION_TOKEN` missing or malformed, 401/403 (on a write the run stops at once), data source not found or not shared, ambiguous search, a schema property missing or of the wrong type (Priority is required; Target date is optional), a needed select option missing, `api.notion.com` unreachable (for example not in the allowed domains), any failed read | copy the `off (<reason>)` line; Jeff fixes the setup |
| 3 | `handoff.md` unusable: file missing, no `## In flight`, no table, no Workstream column | copy the line; the In flight table needs fixing |
| 4 | refused locally: bad flag, bad `--today`, bad `NOTION_VERSION`, `NOTION_API_BASE` not 127.0.0.1 or localhost, `--audit` with `--dry-run` | copy the message; never expected in a Routine |

A Routine never fails because of this script; it reports the line and carries on. Never print, echo or export `NOTION_TOKEN`.

Run the sync on a checkout of `main`. On a feature branch it mirrors unmerged state, and the next daily run overwrites that.

Behaviour: `Notion-Version` 2026-03-11 (override with `NOTION_VERSION`); about 3 requests per second (at least 0.34 s between requests); 429 and 529 retried after `Retry-After` (capped at 30 s), 409, 500, 502, 503, 504 and timeouts retried after 1, 2, 4 s (3 retries); 30 s socket timeout; a create is never blindly retried (after a timeout, 409 or 5xx the data source is queried first, so a page that did land is not created twice); redirects are never followed; the token goes only to `api.notion.com` (`NOTION_API_BASE` accepts only a local test server); nothing is ever deleted or archived. Python 3.9+, standard library only.

### Weekly audit

`python3 scripts/notion-sync.py --audit [--json] [--today D]` checks every card against the policy. It needs `NOTION_TOKEN`, reads all cards (no Source filter), never parses `handoff.md` and never writes. Rules:

| Rule | Violation |
|---|---|
| `wip` | an Owner has more In progress cards than the limit (Jeff 3, Claude Code 5) |
| `p0` | an Owner has more than one open P0 |
| `missing` | an open card lacks Owner, Next step, Priority, Area, a policy Status, Project or Last update |
| `stale` | In progress or Blocked with no update for more than 14 days; Waiting on Jeff for more than 7 |
| `waiting` | Waiting on Jeff and Next step does not start with `Jeff:` plus a need |
| `blocked` | Blocked with an empty Next step |
| `target` | an open P0 without a Target date (`n/a` when the board has no Target date property) |
| `overdue` | an open card whose Target date has passed (`n/a` likewise) |
| `evidence` | Done with no Link, with only the `handoff.md` fallback Link, or closed by leaving In flight |
| `dropped` | Dropped and Next step does not start with `Dropped:` plus a reason |
| `dup` | more than one open card with the same Source and Project (every one after the oldest) |

Privacy (this repository and its reports are public): titles are printed only for cards whose Source equals this run's source label; every other card appears as a count, in the summary line and in one closing line `- <k> more violation(s) on cards from other sources; …`. `wip` and `p0` name an Owner, never a card. Violations are reported, not failures: exit 0 whenever the audit ran, so read the counts. To fix one on this repo's cards, edit the handoff row; for other cards review the board in Notion. `vault-lint` check 9 runs it every Monday (`--audit --today <today>`) and copies the output verbatim into the health report; exit 2 there ("off") is expected until `NOTION_TOKEN` is set.

## Schedule

- `github-stars-sync` step 7 runs the sync daily, after the stars commit and also when there were no new stars; the Routine's final message carries the `notion-sync:` line.
- `vault-lint` check 9 runs the audit every Monday, and Jeff reviews the board that day (policy section 7).
- A session may run the sync once after its handoff change is merged to `main`, to refresh the board without waiting for the next run. Another repo is synced by its own scheduled run or by the next session in it.

## Manual cards (non-repo work)

A session with the connector adds them, on Jeff's word, with Source `manual` and every required field (policy section 3). The sync never reads or writes them, and the audit reports on them as counts only. This vault is public: keep manual project names and details out of the repo, the handoff, the health reports and this skill; they live only in Notion.

## Onboarding another project

The step-by-step guide for an agent in the other project is [`references/joining-projects-hq.md`](references/joining-projects-hq.md): Jeff pastes its raw GitHub link into a session there and the agent follows it. It covers the approval check (status and `review_hash` on one clone of the vault), whose repo it is and whether it is public, the Area and Source options and the project's Board tab, copying the script from that clone, the 7-column handoff, the `CLAUDE.md` / `AGENTS.md` block, `NOTION_TOKEN` on a local computer (Windows and macOS), Jeff confirming the rows and files before anything is written, writing and committing in one go (a PR repo stops until the merge), the first sync, dropping the project's old manual cards once their synced cards exist, and resuming a join that spans several sessions. The join itself is tracked by one manual card, `Projects HQ join: <source>`, in the project's Area: its Next step names the next step and its private page body lists the cards to drop, so the join advances and closes through the connector without extra commits. In short:

- **A repo** becomes one Area. A session with the connector adds its Area option, its Source option (`<repo>/handoff.md`) and a Board tab (`GROUP BY "Status"; FILTER "Area" = "<area>"`), never a separate database. The repo gets `scripts/notion-sync.py` (copied from this skill's `scripts/` folder in a reviewed clone), a 7-column In flight table, and the block in its agent instructions. It is synced by the next session in it, or by its own Routine: `python3 scripts/notion-sync.py --area "<area>" --source "<repo>/handoff.md"`. Run from that repo, `--audit` names only that repo's cards. Same token, same board.
- **A project without a repo** has manual cards only. On Jeff's word, a session with the connector adds the Area option and creates the cards with Source `manual`, then follows the same protocol (open, move, close with a Link to the evidence). No script, no handoff.

`scripts/notion-sync.py` in this skill is a byte-identical copy of the vault's `scripts/notion-sync.py`, so the copy other projects download is covered by this skill's review. Edit both together; `scripts/test_notion_sync.py` fails when they differ.

## Common mistakes

| Mistake | Fix |
|---|---|
| Starting work with no card | Open one first (a handoff row or a manual card); the policy forbids work that is not on a card |
| Done without evidence | Put the PR, commit or report in Detail (Link). The audit flags `evidence` for Done with no Link, only the handoff fallback Link, or closed by leaving In flight |
| A row that silently disappears from In flight | The sync closes its card as Done with "Left … In flight" and no evidence. Set the row to Done (or Dropped with a reason) with its evidence, then move it to Recently done later |
| Over the WIP limit | Finish, park (→ Backlog) or hand over a card before starting another; say so in the summary if you must exceed it. The audit flags `wip` |
| Waiting on Jeff without `Jeff:` | Next step must start `Jeff:` and name the decision or action. The audit flags `waiting` |
| Reopening a Done card by changing its row | A closed card never leaves its column; the row only warns. Use a new Workstream title for follow-up work |
| Deleting a duplicate card by hand | Never delete. The sync sets extra synced copies to Done; set a duplicate manual card to Dropped with a pointer to the live card |
| Editing a sync card in Notion | The next run overwrites it. Edit the handoff row; use a `manual` card for anything the handoff does not hold |
| Renaming a Workstream | It closes the old card and opens a new one. Keep the text stable; rename only when you want a fresh card |
| Pasting the database id from the page URL as `NOTION_PROJECTS_DS` | It must be the data source id. When the lookup 404s the script tries it as a database id and, if that database has exactly one data source, uses it and logs a note; otherwise exit 2. Set the data source id |
| Forgetting to add the integration to the page | Exit 2 "not shared". Projects HQ → ••• → Connections → add it |
| Using the Notion connector from a Routine | Jeff found it unavailable there (2026-10-06). Use `scripts/notion-sync.py` with `NOTION_TOKEN` |
| Pasting `NOTION_TOKEN` with a line break or space inside it | Exit 2 "invalid characters". Re-enter the secret as one line; surrounding whitespace is stripped |
| `api.notion.com` missing from the allowed domains | Exit 2 "cannot reach". Add it to the environment (`routines/README.md` Step 0) |
| A new Area, Owner, Priority or Source value not yet in the board | Exit 2 naming the option. A session with the connector adds it in Notion first, on Jeff's word (see the Source rule) |
| Copying a manual card's title or details into the repo, a report or a commit | The repo is public. Manual cards stay in Notion; the audit prints other cards as counts only |
| Running the sync from a feature branch | The board shows unmerged state until the next run on `main`. Run it on `main` |

## Evidence

- 2026-10-06 — skills-vault: board built and seeded with 16 cards (4 from the handoff In flight table, 12 manual). `scripts/notion-sync.py` has been tested only against a local fake Notion server. v1 (sync only): 51 tests and three independent reviews (spec, API shape, token safety); request shapes checked against the official notion-sdk-js source; the 4 seeded handoff cards, read back from Notion and replayed through the script, gave `created=0 updated=0 unchanged=4`.
- v2 (Priority, Dropped, Target date, `--audit`, explicit Status / Priority / Owner columns): 86 unit tests pass after the 2026-10-06 rename to Jeff (`cd /home/user/skills-vault && python3 -m unittest discover -s scripts -p 'test_*.py'`); three independent reviews on v2 (privacy, correctness, policy fit), with the fixes re-verified.
- Live since 2026-10-07 (skills-vault): first run `created=0 updated=0 unchanged=4` (the seeded cards matched), after PR #32 `updated=1`, then `unchanged=4`; first `--audit`: 16 cards, 3 violations.
- 2026-10-07: `references/joining-projects-hq.md` (joining another project) went through eight rounds of independent multi-session walk-throughs and regression checks; the sync parts were replayed in throwaway repos against the fake Notion server; the script copy in `scripts/` is test-enforced identical to the vault's.

## Source

- Jeff's request, 2026-10-06: a Projects HQ with a Project Status database and a Board view, seeded from the handoff In flight table and his personal projects; a Routine cannot use the connector, so `NOTION_TOKEN` plus `scripts/notion-sync.py`; draft this skill once the schema is stable.
- Jeff's board policy, `references/board-policy.md`: one standard for all projects, with Priority, Dropped, Target date and a weekly audit.
- Files: `scripts/notion-sync.py` (copy in this skill's `scripts/`), `scripts/test_notion_sync.py`, `references/board-policy.md`, `references/joining-projects-hq.md`, `routines/github-stars-sync.md` step 7, `routines/vault-lint.md` check 9, `CLAUDE.md` "Projects HQ".
