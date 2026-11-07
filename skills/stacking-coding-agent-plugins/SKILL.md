---
name: stacking-coding-agent-plugins
description: Installs four coding-agent plugins (Graphify, Agent Skills, Ponytail, OmniRoute) that cut context burn, enforce planning, shrink generated code, and prevent quota interruptions. Use when setting up a coding agent on a large repo, hitting context or quota limits, or wanting a structured workflow.
metadata:
  source_url: "https://www.instagram.com/reel/DdjkD4xi1ma/"
  source_platform: "instagram"
  author: "peterstewiestartup"
  captured_at: "2026-09-26"
  engagement: ""
  origin_type: "post"
  vault_status: "draft"
  reviewed_at: "2026-11-07T07:48:47Z"
  reviewed_by: "routine:skill-review"
  review_hash: "665efe4c655de4c0532073782826114b9b73a91012810a7598a7711b5e3d994b"
  review_report: "outputs/skill-reviews/2026-11-07-stacking-coding-agent-plugins.md"
---

# stacking-coding-agent-plugins

Set up four plugins that address distinct Claude Code bottlenecks: context saturation, unplanned coding, code verbosity, and quota interruption.

## When to use

- Large repo where Claude repeatedly re-reads the same files.
- Sessions interrupted mid-task by Claude quota limits.
- Agent output is over-engineered or bloated.
- You want a repeatable spec → plan → build → test → ship process.

## Steps

### 1. Graphify — repo knowledge graph

Needs Python 3.10+ and uv. Graphify is a Python package, not an npm one, and its PyPI name has two y's (`graphifyy`). Tested on Windows on 2026-11-06.

```bash
# Install once per machine
uv tool install graphifyy==0.9.103
graphify install --platform claude

# Build or refresh the code graph, from the repo root (local, zero LLM calls)
graphify update .
```

To map docs, PDFs, images or video as well, type `/graphify .` in the assistant. That pass uses the assistant's model or a configured API key.

**Changes outside the repo**: adds the `graphify` and `graphify-mcp` commands and `~/.claude/skills/graphify/`, and appends a short `/graphify` registration block to `~/.claude/CLAUDE.md`. It adds no hook. Each repo gets a `graphify-out/` folder.

**Effect**: Claude can query the graph with `graphify query`, `graphify path` and `graphify explain` instead of searching through files.

### 2. Agent Skills — structured engineering workflow

```bash
npx skills add addyosmani/agent-skills
```

Each stage (spec, plan, build, test, review, ship) becomes an invokable skill with its own output artifact. Prevents "just start coding" behaviour.

### 3. Ponytail — justification hook

```bash
git clone https://github.com/DietrichGebert/ponytail
# Follow repo README to register as a Claude Code session-start hook
```

**Effect**: Agent must justify each line before writing it. Reported reduction: ~54% less code on average (up to 94% on over-engineered tasks), ~20% cost saving.

### 4. OmniRoute — multi-provider fallback

```bash
git clone https://github.com/diegosouzapw/OmniRoute
# Point ANTHROPIC_BASE_URL (or equivalent) at the OmniRoute endpoint
# Configure fallback providers in omniroute.config.json
```

**Effect**: When Claude quota runs out mid-session, OmniRoute silently switches to another provider (352 available). Work continues uninterrupted.

## Pitfalls

- Graphify's graph goes stale when files change: run `graphify update .` after changing code.
- Ponytail's justification step adds latency; disable for trivial tasks (single-file scripts).
- OmniRoute fallback models may not match Claude's instruction-following quality — review output after a provider switch.
- Agent Skills stages require a CLAUDE.md or skills folder in every project; set up once per repo.

## Source

- https://www.instagram.com/reel/DdjkD4xi1ma/ — @peterstewiestartup, 2026-09-21
- https://github.com/Graphify-Labs/graphify — Graphify README and v0.9.103 install code, 2026-11-06
