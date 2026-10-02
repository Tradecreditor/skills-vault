---
name: model-tiering
description: "Picks the Claude model tier and effort level for a task: expensive models (Fable/Opus) plan, advise and review, Sonnet executes. Use when spawning subagents, workflows or cron agents, writing code that calls the Claude API (advisor tool), or weighing cost vs quality of Fable/Opus vs Sonnet."
metadata:
  origin_type: "vault-operations"
  captured_at: "2026-09-26"
  vault_status: "draft"
---

# Model Tiering SOP — expensive models advise, cheap models execute

## Overview

**Spend the expensive tokens on judgment, not on volume.** Fable 5 / Opus decide *what* to do (planning, architecture, review, verification); Sonnet / Haiku produce the bulk tokens (execution, search, extraction, formatting). This holds in two contexts with different mechanisms:

1. **Inside Claude Code sessions** → tier via subagents and workflow options (Part A).
2. **Code that calls the Claude API** (Hermes, cron jobs, pipelines, scripts) → tier via the **advisor tool** (Part B).

Current pricing per MTok (in/out): Fable 5 $10/$50 · Opus 4.8 $5/$25 · Sonnet 5 $3/$15 (intro $2/$10 through 2026-08-31) .

## Part A — Inside Claude Code sessions

**Never downgrade the decision-making layer to save cost.** The main loop (the session model — typically Fable 5 or Opus) keeps: task decomposition, architecture decisions, reviewing subagent output, final verification, anything user-facing. Savings come from delegating execution volume downward:

| Work | Where to run it |
|---|---|
| Planning, design, ambiguity resolution, final review | Main loop (Fable/Opus) — do NOT delegate |
| Bulk mechanical coding, broad codebase search, multi-file sweeps | `Agent` tool with `model: "sonnet"` |
| Trivial classification, extraction, formatting, one-fact lookups | `Agent` tool with `model: "sonnet"` |
| Typed yes/no, pick-one or score judgments over many items (classify, gate, rank, dedupe) | Jev via the `judging-with-jev` skill (Part C); Sonnet only for the 0.50–0.80 band |
| Workflow stages that are mechanical (fan-out readers, transforms) | `agent(..., {model: "sonnet", effort: "low"})` |
| Workflow stages that judge (verify, adversarial refute, synthesize) | omit `model` (inherit main-loop model), effort `high`+ |
| First draft of a client-facing proposal (tender / ballpark / quotation) or a slide deck | `Agent` with `model: "opus"` — user rule 2026-09-22; reviewer is a separate Opus agent |

Rules of thumb:
- Cheap subagent output is a **draft until the expensive model has reviewed it**. Delegate → review → integrate; never delegate-and-trust for anything load-bearing.
- When unsure which tier a subagent needs, **omit `model`** — inheriting the session model is the safe default; explicitly downgrade only clearly mechanical work.
- `effort` is a second lever on the same dial: `low` for mechanical stages, `high`/`xhigh` for judgment stages. Lowering effort on the expensive model is often better than switching a judgment task to a cheap model.
- Headless / cron agents (Hermes crons, job-hunt pipeline): pick the tier by the job's judgment content — digests/formatting → cheap tier; scoring/decisions/writing sent to humans → high tier, or cheap executor + advisor (Part B).

## Part B — Code that calls the Claude API: the advisor tool

The API has a built-in server-side pattern for this: a cheap **executor** model consults an expensive **advisor** model mid-generation, in one request, no client orchestration. The advisor reads the full transcript and returns a plan; the executor generates the bulk output at its own (cheap) rate. You get close to advisor-solo quality at executor-dominated cost.

Minimum viable setup (beta):

```python
response = client.beta.messages.create(
    model="claude-sonnet-5",                     # executor
    max_tokens=4096,
    betas=["advisor-tool-2026-03-01"],
    tools=[{
        "type": "advisor_20260301",
        "name": "advisor",
        "model": "claude-fable-5",               # advisor (or claude-opus-4-8)
        "max_tokens": 2048,                      # cap advisor cost; ~7x cheaper, ~0% truncation
    }],
    messages=[...],
)
```

Default pairings for my projects:
- **Sonnet executor + Opus 5 advisor** — similar-or-lower total cost than before, higher quality; advisor advice visible in plaintext.
- **Sonnet executor + Fable 5.1 advisor** — maximum quality lift; advice comes back encrypted (`advisor_redacted_result`) — round-trip it verbatim, don't parse it.
- **Sonnet executor + Opus advisor** — step up from Sonnet alone, still cheaper than switching executor to Sonnet/Opus.
- Skip the advisor for single-turn Q&A or tasks where every turn genuinely needs the big model.

**Before writing any advisor-tool code, read [references/advisor-tool.md](references/advisor-tool.md)** — it has the valid model-pair table, multi-turn round-trip rules (removing the tool mid-conversation 400s unless you also strip result blocks), pause_turn resumption, caching break-even, the measured system-prompt blocks for coding tasks, and per-executor nudge guidance (helps Sonnet, neutral on Sonnet, hurts Opus).

## Part C — Below Sonnet: Jev for judgments

TypeSafe's Jev is a decision model, not a writer: it answers typed yes/no (`noul`), pick-one (`choice`) and rubric (`score`) questions with calibrated probabilities, billed on input tokens only (published median ≈ US$0.000068 per decision). When a step is a judgment over many items rather than a rewrite — is this candidate in scope, is this repo an agent skill, are these two titles the same thing, which 40 of these 450 hits deserve a fetch — ask Jev first and let Sonnet/Opus read only what survives.

Rules: never ask Jev for prose; threshold the probability (`≥ 0.80` act, `0.50–0.80` hand to the routine's own model, `< 0.50` negative branch); never let it override a deterministic gate or regex; keep today's path as the fallback when the key is missing or the call fails, and count the fallbacks; log question, probability and model version. Procedure, request shape and the per-routine question sets: [[../judging-with-jev/SKILL|judging-with-jev]]. Where it pays in this vault and where it does not: `outputs/20261002-jev-in-vault-routines.md`.

## Common mistakes

| Mistake | Fix |
|---|---|
| Downgrading the planner/reviewer to Sonnet to save cost | Savings live in execution volume; keep judgment on the high tier |
| Guessing the advisor tool shape from memory | It's post-cutoff beta surface — always read the reference file first |
| Advisor with no `max_tokens` cap | Advisor output is its largest cost driver; start at 2048 |
| Enabling advisor `caching` on short tasks | Break-even is ~3 advisor calls/conversation; off below that |
| Dropping the advisor tool from `tools` mid-conversation | 400 error — also strip all `advisor_tool_result` blocks from history |
| Adding the advisor-call nudge to Opus executors | Measured to lower Opus pass rates; Sonnet +7pp, Sonnet neutral |

## Evidence

- 2026-09-29 — Charlie Hills ran the same 4 motion-graphics prompts in Claude Code on Sonnet 5.5 vs Opus 5.5, first try, no fixes: $4.95 vs $8.44 (41% less), 19.5 vs 34.7 min; Opus still leads 7 of 8 of Anthropic's benchmarks by 2–3 pts → "Sonnet for daily work, Opus for the hard, open-ended stuff" ([[../../wiki/pages/20260929-sonnet-5-5-vs-opus-5-5-motion-graphics-cost|20260929-sonnet-5-5-vs-opus-5-5-motion-graphics-cost]]). One run, small sample.
- 2026-10-02 — Jev against the vault's four Routines: the saving is in weekly-hot-list prefiltering (~1,250 decisions a week ≈ US$0.09 at the published median, replacing Opus reads of ~450 snippets and ~390 repo objects); capture-link saves almost nothing because Sonnet reads the full text anyway (`outputs/20261002-jev-in-vault-routines.md`).
