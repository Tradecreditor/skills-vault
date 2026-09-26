---
title: "gpt-researcher"
slug: assafelovic--gpt-researcher
type: repo
status: draft
source_url: "https://github.com/assafelovic/gpt-researcher"
source_platform: github
author: "Assaf Elovici"
published: "2023-05-12"
captured_at: "2026-09-20T00:00:00Z"
captured_by: "routine:github-stars-sync"
canonical_id: "github:assafelovic/gpt-researcher"
engagement: "stars=29542 forks=4018"
tags: [agent, ai, automation, deepresearch, llms, mcp, research]
related: [langchain-ai--open_deep_research, bytedance--deer-flow, THU-MAIC--OpenMAIC]
needs_manual_text: false
---

## 摘要
開源嘅 deep research agent，可以同時查網上同本地文件，產出有引用來源、詳細而中立嘅研究報告。架構分 planner 同 execution 兩層：planner 將問題拆成一組子問題，execution agent 逐條去搵資料並記低出處，最後 publisher 將所有發現整合成報告。一份報告會聚合 20 個以上來源、可以超過 2,000 字，支援 PDF／Word 匯出、圖片抓取同篩選。設計上針對幾個具體痛點：LLM 訓練資料過時會幻覺、token 上限寫唔到長報告、來源太少或者有偏。
## Key facts
- Language: Python
- License: Apache 2.0
- Created: 2023-05-12
- Last pushed: 2026-08-27
- Stars: 29,542
- Forks: 4,018
- Homepage: https://gptr.dev
- MCP server available

## 點解值得留意
可以直接當 Claude Skill 裝：`npx skills add assafelovic/gpt-researcher`，裝完 Claude 對話入面就用得。平行化跑多個 agent 令速度同穩定性都好過串行做法。
## Source
GitHub repository: https://github.com/assafelovic/gpt-researcher
Author: Assaf Elovici
Captured: 2026-09-20

## Related

- [[langchain-ai--open_deep_research|open_deep_research]] — 同屬開源 deep research agent，可以比較 planner/execution 架構設計。
- [[bytedance--deer-flow|deer-flow]] — deer-flow 由 deep research 起步演化成通用 harness，可對照 gpt-researcher 點樣留喺 research 本業。
- [[THU-MAIC--OpenMAIC|OpenMAIC]] — 同屬多 agent 協作平台。
