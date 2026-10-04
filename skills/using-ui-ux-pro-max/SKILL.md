---
name: using-ui-ux-pro-max
description: Installs and applies the UI UX Pro Max agent skill to generate industry-specific design systems with 192 reasoning rules, 79 UI styles, and BM25 matching. Use when building UI for Claude Code, Cursor, Windsurf, vibe-coding, design system, tailwind, react, ui-ux, glassmorphism.
metadata:
  source_url: "https://github.com/nextlevelbuilder/ui-ux-pro-max-skill"
  source_platform: "github"
  author: "nextlevelbuilder"
  captured_at: "2026-09-30T20:26:00Z"
  engagement: "stars=unknown"
  origin_type: "repo"
  vault_status: "reviewer-approved"
  reviewed_at: "2026-10-04T15:35:29Z"
  reviewed_by: "claude-code-cloud:vault-skill-reviewer"
  review_hash: "109de2680a9877a779a01971e273020007b6d2a686098fdde4ac858f067f54bd"
  review_report: "outputs/skill-reviews/2026-10-04-using-ui-ux-pro-max.md"
---

# using-ui-ux-pro-max

Install and use the UI UX Pro Max agent skill to inject professional design intelligence into any AI coding assistant.

## When to use

- Starting a new UI project and need a design system (colors, fonts, layout pattern, anti-patterns)
- Vibe-coding: want Claude Code / Cursor / Windsurf to follow consistent UI/UX rules
- Need industry-specific recommendations (SaaS, e-commerce, healthcare, fintech, etc.)
- Want 79 searchable UI styles (Glassmorphism, Bento Grid, Brutalism, Neumorphism, Dark Mode, etc.)

## Steps

### 1. Install (Claude Code — Marketplace, fastest)

```
/plugin marketplace add nextlevelbuilder/ui-ux-pro-max-skill
/plugin install ui-ux-pro-max@ui-ux-pro-max-skill
```

### 2. Install (CLI — for multiple agents at once)

```bash
npm install -g ui-ux-pro-max-cli
cd /path/to/your/project
uipro init --ai claude      # Claude Code only
uipro init --ai all         # All supported agents at once
```

Supported agents: `claude`, `cursor`, `windsurf`, `antigravity`, `copilot`, `kiro`, `codex`, `qoder`, `roocode`, `gemini`, `trae`, `opencode`, `continue`, `codebuddy`, `droid`, `kilocode`, `warp`, `augment`, `codewhale`, `zcode`, `universal`.

No global install: `npx ui-ux-pro-max-cli init --ai claude`

### 3. Generate a design system

After install, ask Claude (or the agent) to build a UI. The skill auto-runs:
1. Multi-domain BM25 search (192 product categories, 79 styles, 192 palettes, 34 landing patterns, 74 font pairings)
2. Reasoning engine matches product type → style priority → color mood → typography → key effects → anti-patterns
3. Outputs complete design system block (Pattern + Style + Colors + Typography + Effects + Pre-delivery checklist)

### 4. Search manually (optional)

```bash
python3 .claude/skills/ui-ux-pro-max/scripts/search.py "SaaS" --domain style
python3 .claude/skills/ui-ux-pro-max/scripts/search.py "Beauty spa" --json   # full output
```

### 5. Uninstall

```bash
uipro uninstall             # from project root
uipro uninstall --global    # global install
```

Or remove manually: `rm -rf .claude/skills/ui-ux-pro-max`

## Pitfalls

- Do NOT upload the full GitHub repo ZIP to Claude.ai — it exceeds the 200-file limit; use Marketplace or CLI instead.
- If `uipro uninstall` says "No installed AI skill directories detected", run from the project root where you originally installed it, or use `--global`.
- Python 3.x required for design system generation scripts; install manually if missing.
- For full JSON output (not truncated), always pass `--json` flag to the search script.
- `uipro-cli` (old package name) is stale — use `ui-ux-pro-max-cli` instead.
- If Claude reports "response exceeded output token maximum", split the task or set `CLAUDE_CODE_MAX_OUTPUT_TOKENS=64000` before starting Claude.

## Source

https://github.com/nextlevelbuilder/ui-ux-pro-max-skill — MIT License
