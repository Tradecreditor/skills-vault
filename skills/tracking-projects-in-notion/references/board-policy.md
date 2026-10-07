# Projects HQ board policy

The working agreement for Jeff's one kanban board (Notion page **Projects HQ**, database **Project Status**). It applies to every
project he runs: each repository (one Area per repo) and every project without a repo. Every agent and every session follows it,
whichever repository it runs in. It is a Kanban system: visualise the work, limit work in progress, make the policies explicit,
manage flow, review on a fixed cadence. Owner of this policy: Jeff. Agents propose changes as `docs:` edits; they never change it
on their own.

## 1. What a card is

- **One card = one workstream**: a deliverable with an observable outcome (something merged, live, decided, shipped or sent),
  normally finishable in 2–6 weeks. A bigger effort is split into several cards ("Jev pilot 1", "Jev pilots 2–4").
- Not a to-do. The steps live in the card's **Next step** (the next one only), in the repository's `handoff.md` and in the
  session's own task list.
- **Title**: an outcome noun phrase, stable for the card's life. No status words, no dates, no "WIP", no owner. Renaming a synced
  card closes it and opens a new one.
- One project can have several cards at once; an Area groups them.
- **One board, per-project views.** Every project's board is a Board view of this one database filtered by its Area (a tab named after the Area). Never create a separate database or board per project: WIP limits, priorities and the weekly review work only across one board. A project that needs task-level tracking keeps it in its own repo (handoff.md / the session task list, or Backlog.md via `tracking-tasks-with-backlog-md`), not as more cards.

## 2. Fields

| Field | Rule |
|---|---|
| Project | the title (above) |
| Status | exactly one of the six columns in section 3 |
| Priority | P0, P1, P2 or P3 (section 4). New cards default to P2 |
| Area | the repository name for repo work (`skills-vault`, …), otherwise the life or business area. New Areas are decided by Jeff and added by a session with the Notion connector on his word (asking a project to join counts) |
| Owner | who moves the card next: `Jeff`, `Claude Code` (any agent session) or `Routine` |
| Next step | one concrete, checkable action that starts with a verb. Waiting on Jeff: starts with `Jeff:` and names the decision or action. Blocked: names the blocker and the condition that unblocks it |
| Target date | the date the outcome is due, not a guess at effort. Required for P0; set it for any card with a real deadline. Set in Notion (UI or connector) on any card; the sync never writes it |
| Link | where the detail or the evidence lives: PR, commit, report, file, Notion page. Required for Done |
| Last update | date of the newest fact on the card. Every status change updates it |
| Source | who owns the row: `<repo>/handoff.md` (written only by `scripts/notion-sync.py`) or `manual` |

## 3. Columns, entry rules and Definition of Done

| Column | A card is here when | Required to enter | Leaves when |
|---|---|---|---|
| **Backlog** | the outcome is agreed as worth doing but nobody has started, or it is parked | Project, Area, Priority, Owner, Next step (the first action) | someone starts it (→ In progress) or it is dropped |
| **In progress** | someone is actively working on it this week | all required fields; Owner under the WIP limit (section 5) | it needs Jeff (→ Waiting on Jeff), it is stuck on something outside Jeff and the agents (→ Blocked), or it meets the Definition of Done |
| **Waiting on Jeff** | work cannot continue until Jeff decides, approves, merges, pays, signs or sets something up | Next step starts with `Jeff:` and says exactly what is needed | Jeff acts (→ In progress or Done) |
| **Blocked** | work is stuck on a third party, an outside service, a date or a dependency nobody here controls | Next step names the blocker and the unblock condition | the condition is met (→ In progress) |
| **Done** | the Definition of Done is met | Link points to the evidence | never; Done cards stay on the board. Follow-up work is a new card (a new Workstream title), not a reopened one |
| **Dropped** | the outcome is no longer wanted | Next step starts with `Dropped:` and gives the reason | never |

**Definition of Done** (all must hold): the outcome exists where it is used (merged to `main` and live, deployed, sent, decided
and written down); it was checked (tests, a run, a read-back, a reviewer's verdict); the Link points to that evidence; the repo
card's `handoff.md` row is set to Done (and moved to "Recently done" in a later update). "Code written", "PR opened" and "waiting
for review" are not Done; the last two are Waiting on Jeff.

## 4. Priority

| Priority | Meaning | Rule |
|---|---|---|
| P0 | urgent: something is broken, at risk or blocking other work | this week; Target date required; at most 1 open P0 per Owner |
| P1 | current focus | set a Target date when there is a real deadline |
| P2 | normal (default) | done when capacity frees up |
| P3 | someday / parked | usually sits in Backlog; reviewed monthly |

Work is pulled in priority order: P0, then P1, then P2. Within one priority, the oldest Last update goes first.

## 5. WIP limits and flow

- **WIP limits for In progress**: Jeff 3, Claude Code 5, Routine no limit. Over the limit: finish, park (→ Backlog) or hand over a
  card before starting another. An agent that has to go over the limit says so in its session summary.
- **Pull, do not push**: start new work only when the Owner is under the limit. Finishing beats starting.
- **Every move updates Next step and Last update in the same edit.**
- **Ageing limits**: In progress or Blocked with no update for 14 days, or Waiting on Jeff for 7 days, is stale. The Owner
  updates it, parks it in Backlog, or closes it.
- **Never delete a card.** A card that should not exist goes to Dropped with the reason. Duplicates are set to Done by the sync
  (synced cards) or Dropped through the connector (manual cards) with a pointer to the live card.

## 6. Opening, moving and closing a card

| Action | Repo work (Source `<repo>/handoff.md`) | Non-repo work (Source `manual`) |
|---|---|---|
| Open | add a row to `handoff.md` "## In flight" with Status (usually Backlog or In progress), Priority, Owner, State, Next step and Detail, in the same commit as the first piece of work. The next sync creates the card | a session with the Notion connector creates the card with every required field, on Jeff's word |
| Move | change the row's Status, Owner, Next step (and State) in `handoff.md` in the same commit as the work that caused the move | a session with the Notion connector edits the card |
| Close | set the row's Status to `Done` (or `Dropped`), Next step `none` (or `Dropped: <reason>`), Detail to the evidence; in a later update move the row to "Recently done". A row that just disappears from In flight is closed by the sync as Done with "Left … In flight" and no evidence; the weekly audit flags it (`evidence`) | a session with the Notion connector sets Status Done (or Dropped) and Link to the evidence |

Never edit a synced card in Notion: the next sync overwrites Status, Priority, Owner, Area, Next step, Link and Last update. Target
date is never written by the sync, so it can be set in Notion on any card.

One manual card per repository is expected: while a repository joins the board, a `Projects HQ join: <source>` card (Source `manual`) in
its Area tracks the join and is closed with the join commit as evidence (`references/joining-projects-hq.md`).

## 7. Cadence

| When | Who | What |
|---|---|---|
| Every session, start | the agent | read `handoff.md`, then (with the Notion connector) the board's cards for this Area. Do not start work that is not on a card: open one first |
| Every session, end | the agent | update the In flight rows it touched (Status, Priority, Owner, Next step) and, for non-repo work, the manual cards; say in the final message which cards moved |
| Daily 06:00 UTC | `github-stars-sync` step 7 | `scripts/notion-sync.py` mirrors `skills-vault/handoff.md` (other repos: their own scheduled run or the next session) |
| Weekly, Monday | `vault-lint` check 9 | `scripts/notion-sync.py --audit` lists policy breaches (WIP, more than one P0, missing fields, stale, Waiting without `Jeff:`, Blocked without a blocker, P0 without Target date, overdue, Done without evidence, Dropped without a reason, duplicates). Counts for every card; names only for this repo's synced cards |
| Weekly, Monday | Jeff (≈15 min) | review in this order: Waiting on Jeff, Blocked, WIP per Owner, P0 and overdue Target dates, stale cards, then Backlog (reprioritise, drop), and tell a session what to change |
| Monthly | Jeff | P3 and Backlog older than 60 days: keep, park or drop |

## 8. Privacy and change control

- **Jeff views the board; he does not edit it** (decided 2026-10-07). Every change goes through an agent: repo cards through
  `handoff.md`, `manual` cards through a session with the Notion connector, both on Jeff's word. Never ask Jeff to drag, edit or
  create a card himself; ask what he wants changed and make the change.
- This vault and its reports are public. Never copy a `manual` card's title, Area or details into a public repository, a report
  or a commit message. One exception: when a project joins the board, its own repo-work manual cards move into its own
  `handoff.md`, keeping their titles only in a private repository; a public repository gets new public-safe titles that Jeff
  has agreed (`references/joining-projects-hq.md` steps 4 and 6). A project's own Area name may appear in its own repository. The
  audit prints other cards as counts only.
- Only Jeff decides on new or renamed columns, priorities, Owners or Areas, and changes this policy; a session with the
  connector makes the change on his word. The sync never changes the schema: a
  value it needs that does not exist yet stops it with exit 2.
- Notion Memory holds a one-paragraph pointer to this policy, so agents in any repository or client that has the Notion connector
  find it.
