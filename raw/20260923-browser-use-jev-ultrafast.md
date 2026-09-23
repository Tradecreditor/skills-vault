---
source_url: "https://github.com/browser-use/jev-ultrafast"
captured_at: "2026-09-23T01:18:14Z"
captured_by: "routine:weekly-hot-list"
reader_used: "exa web_fetch_exa"
---

# browser-use/jev-ultrafast

Fastest and cheapest web agent

- Stars: 18079
- Forks: 1163
- Watchers: 18079
- Open issues: 117
- License: MIT License
- Homepage: https://browser-use.com
- Default branch: main
- Created: 2026-09-16T21:30:12Z

## Languages

- CSS
- HTML
- JavaScript
- Python

## Top Contributors

- gregpr07 (3 contributions)

---

## README

# Jev Ultrafast ⚡

**A browser agent with a dynamic, indexed action space.**

Give it one goal. TypeSafe's Jev picks an operation and an element. A small LLM writes text only when the operation is `TYPE_TEXT`.

**Zürich → London on Google Flights in 7.1 seconds.** One natural-language goal, actual text generation, and loading waits included.

## The action space

Every observation produces a new element table:

```text
[1] button    Change ticket type · Round trip
[2] combobox  Where from?        · San Francisco
[3] combobox  Where to?          · empty
[4] textbox   Departure          · empty
...
```

The operations are `CLICK`, `TYPE_TEXT`, `SELECT`, `SCROLL_UP`, `SCROLL_DOWN`, `WAIT`, `DONE`, and `BLOCKED`. Only supported operations and targets are offered. Two decisions (operation + target) resolve in one TypeSafe network round trip.

There are no site-specific action scripts or prepared field strings in the policy. The Flights example supplies a goal and independently verifies the outcome.

## Try it

```bash
git clone https://github.com/browser-use/jev-ultrafast.git
cd jev-ultrafast
uv sync
cp .env.example .env
# Add TYPESAFE_API_KEY and TEXT_MODEL_API_KEY.
uv run jev
```

Open http://127.0.0.1:8766 and click Start demo → Run automatically.

## Evidence and limits

The current video is a 7,073 ms Google Flights run. In six alternating runs with identical models and settings, both versions passed 3/3. Median task time went from 9.450 s → 7.092 s (25% reduction); median browser protocol calls went from 1,092 → 101 (90.8% fewer). This is three repeats of one task on one browser profile, not a general reliability benchmark.

The DOM reader handles common HTML and ARIA controls, not the full accessible-name specification. Shadow roots, frames, canvas, uploads, pop-up tabs, nested scrolling, and arbitrary keyboard widgets remain outside this MVP.

---

## Verified engagement (source-of-record numbers)

GitHub (mcp__github__search_repositories / web_fetch_exa on github.com, live 2026-09-23T01:1xZ):
- stargazers_count: 18079, forks_count: 1163, open_issues_count: 117
- created_at: 2026-09-16T21:30:12Z (7 days old at time of capture)

X / fxtwitter (api.fxtwitter.com/gregpr07/status/2100411066966749359):
- author: @gregpr07 (Gregor Zunic, founder @browser_use), 30,607 followers, verified
- posted: 2026-09-17T02:26:36Z
- text: "Breaking: Browser Use + Jev = Ultrafast ⚡ Findings flights took 7s and cost only $0.0039 🤯 ..."
- likes: 9046 · retweets: 650 · replies: 282 · quotes: 323 · bookmarks: 9908 · views: 3,149,666
