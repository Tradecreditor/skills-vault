---
name: judging-with-jev
description: "Asks TypeSafe's Jev System One model typed yes/no (noul), pick-one (choice) or rubric (score) questions so an agent can classify, gate, rank or dedupe items cheaply. Use when a routine step is a judgment, not a rewrite: type/topic tags, is-this-a-skill, hot-list prefilter, near-duplicates."
metadata:
  origin_type: "vault-operations"
  captured_at: "2026-10-02"
  vault_status: "draft"
---

# judging-with-jev — let Jev decide, let Sonnet write

## Overview

Jev is TypeSafe AI's "System One" decision model (launched 2026-09-15). It does not write text. You send a **state** (a string, a JSON object or an array) plus a map of named, typed **questions**, and it returns calibrated probabilities your code can branch on. Three question types:

| type | returns | use it for |
|---|---|---|
| `noul` | probability (0–1) that a stated proposition is true | gates: draft a skill or not, topical or not, same item or not |
| `choice` | one probability per label you define | pick one: `type`, `topic/*` tag, which reader worked |
| `score` | fractional position on an ordered 2–10 level rubric you describe; levels count from 0 | rank: relevance to scope, review priority |

Jev is trained with RLCD (reinforcement learning for calibrated decisions), so a 0.8 is right about 80% of the time — that is what makes a threshold meaningful. Several questions in one request share the state's token cost and are answered together. Only input tokens are billed; the published median is about US$0.000068 per decision. In the vault's tiering this sits **below Sonnet**: Jev judges, Sonnet executes, Opus/Fable plans and reviews (see [[../model-tiering/SKILL|model-tiering]], Part C). Where it pays in this vault and where it does not: `outputs/20261002-jev-in-vault-routines.md`.

## Prerequisites

- A TypeSafe API key. Laptop: `TYPESAFE_API_KEY` in your shell profile, sent as `Authorization: Bearer`. Cloud Routines and sessions: `TYPESAFE_API_KEY` as an environment variable on the environment, plus `api.typesafe.ai` in its allowed domains. The platform's proxy-injected **API credential** (Bearer type) was tried for this host on 2026-10-02 and never injected the header: fresh sessions listed it, four request variants (no header, HTTP/1.1, placeholder header, both) all got TypeSafe's 403 `authentication_error`, and the same key answered 200 from a laptop. The custom-header credential used for `SUPADATA_KEY` does work, so this looks specific to the Bearer type; do not rely on it until a fresh session proves otherwise. Code still must not assume the variable: send the header when it is set, otherwise send none, and read a 401, or a 403 whose JSON body says `authentication_error`, as "no accepted key reached the host". Never in the repo, never in `raw/` or a page.
- The host `api.typesafe.ai` must be reachable. Saving the API credential auto-creates the allow rule for it; listing it in the environment's allowed domains as well (routines/README.md, Step 0) is belt and braces; a Claude Code cloud sandbox without it answers `CONNECT tunnel failed, response 403` and every call falls back silently, so always count fallbacks in the final message.
- Text-only state; 64k tokens per request in total, 32k for the state plus the longest question (API reference). Trim: README first 100 lines, post text plus metadata, not a whole `raw/` file.
- Provider, base URL, key and model id are one set. TypeSafe direct: `https://api.typesafe.ai`, model `jev-latest`, console key. Vercel AI Gateway: `https://ai-gateway.vercel.sh/typesafe`, model `typesafe-ai/jev`, AI Gateway key. OpenRouter: `https://openrouter.ai/api`, model `~typesafe/jev-latest`, OpenRouter key. All three speak the same `/v1/systemone` protocol. A key only works on the host that issued it, and TypeSafe answers 403 `authentication_error` to a foreign or invalid key exactly as to no key. Avoid look-alike resellers (jevmodel.org, jev-ai.pro, jevtypesafeai.com and the many `.pro` clones): their own keys, 3–11× list price, and your state passes through their operator.
- Claude Code's auto permission mode (cloud sessions and Routines) runs a classifier over every Bash line. A hand-written `curl -H "Authorization: Bearer $TYPESAFE_API_KEY"` to an external host was denied as "Data Exfiltration" in a development run on 2026-10-02, 35 minutes after the identical probe passed in a production run. Call `scripts/jev_ask.py`: the key stays inside the script, the command line carries no secret, and the caller branches on exit codes. A denial still means Jev is off for that run; say so in the jev line. A project `.claude/settings.json` allow rule does not bypass that classifier (only `autoMode` rules in managed settings do, per the auto-mode docs).

## Request shape

In this vault every request goes through `scripts/jev_ask.py` (Python 3.8+, no dependencies, the reference implementation of the call below):

```sh
python3 skills/judging-with-jev/scripts/jev_ask.py probe                                   # exit 0 = Jev on; 2 = off for the run (reason in the JSON)
python3 skills/judging-with-jev/scripts/jev_ask.py ask --state item.json --act-min 0.80 --defer-min 0.50
```

`item.json` is `{"state": {...}, "questions": {...}}` (or the state alone plus `--questions q.json`; `--state -` reads stdin). Stdout is one JSON object: `answers.<name>.value` (noul 0–1, score counting from 0, choice label), `answers.<name>.band` (`act` / `defer` / `no` from the thresholds you pass), `.probabilities`, `model` (resolved version), `usage`, `state_sha`; stderr gets one `jev <name> p=… band=… model=… state_sha=…` line per question. Exit codes: **0** answered · **2** Jev off for the whole run (no accepted key reached the host, host unreachable) · **3** per-item fallback (402, 429, 5xx, timeout, malformed answer, a 4xx from bad question JSON) · **4** refused locally before any request (the state looks like it carries a key, token or cookie, or is oversized; the key value is never printed). `--base-url` / `JEV_BASE_URL` and `--model` / `JEV_MODEL` select a gateway; `JEV_FAKE=references/jev-fake.example.json` answers from canned values with no key and no network. The wire format it sends, for other languages:

```sh
curl -sS https://api.typesafe.ai/v1/systemone \
  -H "Authorization: Bearer $TYPESAFE_API_KEY" -H "Content-Type: application/json" \
  -H "Idempotency-Key: $(uuidgen)" \
  -d '{
    "state": {"goal": "decide whether this repo is an agent asset", "name": "kepano/obsidian-skills",
              "description": "Agent Skills for Obsidian", "topics": ["agent-skills","obsidian"], "readme_head": "..."},
    "model": "jev-latest",
    "questions": {
      "is_agent_asset": {"type": "noul",
        "instructions": "The repository is itself an agent skill, a Claude Code plugin, an MCP server or an OpenClaw skill that another agent could install."},
      "type": {"type": "choice", "instructions": "Which vault type fits this item best?",
        "criteria": {"skill": "a reusable procedure, prompt or workflow", "tool": "a product, CLI or service",
                     "repo": "a GitHub repository", "concept": "an idea or pattern",
                     "post": "a social post whose value is the discussion itself"}}
    }
  }'
```

Auth probe before a run: one tiny POST (state `"probe"`, one noul) to `<base_url>/v1/systemone` → `200` with `answers` means the key is accepted; `401`, or `403` with an `authentication_error` body, means no accepted key reached the host. `GET /v1/models` is a free alternative on TypeSafe direct and Vercel, but OpenRouter's model list is public, so the POST is the probe everywhere.

The script is that call plus the checks around it (secret-looking state refused, 401/403 `authentication_error` → off, 402/5xx/timeout → fallback, log line per question). The band rule it applies: `act` if value ≥ act_min, `defer` if ≥ defer_min, else `no`. Read the script rather than re-implementing the request; when you must (another language), keep the same three outcomes.

Response shape per the API reference (OpenAPI spec mirrored on jevwiki.ai, read 2026-10-02): `{model, answers, usage}`; `model` is the resolved version (e.g. `jev-1.13.0`), score answers also carry `legend` and `probabilities`, choice and score carry `confidence`, `usage.input_tokens` is what you pay for.

## Question design rules

1. **One proposition per noul.** "This repo is an MCP server" — not "this repo is an MCP server or a plugin and worth a skill".
2. **Choice criteria are the vault's own definitions.** Copy the label meanings from `CLAUDE.md` (type rules, topic vocabulary) so Jev and the lint agree; `references/vault-routine-questions.md` holds them verbatim.
3. **Score = an ordered array of 2–10 level descriptions** (`"criteria": ["…", "…"]`); the answer is a float from 0 to levels-1, so five levels give a 0–4 scale. Threshold the fractional result in code. Choice `criteria` is a map label → description (`null` allowed, max 255 options); noul may add `criteria.true` / `criteria.false`.
4. **Batch what shares a state.** `type`, `topic`, `actionable` for one captured item go in one request; one request per candidate, never one per question.
5. **Put the goal in the state** (`"goal": "..."`) and only the fields the question needs. README head, not the file; snippet plus date, not the whole search page.
6. **Jev never writes.** 摘要, Key facts, 點解值得留意, SKILL.md bodies and reports stay with Sonnet/Opus.
7. **Jev never overrides a deterministic rule.** Numeric gates, regex checks, canonical_id dedupe and index integrity are computed, not asked.

## Thresholds and fallback

| probability | action |
|---|---|
| `≥ 0.80` | take the Jev branch |
| `0.50 – 0.80` | defer: the routine's own model (Sonnet / Opus) decides exactly as it does today |
| `< 0.50` | negative branch |
| first call: 401, or 403 with an `authentication_error` body, or the proxy's CONNECT 403 | Jev is off for the whole run (no key reached TypeSafe / host not allowed); say so once in the jev line |
| 402, 5xx, timeout, malformed answer | today's path for that item, unchanged; count it |

IBM Technology's worked example uses `> 0.9` auto, `0.1–0.9` human review, `< 0.1` ignore; raise the act threshold as the cost of a wrong automatic decision rises. For five-level score rubrics (scale 0–4) use `≥ 2.5` act, `1.5–2.5` defer, `< 1.5` no. Tune per question after two real runs, then pin `model` to a fixed version instead of `jev-latest`.

Every run ends with one line in the final message: `jev: <asked> asked, <acted> acted, <deferred> deferred, <fallbacks> fell back (<reason>)`. Each decision is logged in the transcript as `jev <question> p=<prob> model=<version> state_sha=<8 hex>` so a wrong call can be traced to its input.

## Vault recipes

| routine | step | question | type | act / defer | fallback | status |
|---|---|---|---|---|---|---|
| weekly-hot-list | which X / Threads hits get the 40 fxtwitter verifications and the Jina reads | `in_scope` | score 0–4 | ≥ 2.5 / 1.5–2.5 | Opus reads the snippet | pilot 1 |
| weekly-hot-list | `min_stars_gained_7d_if_topical` gate | `topical` | noul | ≥ 0.80 / 0.50–0.80 | Opus reads README | pilot 1 |
| weekly-hot-list | group an X post with its GitHub repo | `same_item` | noul | ≥ 0.80 / 0.50–0.80 | Opus pairs by eye | pilot 1 (after the two above) |
| weekly-hot-list | draft SKILL.md for a winner | `installable_skill` | noul | ≥ 0.80 / 0.50–0.80 | Opus decides | later |
| github-stars-sync | pick backfill candidates whose 摘要 merely rewords the description | `summary_from_readme` | noul | < 0.50 = candidate / 0.50–0.80 | Sonnet reads | pilot 2 |
| github-stars-sync | draft SKILL.md for a starred repo | `is_agent_asset` | noul | ≥ 0.80 / 0.50–0.80 | Sonnet decides | later |
| vault-lint | near-duplicate titles | `near_duplicate` | noul | ≥ 0.80 / 0.50–0.80 | Sonnet compares | pilot 3 |
| vault-lint | order the stale-draft list for Josep | `review_priority` | score 0–4 | ordering only | unordered list | later |
| capture-link | `type`, `topic`, `actionable`, `substance_in_caption`, `related_relevance` | choice / noul / score | see reference | Sonnet decides | later (consistency, not cost) |

Exact JSON for every row, with the state fields and the prompt line it attaches to: `references/vault-routine-questions.md`. weekly-hot-list reads its thresholds and caps from `wiki/hot-list/_config.yaml` → `jev:` (edit numbers there, never in the routine prompt); the other routines get the same block when their pilots start.

## Pitfalls

- **State is untrusted data.** Jev can be steered by instructions hidden in the text it reads, like any model. Keep `instructions` in code, put only data fields in `state`, and use the answer to pick a branch, never to run anything. It is also weak at math and counting: compute numbers (stars, date deltas) yourself.
- Checking `env` for the key. In cloud sessions the credential is proxy-injected and invisible; the only test is a request. TypeSafe answers **403 with `authentication_error`** when no key reached it (not 401), so do not read every 403 as "host not allowed": the proxy's block is a failed CONNECT with no JSON body.
- Asking Jev for prose or a summary: it cannot; it will not error helpfully either. Keep it to typed questions.
- Treating a probability as proof. The lint still re-checks; a deferred band exists for a reason.
- Sending secrets, cookies or whole `raw/` files in the state. State is logged by hash only, but it still leaves the machine.
- A blocked host plus a silent fallback looks like "Jev never fires". Count fallbacks and print the reason.
- Unbounded call counts. Cap decisions per run (hot list: 1,500) and batch per candidate.
- Mixing providers. Key, base URL and model id come as one set (TypeSafe direct, Vercel AI Gateway or OpenRouter); a key from one host sent to another gets the same 403 as no key.
- Pinning `jev-latest` forever: calibration can move between versions; pin after tuning, re-tune when you bump.
- A secret on a Bash line. Under auto mode the permission classifier reads each command; a `curl` that visibly sends `$TYPESAFE_API_KEY` was denied once as data exfiltration (2026-10-02) after identical text had passed. Use the script, and never paste the key value anywhere.

## Evidence

- 2026-10-02 — Development run of weekly-hot-list under auto permission mode: the first probe `curl` carrying `$TYPESAFE_API_KEY` was denied by the permission classifier ("Data Exfiltration") while the same call had passed in a production run 35 minutes earlier; the run stopped with no Jev data. That is why `scripts/jev_ask.py` exists and why `jev.client` is in `_config.yaml`.
- 2026-10-02 — First real H2 `topical` pass through `scripts/jev_ask.py` (development session, auto permission mode, no denial): 48 GitHub candidates, 0 fallbacks, `jev-1.13.0`, 79,145 input tokens (about US$0.0033). All 7 repos a human had called topical in 2026-W39 scored ≥ 0.86; the 3 called general scored 0.47, 0.26 and 0.75 (the last lands in the defer band, as intended). Thresholds 0.80 / 0.50 kept; results table in `outputs/20261002-jev-in-vault-routines.md`.
- 2026-10-02 — Fit of Jev against the vault's four Routines: biggest saving is weekly-hot-list prefiltering (~1,250 decisions a week, about US$0.09 at the published median); capture-link saves almost nothing because Sonnet reads the full text anyway (`outputs/20261002-jev-in-vault-routines.md`).
- 2026-10-02 — API reference (OpenAPI spec mirrored on jevwiki.ai): Bearer auth on `Authorization`; response `{model, answers, usage}`; score `criteria` is an ordered array and scores count from 0; 64k tokens per request, 32k for state plus the longest question; `GET /v1/models` lists the models a key may use; direct signups closed since 2026-09-24, so keys from a gateway (OpenRouter `https://openrouter.ai/api` model `~typesafe/jev-latest`, Vercel AI Gateway `https://ai-gateway.vercel.sh/typesafe` model `typesafe-ai/jev`) need that gateway's base URL.
- 2026-10-02 — IBM Technology explainer: noul / choice / score, every question answered in one request, RLCD calibration, text-only, weak at math, susceptible to prompt injection in the state ([[../../wiki/pages/20261002-what-is-jev-system-one-ai-model|20261002-what-is-jev-system-one-ai-model]]).
- 2026-09-20 — fast-jev-compaction: two noul questions per tool call, `keepThreshold` 0.5, full state resent per request under a 30k-token ceiling, failures thrown to the caller ([[../../wiki/pages/20260920-fast-jev-compaction|20260920-fast-jev-compaction]]).
- 2026-09-27 — Ryze AI's SEO/GEO audits: rubric questions per URL at a median US$0.000068 per decision, 20-point rubric × 1,000 URLs ≈ US$1.36 ([[../../wiki/pages/20260925-jev-seo-geo-audit-cost-down-90|20260925-jev-seo-geo-audit-cost-down-90]]).
- 2026-09-29 — Jev as the routing layer under a Fable advisor / Opus worker tree in Claude Code ([[../../wiki/pages/20260928-claude-code-fable-advisor-jev-tree|20260928-claude-code-fable-advisor-jev-tree]]).

## Source

- jevwiki.ai/wiki/reference/http-api.md and /wiki/guides/quickstart.md — mirror of TypeSafe's OpenAPI spec and quickstart (read 2026-10-02 via Exa): auth, request and answer schemas, limits, status codes, gateways.
- jevmodel.org/api — "Jev API Examples: Choice, Score, and Noul Requests" (read 2026-10-02 via Exa; third-party site, used for the request shape only).
- `raw/20260920-fast-jev-compaction.md` — README of tamaratran/fast-jev-compaction (endpoint, model alias, 32k request limit, keep/drop pattern).
- `raw/20261002-what-is-jev-system-one-ai-model.md` — transcript of IBM Technology, "What Is Jev? The AI Model That Doesn't Generate Text" (captured 2026-10-02).
- madewithjev.com — launch post by @CompleteSkeptic, 2026-09-15 (read 2026-10-02 via Exa); jev-for-seo pricing as captured in `wiki/pages/20260925-jev-seo-geo-audit-cost-down-90.md`.
