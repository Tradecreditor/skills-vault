# Issue tracker: handoff.md card + files under outputs/

Work in this repo is tracked in two layers.

- **The card** is one row of `handoff.md` "In flight", mirrored to the Projects HQ board by `scripts/notion-sync.py`.
  One card = one workstream. Rules: `CLAUDE.md` "Projects HQ". Open the card before any work.
- **Specs and tickets** are markdown files under `outputs/`. The card's Detail cell links to the folder.

GitHub Issues are not used (Jeff, 2026-11-12). Do not run `gh issue …` or create issues through a connector.

## Conventions

- One feature per directory: `outputs/<yyyymmdd>-<feature-slug>/` (the UTC date the spec is written).
- The spec is `outputs/<yyyymmdd>-<feature-slug>/spec.md`.
- Tickets are one file each: `outputs/<yyyymmdd>-<feature-slug>/issues/<NN>-<slug>.md`, numbered from `01`,
  never one combined file.
- Each ticket starts with `Status: open | claimed | resolved` and, when it has blockers, `Blocked by: NN, NN`.
  A ticket is unblocked when every ticket it lists is `resolved`.
- Comments and history go at the bottom under `## Comments`.
- There are no triage labels (the `triage` skill is not installed). Where a skill says to apply `ready-for-agent`,
  write `Status: open`.
- Never delete or rename a spec or ticket file (vault rule). A dropped ticket gets `Status: resolved` and one line saying why.

## When a skill says "publish to the issue tracker"

Create the file under `outputs/<yyyymmdd>-<feature-slug>/`. In the same commit, make sure the feature has an In flight row
in `handoff.md` whose Detail links to the folder.

## When a skill says "fetch the relevant ticket"

Read the file at the given path. A bare number means `issues/<NN>-*.md` in the folder the card links to.

## How work closes

Set `Status: resolved` in the commit that finishes the ticket and note the commit or PR under `## Comments`.
Changes reach `main` the way `CLAUDE.md` "Access rules" says (core: a commit or a PR; non-core: always a PR); there is no
issue to close. The card moves to `Done` under the Definition of Done in
`skills/tracking-projects-in-notion/references/board-policy.md`.
