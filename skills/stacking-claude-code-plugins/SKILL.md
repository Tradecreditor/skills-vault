---
name: stacking-claude-code-plugins
description: Installs and configures four complementary Claude Code plugins (Graphify, Agent Skills, Ponytail, OmniRoute) to reduce context burn, enforce a planning workflow, cut generated code size, and prevent quota-based interruptions. Use when setting up Claude Code for a large repo, hitting context or quota limits, or wanting a structured agent engineering workflow.
metadata:
  source_url: "https://www.instagram.com/reel/DdjkD4xi1ma/"
  source_platform: "instagram"
  author: "peterstewiestartup"
  captured_at: "2026-09-26"
  engagement: ""
  origin_type: "post"
  vault_status: "draft"
---

# stacking-claude-code-plugins

Set up four plugins that address distinct Claude Code bottlenecks: context saturation, unplanned coding, code verbosity, and quota interruption.

## When to use

- Large repo where Claude repeatedly re-reads the same files.
- Sessions interrupted mid-task by Claude quota limits.
- Agent output is over-engineered or bloated.
- You want a repeatable spec → plan → build → test → ship process.

## Steps

### 1. Graphify — repo knowledge graph

```bash
# Install
git clone https://github.com/Graphify-Labs/graphify
cd graphify && npm install

# Build the graph (run once per repo, zero LLM calls)
npx graphify build --repo /path/to/your/repo

# Add to CLAUDE.md or a session-start hook so Claude reads the graph first
```

**Effect**: Claude follows the pre-built map instead of re-reading files; eliminates redundant file reads.

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

- Graphify's graph goes stale when files change significantly — rebuild after large refactors.
- Ponytail's justification step adds latency; disable for trivial tasks (single-file scripts).
- OmniRoute fallback models may not match Claude's instruction-following quality — review output after a provider switch.
- Agent Skills stages require a CLAUDE.md or skills folder in every project; set up once per repo.

## Source

- https://www.instagram.com/reel/DdjkD4xi1ma/ — @peterstewiestartup, 2026-09-21
