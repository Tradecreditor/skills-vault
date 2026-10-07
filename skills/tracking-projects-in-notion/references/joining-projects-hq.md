# Joining Projects HQ — for an agent working in another project

You are an agent working in one of Jeff's projects, and Jeff asked you to put this project on his kanban, **Projects HQ**.
Follow the steps in order and stop wherever a step says stop.

What Jeff pastes into a session in the project:

```
Join this project to my Projects HQ kanban. Follow
https://raw.githubusercontent.com/Tradecreditor/skills-vault/main/skills/tracking-projects-in-notion/references/joining-projects-hq.md
step by step. My name is Jeff.
```

`<guide>` below means this guide pinned to the reviewed vault commit that step 0 prints:
`https://raw.githubusercontent.com/Tradecreditor/skills-vault/<commit id>/skills/tracking-projects-in-notion/references/joining-projects-hq.md`.

**The join needs the Notion connector.** Steps 2, 3 and 9 read and change the board through it. Claude Code signed in with
Jeff's Claude account has it when Notion is connected there. Without it, stop at step 2 and ask Jeff to run the join in a session
that has it. After the join, any agent (Codex, Gemini CLI…) keeps this repo's cards current through `handoff.md` and the sync.

**Nothing is written into the project until Jeff has confirmed it (step 6).** Steps 1 to 5 only read and draft.

## Resuming a join

A join can span several sessions: Jeff may set the token and restart the agent, or merge a PR first. Decide from what is
**committed**, not from the working tree:

- Run `git fetch` if there is a remote, then `git show <default>:handoff.md`, where `<default>` is `origin/main` (or the remote's
  default branch) or, with no remote, the local default branch.
- It has a **`Projects HQ join`** row that is not Done: continue at the step its Next step names, reading the guide address in
  the row. Do not redo earlier steps.
- Only a feature branch or an open PR has the join row: the join waits for Jeff's merge. Say so in one line and carry on with
  whatever else Jeff asked for.
- The join row is Done, or gone while the instruction files already carry the Projects HQ block: this project has joined. Say so.
- No commit has the join row: start at step 0. If the working tree holds an uncommitted join row, block or
  `scripts/notion-sync.py` from an earlier attempt, show Jeff and, on his word, reuse them instead of adding second copies.
- A step needs something this session lacks (`NOTION_TOKEN`, the connector, Jeff's answer): say so in one line and carry on with
  whatever else Jeff asked for.

Jeff can resume on purpose with `claude --continue`, or by pasting "Resume the Projects HQ join: <the guide address in the join
row>".

## Ground rules

- **Read the board policy before step 2**:
  https://github.com/Tradecreditor/skills-vault/blob/main/skills/tracking-projects-in-notion/references/board-policy.md
  (columns, fields, Definition of Done, P0–P3, WIP limits). Where it says Jeff decides Areas or options, a session makes the
  change on his word, and his request to join is that word.
- **Jeff only views the board; he never edits it.** You make every change. Never ask him to drag, edit or create a card.
- **Never delete a card.** A card that should not exist goes to Dropped with a reason.
- **Never print, echo, paste or commit `NOTION_TOKEN`** (step 8).
- **His name is Jeff** in everything you write for this join: handoff rows, Owner `Jeff`, `Waiting on Jeff`, `Jeff:` next steps,
  the instruction block. Do not rename him anywhere else (LICENSE, legal or user-facing text, emails, handles, code, git config).
  If you see another name or spelling for him there, list the files for Jeff instead.
- **Do not edit the skills-vault repository** from here. If the vault needs a change, tell Jeff.
- **Python**: in this guide `python3` means `python3` on macOS and Linux and `py -3` on Windows. On Windows `python3` is usually
  the Microsoft Store stub, which prints "Python was not found". Check first: `py -3 --version` or `python3 --version`. If
  neither prints a version, Python is missing; tell Jeff.
- **Shell variables do not survive between commands** in most agents. Where a step prints a path, note it and type it in full
  in later commands.
- **Write files as UTF-8.** Use your file tool; in PowerShell 5.1, `Set-Content`, `Out-File` and `>` write ANSI or UTF-16 unless
  given `-Encoding utf8`.

## 0. Check the skill's review

**No repository**: this kind of join runs no vault code. Open
https://raw.githubusercontent.com/Tradecreditor/skills-vault/main/skills/tracking-projects-in-notion/SKILL.md and continue to
step 1 only if its `vault_status` line says `reviewer-approved` or `verified`; otherwise stop and tell Jeff.

**A repository**: other projects may run code only from a vault skill that passed review, and only the files as reviewed.
Check on one checkout made outside this repository, in two parts.

**0a. Clone and read the status lines; this runs no vault code.** Run your shell's block as one command and note the last two
lines it prints: the checkout's path and its commit id.

```
# Git Bash / macOS / Linux
VAULT="$(mktemp -d)/skills-vault" && git clone -q --depth 1 -c core.autocrlf=false https://github.com/Tradecreditor/skills-vault "$VAULT" && grep -H -E '^  (vault_status|review_hash):' "$VAULT/skills/auditing-agent-skills/SKILL.md" "$VAULT/skills/tracking-projects-in-notion/SKILL.md"; echo "$VAULT"; git -C "$VAULT" rev-parse --short HEAD

# Windows PowerShell
$VAULT = Join-Path $env:TEMP ("skills-vault-" + (Get-Random)); git clone -q --depth 1 -c core.autocrlf=false https://github.com/Tradecreditor/skills-vault $VAULT; Select-String -Path "$VAULT\skills\auditing-agent-skills\SKILL.md", "$VAULT\skills\tracking-projects-in-notion\SKILL.md" -Pattern '^  (vault_status|review_hash):'; $VAULT; git -C $VAULT rev-parse --short HEAD
```

Continue only if **both** skills show `reviewer-approved` or `verified` and a `review_hash`. Otherwise stop and tell Jeff.

**0b. Compare the hashes.** The scanner belongs to `auditing-agent-skills`, so hash that skill first, then this one (put the
path from 0a in place of `<path>`):

```
# Git Bash / macOS / Linux
for s in auditing-agent-skills tracking-projects-in-notion; do echo "$s $(python3 -I '<path>/skills/auditing-agent-skills/scripts/static_scan.py' --hash "<path>/skills/$s")"; done

# Windows PowerShell
foreach ($s in 'auditing-agent-skills', 'tracking-projects-in-notion') { "$s " + (py -3 -I '<path>\skills\auditing-agent-skills\scripts\static_scan.py' --hash "<path>\skills\$s") }
```

Continue only if each printed hash equals that skill's `review_hash` from 0a. Otherwise stop and tell Jeff: the files changed
after the review and the next review has not run yet. (The scanner hashes itself, so this catches a draft or an edited skill;
only Jeff's own account can push to the vault's `main`, and the daily review resets any approved skill whose files changed.)
Whenever the script is copied again later, repeat step 0 first.

## 1. What kind of project is this?

- **No repository** (job hunt, admin, a client relationship): its cards are **manual** (Source `manual`), created and moved
  through the Notion connector. Do steps 2 and 3, then step 10. No script, no handoff, no token.
- **A git repository**: it becomes one **Area** on the board, and its `handoff.md` "In flight" table becomes its cards, which
  a script mirrors into Notion. Do every step. First find out two things:
  - **Whose repository is it?** Look at `git remote get-url origin` and the recent authors (`git log --format='%an' -50 | sort -u`).
    If it is not Jeff's own repository (a client's, an employer's, an open-source upstream), or other people commit to it,
    stop and ask Jeff before you write anything. Offer to track it as manual cards instead (steps 2–3 only).
  - **Is it public?** Use `gh repo view --json visibility` if `gh` works, otherwise ask Jeff. If you cannot tell, treat it as
    public. In a public repository its `handoff.md`, instruction files, commit messages, branch names, PR titles and
    descriptions and the Session log are all public.

## 2. Look at the board and pick the Area (Notion connector)

No connector in this session: stop and ask Jeff to start the join in a session that has it.

Find the page **Projects HQ** and its database **Project Status**. There is exactly one; never create another database or board.

1. Fetch the database's data source: its Area and Source options (names and colours), and the cards of any Area that could be
   this project.
2. **Area**: if an Area already names this project (manual cards were seeded for several projects), reuse it exactly as written.
   Otherwise a repo uses its repository name; a project without a repo asks Jeff for the name of its life or business area.
   Ask Jeff too when two Areas could both be this project.
3. **Source** (repo only): `<repo>/handoff.md`, where `<repo>` is the last path component of `git remote get-url origin`
   without `.git` (no `origin` remote: the folder name, or ask Jeff). If that Source option exists, query the cards with that
   Source. None: the option is unused (an earlier attempt at this join added it); reuse it. Some: another repository owns it;
   use `<owner>-<repo>` for both the Area and the Source (`<owner>-<repo>/handoff.md`), passed with `--area` and `--source`.
4. List this Area's **open** manual cards (Backlog, In progress, Waiting on Jeff, Blocked) with their Notion URL, Status, Owner,
   Priority, Next step and Target date. Done and Dropped manual cards stay as they are. Step 4 (repo) or step 3 (no repo)
   decides what happens to the open ones; the same work must never be tracked twice.
5. Count the In progress cards per Owner across the **whole board**. The WIP limits (Jeff 3, Claude Code 5) count every project
   together. Cards that already exist keep their Status. Only a workstream that was not on the board before starts in Backlog
   when In progress would push its Owner over the limit. Report the counts in step 10.

## 3. Prepare the board (Notion connector)

1. **Options.** The connector changes a select property's options only by restating the whole list
   (`ALTER COLUMN "Area" SET SELECT('opt':color, …)`), and an option left out is deleted from every card that uses it, which
   cannot be undone. So: take the full list from step 2.1, send every existing option with its exact name and colour plus the
   new one, then fetch the data source again and check that the count rose by exactly one and nothing was renamed or
   recoloured. Add the Area option if it is new, and for a repo the Source option if it is new. Never rename, recolour or
   remove an option.
2. If the database has no Board view named after the Area yet, add one: a **Board** view of Project Status,
   `GROUP BY "Status"; FILTER "Area" = "<area>"`. A view of the one database, never a new database. An Area that was seeded
   earlier usually has its tab already; leave it alone.
3. **No repo**: show Jeff the Area's open manual cards and ask which workstreams he wants on the board (title, Status, Owner,
   Next step, Priority and any deadline). Create only the cards that do not exist yet, with every required field (policy
   section 3), Last update today and Source `manual`. Never invent workstreams. If the project has a local folder, add this
   block to the instruction file of every agent that works there (`CLAUDE.md` for Claude Code, `AGENTS.md` for Codex,
   `GEMINI.md` for Gemini CLI), creating your own agent's file if it is missing:

   ```
   ## Projects HQ (Jeff's kanban for every project)
   This project's cards: Area "<area>", Source manual, on the private Notion board Projects HQ (database Project Status). Change them only through the Notion connector, on Jeff's word.
   Policy: https://github.com/Tradecreditor/skills-vault/blob/main/skills/tracking-projects-in-notion/references/board-policy.md
   - Columns: Backlog, In progress, Waiting on Jeff, Blocked, Done, Dropped. Priority P0-P3 (P2 default; P0 needs a Target date). WIP limit for In progress, counted across the whole board: Jeff 3, Claude Code 5.
   - Start: read this Area's cards. Work only on something that has a card; open one first (every required field, Source manual).
   - Move: every move updates Next step and Last update in the same edit. Waiting on Jeff: Next step starts "Jeff:" and names the decision. Blocked: name the blocker and what unblocks it.
   - Close: Done only with Link = the evidence. Abandoned: Status Dropped, Next step "Dropped: <reason>". Never delete a card.
   - End: name the cards you opened, moved or closed in your final message. Jeff only views the board; never ask him to edit it.
   ```

   Then go to step 10.

The sync script never changes the schema. It stops with exit 2 naming any option it needs that does not exist yet, before it
writes anything, so a typo in the Area or the Source cannot create stray cards.

## 4. Draft the In flight rows (repo only; do not write yet)

The repo's `handoff.md` gets an In flight table with exactly these columns:

```
| Workstream | Status | Priority | Owner | State | Next step | Detail |
|---|---|---|---|---|---|---|
```

| Column | What goes in it |
|---|---|
| Workstream | one outcome, finishable in 2–6 weeks, as a stable noun phrase. **It is the card title, and renaming it later closes the card and opens a new one.** The sync strips links, `**` and backticks and drops one trailing ` (…)` group, so write titles with no formatting and no trailing parenthetical, and no two alike |
| Status | Backlog, In progress, Waiting on Jeff, Blocked, Done or Dropped |
| Priority | P0 (urgent, this week), P1 (current focus), P2 (default), P3 (someday). A P0 needs a Target date, which has no column: it is recorded in the join row (below) and set on the synced card in step 9 |
| Owner | Jeff, Claude Code (any agent session) or Routine (a scheduled job) |
| State | the facts: what is merged, live or proven, and what is not yet |
| Next step | one concrete action that starts with a verb. Waiting on Jeff: starts `Jeff:` and names the decision. Blocked: names the blocker and what unblocks it. Done: `none`. Dropped: `Dropped: <reason>` |
| Detail | the evidence or the detail, as a full URL (PR, commit, report) or a file path in backticks. A Done row needs evidence. Backtick paths and `PR #<n>` become `https://github.com/<owner>/<repo>/blob/main/<path>` and `…/pull/<n>`, so if the default branch is not `main` or the remote is not on GitHub, write full URLs |

Draft the rows, in the chat:

- **The open manual cards from step 2.4 that are repo work** become rows, keeping their Status, Owner and Priority. In a
  **private** repo you may keep their titles (adjusted to the Workstream rule). In a **public** repo never copy a manual card's
  title or details: write a new public-safe title. In every repo keep manual card titles out of commit messages, branch names
  and PR titles and descriptions. Manual cards that are not repo work stay manual.
- **New workstreams**: only ones that are clearly active (an open PR, recent commits toward one outcome). TODOs, issues and
  ideas go to Open loops, not In flight: every row becomes a card, and a card can be dropped but never removed.
- **The join row**, first in the table: Workstream `Projects HQ join`, Priority P2, Detail `<guide>`; Status, Owner and Next step
  are set in step 7. Its **State** records what step 9 needs, without any manual card title:
  `Joining since <today YYYY-MM-DD>. Replaces manual cards: <id> -> "<row title>"; <id> -> "<row title>"; …. Target dates: "<row title>" <YYYY-MM-DD>; ….`
  `<id>` is the 32-character id at the end of the old card's Notion URL (never the whole URL, whose readable part can contain
  the title). Target dates are the old cards' dates and the P0 dates Jeff gives in step 6. Write `none` for an empty list.
- Task-level tracking (Backlog.md, GitHub issues, Linear) stays where it is. A card is a workstream, not a task.

## 5. Draft the instruction block (repo only; do not write yet)

The block goes into the instruction file of every agent that works in this project (`CLAUDE.md` for Claude Code, `AGENTS.md` for
Codex, `GEMINI.md` for Gemini CLI; create your own agent's file if it is missing), with `<area>` and `<source>` filled in. If the
repo has no `origin` remote on GitHub, append `--repo-url "https://github.com/<owner>/<repo>"` to the Sync line, or write full
URLs in Detail. If `handoff.md` is new, the files also get `handoff.md` in their read-first list and the rule "update
`handoff.md` before ending a session that changed state; append one line to its Session log".

```
## Projects HQ (Jeff's kanban for every project)
Board: private Notion page Projects HQ, database Project Status. This repo's cards: Area "<area>", Source "<source>".
Policy: https://github.com/Tradecreditor/skills-vault/blob/main/skills/tracking-projects-in-notion/references/board-policy.md
Sync: python3 scripts/notion-sync.py --area "<area>" --source "<source>"   (Windows: py -3; needs NOTION_TOKEN; never print it)
- Columns: Backlog, In progress, Waiting on Jeff, Blocked, Done, Dropped. Priority P0-P3 (P2 default). WIP limit for In progress, counted across the whole board: Jeff 3, Claude Code 5.
- Syncing: on the default branch with NOTION_TOKEN set, run the Sync line. Exception: while In flight has a "Projects HQ join" row that is not Done, run it with --dry-run first; if that shows unchanged=0 and updated=0, the first sync has not happened yet and belongs to the join (below): do not sync.
- Join: while In flight has a "Projects HQ join" row that is not Done, do the step it names when you can (the row links the guide); if that needs something you lack (the Notion connector, NOTION_TOKEN, a merge, Jeff's answer), say so in one line and carry on with your task.
- Start: read handoff.md (and this Area's cards if you have the Notion connector), then sync. Work only on something that has a card; open one first.
- Open: add a row to handoff.md "In flight" (| Workstream | Status | Priority | Owner | State | Next step | Detail |) in the same commit as the first piece of work. Keep the Workstream text stable: renaming it opens a new card.
- Move: change the row's Status / Owner / Next step in the same commit as the work. Waiting on Jeff: Next step starts "Jeff:" and names the decision. Blocked: name the blocker and what unblocks it.
- Close: Done only with evidence in Detail (merged, live, checked). Abandoned: Status Dropped, Next step "Dropped: <reason>". Never delete a card; follow-up work is a new row.
- Every commit that changes a row also sets handoff.md's "Last updated:" line to now (the sync never dates a card later than it).
- End: update the rows you touched. Once the change is on the default branch, sync. Name the cards you opened, moved or closed in your final message.
- Jeff only views the board; never ask him to edit it. Never edit a synced card in Notion, except its Target date (the sync never writes that field and overwrites all the others). Manual cards change only through the Notion connector, on Jeff's word.
```

## 6. Jeff confirms (repo only)

Every row will become a permanent card. Show Jeff, in the chat: the In flight rows (Workstream, Status, Priority, Owner, Next
step), which old manual card each row replaces (by its current title: the chat is private), the Target dates (ask him for any P0
that has none), the files you will write (`scripts/notion-sync.py`, `handoff.md`, and which instruction files get the block), and
whether this repo lands changes by PR or by direct push. Change what he asks for. Continue only when he agrees. If the session
ends here, nothing was written: the next one starts again.

## 7. Write and commit (repo only)

Run the step-8 check now, so Jeff hears about a missing token while he is here. Then:

1. **Copy the script from the step-0 checkout**, never from a second download. It must sit directly in `<repo>/scripts/`,
   because it finds the repo root, `handoff.md` and the git remote from its own location. If `scripts/notion-sync.py` already
   exists and its docstring does not start with `notion-sync.py - one-way mirror of handoff.md`, it is a different file: stop
   and ask Jeff.

   ```
   # Git Bash / macOS / Linux  (put the path step 0 printed in place of <path>)
   mkdir -p scripts && cp '<path>/skills/tracking-projects-in-notion/scripts/notion-sync.py' scripts/notion-sync.py

   # Windows PowerShell
   New-Item -ItemType Directory -Force scripts | Out-Null; Copy-Item '<path>\skills\tracking-projects-in-notion\scripts\notion-sync.py' scripts\notion-sync.py
   ```

   It is a single Python 3.9+ file that uses only the standard library. It sends `NOTION_TOKEN` only to `https://api.notion.com`,
   never deletes or archives anything, and writes only the cards whose Source is this repo's label. Commit it byte for byte: if
   a formatter or linter hook changes it, exclude `scripts/notion-sync.py` from that hook instead of accepting the change. It
   does not update itself: copy it again only when Jeff asks, repeating step 0 first.
2. **Write `handoff.md`**. No handoff yet: create it from the checkout's `skills/keeping-handoff-docs/references/handoff-template.md`
   (Snapshot, In flight, Open loops, Recently done, Environment facts, Session log), filled from the repo and under about 150
   lines. A handoff already exists: keep everything and change only its In flight table. Either way: the heading is exactly
   `## In flight` (level 2, this capitalisation, at the start of a line) and the table is the first table under it, or the sync
   exits 3; set the `Last updated:` line to now; add under "Environment facts" `notion-sync.py copied from skills-vault <commit
   id from step 0> (reviewed)`; append a Session log line.
3. **Set the join row** and the route:
   - **Pull requests here**: Status Waiting on Jeff, Owner Jeff, Next step `Jeff: merge the join PR; then a session with the
     Notion connector on the default branch does step 9 of <guide>`.
   - **Direct pushes to the default branch**: Status In progress, Owner Claude Code, Next step `Run the first sync and the
     clean-up: step 9 of <guide>`. If Claude Code is already at its WIP limit, say so in step 10.
4. **Add the instruction block** from step 5 to the instruction files. Add to them; never rewrite what is already there.
5. **Commit** `scripts/notion-sync.py`, `handoff.md` and the instruction files together, following this repository's rules.
   Pull requests: open the PR, tell Jeff the first sync and the clean-up happen after the merge in a session with the Notion
   connector on the default branch (the block sends it there), include the token steps if the check printed `missing`, and stop
   the join. Direct push: push, then step 8.

## 8. NOTION_TOKEN on this computer (Jeff, once per computer)

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

When this check runs at the start of step 7, note the result and go back to step 7. Otherwise: `set` → step 9. `missing` → give
Jeff the steps below, then go to step 10 and stop the join; it resumes at step 9 after the restart.

1. Open https://www.notion.so/profile/integrations, choose the integration that is connected to Projects HQ, and copy its
   Internal Integration Secret.
2. **Windows**: Start → "Edit environment variables for your account" → New… → Name `NOTION_TOKEN`, Value: paste the secret → OK.
   **macOS / Linux**: open your shell profile (`~/.zshrc` on macOS) in an editor and add the line
   `export NOTION_TOKEN='<the secret>'`. First make sure that file is not tracked by git: a profile symlinked into a dotfiles
   repository would publish the secret.
3. Fully restart the terminal and the agent so they see the variable, then resume the join (see "Resuming a join"). On macOS an
   agent started from the Dock or an editor may not read the shell profile: start it from a terminal.

If the secret ever lands anywhere else (a chat, a log, a repository file, a handoff), do not use it. Tell Jeff to refresh it at
notion.so/profile/integrations (the integration → its secret's refresh option) and then update `NOTION_TOKEN` on the cloud
environment "Skills Management" and on every computer that has it, or the daily sync goes off.

## 9. First sync and clean-up (repo only; default branch; Notion connector)

Work on an up-to-date checkout of the default branch, with the connector and with the step-8 check printing `set`; without
either, say so in one line and carry on with whatever else Jeff asked for. "The Sync line" is the command in the instruction
block (with any `--repo-url`). This step is safe to re-enter. If an open PR already closes the join row (its description says
so), the join is finished apart from the merge: say so in one line and carry on.

1. **Check the old cards first.** For each `<id>` in the join row's State, fetch the card. One that is no longer open (Done or
   Dropped since the join was drafted): leave it alone, and update its row to match (Done with that card's Link as evidence, or
   Dropped with its reason) in the 9.4 commit. Note any other change (Status, Owner, Next step) for the same commit.
2. **Dry run**: the Sync line with `--dry-run`. It reads Notion and writes nothing; the summary is on stdout, the plan on stderr.
   - `created=<number of rows>` and nothing else: the first sync is due; go to 9.3.
   - `created=0`, or any `unchanged` or `updated` (this repo's cards exist): the first sync already ran; run the Sync line once
     and go to 9.4.
   - stderr says `duplicate project`, or `created` is neither of those: two rows share a title, or some cards are missing. Fix
     the rows (or re-run after a partly failed run, which creates only the missing cards); stop if it does not add up.
   - Every card with this Source must have Area `<area>`; if not, stop and tell Jeff (another repository shares this Source).
3. **First sync**: the Sync line, then once more. The second run must say `created=0` and `unchanged=<rows>`. Keep the two sync
   lines for 9.5.
4. **Clean-up in Notion.** Done already when each card in State's `Replaces manual cards` list is Dropped (or was closed, 9.1)
   and each card in `Target dates` has its date. Otherwise: set each `Target dates` entry on the synced card with that title
   and Source; then set each old card that is still open (page `<id>`) to **Dropped**, in one edit with Next step
   `Dropped: moved to <source> as "<row title>"` and Last update today. Touch no other card; never delete one.
5. **Close the join row**: Status Done, Owner Claude Code, Next step `none`, State = the latest two sync lines (run the Sync line
   now if you have none) and `clean-up done`, Detail = the full URL of the join commit or the merged join PR (the evidence the
   audit accepts; a bare sync line is not). Apply the row updates from 9.1, set `Last updated:` to now, and commit following
   this repository's rules (a PR repo: a PR whose description says it closes the Projects HQ join). Run the Sync line once more
   after it lands, so the join card shows Done.

Exit codes: `2` = off (token missing, page not shared with the integration, an option missing, Notion unreachable; the reason
is in the `off (…)` line); `3` = `handoff.md` cannot be parsed (the heading, the columns, or a file that is not UTF-8); `4` = bad
flag. The full table is in the skill's SKILL.md, "Running the sync". A repo with no remote at all has no URLs for evidence: the
weekly audit flags its Done cards (`evidence`) until it is pushed to GitHub (a private repository is fine).

## 10. Report to Jeff

Your final message gives: the Area and the Source, the cards created and the manual cards dropped (counts; titles only if this
repo is private), the sync lines, the In progress count per Owner across the board, anything still open (a PR to merge, a token
to set, files that use another name for him), and the vault commit id from step 0.

## After joining

- Every session follows the block from step 5: open, move and close cards through `handoff.md`, and sync once the change is on
  the default branch. There is no daily Routine for a local project. If Jeff wants one, a cloud Routine on this repo can run the
  same command with `NOTION_TOKEN` set and `api.notion.com` in its allowed domains.
- `python3 scripts/notion-sync.py --audit --source "<source>"` checks the policy across the board, read-only. It names only this
  repo's cards; every other card appears as a count.
- Jeff reviews the whole board on Mondays and tells a session what to change. You make the change.
