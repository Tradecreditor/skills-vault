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
| `score` | fractional position on an ordered 2–10 level rubric you describe | rank: relevance to scope, review priority |

Jev is trained with RLCD (reinforcement learning for calibrated decisions), so a 0.8 is right about 80% of the time — that is what makes a threshold meaningful. Several questions in one request share the state's token cost and are answered together. Only input tokens are billed; the published median is about US$0.000068 per decision. In the vault's tiering this sits **below Sonnet**: Jev judges, Sonnet executes, Opus/Fable plans and reviews (see [[../model-tiering/SKILL|model-tiering]], Part C). Where it pays in this vault and where it does not: `outputs/20261002-jev-in-vault-routines.md`.

## Prerequisites

- A TypeSafe API key. Laptop: `TYPESAFE_API_KEY` in your shell profile, sent as `Authorization: Bearer`. Cloud Routines and sessions: an **API credential** on the environment (Add credential → Name `TYPESAFE_API_KEY`, type Bearer, Allowed websites `api.typesafe.ai`, header `Authorization: Bearer <key>`). There the proxy injects the header on every request to that host and the variable is usually not visible in the shell (the vault's `SUPADATA_KEY` behaves the same), so code must not require it: send the header when the variable is set, otherwise send none, and read a 401 as "no credential". Never in the repo, never in `raw/` or a page.
- The host `api.typesafe.ai` must be reachable. Saving the API credential auto-creates the allow rule for it; listing it in the environment's allowed domains as well (routines/README.md, Step 0) is belt and braces; a Claude Code cloud sandbox without it answers `CONNECT tunnel failed, response 403` and every call falls back silently, so always count fallbacks in the final message.
- Text-only state, about 32k tokens per request. Trim: README first 100 lines, post text plus metadata, not a whole `raw/` file.
- Do not use third-party mirrors such as `jevmodel.org/v1/systemone`; the official endpoint is `https://api.typesafe.ai/v1/systemone`.

## Request shape

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

Python, no dependencies, with a sandbox switch (`JEV_FAKE=<path.json>` returns canned answers so the surrounding logic can be tested with no key and no network — `references/jev-fake.example.json` is a starting fixture):

```python
import hashlib, json, os, urllib.error, urllib.request, uuid

JEV_URL = os.environ.get("JEV_URL", "https://api.typesafe.ai/v1/systemone")

def ask_jev(state, questions, model="jev-latest", timeout=10):
    """Return {name: float | {label: float}} — noul/score give a float, choice gives label -> probability.
    Raises on 401 (no credential), 403 (host not allowed), transport or other HTTP errors: the caller decides the fallback."""
    fake = os.environ.get("JEV_FAKE")
    if fake:
        canned = json.load(open(fake, encoding="utf-8"))
        return {q: canned[q] for q in questions}
    key = os.environ.get("TYPESAFE_API_KEY")          # usually unset in cloud sessions: the proxy injects the header
    headers = {"Content-Type": "application/json", "Idempotency-Key": str(uuid.uuid4())}
    if key:
        headers["Authorization"] = f"Bearer {key}"
    body = json.dumps({"state": state, "model": model, "questions": questions}).encode()
    req = urllib.request.Request(JEV_URL, data=body, method="POST", headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            resp = json.load(r)
    except urllib.error.HTTPError as e:
        if e.code == 401: raise RuntimeError("jev off: no credential on this environment (401)") from e
        if e.code == 403: raise RuntimeError("jev off: api.typesafe.ai not allowed by the network policy (403)") from e
        raise
    out = {}
    answers = resp.get("answers") or resp.get("questions") or resp      # field name unverified: confirm in the Playground once
    for name, q in questions.items():
        a = answers[name]
        if isinstance(a, dict):
            a = a.get("probability", a.get("score", a.get("probabilities", a)))
        out[name] = a
    sha = hashlib.sha1(json.dumps(state, sort_keys=True, ensure_ascii=False).encode()).hexdigest()[:8]
    for name, a in out.items():
        print(f"jev {name} p={a if not isinstance(a, dict) else max(a, key=a.get)} model={resp.get('model', model)} state_sha={sha}")
    return out

def band(p, act=0.80, defer=0.50):
    """act: take the Jev branch · defer: hand the decision to the routine's own model · no: negative branch."""
    return "act" if p >= act else "defer" if p >= defer else "no"
```

The response field names above are a best guess from secondary sources (official docs were unreachable when this skill was written). Before the first live run, send one noul, one choice and one score in the TypeSafe Playground and fix the `answers` line to match.

## Question design rules

1. **One proposition per noul.** "This repo is an MCP server" — not "this repo is an MCP server or a plugin and worth a skill".
2. **Choice criteria are the vault's own definitions.** Copy the label meanings from `CLAUDE.md` (type rules, topic vocabulary) so Jev and the lint agree; `references/vault-routine-questions.md` holds them verbatim.
3. **Score = a named, ordered rubric**, 2–10 levels, each level one sentence. Threshold the fractional result in code.
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
| 401 or 403 on the first call | Jev is off for the whole run (no credential / host not allowed); say so once in the jev line |
| 402, 5xx, timeout, malformed answer | today's path for that item, unchanged; count it |

IBM Technology's worked example uses `> 0.9` auto, `0.1–0.9` human review, `< 0.1` ignore; raise the act threshold as the cost of a wrong automatic decision rises. For `score 1–5` rubrics use `≥ 3.5` act, `2.5–3.5` defer, `< 2.5` no. Tune per question after two real runs, then pin `model` to a fixed version instead of `jev-latest`.

Every run ends with one line in the final message: `jev: <asked> asked, <acted> acted, <deferred> deferred, <fallbacks> fell back (<reason>)`. Each decision is logged in the transcript as `jev <question> p=<prob> model=<version> state_sha=<8 hex>` so a wrong call can be traced to its input.

## Vault recipes

| routine | step | question | type | act / defer | fallback | status |
|---|---|---|---|---|---|---|
| weekly-hot-list | which X / Threads hits get the 40 fxtwitter verifications and the Jina reads | `in_scope` | score 1–5 | ≥ 3.5 / 2.5–3.5 | Opus reads the snippet | pilot 1 |
| weekly-hot-list | `min_stars_gained_7d_if_topical` gate | `topical` | noul | ≥ 0.80 / 0.50–0.80 | Opus reads README | pilot 1 |
| weekly-hot-list | group an X post with its GitHub repo | `same_item` | noul | ≥ 0.80 / 0.50–0.80 | Opus pairs by eye | pilot 1 (after the two above) |
| weekly-hot-list | draft SKILL.md for a winner | `installable_skill` | noul | ≥ 0.80 / 0.50–0.80 | Opus decides | later |
| github-stars-sync | pick backfill candidates whose 摘要 merely rewords the description | `summary_from_readme` | noul | < 0.50 = candidate / 0.50–0.80 | Sonnet reads | pilot 2 |
| github-stars-sync | draft SKILL.md for a starred repo | `is_agent_asset` | noul | ≥ 0.80 / 0.50–0.80 | Sonnet decides | later |
| vault-lint | near-duplicate titles | `near_duplicate` | noul | ≥ 0.80 / 0.50–0.80 | Sonnet compares | pilot 3 |
| vault-lint | order the stale-draft list for Josep | `review_priority` | score 1–5 | ordering only | unordered list | later |
| capture-link | `type`, `topic`, `actionable`, `substance_in_caption`, `related_relevance` | choice / noul / score | see reference | Sonnet decides | later (consistency, not cost) |

Exact JSON for every row, with the state fields and the prompt line it attaches to: `references/vault-routine-questions.md`. weekly-hot-list reads its thresholds and caps from `wiki/hot-list/_config.yaml` → `jev:` (edit numbers there, never in the routine prompt); the other routines get the same block when their pilots start.

## Pitfalls

- **State is untrusted data.** Jev can be steered by instructions hidden in the text it reads, like any model. Keep `instructions` in code, put only data fields in `state`, and use the answer to pick a branch, never to run anything. It is also weak at math and counting: compute numbers (stars, date deltas) yourself.
- Checking `env` for the key. In cloud sessions the credential is proxy-injected and invisible; the only test is a request, and 401 is the answer "no credential".
- Asking Jev for prose or a summary: it cannot; it will not error helpfully either. Keep it to typed questions.
- Treating a probability as proof. The lint still re-checks; a deferred band exists for a reason.
- Sending secrets, cookies or whole `raw/` files in the state. State is logged by hash only, but it still leaves the machine.
- A blocked host plus a silent fallback looks like "Jev never fires". Count fallbacks and print the reason.
- Unbounded call counts. Cap decisions per run (hot list: 1,500) and batch per candidate.
- Mixing endpoints. `api.typesafe.ai` with `TYPESAFE_API_KEY`; nothing else.
- Pinning `jev-latest` forever: calibration can move between versions; pin after tuning, re-tune when you bump.

## Evidence

- 2026-10-02 — Fit of Jev against the vault's four Routines: biggest saving is weekly-hot-list prefiltering (~1,250 decisions a week, about US$0.09 at the published median); capture-link saves almost nothing because Sonnet reads the full text anyway (`outputs/20261002-jev-in-vault-routines.md`).
- 2026-10-02 — IBM Technology explainer: noul / choice / score, every question answered in one request, RLCD calibration, text-only, weak at math, susceptible to prompt injection in the state ([[../../wiki/pages/20261002-what-is-jev-system-one-ai-model|20261002-what-is-jev-system-one-ai-model]]).
- 2026-09-20 — fast-jev-compaction: two noul questions per tool call, `keepThreshold` 0.5, full state resent per request under a 30k-token ceiling, failures thrown to the caller ([[../../wiki/pages/20260920-fast-jev-compaction|20260920-fast-jev-compaction]]).
- 2026-09-27 — Ryze AI's SEO/GEO audits: rubric questions per URL at a median US$0.000068 per decision, 20-point rubric × 1,000 URLs ≈ US$1.36 ([[../../wiki/pages/20260925-jev-seo-geo-audit-cost-down-90|20260925-jev-seo-geo-audit-cost-down-90]]).
- 2026-09-29 — Jev as the routing layer under a Fable advisor / Opus worker tree in Claude Code ([[../../wiki/pages/20260928-claude-code-fable-advisor-jev-tree|20260928-claude-code-fable-advisor-jev-tree]]).

## Source

- jevmodel.org/api — "Jev API Examples: Choice, Score, and Noul Requests" (read 2026-10-02 via Exa; third-party site, used for the request shape only).
- `raw/20260920-fast-jev-compaction.md` — README of tamaratran/fast-jev-compaction (endpoint, model alias, 32k request limit, keep/drop pattern).
- `raw/20261002-what-is-jev-system-one-ai-model.md` — transcript of IBM Technology, "What Is Jev? The AI Model That Doesn't Generate Text" (captured 2026-10-02).
- madewithjev.com — launch post by @CompleteSkeptic, 2026-09-15 (read 2026-10-02 via Exa); jev-for-seo pricing as captured in `wiki/pages/20260925-jev-seo-geo-audit-cost-down-90.md`.
