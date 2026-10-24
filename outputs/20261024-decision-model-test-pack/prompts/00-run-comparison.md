# Prompt: run the decision-model comparison

Paste everything below the line into the agent that drives your lab (a Claude Code session opened in this folder works).
Edit the contestant table first: delete rows you cannot reach, fill in the model ids your accounts show.

---

You are running a head-to-head test of decision models on real judgments from Jeff's skills-vault.
The folder you are in is the test pack. Read `README.md` first, then do the steps below in order.
Do not change `cases.jsonl` or anything under `prompts/`.

## The test

`cases.jsonl` has 258 cases in four suites. Each line is `{id, suite, request, gold, ref, meta}`.
`request` = `{state, questions}` in TypeSafe Jev's native format. **Only `request` may ever reach a model.**
`gold`, `ref` and `meta` are the answer key; if any of their text reaches a model, the run is void.

| suite | question | type | what the vault uses it for | cases |
|---|---|---|---|---|
| A-topical | `topical` (H2) | noul | weekly-hot-list: which star gate a GitHub candidate gets. Live since 2026-10-05 | 61 |
| B-in_scope | `in_scope` (H1) | score, 5 levels (0-4) | weekly-hot-list: which X / Threads search hits get one of 40 verifications. Live | 81 |
| C-type_topic | `type` + `topic` | two choices in one request | capture-link: vault type and topic tag of a new capture. Planned | 83 |
| D-same_item | `same_item` (H3) | noul | weekly-hot-list: is this post about this repo. Configured, switched off | 33 |

## Contestants

| label (= run file name) | kind | how to call | notes |
|---|---|---|---|
| `jev-1.13.0` | decision model | `POST https://api.typesafe.ai/v1/systemone`, body = `request` + `"model": "jev-1.13.0"`, header `Authorization: Bearer $TYPESAFE_API_KEY` | the vault's production pin; the reference everyone is compared with |
| `jev-1.14.0` | decision model | same, `"model": "jev-1.14.0"` | latest; tells Jeff whether to move the pin |
| `clef` | decision model | Cloudflare Workers AI, Jev-compatible body `{state, questions}` | take the model id from the Workers AI catalog; do not guess it |
| `clef-flash` | decision model | same, the flash id | |
| `strands-decider-2b` | decision model | self-hosted (CPU is fine) | if it has no score type, skip suite B for it and say so |
| `claude-haiku-4-5` | LLM baseline | Anthropic Messages API with `prompts/10-llm-baseline.md` | |
| `claude-sonnet-5-5` | LLM baseline | same | |
| (others) | LLM baseline | same prompt, any provider | |

Gateways: on OpenRouter, Jev is `POST https://openrouter.ai/api/alpha/decisions` with model `typesafe/jev-1.13` or `typesafe/jev-1.14`; its adapter takes `instructions` and `criteria` as strings only, so export with `python3 pack.py split --flatten`. Keep base URL, key and model id from the same provider: a key from one host is refused by another.

## Steps

1. **Keys.** Read every API key from an environment variable. Never print a key, never put one on a command line you echo, never write one to a file in this folder.
2. **Probe** each contestant with one tiny request (state `"probe"`, one noul question). Record the resolved model id it reports. A contestant that fails its probe is dropped from the run; say why in the report.
3. **Run** every case for every contestant, **3 repeats** each (repeats are what measure stability; for an expensive LLM you may use 1 and say so). At most 4 requests in flight per provider. Send an `Idempotency-Key` where the API accepts one. On 429 / 5xx / timeout retry once after a pause; a second failure is recorded with `"error"` and not retried again.
   Write one line per call to `runs/<label>.jsonl`:
   `{"id", "rep", "model" (as the API resolved it), "answers" (the answers object exactly as returned), "latency_ms", "input_tokens", "output_tokens", "cost_usd", "error"}`.
   Decision models: send `request` unchanged (plus the model field the API wants). LLM baselines: use `prompts/10-llm-baseline.md`.
   Cost: the provider's reported cost if it returns one, else tokens times list price on the day.
4. **Score:** `python3 pack.py score --runs runs --out report-scores.md --json summary.json`.
   Add the vault's real production numbers as an extra row: `cp baselines/jev-1.13.0-production.jsonl runs/` before scoring (suite A only, 54 cases, jev-1.13.0 as the routine saw it in W40 to W42).
5. **Read the misses.** For each contestant, open every case listed under "auto-wrong", "missed act items" and "noise acted", and every case where the contestant disagrees with `jev-1.13.0` by more than 0.3 (noul) or 1.0 level (score). Write one line each: case id, item, gold, the contestant's answer, and why it went wrong (the state misled it, the question is ambiguous, or the gold label looks wrong). If the gold label looks wrong, say so; do not change it.
6. **Write `report.md`** with the sections below and stop.

## Report

1. **Verdict, three sentences.** Which contestant you would put in the vault's routines, whether Clef can be a drop-in fallback for Jev, and whether to move the pin from `jev-1.13.0` to `jev-1.14.0`.
2. **Scores table** from `report-scores.md`, unchanged.
3. **Against the vault's acceptance rules**, one row per contestant with ✅ / ❌ per rule:
   - A clear cases: auto-wrong ≤ `jev-1.13.0`'s + 2 points.
   - B: missed act items ≤ `jev-1.13.0`'s, and noise acted ≤ `jev-1.13.0`'s + 1.
   - D clear cases: auto-wrong ≤ `jev-1.13.0`'s.
   - Deferred share on A and D clear cases ≤ 1.5 × `jev-1.13.0`'s (every deferral costs Opus tokens).
   - Repeat band flips ≤ `jev-1.13.0`'s.
   - Cost per 1,000 decisions and p50 latency: report, no pass mark.
4. **Calibration.** Brier and ECE per noul suite; for any contestant with ECE above 0.10, say which probability range is off.
5. **Borderline cases** (A and D cases marked `borderline`): did each contestant defer them (0.50 to 0.80) rather than act? A model that acts confidently on these is riskier than its accuracy suggests.
6. **The misses** from step 5.
7. **Gold labels to review**: case ids where two or more contestants agree against the gold label.
8. **Run facts**: date, resolved model ids, repeats, calls, errors and their reasons, total cost.
