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

**The join needs the Notion connector** (steps 2, 3, 7 and 9). Claude Code signed in with Jeff's Claude account has it when
Notion is connected there. Without it, stop at step 2 and ask Jeff to run the join in a session that has it. After the join, any
agent (Codex, Gemini CLI…) keeps a repo's cards current through `handoff.md` and the sync.

**Nothing is written into the project, and no card is created, until Jeff has confirmed it (step 6).** Steps 1 to 5 read and
draft; the only writes before that are step 3's Area and Source options and Board tab. From the end of step 7 on, the join is
tracked on the board itself, by one manual card titled `Projects HQ join: <source>` in this project's Area. Its Next step always
says what comes next, and its private page body records the confirmed plan and what the clean-up needs. It is moved through the
connector, so no commit is needed to advance or close the join.

## Resuming a join

With the connector, look for a card titled `Projects HQ join: <repo>/handoff.md` or `Projects HQ join: <owner>-<repo>/handoff.md`
(the Source this repository uses; see step 2.3), whose page body names this repository:

- **Open**: continue at the step its Next step names, reading the guide address in its Link. Do not redo earlier steps. If its
  Next step names step 7: when the working tree holds the join's files, show Jeff and reuse them instead of adding second
  copies; when it does not, redo step 0 (a new checkout; put the new `<guide>` in the card's Link), show Jeff the plan from the
  card's page body, and write the files only on his yes. Never create a second join card.
- **Done**: the project has joined. Say so.
- **Dropped**: tell Jeff and wait for his word. Never restart at step 0 while cards with this repo's Source exist.
- **None**: start at step 0. (Cards with this repo's Source but no join card: tell Jeff instead.)

Without the connector, say in one line that the join needs a session with it, and carry on with whatever else Jeff asked for.
Jeff can resume on purpose with `claude --continue`, or by pasting "Resume the Projects HQ join: `<guide>`".

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
- **Files are UTF-8.** Use your file tools. In PowerShell 5.1 pass `-Encoding utf8` to `Get-Content`, `Set-Content` and
  `Out-File`, and never use `>`; otherwise dashes and non-English text are garbled, and garbled titles become card titles.

## 0. Check the skill's review

**No repository**: this kind of join runs no vault code. Open
https://raw.githubusercontent.com/Tradecreditor/skills-vault/main/skills/tracking-projects-in-notion/SKILL.md and continue to
step 1 only if its `vault_status` line says `reviewer-approved` or `verified`; otherwise stop and tell Jeff. Use the main-branch
address of this guide as `<guide>`.

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
  through the Notion connector. Do steps 2 and 3, then step 10. No script, no handoff, no token, no join card.
- **A git repository without a GitHub remote**: card evidence needs URLs. Ask Jeff to push it to GitHub first (a private
  repository is fine), or track it as manual cards (steps 2–3 only).
- **A git repository**: it becomes one **Area** on the board, and its `handoff.md` "In flight" table becomes its cards, which
  a script mirrors into Notion. Do every step. First find out two things:
  - **Whose repository is it?** Look at `git remote get-url origin` and the recent authors (`git log --format='%an' -50 | sort -u`).
    If it is not Jeff's own repository (a client's, an employer's, an open-source upstream), or other people commit to it,
    stop and ask Jeff before you write anything. Offer to track it as manual cards instead (steps 2–3 only).
  - **Is it public?** Use `gh repo view --json visibility` if `gh` works, otherwise ask Jeff. If you cannot tell, treat it as
    public. In a public repository its `handoff.md`, instruction files, commit messages, branch names, PR titles and
    descriptions and the Session log are all public; the Notion board is private.

## 2. Look at the board and pick the Area (Notion connector)

No connector in this session: stop and ask Jeff to start the join in a session that has it.

Find the page **Projects HQ** and its database **Project Status**. There is exactly one; never create another database or board.

1. Fetch the database's data source: its Area and Source options (names and colours), and the cards of any Area that could be
   this project.
2. **Area**: if an Area already names this project (manual cards were seeded for several projects), reuse it exactly as written,
   unless it already holds another repository's synced cards or join card; then use `<owner>-<repo>`.
   Otherwise a repo uses its repository name; a project without a repo asks Jeff for the name of its life or business area.
   Ask Jeff too when two Areas could both be this project.
3. **Source** (repo only): `<repo>/handoff.md`, where `<repo>` is the last path component of `git remote get-url origin`
   without `.git` (no `origin` remote: the folder name, or ask Jeff). Another repository owns that Source if any card has it, or
   if a `Projects HQ join: <repo>/handoff.md` card exists whose page body names a different repository; then use
   `<owner>-<repo>` for both the Area and the Source (`<owner>-<repo>/handoff.md`), passed with `--area` and `--source`.
   Otherwise an existing option is unused (an earlier attempt at this join added it): reuse it.
4. List this Area's **open** manual cards (Backlog, In progress, Waiting on Jeff, Blocked) with their Notion URL, Status, Owner,
   Priority, Next step and Target date; if step 2.2 moved off an Area that names this project, list that Area's open manual
   cards too, so step 6 can show Jeff which of them are this repository's work. Done and Dropped manual cards stay as they are. Step 4 (repo) or step 3 (no repo)
   decides what happens to the open ones; the same work must never be tracked twice.
5. Count the In progress cards per Owner across the **whole board**. The WIP limits (Jeff 3, Claude Code 5) count every project
   together. Cards that already exist keep their Status. Only a workstream that was not on the board before starts in Backlog
   when In progress would push its Owner over the limit. Report the counts in step 10.

## 3. Prepare the board (Notion connector)

1. **Options.** The connector changes a select property's options only by restating the whole list
   (`ALTER COLUMN "Area" SET SELECT('opt':color, …)`), and an option left out is deleted from every card that uses it, which
   cannot be undone. So, for each option to add: fetch the data source again right before the change (never reuse the step-2.1
   list, which another session may have changed since), send every option of that fresh list with its exact name and colour
   plus the new one, then fetch once more and check that every option of the fresh list is still there unchanged and the new one
   is present. If anything disappeared, stop and tell Jeff. Add the Area option if it is new, and for a repo the Source option
   if it is new. Never rename, recolour or remove an option. When several projects join at once, do step 3 in one session at a
   time.
2. If the database has no Board view named after the Area yet, add one: a **Board** view of Project Status,
   `GROUP BY "Status"; FILTER "Area" = "<area>"`. A view of the one database, never a new database. An Area that was seeded
   earlier usually has its tab already; leave it alone.
3. **No repo**: show Jeff the Area's open manual cards and ask which workstreams he wants on the board (title, Status, Owner,
   Next step, Priority and any deadline). Create only the cards that do not exist yet, with every required field (policy
   section 3), Last update today and Source `manual`. Never invent workstreams. If the project has a local folder, show Jeff
   this block and, on his yes, add it to the instruction file of every agent that works there (`CLAUDE.md` for Claude Code, `AGENTS.md` for Codex,
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
   - Without the Notion connector: say so in one line, do the task, and end your message with the card changes for a session with the connector to make. Never record cards anywhere else.
   ```

   For a repository that is not Jeff's own (step 1), write nothing into it unless Jeff asks; if he wants the block there, put it
   in an untracked local file (for example `CLAUDE.local.md`, or a file listed in `.git/info/exclude`). Then go to step 10.

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
| Priority | P0 (urgent, this week), P1 (current focus), P2 (default), P3 (someday). A P0 needs a Target date, which has no column: it is set on the synced card in step 9 |
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
- Start: read handoff.md (and this Area's cards if you have the Notion connector). On the default branch with NOTION_TOKEN set, run the Sync line. With the connector, if the board has an open "Projects HQ join: <source>" card, finish it as its Next step says. Work only on something that has a card; open one first.
- Open: add a row to handoff.md "In flight" (| Workstream | Status | Priority | Owner | State | Next step | Detail |) in the same commit as the first piece of work. Keep the Workstream text stable: renaming it opens a new card.
- Move: change the row's Status / Owner / Next step in the same commit as the work. Waiting on Jeff: Next step starts "Jeff:" and names the decision. Blocked: name the blocker and what unblocks it.
- Close: Done only with evidence in Detail (merged, live, checked). Abandoned: Status Dropped, Next step "Dropped: <reason>". Never delete a card; follow-up work is a new row.
- Every commit that changes a row also sets handoff.md's "Last updated:" line to now (the sync never dates a card later than it).
- End: update the rows you touched. Once the change is on the default branch, run the Sync line. Name the cards you opened, moved or closed in your final message.
- Jeff only views the board; never ask him to edit it. Never edit a synced card in Notion, except its Target date (the sync never writes that field and overwrites all the others). Manual cards change only through the Notion connector, on Jeff's word.
```

## 6. Jeff confirms (repo only)

Every row will become a permanent card. Show Jeff, in the chat: the In flight rows (Workstream, Status, Priority, Owner, Next
step), which old manual card each row replaces (by its current title: the chat is private), the Target date for each P0 (ask
him for any that has none), the files you will write (`scripts/notion-sync.py`, `handoff.md`, and which instruction files get
the block), and whether this repo lands changes by PR or by direct push. Change what he asks for. Continue only when he agrees.
If the session ends here, nothing was written: the next one starts again.

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
3. **Add the instruction block** from step 5 to the instruction files. Add to them; never rewrite what is already there.
4. **Create the join card** in Notion, or reuse the open one that "Resuming a join" found (never a second): Source `manual`,
   Area `<area>`, Project `Projects HQ join: <source>`, Priority P2, Link `<guide>`, Last update today, Status In progress, Owner
   Claude Code, Next step `Commit the join (step 7 of <guide>)`; if Claude Code is at its WIP limit, say so in step 10. Its page
   body is private and records the repository (its remote URL) and the plan Jeff confirmed in step 6: the rows (all seven columns), the Source, the instruction
   files, PR or direct push, the step-0 commit id, and what step 9 needs: for each row that replaces a manual card,
   `<old card URL> → "<row title>"`, and the Target dates. Whenever the rows change before step 9 (for example Jeff asks for a
   change in the PR), update the page body in the same session.
5. **Commit** `scripts/notion-sync.py`, `handoff.md` and the instruction files together, following this repository's rules.
   - **Pull requests**: open the PR, then set the join card to Waiting on Jeff, Owner Jeff, Next step `Jeff: merge the join PR
     (<PR URL>); the next session here with the Notion connector then finishes the join (step 9 of <guide>)`, adding `and set
     NOTION_TOKEN on this computer (step 8)` if the check printed `missing`. Tell Jeff the same (with steps 1–3 of step 8 if the
     token is missing) and stop the join.
   - **Direct push**: push, set the join card's Next step to `First sync and clean-up (step 9 of <guide>)`, then step 8.

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

When this check runs at the start of step 7, note the result and go back to step 7. Otherwise: `set` → step 9. `missing` → set
the join card to Waiting on Jeff, Owner Jeff, Next step `Jeff: set NOTION_TOKEN on this computer and restart the agent (step 8
of <guide>); then step 9`, give Jeff the steps below, then go to step 10 and stop the join; it resumes at step 9 after the
restart.

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

## 9. First sync, clean-up and close (repo only; default branch; Notion connector)

Work on an up-to-date checkout of the default branch that contains the join (the pushed join commit, or the join PR merged in
any way), with the connector, and with the step-8 check printing `set`. Without the connector, say so in one line and carry on
with whatever else Jeff asked for. With the connector but without one of the others, set the join card to Waiting on Jeff,
Owner Jeff, with a `Jeff:` Next step naming what is missing: the merge (`<PR URL>`), or the token (follow step 8's `missing`
branch, which also gives Jeff the instructions). Then carry on. "The Sync line" is
the command in the instruction block (with any `--repo-url`). Every part is safe to repeat.

1. **Sync.** First the Sync line with `--dry-run` (it writes nothing; summary on stdout, plan on stderr). Stop and tell Jeff if
   stderr says `duplicate project` (two rows share a title: fix the rows in a normal commit first), or if any card with this
   Source has an Area other than `<area>`, or if the dry run plans to close any card while it shows `unchanged=0 updated=0`
   (both mean another repository shares this Source). Otherwise run the Sync line, then once more:
   the second run must say `created=0`. A session before this one may already have synced; that is fine. An exit 2 naming a
   missing option means it was lost or never added: redo step 3.1 for it, then sync again.
2. **Clean-up**, from the join card's page body. For each `<old card> → "<row title>"`, first check that a card with Source
   `<source>` and Project `<row title>` exists (any status); if none does, leave the old card alone and ask Jeff. Then:
   - the old card is open: set it to **Dropped**, in one edit with Next step `Dropped: moved to <source> as "<row title>"` and
     Last update today;
   - it is Dropped as moved to `<source>`, or as a duplicate of (or pointing at) that synced card: already handled; nothing to do;
   - it was finished (Done) or abandoned (Dropped for a reason about the work itself) meanwhile: leave it, and close the
     matching row in `handoff.md` the same way in a normal commit (Done with evidence, or `Dropped: <reason>`). In a public repo
     write a public-safe reason and public evidence, never the card's Notion link or text; ask Jeff if there is none.

   Then for each synced P0 card, and each synced card that replaced a card with a Target date, set the Target date only if the
   synced card has none: the old card's current date if it has one, otherwise the date Jeff gave (page body). Touch no other card;
   never delete one.
3. **Close the join card**, once every pair in 9.2 is resolved (otherwise set it to Waiting on Jeff, Owner Jeff, Next step
   `Jeff: decide what happens to the <n> old card(s) listed in this card's page body (step 9.2 of <guide>)`): Status Done, Owner Claude Code, Next step `none`, Link = the full URL of the join commit or the merged
   join PR (the evidence the audit accepts), Last update today, and the two sync lines in its page body. No repository commit is
   needed.

Exit codes: `2` = off (token missing, page not shared with the integration, an option missing, Notion unreachable; the reason
is in the `off (…)` line); `3` = `handoff.md` cannot be parsed (the heading, the columns, or a file that is not UTF-8); `4` = bad
flag. The full table is in the skill's SKILL.md, "Running the sync". A repo with no remote at all has no URLs for evidence: the
weekly audit flags its Done cards (`evidence`) until it is pushed to GitHub (a private repository is fine).

## 10. Report to Jeff

Your final message gives: the Area and the Source, the cards created and the manual cards dropped (counts; titles only if this
repo is private), the sync lines, the In progress count per Owner across the board, anything still open (a PR to merge, a token
to set, files that use another name for him), and the vault commit id from step 0.

## After joining

- Every session follows the block from step 5: open, move and close cards through `handoff.md`, and run the Sync line once the
  change is on the default branch. There is no daily Routine for a local project. If Jeff wants one, a cloud Routine on this repo
  can run the same command with `NOTION_TOKEN` set and `api.notion.com` in its allowed domains.
- `python3 scripts/notion-sync.py --audit --source "<source>"` checks the policy across the board, read-only. It names only this
  repo's cards; every other card appears as a count.
- Jeff reviews the whole board on Mondays and tells a session what to change. You make the change.
