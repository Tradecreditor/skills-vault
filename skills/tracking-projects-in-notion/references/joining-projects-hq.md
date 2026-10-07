# Joining Projects HQ — for an agent working in another project

You are an agent (Claude Code, Codex, Gemini CLI or another) working in one of Jeff's projects, and Jeff asked you to put
this project on his kanban, **Projects HQ**. Follow the steps in order and stop wherever a step says stop.

What Jeff pastes into a session in the project:

```
Join this project to my Projects HQ kanban. Follow
https://raw.githubusercontent.com/Tradecreditor/skills-vault/main/skills/tracking-projects-in-notion/references/joining-projects-hq.md
step by step. My name is Jeff.
```

`<guide>` below means this guide pinned to the reviewed vault commit that step 0 prints:
`https://raw.githubusercontent.com/Tradecreditor/skills-vault/<commit id>/skills/tracking-projects-in-notion/references/joining-projects-hq.md`.

**Nothing is written into the project until Jeff has confirmed it (step 6).** Steps 1 to 5 only read and draft. If a session ends
before step 7, the next one simply starts again; options and tabs added to the board in step 3 are then this join's own.

## Resuming a join

A join can span several sessions: Jeff may set the token and restart the agent, or merge a PR first. Look for a **`Projects HQ
join`** row in `handoff.md` **as committed**, not in the working tree (other uncommitted edits are ordinary work):

- Run `git fetch` if there is a remote, then `git show <default>:handoff.md`, where `<default>` is `origin/main` (or the remote's
  default branch) or, with no remote, the local default branch. If it has the join row and the row is not Done, continue at the
  step the row's Next step names, reading the guide address in the row. Do not redo earlier steps.
- If only a feature branch or an open PR has the join row, the join waits for Jeff's merge: say so in one line, do not sync, and
  carry on with whatever else Jeff asked for.
- If no commit has the join row, start at step 0.
- If the step needs something this session lacks (`NOTION_TOKEN`, the Notion connector, Jeff's answer), say so in one line and
  carry on with whatever else Jeff asked for.

Jeff can resume on purpose with `claude --continue` / `codex resume --last`, or by pasting
"Resume the Projects HQ join: <the guide address in the join row>".

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
  through the Notion connector. Do steps 2 and 3, then step 10. No script, no handoff, no token. Without the Notion connector
  you cannot do any of it: stop and ask Jeff to paste the join request into a session that has the connector.
- **A git repository**: it becomes one **Area** on the board, and its `handoff.md` "In flight" table becomes its cards, which
  a script mirrors into Notion. Do every step. First find out two things:
  - **Whose repository is it?** Look at `git remote get-url origin` and the recent authors (`git log --format='%an' -50 | sort -u`).
    If it is not Jeff's own repository (a client's, an employer's, an open-source upstream), or other people commit to it,
    stop and ask Jeff before you write anything. Offer to track it as manual cards instead (steps 2–3 only).
  - **Is it public?** Use `gh repo view --json visibility` if `gh` works, otherwise ask Jeff. If you cannot tell, treat it as
    public. In a public repository its `handoff.md`, instruction files, commit messages, branch names, PR titles and
    descriptions and the Session log are all public.

## 2. Look at the board and pick the Area (Notion connector)

Find the page **Projects HQ** and its database **Project Status**. There is exactly one; never create another database or board.

1. Fetch the database's data source: its Area and Source options (names and colours), and the cards of any Area that could be
   this project.
2. **Area**: if an Area already names this project (manual cards were seeded for several projects), reuse it exactly as written.
   Otherwise a repo uses its repository name; a project without a repo asks Jeff for the name of its life or business area.
   Ask Jeff too when two Areas could both be this project.
3. **Source** (repo only): `<repo>/handoff.md`, where `<repo>` is the last path component of `git remote get-url origin`
   without `.git` (no `origin` remote: the folder name, or ask Jeff). If that Source option already exists, ask Jeff whether an
   earlier attempt at this join added it. If not, another repository with the same name owns it; the usual answer is
   `<owner>-<repo>` for both the Area and the Source (`<owner>-<repo>/handoff.md`), passed with `--area` and `--source`.
4. List this Area's **open** manual cards (Backlog, In progress, Waiting on Jeff, Blocked) with their Notion URL, Status, Owner,
   Priority, Next step and Target date. Done and Dropped manual cards stay as they are. Step 4 (repo) or step 3 (no repo)
   decides what happens to the open ones; the same work must never be tracked twice.
5. Count the In progress cards per Owner across the **whole board**. The WIP limits (Jeff 3, Claude Code 5) count every project
   together. Cards that already exist keep their Status. Only a workstream that was not on the board before starts in Backlog
   when In progress would push its Owner over the limit. Report the counts in step 10.

**A repo, but no Notion connector in this session?** Give Jeff this sentence, with `<project>` and `<repo>` filled in, to say in
any Claude session that has the connector:

> On Projects HQ (database Project Status): if an Area option already names `<project>`, tell me its exact name; otherwise add
> Area option `<repo>`. Add Source option `<repo>/handoff.md`; if it already exists, stop and tell me. To add an option, restate
> every existing option of that property with its exact name and colour, then check that nothing else changed. Add a Board tab
> for that Area, grouped by Status and filtered to it, only if it has none. List that Area's open manual cards (Notion URL,
> title, Status, Owner, Priority, Next step, Target date) and the In progress count per Owner across the board.

Then stop. When Jeff brings the answer back, resume at step 2.4 with it, skip step 3, and do the rest.

## 3. Prepare the board (Notion connector)

1. **Options.** The connector changes a select property's options only by restating the whole list
   (`ALTER COLUMN "Area" SET SELECT('opt':color, …)`), and an option left out is deleted from every card that uses it, which
   cannot be undone. So: take the full list from step 2.1, send every existing option with its exact name and colour plus the
   new one, then fetch the data source again and check that the count rose by exactly one and nothing was renamed or
   recoloured. Add the Area option if it is new, and for a repo the Source option. Never rename, recolour or remove an option.
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
| Workstream | one outcome, finishable in 2–6 weeks, as a stable noun phrase. It becomes the card title. **Renaming it later closes the card and opens a new one** |
| Status | Backlog, In progress, Waiting on Jeff, Blocked, Done or Dropped |
| Priority | P0 (urgent, this week), P1 (current focus), P2 (default), P3 (someday). A P0 needs a Target date, which has no column: it is recorded in the join row (below) and set on the synced card in step 9 |
| Owner | Jeff, Claude Code (any agent session) or Routine (a scheduled job) |
| State | the facts: what is merged, live or proven, and what is not yet |
| Next step | one concrete action that starts with a verb. Waiting on Jeff: starts `Jeff:` and names the decision. Blocked: names the blocker and what unblocks it. Done: `none`. Dropped: `Dropped: <reason>` |
| Detail | the evidence or the detail, as a full URL (PR, commit, report) or a file path in backticks. A Done row needs evidence. Backtick paths and `PR #<n>` become `https://github.com/<owner>/<repo>/blob/main/<path>` and `…/pull/<n>`, so if the default branch is not `main` or the remote is not on GitHub, write full URLs |

Draft the rows, in the chat:

- **The open manual cards from step 2.4 that are repo work** become rows, keeping their Status, Owner and Priority. In a
  **private** repo you may keep their titles. In a **public** repo never copy a manual card's title or details: write a new
  public-safe title. In every repo keep manual card titles out of commit messages, branch names and PR titles and descriptions.
  Manual cards that are not repo work stay manual.
- **New workstreams**: only ones that are clearly active (an open PR, recent commits toward one outcome). TODOs, issues and
  ideas go to Open loops, not In flight: every row becomes a card, and a card can be dropped but never removed.
- **The join row**, first in the table: Workstream `Projects HQ join`, Priority P2, Detail `<guide>`; Status, Owner and Next step
  are set in step 7. Its **State** records what step 9 needs later, without any manual card title:
  `Joining since <today YYYY-MM-DD>. Replaces manual cards: <id> -> "<row title>" (target <YYYY-MM-DD>); <id> -> "<row title>"; …. P0 targets: "<row title>" <YYYY-MM-DD>.`
  `<id>` is the 32-character id at the end of the old card's Notion URL (never the whole URL, whose readable part can contain
  the title). Write `Replaces manual cards: none` when there are none.
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
- Join: while handoff.md's "Projects HQ join" row is not Done, run the sync only as the guide linked in that row says (its step 9), and do the step the row names when you can; if it needs something you lack (NOTION_TOKEN, the connector, a merge, Jeff's answer), say so in one line and carry on with your task.
- Start: read handoff.md (and this Area's cards if you have the Notion connector). Once the join row is Done: on the default branch with NOTION_TOKEN set, run the sync once. Work only on something that has a card; open one first.
- Open: add a row to handoff.md "In flight" (| Workstream | Status | Priority | Owner | State | Next step | Detail |) in the same commit as the first piece of work. Keep the Workstream text stable: renaming it opens a new card.
- Move: change the row's Status / Owner / Next step in the same commit as the work. Waiting on Jeff: Next step starts "Jeff:" and names the decision. Blocked: name the blocker and what unblocks it.
- Close: Done only with evidence in Detail (merged, live, checked). Abandoned: Status Dropped, Next step "Dropped: <reason>". Never delete a card; follow-up work is a new row.
- End: update the rows you touched. Once the join row is Done and the change is on the default branch, run the sync. Name the cards you opened, moved or closed in your final message.
- Jeff only views the board; never ask him to edit it. Never edit a synced card in Notion, except its Target date (the sync never writes that field and overwrites all the others). Manual cards change only through the Notion connector, on Jeff's word.
```

## 6. Jeff confirms (repo only)

Every row will become a permanent card. Show Jeff, in the chat: the In flight rows (Workstream, Status, Priority, Owner, Next
step), which old manual card each row replaces (by its current title: the chat is private), the P0 Target dates, the files you
will write (`scripts/notion-sync.py`, `handoff.md`, and which instruction files get the block), and whether this repo lands
changes by PR or by direct push. Change what he asks for. Continue only when he agrees. If the session ends here, nothing was
written: the next one starts again.

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
   never deletes or archives anything, and writes only the cards whose Source is this repo's label. It does not update itself:
   copy it again only when Jeff asks, repeating step 0 first.
2. **Write `handoff.md`**. No handoff yet: create it from the checkout's `skills/keeping-handoff-docs/references/handoff-template.md`
   (Snapshot, In flight, Open loops, Recently done, Environment facts, Session log), filled from the repo and under about 150
   lines. A handoff already exists: keep everything and change only its In flight table. Either way: the heading is exactly
   `## In flight` (level 2, this capitalisation, at the start of a line) and the table is the first table under it, or the sync
   exits 3; set the `Last updated:` line to now (the sync never dates a card later than that line); add under "Environment
   facts" `notion-sync.py copied from skills-vault <commit id from step 0> (reviewed)`; append a Session log line.
3. **Set the join row** and the route:
   - **Pull requests here**: Status Waiting on Jeff, Owner Jeff, Next step `Jeff: merge the join PR; then a session on the
     default branch does step 9 of <guide>`.
   - **Direct pushes to the default branch**: Status In progress, Owner Claude Code, Next step `Run the first sync and the
     clean-up: step 9 of <guide>`. If Claude Code is already at its WIP limit, say so in step 10.
4. **Add the instruction block** from step 5 to the instruction files. Add to them; never rewrite what is already there.
5. **Commit** `scripts/notion-sync.py`, `handoff.md` and the instruction files together, following this repository's rules.
   Pull requests: open the PR and stop. Tell Jeff that the first sync and the clean-up happen after the merge, in any session on
   the default branch (the block sends it to step 9), and include the token steps if the check printed `missing`. Direct push:
   push, then step 8.

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
Jeff the steps below, then go to step 10 and stop; the join resumes at step 9 after the restart.

1. Open https://www.notion.so/profile/integrations, choose the integration that is connected to Projects HQ, and copy its
   Internal Integration Secret.
2. **Windows**: Start → "Edit environment variables for your account" → New… → Name `NOTION_TOKEN`, Value: paste the secret → OK.
   **macOS / Linux**: open your shell profile (`~/.zshrc` on macOS) in an editor and add the line
   `export NOTION_TOKEN='<the secret>'`. First make sure that file is not tracked by git: a profile symlinked into a dotfiles
   repository would publish the secret.
3. Fully restart the terminal and the agent so they see the variable, then resume the join (see "Resuming a join").

If the secret ever lands anywhere else (a chat, a log, a repository file, a handoff), do not use it. Tell Jeff to refresh it at
notion.so/profile/integrations (the integration → its secret's refresh option) and then update `NOTION_TOKEN` on the cloud
environment "Skills Management" and on every computer that has it, or the daily sync goes off.

## 9. First sync and clean-up (repo only, on the default branch)

Safe to re-enter. Work on an up-to-date checkout of the default branch, with the step-8 check printing `set`. "The Sync line"
is the command in the instruction block (with any `--repo-url`). Check the parts from the end:

- **Already finished** if the committed join row is Done, or an open PR already sets it to Done: nothing to do.
- **Clean-up already done** if Jeff has told you so, or (with the connector) every card listed in the join row's State as
  replaced is Dropped: go to 9.4.
- **First sync already ran** if the Area's tab or the dry run shows cards with this Source: go to 9.3 (the Sync line runs as
  routine there).

1. **Dry run**: the Sync line with `--dry-run`. It reads Notion and writes nothing; the summary is on stdout, the plan on stderr.
   On the first sync it should show `created=<number of rows on the default branch>` and nothing else (step 2.3 made sure no
   other repository uses this Source).
2. **Sync**: the Sync line, then once more. The second run must say `created=0` and `unchanged=<rows>`. A run that ends with
   exit 1 (some writes failed) is simply run again; it creates only the missing cards.
3. **Clean-up in Notion.** Run the Sync line once (routine). Then, with the connector: set each `P0 targets` date from the join
   row's State on its synced card, and for each `<id> -> "<row title>"` pair, copy the old card's Target date to the synced card
   with that title and Source, then set the old card (page `<id>`) to **Dropped**, in one edit with Next step
   `Dropped: moved to <source> as "<row title>"` and Last update today. Touch no other card; never delete one.
   **No connector in this session?** Give Jeff, in the chat, this sentence with the pairs filled in from the join row:
   *"On Projects HQ, Area `<area>`: for each pair below, copy the Target date of the old manual card (Notion page id) to the card
   titled "<row title>" with Source `<source>`, then set the old card to Dropped in one edit with Next step `Dropped: moved to
   <source> as "<row title>"` and Last update today. Also set these Target dates: <P0 targets>. Touch no other card. Pairs:
   <id> -> "<row title>"; …"* Set the join row to Status Waiting on Jeff, Owner Jeff, Next step `Jeff: paste the clean-up
   sentence into a session with the Notion connector, then tell a session here "clean-up done" (step 9 of <guide>)`, and commit
   it following this repository's rules. Stop here.
4. **Close the join row**: Status Done, Owner Claude Code, Next step `none`, State = the two sync lines from 9.2 and
   `clean-up done`, Detail = the full URL of the join commit or the merged join PR (the evidence the audit accepts; a bare sync
   line is not). Commit following this repository's rules (a PR repo: a PR whose description says it closes the Projects HQ
   join), and run the Sync line once more after it lands, so the join card shows Done.

Exit codes: `2` = off (token missing, page not shared with the integration, an option missing, Notion unreachable; the reason
is in the `off (…)` line); `3` = the In flight table cannot be parsed (check the heading and the columns); `4` = bad flag. The
full table is in the skill's SKILL.md, "Running the sync". A repo with no remote at all has no URLs for evidence: the weekly
audit flags its Done cards (`evidence`) until it is pushed to GitHub (a private repository is fine).

## 10. Report to Jeff

Your final message gives: the Area and the Source, the cards created and the manual cards dropped (counts; titles only if this
repo is private), the sync lines, the In progress count per Owner across the board, anything still open (a PR to merge, a
clean-up waiting for a connector session, a token to set, files that use another name for him), and the vault commit id from
step 0.

## After joining

- Every session follows the block from step 5: open, move and close cards through `handoff.md`, and run the sync once the change
  is on the default branch. There is no daily Routine for a local project. If Jeff wants one, a cloud Routine on this repo can
  run the same command with `NOTION_TOKEN` set and `api.notion.com` in its allowed domains.
- `python3 scripts/notion-sync.py --audit --source "<source>"` checks the policy across the board, read-only. It names only this
  repo's cards; every other card appears as a count.
- Jeff reviews the whole board on Mondays and tells a session what to change. You make the change.
