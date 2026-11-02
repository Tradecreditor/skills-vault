---
title: "deepseek-ai/dsh-superagent-prototype — dsh-superagent: proactive coding agent that works a repo's issues and PRs"
slug: 20261102-dsh-superagent-proactive-coding-agent
type: repo
status: draft
source_url: "https://github.com/deepseek-ai/dsh-superagent-prototype"
source_platform: github
author: "deepseek-ai"
published: "2026-10-31"
captured_at: "2026-11-02T08:50:00Z"
captured_by: "routine:weekly-hot-list"
canonical_id: "github:deepseek-ai/dsh-superagent-prototype"
engagement: "stars=10205 forks=1043 (created 2026-10-31; 10169 at the W44 sweep)"
tags: [hot-list, 2026-W44, coding-agents, agent-harness, deepseek, dsh, dsh-plugin, github-automation, multi-agent]
related: [hot-list/2026-W44]
needs_manual_text: false
---

## 摘要

dsh-superagent 係 DeepSeek 喺 2026-10-31 開源嘅研究原型：一個「主動」coding agent，以 DeepSeek Harness（dsh）bundle 形式安裝，專門守住一個 GitHub repo。佢監聽 GitHub（可選 Feishu），有權限嘅人叫佢做嘢，佢就開一個 work item，喺自己嘅 agent session 同目錄入面做，再喺原本對話度回覆，例如開 PR；仲有一個 web panel 列出邊啲嘢要人處理。設計原則係「用最少嘅人類注意力，換最多價值」：只喺被叫或者團隊寫好嘅規則容許時先行動，只喺有人要行動時先出聲。README 明言係研究代碼、唔係官方產品，好多工程都係 coding agent 自己做。開源兩日已經過萬星，係 2026-W44 hot list 第一名。

## Key facts

- **What**: a proactive coding agent for one GitHub repository, packaged as a bundle for DeepSeek Harness (dsh). It listens to GitHub (and optionally Feishu), opens a work item per request, runs it in its own agent session and directory, and answers in the original thread (for example with a pull request). A web panel shows what needs a person.
- **Setup**: ask your coding agent "Read SETUP.md in this repository and set up dsh-superagent with me." It asks one question at a time, shows the plan, then installs and configures. Development: `pnpm check` (typecheck, tests, build). MIT, TypeScript.
- **Docs**: numbered `docs/000-philosophy.md` … `docs/008-cookbook.md` (domain model, authorization, execution, prompts, panel, deployment, architecture, adding a Source).
- **Caveat** (README): research prototype, not an official DeepSeek product; not identical to the internal version or to the article *Exploring Super-agent Design: Towards a More Autonomous Agent System*; some designs in the article are not implemented.
- **Numbers**: 10,169 stars at the W44 sweep (2026-11-02 ~08:10 UTC), 10,205 / 1,043 forks shortly after; created 2026-10-31, so its whole total is its gain. Clears the new-repo gate (10,000) and the gain gate (3,000).
- **X**: @lvwerra [2116634303073321237](https://x.com/lvwerra/status/2116634303073321237) (10-31) 2,475 likes / 252 reposts / 171,357 views (fxtwitter). Likes clear the X threshold but reposts and views do not, and no second author was verified, so no X gate.

## 點解值得留意

- 2026-W44 hot list 第一名（heat 0.80，GitHub 單平台），詳見 [[hot-list/2026-W44|hot-list/2026-W44]]。
- 佢係「agent 守 repo、人只處理要決定嘅嘢」呢個方向嘅官方參考實作，同上星期第一名 DeepSeek Harness 屬同一生態。
- 「少用人類注意力」嘅原則同呢個 vault 嘅 Routine 做法（有事先 notify、冇事就靜）一致，`docs/000-philosophy.md` 值得一讀。
- 研究代碼：要畀佢 GitHub 權限之前，先睇 `docs/002-authorization.md`。

## Source

- https://github.com/deepseek-ai/dsh-superagent-prototype — deepseek-ai — created 2026-10-31
- Reader: raw.githubusercontent.com README (curl), GitHub search API (`gh api`) for counts, api.fxtwitter.com for the @lvwerra post. Raw text in `raw/20261102-dsh-superagent-proactive-coding-agent.md`.

## Related

- [[hot-list/2026-W44]]
- [[pages/20261026-deepseek-harness-everything-is-a-plugin]]: the harness it runs on (W43 winner)
- [[pages/20261019-orca-ade-parallel-coding-agents]]: another way to run many coding agents in parallel
