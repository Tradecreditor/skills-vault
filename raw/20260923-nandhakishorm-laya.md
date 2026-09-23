---
source_url: "https://github.com/NandhaKishorM/laya"
captured_at: "2026-09-23T01:18:14Z"
captured_by: "routine:weekly-hot-list"
reader_used: "exa web_fetch_exa"
---

# NandhaKishorM/laya

- Stars: 16609
- Forks: 1390
- Watchers: 16609
- Open issues: 122
- License: Apache License 2.0
- Default branch: main
- Created: 2026-09-18T04:46:33Z

## Languages

- Jupyter Notebook
- Python

## Top Contributors

- NandhaKishorM (53 contributions)
- (9 first-time contributors, 1 contribution each)

---

## README

**Multilingual, non-autoregressive System 1 decision engine.** Typed decisions over 100+ languages in a single forward pass — 33 ms — trained with reinforcement learning against strictly proper scoring rules (RLCD), with a router that picks the right checkpoint per request.

Laya evaluates typed questions (`choice`, `score`, `noul`) over any state (text, email, ticket or JSON document) in a single forward pass — 33 ms for one question, 7.2 ms/question batched, measured on a T4. No text generation, so nothing to parse and nothing to hallucinate.

Three checkpoints, and a `Router` that picks between them per request:

| | encoder | params | context | use it for |
|---|---|---|---|---|
| `laya` | ModernBERT-large | 421M | 512 | English |
| `laya-multilingual` | mmBERT-base | 322M | 1024 | 100+ languages, 2x faster |
| `laya-typed-decisions` | ModernBERT-large | 421M | 1024 | the typed-decisions workflows |

Install: `pip install laya` (Python 3.10+)

### Laya (with routing) vs Jev

| | Jev 1.13.0 | Laya (routed) | |
|---|---|---|---|
| typed-decisions, 2,000 decisions | 0.727 | 0.766 | +0.039 |
| AG News, 4 labels | 0.910 | 0.950 | +0.040 |
| DAIR Emotion, 6 labels | 0.480 | 0.595 | +0.115 |
| Banking77 (72 vs 77 labels) | 0.870 | 0.425 | Jev leads on >20 options |
| ECE (lower better) | 0.246 | 0.081 | 3x better (post-temperature) |
| p50 latency, 1 question | 236-276 ms | 32.8 ms | 7.8x faster |
| Languages usable | no published benchmark | 45 of 51 | — |
| Weights | closed API | Apache 2.0 | — |
| Cost | $0.042 / 1M tokens | $0 self-hosted | — |

Every Laya figure is what `Router().predict(...)` actually returns; Jev figures are third-party published, never measured by the Laya authors (no TypeSafe API access), so sample sizes and prompts differ. Laya's own README notes Jev leads on high-cardinality label spaces (>20 options at default settings).

### Origin story (from the author's own posts, Dev.to / Aetos.AI / Hacker News, 2026-09-18/19)

Author Nandakishor Mukkunnoth (ConvAI Innovations) states he published a non-autoregressive, PPO-trained decision-model architecture in an arXiv paper in March 2025 (arXiv:2503.23303) with open weights, dataset and a PyPI package, before TypeSafe AI's Jev launched in September 2026 with a similar non-autoregressive decision-model pitch but no technical paper, open weights or open dataset. Laya is presented as his open-source, rebuilt response, benchmarked head-to-head against Jev's published numbers. This priority dispute is contested in the linked Hacker News thread (id 49765348, 310+ comments as of capture) — some commenters call Laya's claims uncorroborated ("vibecoded... posted yesterday") and dispute that the two architectures are equivalent. Recorded here as reported by the author and discussed publicly; not independently verified by this vault.

---

## Verified engagement (source-of-record numbers)

GitHub (mcp__github__search_repositories / web_fetch_exa on github.com, live 2026-09-23T01:1xZ):
- stargazers_count: 16609, forks_count: 1390, open_issues_count: 122
- created_at: 2026-09-18T04:46:33Z (5 days old at time of capture)

Hacker News (news.ycombinator.com/item?id=49765348, via Zeli/gitnova secondary sources): 560 points, 310 comments (headline "Laya beats Jev with 33ms open-source decision engine"), 2026-09-19.

X / fxtwitter (api.fxtwitter.com/Nandakishorm1/status/2100451354670195196), author's own post quoting TypeSafe's Jev launch tweet:
- author: @Nandakishorm1 (Nandakishor M), 5,077 followers, verified
- posted: 2026-09-17T05:06:42Z
- likes: 140 · retweets: 21 · views: 12,132 (below this vault's X gate thresholds — Laya's spread was primarily via Hacker News/blog, not X)
