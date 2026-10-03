---
name: keeping-handoff-docs
description: "Keeps one handoff.md per project so any later session or agent resumes without re-reading history: read it first, update it before ending a session that changed state. Use when starting work in a repo, ending or pausing a session, handing a plan to another agent, or onboarding a new one."
metadata:
  origin_type: "vault-operations"
  captured_at: "2026-10-03"
  vault_status: "draft"
---

# keeping-handoff-docs — one handoff.md per project

## Overview

Work on a project is spread over many sessions and several agents (Claude Code cloud and local, Codex, Gemini CLI, OpenClaw, cloud Routines). Each one starts with an empty context. Without a handoff the state lives in chat transcripts nobody re-reads, in PR descriptions, and in the head of whoever ran the last session; the next agent either repeats work or guesses. The fix is boring and reliable: **one `handoff.md` at the project root**, read first, updated last. This is Josep's standing rule for every project (2026-10-03).

## The rule

1. **One file, one project**: `handoff.md` at the repository root. Never two, never per-branch.
2. **Read it first**, before CLAUDE.md / AGENTS.md details, before any search. It tells you where the project stands and which detailed document to open next.
3. **Update it before you end** any session that changed code, prompts, config, skills, data, infrastructure or the plan. Commit it in the same change (same commit or PR), never as an afterthought in a later session.
4. **Append one line to its Session log** every time you update it: date · who (agent, model, session id if you have one) · what changed · what is next. Never rewrite or delete old lines.
5. **Cron / scheduled agents read it and never edit it.** Their output goes to the project's own logs (in this vault: `wiki/log.md`, `wiki/hot.md`, `outputs/health/`).

## What goes in (sections, in this order)

| Section | Holds | Rule of thumb |
|---|---|---|
| header | purpose line, "last updated" with UTC time and who | one paragraph |
| **Snapshot** | what the project is, where the rules live, who may push where, what runs on a schedule | 3–6 bullets, stable for weeks |
| **In flight** | a table: workstream · state · next concrete step · link to the detailed doc | one row per open workstream; this is the part the next agent acts on |
| **Open loops** | known unfinished items that are nobody's current task (expiring tokens, settings to flip, reviews pending) | each with where it is documented |
| **Recently done** | last ~7 days, PR numbers and dates | prune older lines when you add new ones |
| **Environment facts that bite** | things that cost a session an hour and will again | one line each + link to the long form |
| **How to update this file** | the five rules above, in the project's words | copy from the template |
| **Session log** | append-only, one line per updating session, newest last | never edited, only appended |

## What stays out

- Long analysis, research, run reports and design notes: write them where the project keeps long-form output (in this vault `outputs/<yyyymmdd>-<topic>.md`; elsewhere `docs/`), and **link** them from In flight. A workstream that spans more than a week deserves its own `…-handoff.md` there, with its own status / to-do / pitfalls sections, linked from the row.
- Anything already logged elsewhere (commit history, `wiki/log.md`, CI output). Point, do not copy.
- Secrets, tokens, cookies, personal data. Name where a credential lives, never its value.
- Narrative ("first I tried…"). State facts: what is merged, what is live, what is proven, what is not, what is next.

## Writing rules

- Facts with anchors: dates (UTC), PR numbers, commit hashes, trigger / session ids, file paths. "Proven" and "not yet proven" are separate lists.
- Keep the whole file under about 150 lines. When a section grows past that, move detail to a linked document and leave the summary.
- Links use the project's own convention (this vault: relative paths and `[[wikilinks]]` where Obsidian reads them).
- Language: the project's working language for agents (this vault: English, since Codex and Gemini CLI read it too); summaries for Josep stay in the reports.
- Never rename or delete the file; the name is the contract other agents rely on.

## Session workflow

**Start**: read `handoff.md` → open the detailed doc its In flight row points to → then the rules file (CLAUDE.md / AGENTS.md) for conventions. Say in your first message what you believe the state is, so a wrong handoff gets corrected early.

**During**: when you make a decision that a later agent would otherwise re-litigate (a threshold, a rejected approach, a platform limit you hit), note it in the detailed doc or the Environment facts section while it is fresh.

**End**: update Snapshot if anything structural changed, the In flight rows you touched (state + next step), Recently done, Environment facts; append your Session log line; include the file in the commit / PR that carries the change. If the session ends without changing state, do not touch the file.

## Installing the SOP in another project

1. Copy `references/handoff-template.md` from this skill to the project root as `handoff.md` and fill the Snapshot and In flight sections from what you know; mark the rest "unknown — fill in".
2. Add two lines to the project's `CLAUDE.md` / `AGENTS.md` (or equivalent): under "read first", `handoff.md — where the project stands, what is in flight, what to do next`; under the working rules, `Update handoff.md before ending a session that changed state; append one line to its Session log; scheduled agents read it and never edit it.`
3. Commit both together. From then on the rule enforces itself: every session that reads the rules file reads the handoff.

Install this skill in another agent with `npx skills add Tradecreditor/skills-vault --skill keeping-handoff-docs`.

## Evidence

- 2026-10-03 — skills-vault: the Jev pilot work spanned two days, five PRs, three sub-sessions and two cloud Routines. Its state was scattered over a report's 下一步 (with config names that had already changed), a skill reference, `routines/README.md` and PR bodies. Writing `outputs/20261003-jev-pilots-handoff.md` and then the root `handoff.md` took under an hour and is now the entry point for the next pilot; Josep made it the rule for every project.

## Source

- Josep's instruction, 2026-10-03: "Keeping a handoff document should be an SOP for any projects to follow. This is for multi sessions or multi agents to work. Keep a handoff.md in every project."
- First instance: `handoff.md` and `outputs/20261003-jev-pilots-handoff.md` in this repository.
