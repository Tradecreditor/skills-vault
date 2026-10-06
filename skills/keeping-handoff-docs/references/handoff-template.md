# handoff.md — where <project> stands (read this first)

One file, one project. Any session or agent that changes code, prompts, config, data or the plan updates this file before it ends (SOP: `keeping-handoff-docs`). Scheduled / cron agents read it and never edit it. Keep it under ~150 lines; long detail goes to `<docs folder>/` and is linked from here.

Last updated: <YYYY-MM-DD HH:MM UTC> by <agent / model / session id>.

## Snapshot
- What this project is: <one line>. Rules: `<CLAUDE.md / AGENTS.md / CONTRIBUTING.md>`.
- Who may push where: <accounts, branches, review rules>.
- What runs on a schedule: <jobs, when, where their prompts / code live>.
- Environments and credentials (names only, never values): <where each lives>.

## In flight
| Workstream | Status | Priority | Owner | State | Next step | Detail |
|---|---|---|---|---|---|---|
| <stable outcome title> | <Backlog / In progress / Waiting on Josep / Blocked / Done / Dropped> | <P0–P3, default P2> | <Josep / Claude Code / Routine> | <facts: merged / live / proven / not yet> | <one concrete action; `Josep: …` when waiting on him> | `<path, PR or evidence>` |

Each row is one card on the Projects HQ board (`tracking-projects-in-notion`; policy in its `references/board-policy.md`).

## Open loops
- <item> — <where it is documented>.

## Recently done (last 7 days)
- <YYYY-MM-DD>: <PR #n — what>.

## Environment facts that bite
- <one line> — details: `<path>`.

## How to update this file
- Edit the sections above in place; keep facts, dates, PR numbers, ids.
- Append one line to the Session log; never rewrite old lines.
- Commit it with the change it describes (same commit or PR).
- Scheduled agents read it and never edit it.

## Session log (append-only; newest last)
- <YYYY-MM-DD> · <agent / model / session id> · <what changed> · next: <what>.
