---
name: configuring-fable-advisor-jev-tree
description: Configures Claude Code with Fable 5.1 as advisor and an Opus 5.5 + Jev-routed multi-agent tree. Use when setting up advisor model, scaffolding explorer/worker/researcher subagents, auditing effort env vars, or adding Jev routing to a Claude Code session.
metadata:
  source_url: "https://x.com/thedelost/status/2104677530825634273"
  source_platform: "x"
  author: "thedelost"
  captured_at: "2026-09-29"
  engagement: "likes=1902 retweets=151 views=446089 bookmarks=3708"
  origin_type: "post"
  vault_status: "draft"
  reviewed_at: "2026-10-04T15:35:29Z"
  reviewed_by: "claude-code-cloud:vault-skill-reviewer"
  review_hash: "5636bb9d2f04edcccada9855c9d38ef40bde74f258cea59987cbb5eda121c1a5"
  review_report: "outputs/skill-reviews/2026-10-04-configuring-fable-advisor-jev-tree.md"
---

# configuring-fable-advisor-jev-tree

Set up Claude Code so Fable 5.1 reviews and Opus 5.5 ships, with a three-agent subagent tree and Jev handling routing decisions.

## When to use

- You want Fable 5.1 to review plans, recurring errors, and final checks without interrupting the main flow.
- You need to scaffold explorer/worker/researcher subagents and set the main session effort to `high`.
- You want to audit environment variables that silently disable the advisor or override effort levels.

## Steps

1. **Enable the advisor** — run inside your Claude Code session:
   ```
   /advisor fable
   ```

2. **Paste this setup prompt into Claude Code** (diffs first, edits nothing until you approve):

   ```
   Rebuild my Claude Code setup around this tree:

   1. Check ~/.claude/agents and .claude/agents for subagents that already fit explorer, worker and researcher.

   > Draft new ones only for missing roles
   > Give each model: opus, effort: medium
   > Skip any that pin a different model and list them

   2. Set the main session to high via effortLevel in ~/.claude/settings.json, and set advisorModel to fable

   3. Find anything that keeps the advisor off (CLAUDE_CODE_DISABLE_ADVISOR_TOOL, DISABLE_TELEMETRY, any variable that stops feature-flag fetching) plus CLAUDE_CODE_EFFORT_LEVEL, which overrides subagent effort. Report them, change nothing

   4. Add one rule to ~/.claude/CLAUDE.md: consult the advisor before a large plan, when an error repeats, and before calling a long task done

   Show me every change as a diff first. No edits until I say go.
   ```

3. **Review the diff** Claude Code shows, then say "go" to apply.

## Agent tree reference

| Role | Model | Effort |
|---|---|---|
| Main session | Opus 5.5 | high |
| explorer | opus | medium |
| worker | opus | medium |
| researcher | opus | medium |
| Advisor | Fable 5.1 | — |

## Advisor checkpoints

Fable 5.1 speaks only at three points:

- **Before a plan**: "is this the right approach?"
- **When the same error recurs**: "am I digging in the wrong place?"
- **Before marking done**: "what did I miss?"

## Pitfalls

- `CLAUDE_CODE_EFFORT_LEVEL` env var overrides subagent effort — audit it before assuming medium is active.
- `CLAUDE_CODE_DISABLE_ADVISOR_TOOL` silently turns off the advisor; check for it in your shell profile.
- Do not set `advisorModel: fable` in settings without also running `/advisor fable` in the session.
- Fable 5.1 reads the full session including every tool call — keep context lean so reviews stay fast.

## Source

https://x.com/thedelost/status/2104677530825634273 · @thedelost · 2026-09-28
Docs: https://code.claude.com/docs/en/advisor
