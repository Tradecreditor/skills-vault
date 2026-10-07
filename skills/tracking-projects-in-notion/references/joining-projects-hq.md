# Joining Projects HQ — for an agent working in another project

You are an agent (Claude Code, Codex, Gemini CLI or another) working in one of Jeff's projects, and Jeff asked you to put
this project on his kanban, **Projects HQ**. Follow the steps in order and stop wherever a step says stop.

What Jeff pastes into a session in the project:

```
Join this project to my Projects HQ kanban. Follow
https://raw.githubusercontent.com/Tradecreditor/skills-vault/main/skills/tracking-projects-in-notion/references/joining-projects-hq.md
step by step. My name is Jeff.
```

## Ground rules

- **Read the board policy before step 2**:
  https://github.com/Tradecreditor/skills-vault/blob/main/skills/tracking-projects-in-notion/references/board-policy.md
  (columns, fields, Definition of Done, P0–P3, WIP limits). Where it says Jeff adds Areas or options, it means *on his word*:
  you make the change, and his request to join is that word.
- **Jeff only views the board; he never edits it.** You make every change. Never ask him to drag, edit or create a card.
- **Never delete a card.** A card that should not exist goes to Dropped with a reason.
- **Never print, echo, paste or commit `NOTION_TOKEN`** (step 7).
- **His name is Jeff** in everything you write for this join: handoff rows, Owner `Jeff`, `Waiting on Jeff`, `Jeff:` next steps,
  the instruction block. Do not rename him anywhere else (LICENSE, legal or user-facing text, emails, handles, code, git config).
  If you see another name or spelling for him there, list the files for Jeff instead.
- **Do not edit the skills-vault repository** from here. If the vault needs a change, tell Jeff.
- **Python**: in this guide `python3` means `python3` on macOS and Linux and `py -3` on Windows. On Windows `python3` is usually
  the Microsoft Store stub, which prints "Python was not found". Check the interpreter first: `py -3 --version` or
  `python3 --version`. If neither prints a version, Python is missing; tell Jeff.

## 0. Get a reviewed copy of the skill

Other projects may only run code from a vault skill that passed review, and only the files as reviewed. Check both on one
checkout, made outside this repository, and keep that checkout for step 4:

```
# Git Bash / macOS / Linux
VAULT="$(mktemp -d)/skills-vault"
git clone --depth 1 -c core.autocrlf=false https://github.com/Tradecreditor/skills-vault "$VAULT"
git -C "$VAULT" rev-parse --short HEAD
grep -E '^  (vault_status|review_hash):' "$VAULT/skills/tracking-projects-in-notion/SKILL.md"
python3 -I "$VAULT/skills/auditing-agent-skills/scripts/static_scan.py" --hash "$VAULT/skills/tracking-projects-in-notion"

# Windows PowerShell
$VAULT = Join-Path $env:TEMP ("skills-vault-" + (Get-Random))
git clone --depth 1 -c core.autocrlf=false https://github.com/Tradecreditor/skills-vault $VAULT
git -C $VAULT rev-parse --short HEAD
Select-String -Path "$VAULT\skills\tracking-projects-in-notion\SKILL.md" -Pattern '^  (vault_status|review_hash):'
py -3 -I "$VAULT\skills\auditing-agent-skills\scripts\static_scan.py" --hash "$VAULT\skills\tracking-projects-in-notion"
```

Continue only if `vault_status` is `reviewer-approved` or `verified` **and** the hash printed by the last command equals
`review_hash`. Otherwise stop and tell Jeff: either the skill is still a draft, or its files changed after the review and the
next review has not run yet. Note the short commit id: it goes into the handoff in step 5. Whenever the script is copied again
later, repeat this step first.

## 1. What kind of project is this?

- **No repository** (job hunt, admin, a client relationship): its cards are **manual** (Source `manual`), created and moved
  through the Notion connector. Do steps 2 and 3, then step 10. You need no script, no handoff and no token.
- **A git repository**: it becomes one **Area** on the board, and its `handoff.md` "In flight" table becomes its cards, which
  a script mirrors into Notion. Do every step. First find out two things:
  - **Whose repository is it?** Look at `git remote get-url origin` and the recent authors (`git log --format='%an' -50 | sort -u`).
    If it is not Jeff's own repository (a client's, an employer's, an open-source upstream), or other people commit to it,
    stop and ask Jeff before you write anything. Offer to track it as manual cards instead (steps 2–3 only).
  - **Is it public?** Use `gh repo view --json visibility` if `gh` works, otherwise ask Jeff. If you cannot tell, treat it as
    public. Everything in a public repository's `handoff.md`, instruction files, commits and Session log is public.

## 2. Look at the board and pick the Area (Notion connector)

Find the page **Projects HQ** and its database **Project Status**. There is exactly one; never create another database or board.

1. Read the database's Area and Source options, and the cards of any Area that could be this project.
2. **Area**: if an Area already names this project (manual cards were seeded for several projects), reuse it exactly as written.
   Otherwise: a repo uses its repository name; a project without a repo asks Jeff for the name of its life or business area.
   Ask Jeff too when two Areas could both be this project.
3. **Source** (repo only): `<repo>/handoff.md`, where `<repo>` is the last path component of `git remote get-url origin`
   without `.git`. If that Source option already exists, another repository may own it (two repos with the same name): stop
   and ask Jeff. The usual answer is `<owner>-<repo>/handoff.md`, passed with `--source` everywhere.
4. List this Area's existing manual cards and their Status, Owner, Priority, Next step and Target date. Step 5 (repo) or step 3
   (no repo) decides what happens to them; the same work must never be tracked twice.
5. Count the In progress cards per Owner across the **whole board**. The WIP limits (Jeff 3, Claude Code 5) count every project
   together. Cards that already exist keep their Status. Only a workstream that was not on the board before starts in Backlog
   when In progress would push its Owner over the limit. Report the counts in step 10.

**No Notion connector in this session?** Steps 2 and 3 need it. Give Jeff this sentence, with `<project>` and `<repo>` filled in,
to say in any Claude session that has the connector:

> On Projects HQ: if an Area option already names `<project>`, tell me its exact name, otherwise add Area option `<repo>`. Add
> Source option `<repo>/handoff.md` (if it already exists, stop and tell me). Add a Board tab for that Area, grouped by Status and
> filtered to it, only if it has none. List that Area's manual cards (title, Status, Owner, Priority, Next step, Target date)
> and the In progress count per Owner across the board.

Then stop. When Jeff brings the answer back, resume at step 2.4 with it and skip step 3. Dropping the old manual cards (step 9)
will need a session with the connector too.

## 3. Prepare the board (Notion connector)

1. Add the Area option if it is new. Leave existing options alone: never rename, recolour or remove one.
2. Repo only: add the Source option.
3. If the database has no Board view named after the Area yet, add one: a **Board** view of Project Status,
   `GROUP BY "Status"; FILTER "Area" = "<area>"`. A view of the one database, never a new database. An Area that was seeded
   earlier usually has its tab already; leave it alone.
4. **No repo**: show Jeff the Area's existing manual cards and ask which workstreams he wants on the board (title, Status,
   Owner, Next step, Priority and any deadline). Create only the cards that do not exist yet, with every required field
   (policy section 3), Last update today and Source `manual`. Never invent workstreams. If the project has a local folder with
   a `CLAUDE.md` / `AGENTS.md`, add these lines to it:

   ```
   ## Projects HQ (Jeff's kanban for every project)
   This project's cards: Area "<area>", Source manual, on the private Notion board Projects HQ (database Project Status).
   Policy: https://github.com/Tradecreditor/skills-vault/blob/main/skills/tracking-projects-in-notion/references/board-policy.md
   Change cards only through the Notion connector, on Jeff's word; every move updates Next step and Last update. Never delete a card. Jeff only views the board.
   ```

   Then go to step 10.

The sync script never changes the schema. It stops with exit 2 naming any option it needs that does not exist yet, before it
writes anything, so a typo in the Area or the Source cannot create stray cards.

## 4. Copy the script (repo only)

Copy it **from the step-0 checkout**, never from a second download. It must sit directly in `<repo>/scripts/`, because it finds
the repo root, `handoff.md` and the git remote from its own location. If `scripts/notion-sync.py` already exists and its
docstring does not start with `notion-sync.py - one-way mirror of handoff.md`, it is a different file: stop and ask Jeff.

```
# Git Bash / macOS / Linux
mkdir -p scripts && cp "$VAULT/skills/tracking-projects-in-notion/scripts/notion-sync.py" scripts/notion-sync.py

# Windows PowerShell
New-Item -ItemType Directory -Force scripts | Out-Null
Copy-Item "$VAULT\skills\tracking-projects-in-notion\scripts\notion-sync.py" scripts\notion-sync.py
```

It is a single Python 3.9+ file that uses only the standard library. It sends `NOTION_TOKEN` only to `https://api.notion.com`,
never deletes or archives anything, and writes only the cards whose Source is this repo's label. It does not update itself:
copy it again only when Jeff asks, repeating step 0 first. An exit 2 that names a missing option or property is fixed in Notion
(step 3), not by a new copy.

## 5. Give the repo a handoff with the 7-column In flight table (repo only)

- **No `handoff.md` yet**: create one from the template in the checkout,
  `skills/keeping-handoff-docs/references/handoff-template.md` (Snapshot, In flight, Open loops, Recently done, Environment
  facts, Session log). Fill it from the repo itself and keep it under about 150 lines.
- **A `handoff.md` already exists**: keep everything; change only its In flight table to the columns below.
- The heading must be exactly `## In flight` (level 2, this capitalisation, at the start of a line), and the table must be the
  first table under it. Otherwise the sync exits 3.
- Under "Environment facts", add: `notion-sync.py copied from skills-vault <short commit id> (reviewed)`.

```
| Workstream | Status | Priority | Owner | State | Next step | Detail |
|---|---|---|---|---|---|---|
```

| Column | What goes in it |
|---|---|
| Workstream | one outcome, finishable in 2–6 weeks, as a stable noun phrase. It becomes the card title. **Renaming it later closes the card and opens a new one** |
| Status | Backlog, In progress, Waiting on Jeff, Blocked, Done or Dropped |
| Priority | P0 (urgent, this week), P1 (current focus), P2 (default), P3 (someday). A P0 needs a Target date, which has no column: set it on the synced card in step 9 |
| Owner | Jeff, Claude Code (any agent session) or Routine (a scheduled job) |
| State | the facts: what is merged, live or proven, and what is not yet |
| Next step | one concrete action that starts with a verb. Waiting on Jeff: starts `Jeff:` and names the decision. Blocked: names the blocker and what unblocks it. Done: `none`. Dropped: `Dropped: <reason>` |
| Detail | the evidence or the detail: a full URL (PR, commit, report), or a file path in backticks. Backtick paths and `PR #<n>` become `https://github.com/<owner>/<repo>/blob/main/<path>` and `…/pull/<n>`, so if the default branch is not `main` or the remote is not on GitHub, write full URLs. A Done row needs evidence |

What goes in the table:

- **This Area's manual cards that are repo work** become rows, keeping their Status, Owner and Priority. In a **private** repo
  you may keep their titles. In a **public** repo never copy a manual card's title or details: write a new public-safe title,
  show Jeff the old → new list in chat, and commit only after he agrees. In every repo, keep manual card titles out of commit
  messages. The old manual cards are set to Dropped in step 9, after their synced cards exist.
- **New workstreams**: only ones that are clearly active (an open PR, recent commits toward one outcome). TODOs, issues and
  ideas go to Open loops, not In flight: every row becomes a card, and a card can be dropped but never removed.
- **A row for this join**: `Projects HQ join` with Status In progress, Owner Claude Code, Next step `Run the first sync on the
  default branch`. Step 9 sets it to Done with the sync line as evidence.
- Task-level tracking (Backlog.md, GitHub issues, Linear) stays where it is. A card is a workstream, not a task.
- Rows are only drafts until Jeff has seen them: he confirms them in step 9, before the first real sync.

## 6. Put the rules in the agent instructions (repo only)

Add this block to the project's `CLAUDE.md`, and to `AGENTS.md` / `GEMINI.md` if they exist, with `<area>` and `<source>` filled
in. If `handoff.md` is new, also add it to the files to read first, plus the rule "update `handoff.md` before ending a session
that changed state; append one line to its Session log". Add to these files; never rewrite what is already there.

```
## Projects HQ (Jeff's kanban for every project)
Board: private Notion page Projects HQ, database Project Status. This repo's cards: Area "<area>", Source "<source>".
Policy: https://github.com/Tradecreditor/skills-vault/blob/main/skills/tracking-projects-in-notion/references/board-policy.md
Sync: python3 scripts/notion-sync.py --area "<area>" --source "<source>"   (Windows: py -3; needs NOTION_TOKEN; never print it)
- Columns: Backlog, In progress, Waiting on Jeff, Blocked, Done, Dropped. Priority P0-P3 (P2 default). WIP limit for In progress, counted across the whole board: Jeff 3, Claude Code 5.
- Start: read handoff.md (and this Area's cards if you have the Notion connector). On the default branch with NOTION_TOKEN set, run the sync once. Work only on something that has a card; open one first.
- Open: add a row to handoff.md "In flight" (| Workstream | Status | Priority | Owner | State | Next step | Detail |) in the same commit as the first piece of work. Keep the Workstream text stable: renaming it opens a new card.
- Move: change the row's Status / Owner / Next step in the same commit as the work. Waiting on Jeff: Next step starts "Jeff:" and names the decision. Blocked: name the blocker and what unblocks it.
- Close: Done only with evidence in Detail (merged, live, checked). Abandoned: Status Dropped, Next step "Dropped: <reason>". Never delete a card; follow-up work is a new row.
- End: update the rows you touched. Once the change is on the default branch, run the sync. Name the cards you opened, moved or closed in your final message.
- Jeff only views the board; never ask him to edit it. Never edit a synced card in Notion, except its Target date (the sync never writes that field and overwrites all the others). Manual cards change only through the Notion connector, on Jeff's word.
```

## 7. NOTION_TOKEN on this computer (Jeff, once per computer)

The script reads the Notion integration secret from the environment variable `NOTION_TOKEN`. It is the same secret the cloud
Routines use; Jeff needs no new integration. Check whether it is set, without revealing it:

```
# Git Bash / macOS / Linux
[ -n "${NOTION_TOKEN:-}" ] && echo set || echo missing
# Windows PowerShell
if ([string]::IsNullOrWhiteSpace($env:NOTION_TOKEN)) { 'missing' } else { 'set' }
# Windows cmd
if defined NOTION_TOKEN (echo set) else (echo missing)
```

Never run `echo $NOTION_TOKEN`, `echo %NOTION_TOKEN%`, `$env:NOTION_TOKEN` on its own, `env`, `printenv`, `set` or
`Get-ChildItem Env:`: each prints the secret. Never ask Jeff to paste it into the chat.

If it is missing, give Jeff these steps and wait:

1. Open https://www.notion.so/profile/integrations, choose the integration that is connected to Projects HQ, and copy its
   Internal Integration Secret.
2. **Windows**: Start → "Edit environment variables for your account" → New… → Name `NOTION_TOKEN`, Value: paste the secret → OK.
   **macOS / Linux**: open your shell profile (`~/.zshrc` on macOS) in an editor and add the line
   `export NOTION_TOKEN='<the secret>'`. First make sure that file is not tracked by git: a profile symlinked into a dotfiles
   repository would publish the secret.
3. Fully restart the terminal and the agent (Claude Code, Codex…) so they see the variable, then run the check again.

If the secret is ever pasted into a chat, printed or written to a file, do not use it. Tell Jeff to refresh it at
notion.so/profile/integrations (the integration → the secret's refresh option) and then update `NOTION_TOKEN` on the cloud
environment "Skills Management" and on every computer that has it, or the daily sync goes off.

## 8. Commit (repo only)

Commit `scripts/notion-sync.py`, `handoff.md` and the instruction files together, following this repository's own rules
(branch or direct push, commit message style, its handoff rule).

- **Changes land through pull requests here**: open the PR and stop. Set the join row's Next step to `Jeff: merge PR <n>; the
  next session on the default branch runs the first sync (step 9 of the joining guide)`, Status Waiting on Jeff, Owner Jeff.
  Tell Jeff that the first sync, the second run and dropping the old manual cards (list how many) happen after the merge, in
  any session on the default branch. That session follows step 9.
- **Direct pushes to the default branch**: push, then do step 9 now.

## 9. First sync (repo only, on the default branch)

On an up-to-date checkout of the default branch, with the step-7 check printing `set`:

```
python3 scripts/notion-sync.py --dry-run --area "<area>" --source "<source>"
```

1. The dry run reads Notion and writes nothing. Its summary line is on stdout and the planned changes on stderr. Expect
   `created=<number of rows>` and nothing else. If `updated` or `closed` is above 0, cards with this Source already exist:
   find out why before you continue.
2. **Show Jeff the rows the run will create** (title, Status, Owner, Priority) and run the real sync only after he agrees:

   ```
   python3 scripts/notion-sync.py --area "<area>" --source "<source>"
   ```

   Expect `notion-sync: created=<n> updated=0 closed=0 unchanged=0 failed=0 source=<source> …`. Run it again: the second run
   must say `unchanged=<n>` and create nothing.
3. With the connector: open the Area's tab and check that the cards match the rows. Set the Target date on synced P0 cards,
   and copy each migrated manual card's Target date to its new synced card. Then set each old manual card that was moved into
   the handoff to **Dropped**, in one edit with Next step `Dropped: moved to <source>; live card <URL of the synced card>` and
   Last update today. Never delete one.
4. Set the join row to Done (Next step `none`, Detail = the two sync lines), commit that per the repo's rules, and run the sync
   once more after it lands, so the join card shows Done.

Exit codes: `2` = off (token missing, page not shared with the integration, an option missing, Notion unreachable; the reason
is in the `off (…)` line); `3` = the In flight table cannot be parsed (check the heading and the columns); `4` = bad flag. The
full table is in the skill's SKILL.md, "Running the sync". No git remote at all: links fall back to nothing, so put full URLs
in Detail, or pass `--repo-url https://github.com/<owner>/<repo>`.

## 10. Report to Jeff

Your final message gives: the Area and the Source, the cards created and the manual cards dropped (counts; titles only if this
repo is private), the sync lines, the In progress count per Owner across the board, anything still open (a PR to merge, a token
on another computer, files that use another name for him), and the vault commit id from step 0.

## After joining

- Every session follows the block from step 6: open, move and close cards through `handoff.md`, and run the sync once the change
  is on the default branch. There is no daily Routine for a local project. If Jeff wants one, a cloud Routine on this repo can
  run the same command with `NOTION_TOKEN` set and `api.notion.com` in its allowed domains.
- `python3 scripts/notion-sync.py --audit --source "<source>"` checks the policy across the board, read-only. It names only this
  repo's cards; every other card appears as a count.
- Jeff reviews the whole board on Mondays and tells a session what to change. You make the change.
