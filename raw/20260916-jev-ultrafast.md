---
slug: 20260916-jev-ultrafast
source_url: "https://github.com/browser-use/jev-ultrafast"
canonical_id: "github:browser-use/jev-ultrafast"
fetched_at: "2026-09-22T02:15:00Z"
reader: "github-connector+exa"
---

## Repo metadata (mcp__github__search_repositories, fetched 2026-09-22T02:15:00Z)

```json
{
  "full_name": "browser-use/jev-ultrafast",
  "description": "Fastest and cheapest web agent",
  "homepage": "https://browser-use.com",
  "created_at": "2026-09-16T21:30:12Z",
  "pushed_at": "2026-09-18T16:28:35Z",
  "language": "Python",
  "license": "MIT",
  "stargazers_count": 15806,
  "forks_count": 988,
  "open_issues_count": 108,
  "html_url": "https://github.com/browser-use/jev-ultrafast"
}
```

## README.md (raw.githubusercontent.com, main branch)

# Jev Ultrafast ⚡

A browser agent with a dynamic, indexed action space. Give it one goal. TypeSafe's Jev picks an operation
(`CLICK`, `TYPE_TEXT`, `SELECT`, `SCROLL_UP`, `SCROLL_DOWN`, `WAIT`, `DONE`, `BLOCKED`) and an element from a
freshly-indexed element table on every observation. A small LLM only writes free text when the operation is
`TYPE_TEXT`; every other decision skips text generation entirely, which is why it moves the way it does — one
network round trip covers both the operation and the target.

Headline demo: found Zürich → London flights on Google Flights in 7.1 seconds end-to-end (real text
generation, real loading waits, independently outcome-verified — not a canned script). In six alternating
runs on the same models/settings, median task time went 9.450s → 7.092s (-25%) and median browser protocol
calls went 1,092 → 101 (three repeats of one task, not a general benchmark).

Install / try:
```bash
git clone https://github.com/browser-use/jev-ultrafast.git
cd jev-ultrafast
uv sync
cp .env.example .env   # needs TYPESAFE_API_KEY and TEXT_MODEL_API_KEY
uv run jev
```
Library use:
```python
from jev_ultrafast import Agent
with Agent(url, "Find one-way flights from Zurich to London ...") as agent:
    for state in agent.run():
        print(state["elapsed_ms"], state["status"])
```
Depends on Browser Use's own `browser-harness` (Chrome remote-debugging bridge) and TypeSafe's Jev API
(the same decision-model provider behind last week's winner, `tamaratran/fast-jev-compaction`).
Limits stated by the authors: MVP, not a general reliability benchmark; no shadow-DOM/iframe/canvas/upload
support yet; `DONE` still needs independent outcome verification, which the demo itself performs.

## X: launch post (fxtwitter-verified, fetched 2026-09-22T02:10:00Z)

`https://api.fxtwitter.com/gregpr07/status/2100411066966749359`
- Author: Gregor Zunic (@gregpr07), founder of Browser Use, 30,505 followers, verified individual.
- Posted: 2026-09-17T02:26:36Z (inside the 2026-09-15..21 window)
- Text: "Breaking: Browser Use + Jev = Ultrafast ⚡ Findings flights took 7s and cost only $0.0039 🤯 > new
  action space every step > DOM state space > small LLM fallback to type (this video is at 1x speed btw)
  Built a tiny open source browser agent. try it below ↓"
- Metrics: likes=8,956 · retweets=643 · replies=276 · quotes=320 · bookmarks=9,811 · views=3,070,384

Two corroborating posts found (not independently gate-verified, cited for context only):
- @VaibhavSisinty: "Jev launched 48 hours ago. What people are building with it is genuinely insane... $42
  per billion tokens. Output tokens free. 200x faster than LLMs." (x.com/VaibhavSisinty/status/2100619641827836222)
- @davecyen: "Browser/computer use might be the perfect application for Jev" (x.com/davecyen/status/2100423988707303676)
