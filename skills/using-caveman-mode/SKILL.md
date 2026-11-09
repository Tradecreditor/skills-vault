---
name: using-caveman-mode
description: Installs and applies the caveman skill, a terse answer-first voice that cuts output tokens while keeping code, commands, paths and errors verbatim. Use when replies are too long, to save tokens, or on /caveman, /ultracave, /megacave, "caveman mode" or "be brief".
metadata:
  source_url: "https://github.com/JuliusBrussee/caveman"
  source_platform: "github"
  author: "JuliusBrussee"
  captured_at: "2026-11-09"
  engagement: "stars=118625 forks=6907"
  origin_type: "repo"
  vault_status: "draft"
---

# using-caveman-mode

Install only the **caveman skill** (a Markdown prompt, no scripts) from `JuliusBrussee/caveman`, and know what the
rest of that repo (CLI, proxy, plugin hooks, Caveman Cloud) does before you add any of it.

## When to use

- Agent answers are long and you pay per output token (API, metered plans).
- You want answer-first replies in a terminal, with code, commands, paths and error strings untouched.
- Not useful when you pay per request (e.g. GitHub Copilot): shorter answers save nothing there.

## The three voices

| Command | Effect |
|---|---|
| `/caveman` | Answer first, no ceremony, articles optional, every fact kept. Upstream measured ~3% fewer tokens than a plain "Answer concisely." |
| `/ultracave` | Grammar stripped, fragments. ~35% fewer than "Answer concisely." |
| `/megacave` | Classical Chinese (文言文); technical terms verbatim |
| `/caveman status` | Report the mode, change nothing |
| `stop caveman` / `normal mode` | Back to normal prose |

The voice drops back to full sentences for security warnings, irreversible actions, step sequences, a confused user,
and anything persisted outside chat (code, commits, docs, PRs). It never rewrites your prompt.
The rules cost about 1,160 input tokens per session.

## Steps

1. Pick the smallest install that does the job. Recommended: **skill only**, nothing else:
   ```bash
   npx skills add JuliusBrussee/caveman --skill caveman -g
   ```
   Drop `--skill caveman` to also get `ultracave`, `megacave` and the other skills in the repo (several of them drive the
   proxy; read each before using it). Omit `-g` to install into the current project only.
2. In the agent, type `/caveman` (`$caveman` in Codex) if it does not start on its own. Say `stop caveman` to stop.
3. Record the install: `python3 scripts/skills-inventory.py` (or `/skills-vault:skillsync`); see `tracking-skill-installs-in-notion`.
4. To remove: `npx skills remove caveman` (add `-g` if installed globally), then record again.

## What the other install routes add (decide before using them)

- **Full CLI** `npx @caveman-ai/cli@latest` (Node 22.13+): installs a local proxy in front of every agent it finds
  ("finds your agents and your logins"), plus Read-less compression, Blocks, Browse and Auto routing.
  Sends usage telemetry by default (commands, token counts, random install ID, OS, IP): turn off with
  `caveman telemetry off` or `DO_NOT_TRACK=1`.
- **Auto** (after `caveman login`): sends your latest ask, any attached CLAUDE.md / memory / @-files, and part of the last
  reply to Caveman Cloud; the Free plan may keep it. `caveman off routing` stops it.
- **Claude Code plugin** (`.claude-plugin/plugin.json`): four Node hooks (SessionStart, SubagentStart, UserPromptSubmit,
  SessionEnd) that turn the voice on in every session and subagent and write local stats.
- Uninstall the CLI: `npx -y github:JuliusBrussee/caveman -- --uninstall`.

## Pitfalls

- The Claude Code plugin and the CLI turn the voice on by default in every session. Set `{"defaultMode":"manual"}` in
  `.caveman.json` to start sessions in normal prose.
- A reply-language instruction (e.g. a user preference for Cantonese) still wins; the voice compresses style, not language.
- `/caveman-compress` sends the file you compress to your model provider.
- The upstream skill is unpinned: re-check the upstream `skills/caveman/SKILL.md` after updates.

## Source

- https://github.com/JuliusBrussee/caveman (Apache-2.0), README and `skills/caveman/SKILL.md` at commit `3dc497a7`, 2026-11-09.
- Upstream skill text: `references/source.md`. Vault note: `wiki/pages/20261109-caveman-terse-voice-and-token-proxy.md`.
