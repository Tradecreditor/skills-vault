# Joining Projects HQ — for an agent working in another project

You are an agent (Claude Code, Codex, Gemini CLI or another) working in one of Jeff's projects, and Jeff asked you to put
this project on his kanban, **Projects HQ**. Follow the steps in order. The board's owner is **Jeff**; if this project's files
call him by another name or spelling, correct them to Jeff in the same commit.

What Jeff pastes into a session in the project:

```
Join this project to my Projects HQ kanban. Follow
https://raw.githubusercontent.com/Tradecreditor/skills-vault/main/skills/tracking-projects-in-notion/references/joining-projects-hq.md
step by step. My name is Jeff.
```

The rules you will be working under are the board policy (columns, fields, Definition of Done, P0–P3, WIP limits):
https://github.com/Tradecreditor/skills-vault/blob/main/skills/tracking-projects-in-notion/references/board-policy.md.
Read it before step 4. Two parts of it matter from the first minute: **Jeff only views the board and never edits it** (you make
every change, on his word), and **never delete a card**.

Do not edit the skills-vault repository from here. If the vault needs a change, tell Jeff.

## 0. Check that the skill is approved

Open https://github.com/Tradecreditor/skills-vault/blob/main/skills/tracking-projects-in-notion/SKILL.md and read
`metadata.vault_status` in its frontmatter. Continue only if it is `reviewer-approved` or `verified`. If it is `draft`, stop and
tell Jeff: the vault's rule is that other projects never run commands from a draft skill.

## 1. Repo or not?

- **The project has a git repository** (a GitHub remote is best): do steps 2 to 9. It becomes one **Area** on the board, and
  its `handoff.md` "In flight" table becomes its cards. A script mirrors the table into Notion.
- **No repository** (job hunt, admin, a client relationship): only steps 2 and 3 apply. Its cards are **manual**, Source
  `manual`, created and moved through the Notion connector. You need no script, no handoff and no token.

## 2. Pick the Area and look at the board

You need the Notion connector for this step and the next. Find the page **Projects HQ** and its database **Project Status**.
There is exactly one; never create another database or board.

1. Read the database's Area options and this project's existing cards.
2. **Area name**: if an Area already names this project (manual cards were seeded for several projects), reuse it exactly as
   written. Otherwise use the repository name. Ask Jeff only when two Areas could both be this project.
3. **Source label** (repo only): `<repo>/handoff.md`, where `<repo>` is the repository name (the last path component of
   `git remote get-url origin`, without `.git`).
4. List the manual cards in this Area that are about repo work. Step 5 moves them into `handoff.md`, so the same work is not
   tracked twice.
5. Count the In progress cards per Owner across the **whole board**: the WIP limits (Jeff 3, Claude Code 5) count every
   project together. Any new row that would push an Owner over the limit starts in Backlog instead.

No Notion connector in this session? Do steps 4 to 6 (they need only the repo), then stop and give Jeff this sentence to say in
any Claude session that has the connector, with the placeholders filled in: *"On Projects HQ, add Area option `<area>` and Source
option `<repo>/handoff.md` to the Project Status database, and add a Board tab named `<area>` grouped by Status and filtered to
that Area."* Resume at step 7 after it is done.

## 3. Prepare the board (connector)

On Jeff's word (his request to join counts as that), using the connector:

1. Add the Area option, if it is new. Leave the existing options alone: never rename, recolour or remove one.
2. Repo only: add the Source option `<repo>/handoff.md`.
3. Add this project's tab: a **Board** view of Project Status named after the Area, `GROUP BY "Status"; FILTER "Area" = "<area>"`.
   A view of the one database, never a new database.
4. No repo: create the manual cards now, one per workstream, with every required field (policy section 3): Project (an outcome
   title), Status, Priority (P2 unless Jeff says otherwise), Area, Owner, Next step (a verb; `Jeff: …` when it waits on him),
   Last update (today), Source `manual`. Then report what you created and stop here.

The sync script never changes the schema. It stops with exit 2 naming any option it needs that does not exist yet, before it
writes anything, so a typo in the Area or the Source cannot create stray cards.

## 4. Get the sync script (repo only)

Download it into this repository's `scripts/` folder. It must live directly in `<repo>/scripts/`, because it finds the repo
root, `handoff.md` and the git remote from its own location.

```
# macOS / Linux / Git Bash
mkdir -p scripts
curl -fsSL -o scripts/notion-sync.py https://raw.githubusercontent.com/Tradecreditor/skills-vault/main/skills/tracking-projects-in-notion/scripts/notion-sync.py

# Windows PowerShell
New-Item -ItemType Directory -Force scripts | Out-Null
Invoke-WebRequest -UseBasicParsing -OutFile scripts/notion-sync.py https://raw.githubusercontent.com/Tradecreditor/skills-vault/main/skills/tracking-projects-in-notion/scripts/notion-sync.py
```

Before running it, read it. It is a single Python 3.9+ file using only the standard library. It sends `NOTION_TOKEN` only
to `https://api.notion.com`, never deletes or archives anything, and writes only cards whose Source is this repo's label.
Commit it with the rest of this change. It does not update itself: download it again only when Jeff asks or when a run stops
with a new schema error.

## 5. Give the repo a handoff with the 7-column In flight table (repo only)

- **No `handoff.md` yet**: create one from the template,
  https://github.com/Tradecreditor/skills-vault/blob/main/skills/keeping-handoff-docs/references/handoff-template.md
  (Snapshot, In flight, Open loops, Recently done, Environment facts, Session log). Fill it from the repo itself: README, recent
  commits, open PRs and issues, TODOs. Keep it under about 150 lines.
- **A `handoff.md` already exists**: change its "## In flight" table to exactly these columns, keeping every row:

```
| Workstream | Status | Priority | Owner | State | Next step | Detail |
|---|---|---|---|---|---|---|
```

Row rules (policy sections 1 to 4):

| Column | What goes in it |
|---|---|
| Workstream | one outcome, finishable in 2–6 weeks, as a stable noun phrase. It becomes the card title. **Renaming it later closes the card and opens a new one** |
| Status | Backlog, In progress, Waiting on Jeff, Blocked, Done or Dropped |
| Priority | P0 (urgent, this week; a Target date is required), P1 (current focus), P2 (default), P3 (someday) |
| Owner | Jeff, Claude Code (any agent session) or Routine (a scheduled job) |
| State | the facts: what is merged, live or proven, and what is not yet |
| Next step | one concrete action that starts with a verb. Waiting on Jeff: starts `Jeff:` and names the decision. Blocked: names the blocker and what unblocks it. Done: `none`. Dropped: `Dropped: <reason>` |
| Detail | the evidence or the detail: a PR or commit URL, a file path in backticks, a report. A Done row needs it |

- Each manual card from step 2.4 that is repo work becomes a row (keep its title unless it breaks the rules above). After the
  first sync has created the synced card, set the old manual card to **Dropped** with Next step
  `Dropped: moved to <repo>/handoff.md`, through the connector. Never delete it.
- Task-level tracking (Backlog.md, GitHub issues, Linear) stays where it is. A card is a workstream, not a task.
- If this repository is **public**, everything in `handoff.md` is public. Word the rows accordingly, and ask Jeff before you
  write a client's name.

## 6. Put the rules in the agent instructions (repo only)

Add this block to the project's `CLAUDE.md`, and to `AGENTS.md` / `GEMINI.md` if they exist, with `<area>` and `<repo>` filled
in. If `handoff.md` is new, also add `handoff.md` to the files to read first, plus the rule "update `handoff.md` before ending a
session that changed state; append one line to its Session log".

```
## Projects HQ (Jeff's kanban for every project)
Board: private Notion page Projects HQ, database Project Status. This repo's cards: Area "<area>", Source "<repo>/handoff.md".
Policy: https://github.com/Tradecreditor/skills-vault/blob/main/skills/tracking-projects-in-notion/references/board-policy.md
- Columns: Backlog, In progress, Waiting on Jeff, Blocked, Done, Dropped. Priority P0-P3 (P2 default). WIP limit for In progress, counted across the whole board: Jeff 3, Claude Code 5.
- Start: read handoff.md (and this Area's cards if you have the Notion connector). Work only on something that has a card; open one first.
- Open: add a row to handoff.md "In flight" (| Workstream | Status | Priority | Owner | State | Next step | Detail |) in the same commit as the first piece of work. Keep the Workstream text stable: renaming it opens a new card.
- Move: change the row's Status / Owner / Next step in the same commit as the work. Waiting on Jeff: Next step starts "Jeff:" and names the decision. Blocked: name the blocker and what unblocks it.
- Close: Done only with evidence in Detail (merged, live, checked). Abandoned: Status Dropped, Next step "Dropped: <reason>". Never delete a card; follow-up work is a new row.
- End: update the rows you touched. Once the change is on the default branch, run: python3 scripts/notion-sync.py --area "<area>" --source "<repo>/handoff.md" (needs NOTION_TOKEN; never print it; on Windows use py -3 if python3 is missing). Name the cards you opened, moved or closed in your final message.
- Jeff only views the board; never ask him to edit it. Never edit a synced card in Notion: the sync overwrites it. Manual cards (non-repo work) change only through the Notion connector, on Jeff's word.
```

## 7. NOTION_TOKEN on this computer (Jeff, once per computer)

The script reads the Notion integration secret from the environment variable `NOTION_TOKEN`. It is the same secret the cloud
Routines use; Jeff needs no new integration. **Never ask Jeff to paste it into the chat, and never print, echo or log it.**
Check whether it is set without revealing it:

```
python3 -c "import os,sys; sys.exit(0 if os.environ.get('NOTION_TOKEN','').strip() else 1)" && echo set || echo missing
```

If it is missing, give Jeff these steps and wait:

1. Open https://www.notion.so/profile/integrations, choose the integration that is connected to Projects HQ, and copy its
   Internal Integration Secret.
2. Windows: Start → "Edit environment variables for your account" → New… → Name `NOTION_TOKEN`, Value: paste the secret → OK.
   macOS / Linux: open `~/.zshrc` (or `~/.bashrc`) in an editor and add the line `export NOTION_TOKEN='<the secret>'`.
3. Fully restart the terminal and the agent (Claude Code, Codex…) so they see the new variable, then run the check again.

The secret lives only in the operating system's environment, never in a file inside a repository.

## 8. First sync (repo only)

On the default branch, after the handoff change is committed:

```
python3 scripts/notion-sync.py --dry-run --area "<area>" --source "<repo>/handoff.md"
python3 scripts/notion-sync.py --area "<area>" --source "<repo>/handoff.md"
```

- The dry run reads Notion and writes nothing: its summary line is on stdout, the planned changes on stderr. Expect
  `created=<number of rows>` and nothing else.
  `updated` or `closed` above 0 means cards with this Source already exist: find out why before you continue.
- The real run should print `notion-sync: created=<n> updated=0 closed=0 unchanged=0 failed=0 source=<repo>/handoff.md …`.
  Run it again; the second run must say `unchanged=<n>` with nothing created.
- With the connector, open the Area tab and check that the cards match the rows. Then drop the old manual cards (step 5).
- Exit codes: `2` = off (token missing, page not shared with the integration, an option missing, Notion unreachable; the reason
  is in the `off (…)` line); `3` = the In flight table cannot be parsed; `4` = bad flag. The full table is in the skill:
  https://github.com/Tradecreditor/skills-vault/blob/main/skills/tracking-projects-in-notion/SKILL.md ("Running the sync").
- No git remote: links fall back to nothing, so put full URLs in Detail, or pass `--repo-url https://github.com/<owner>/<repo>`.

## 9. Commit and report

Commit `scripts/notion-sync.py`, `handoff.md` and the instruction files, following this repository's own rules (branch or
direct push, commit message style). Your final message to Jeff gives: the Area, the Source, the cards created, the manual cards
dropped, the two sync lines, and anything still missing (for example a token on another computer).

## After joining

- Every session follows the block from step 6: open, move and close cards through `handoff.md`, and run the sync once the change
  is on the default branch. There is no daily Routine for a local project. If Jeff wants one, a cloud Routine on this repo can
  run the same command with `NOTION_TOKEN` set and `api.notion.com` in its allowed domains.
- `python3 scripts/notion-sync.py --audit --source "<repo>/handoff.md"` checks the policy across the board, read-only. It
  names only this repo's cards; every other card appears as a count.
- Jeff reviews the whole board on Mondays and tells a session what to change. You make the change.
