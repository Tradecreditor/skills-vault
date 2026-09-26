# Advisor Tool — full reference

Source: https://platform.claude.com/docs/en/agents-and-tools/tool-use/advisor-tool (fetched 2026-07-11). Beta — verify against the live doc if anything here 400s unexpectedly.

## What it is

A server-side tool that lets a cheap **executor** (the request's top-level `model`) consult an expensive **advisor** (the `model` inside the tool definition) mid-generation. The executor emits `server_tool_use` with `name: "advisor"` and empty `input`; Anthropic runs a separate advisor inference server-side, feeding it the executor's **full transcript** (system prompt, tools, prior turns, tool results, text produced so far). The advice returns as an `advisor_tool_result` block and the executor continues — all inside one `/v1/messages` request. The advisor runs with no tools, no context management; its thinking is dropped, only advice text reaches the executor. ZDR-eligible.

## Request shape

- Beta header: `advisor-tool-2026-03-01` (`betas=["advisor-tool-2026-03-01"]` on `client.beta.messages.create`).
- Tool definition parameters:

| Param | Required | Notes |
|---|---|---|
| `type` | ✅ | `"advisor_20260301"` |
| `name` | ✅ | `"advisor"` |
| `model` | ✅ | Advisor model ID; sub-inference billed at this model's rates |
| `max_uses` | — | Per-request cap on advisor calls; exceeding returns `error_code: "max_uses_exceeded"` and the executor continues. NOT per-conversation |
| `max_tokens` | — | Caps advisor output (thinking + text) per call, min 1024. Server also tells the advisor its remaining budget so it shapes the answer to fit |
| `caching` | — | `{"type": "ephemeral", "ttl": "5m" | "1h"}` — on/off switch for advisor-side prompt caching (server places boundaries; not a breakpoint marker) |

Also accepts generic tool props: `cache_control`, `allowed_callers`, `defer_loading`, `strict`.

## Model compatibility (invalid pair → 400)

Advisor must be Sonnet 4.6+ and at least as capable as the executor. Equal-capability models can advise each other.

| Executor | Valid advisors |
|---|---|
| `claude-haiku-4-5` | fable-5, mythos-5, opus-4-8, opus-4-7, opus-4-6, sonnet-4-6 |
| `claude-sonnet-4-6` | fable-5, mythos-5, opus-4-8, opus-4-7, opus-4-6, sonnet-4-6 |
| `claude-sonnet-5` | fable-5, mythos-5, opus-4-8, opus-4-7 |
| `claude-opus-4-6` | fable-5, mythos-5, opus-4-8, opus-4-7, opus-4-6 |
| `claude-opus-4-7` / `claude-opus-4-8` | fable-5, mythos-5, opus-4-8, opus-4-7 |
| `claude-fable-5` | fable-5 only |
| `claude-mythos-5` | mythos-5 only |

Platform availability: Claude API and Claude Platform on AWS only. NOT on Amazon Bedrock, Vertex AI, or Microsoft Foundry.

## Result variants

`advisor_tool_result.content` is a discriminated union:

| Variant | Fields | When |
|---|---|---|
| `advisor_result` | `text`, `stop_reason`* | Plaintext advisors (e.g. Opus 4.8) |
| `advisor_redacted_result` | `encrypted_content`, `stop_reason`* | Fable 5 / Mythos 5 advisors — opaque blob; server decrypts it into the executor's prompt next turn |

\* `stop_reason` present only when you set `max_tokens` on the tool definition (`"end_turn"` or `"max_tokens"`).

**Round-trip the content verbatim on subsequent turns** in both variants. If you need to *read* the advice in your client, use `claude-opus-4-8` as the advisor instead of Fable. If you switch advisor models mid-conversation, branch on `content.type`.

Error results: `content.type: "advisor_tool_result_error"` with `error_code` ∈ `max_uses_exceeded`, `too_many_requests` (advisor rate-limited — draws from the advisor model's own bucket), `overloaded`, `prompt_too_long`, `execution_time_exceeded`, `unavailable`. The request itself does not fail; the executor continues without advice. (Executor rate limit = whole request 429s.)

## Multi-turn rules (the 400 traps)

- Append the **full** assistant `response.content` (including `advisor_tool_result` blocks) back to `messages` each turn.
- Omitting the advisor tool from `tools` on a later turn while history still contains `advisor_tool_result` blocks → `400 invalid_request_error`. To retire the advisor mid-conversation: remove the tool from `tools` **and** strip all `advisor_tool_result` blocks from history.
- No built-in conversation-level cap — count advisor calls client-side; when over budget, do the removal above.

### Resuming a paused turn (`pause_turn`)

A response can end `stop_reason: "pause_turn"` with a `server_tool_use` advisor block that has no result. Resume by appending that assistant message unchanged and re-sending with the same advisor tool + beta header — no user message or `tool_result` needed. Can pause repeatedly; repeat. If the executor also called one of your client tools in that turn, you instead get `stop_reason: "tool_use"` — send your `tool_result`s as usual and the pending advisor call runs at the start of the next request.

## Streaming

The advisor sub-inference doesn't stream: the executor's stream pauses after the advisor `server_tool_use` block closes (SSE `ping` keepalives ~30s), then the `advisor_tool_result` arrives fully formed in one `content_block_start`, executor output resumes, and a `message_delta` carries updated `usage.iterations`.

## Billing

- Reported in `usage.iterations[]`: `type: "advisor_message"` entries bill at the advisor model's rates; `type: "message"` at executor rates. Top-level `usage` = executor only (`output_tokens` sums executor iterations; `input_tokens`/`cache_read` are first executor iteration only). Build cost tracking off `iterations`.
- Typical advisor output: 400–700 text tokens (1,400–1,800 incl. thinking) on light workloads; ~4,200–5,900 on hard reasoning with no cap.
- Top-level request `max_tokens` does NOT bound the advisor; nor do executor task budgets.
- Priority Tier is per-model — an executor commitment doesn't cover the advisor.

## Cost controls (apply in this order)

1. **`max_tokens: 2048` on the tool definition** — measured ~7x reduction in mean advisor output with ~0% truncation and no detectable quality loss. 1024 = ~10x but ~10% truncated. On truncation the result carries `stop_reason: "max_tokens"` and the advice text gets `[Advisor output truncated at max_tokens=N.]` appended so the executor sees it.
2. **Soft prompt trim** — a line in the *user message* (advisor reads it as quoted context; first-person works best): `(Advisor: please keep your guidance under 80 words — I need a focused starting point, not a comprehensive plan.)` Ask for ~80% of the true ceiling. Side effect: raises consult frequency, but net cost still fell in testing.
3. **`caching`** — advisor-side cache breaks even at ~3 advisor calls per conversation; enable for long agent loops, keep off for short tasks, and never toggle mid-conversation. Warning: `clear_thinking` with `keep` ≠ `"all"` shifts the advisor's quoted transcript every turn → cache misses (cost only, not quality). On pre-4.5 Opus/Sonnet and all Haiku the default with extended thinking is `keep: thinking_turns 1` — set `keep: "all"` for advisor cache stability.
4. **Effort pairing** — Sonnet executor at `effort: "medium"` + Opus advisor ≈ Sonnet-at-default-effort intelligence at lower cost. Keep default effort for max intelligence.

Executor-side, `advisor_tool_result` blocks cache like any content block (identical behavior for both result variants).

## Prompting the executor (measured guidance)

Built-in tool description already nudges calling near the start of complex tasks and when stuck; research tasks usually need nothing extra. Coding/agent tasks under-call by default — the win comes from (1) an early first call after a few exploratory reads, and (2) for hard tasks a final call after writes/tests are in the transcript. If the agent has planner-like tools (todo list), prompt advisor-before-planner so the plan funnels in.

### Suggested system prompt blocks for coding tasks (prepend before other advisor mentions)

Timing block:

```text
You have access to an `advisor` tool backed by a stronger reviewer model. It takes NO parameters — when you call advisor(), your entire conversation history is automatically forwarded. They see the task, every tool call you've made, every result you've seen.

Call advisor BEFORE substantive work — before writing, before committing to an interpretation, before building on an assumption. If the task requires orientation first (finding files, fetching a source, seeing what's there), do that, then call advisor. Orientation is not substantive work. Writing, editing, and declaring an answer are.

Also call advisor:
- When you believe the task is complete. BEFORE this call, make your deliverable durable: write the file, save the result, commit the change. The advisor call takes time; if the session ends during it, a durable result persists and an unwritten one doesn't.
- When stuck — errors recurring, approach not converging, results that don't fit.
- When considering a change of approach.

On tasks longer than a few steps, call advisor at least once before committing to an approach and once before declaring done. On short reactive tasks where the next action is dictated by tool output you just read, you don't need to keep calling — the advisor adds most of its value on the first call, before the approach crystallizes.
```

Advice-weight block (directly after):

```text
Give the advice serious weight. If you follow a step and it fails empirically, or you have primary-source evidence that contradicts a specific claim (the file says X, the paper states Y), adapt. A passing self-test is not evidence the advice is wrong — it's evidence your test doesn't check what the advice is checking.

If you've already retrieved data pointing one way and the advisor points another: don't silently switch. Surface the conflict in one more advisor call — "I found X, you suggest Y, which constraint breaks the tie?" The advisor saw your evidence but may have underweighted it; a reconcile call is cheaper than committing to the wrong branch.
```

### Per-executor tuning (measured)

| Executor | Guidance |
|---|---|
| Haiku 4.5 (coding-heavy) | Swap in the doc's alternative Haiku block, whose extra lines add: "Call advisor for design, architecture, and risk questions where you won't touch a file…" plus the hard rule "your first write_file, edit_file, or state-changing bash call on a task must be preceded by an advisor call… read-only orientation commands (ls, cat, grep, find) are not state-changing… applies to one-line edits too." Measured +7.5pp pass rate on coding; but −4pp on browse/lookup — gate on workload type |
| Haiku (mid-conversation nudge) | If no advisor call by end of assistant turn 1, append a user message: "You have not consulted the advisor yet. If the task has a non-obvious design decision or a failure mode you haven't ruled out, call advisor now before committing to an approach." Measured +7pp on Haiku. Append as its own user message after tool results. If baseline first-call turn is N, set nudge turn > N (a turn-2 nudge on turn-7-baseline workloads cost 3–4pp) |
| Sonnet | Nudge had no measurable effect; timing/system-prompt blocks are what matter |
| Opus | Do NOT nudge (slightly lowered pass rates). Only add the hard-rule checkpoint block if you've observed under-calling — net flat on mixed workloads |

To force a consult on one request: `tool_choice: {"type": "tool", "name": "advisor"}` — incompatible with extended thinking (400).

## Composing with other tools

Advisor sits in the same `tools` array as web search, custom tools, etc.; the plan can inform which tools the executor reaches for. Batches: supported (`usage.iterations` per item). Token counting: returns executor first-iteration only; estimate the advisor by calling `count_tokens` with the advisor model on the same messages. Context editing: `clear_tool_uses` not fully compatible with advisor blocks; `clear_thinking` see caching warning above.
