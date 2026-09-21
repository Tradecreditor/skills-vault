---
name: delegating-to-codex
description: Calls OpenAI Codex from inside Claude Code for a read-only code review or to hand off a task to Codex as a background job. Use when asked to "review with codex", "get a second opinion from codex", or "delegate this to codex".
metadata:
  source_url: "https://github.com/openai/codex-plugin-cc"
  source_platform: github
  author: "OpenAI"
  captured_at: "2026-09-21T23:07:37Z"
  engagement: "stars=33429 forks=2321"
  origin_type: "repo"
  vault_status: "draft"
---

# delegating-to-codex

Draft, unreviewed. Wraps the official `openai/codex-plugin-cc` Claude Code plugin. Requires a ChatGPT subscription (free tier works) or an OpenAI API key, Node.js 18.18+, and the Codex CLI logged in locally (`codex login`).

## Install
```
/plugin marketplace add openai/codex-plugin-cc
/plugin install codex@openai-codex
/reload-plugins
/codex:setup
```
`/codex:setup` checks whether Codex is installed/authenticated and can install it via `npm install -g @openai/codex` if missing.

## Commands
- `/codex:review [--base <branch>] [--wait|--background]` — read-only review of uncommitted changes or a branch diff. Not steerable, no custom focus text.
- `/codex:adversarial-review [--base <branch>] [--wait|--background] <focus text>` — steerable, challenges the chosen design/tradeoffs/risk areas instead of just linting the diff.
- `/codex:rescue [--background|--wait|--resume|--fresh] [--model <name>] [--effort <level>] <task>` — hands a task to Codex via the `codex:codex-rescue` subagent (investigate a bug, try a fix, continue a prior Codex thread).
- `/codex:transfer [--source <path>]` — turns the current Claude Code session into a resumable Codex thread; prints a `codex resume <id>` command.
- `/codex:status [<task-id>]` / `/codex:result [<task-id>]` / `/codex:cancel [<task-id>]` — check, fetch, or cancel a background Codex job.

## Typical flow
```
/codex:review --background
/codex:status
/codex:result
```

## Notes
- All review commands are read-only; they never modify code themselves.
- `/codex:setup --enable-review-gate` turns on a `Stop` hook that runs a targeted Codex review before Claude can finish a turn, blocking on unresolved issues — can create a long Claude/Codex loop and burn usage quickly, only enable while actively watching the session.
- Codex reuses the same local Codex CLI auth, config (`~/.codex/config.toml` or project `.codex/config.toml`), and repo checkout — no separate runtime or account needed if Codex is already set up on the machine.
