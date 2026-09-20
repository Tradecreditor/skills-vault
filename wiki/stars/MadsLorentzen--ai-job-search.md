---
title: "ai-job-search"
slug: MadsLorentzen--ai-job-search
type: repo
status: draft
source_url: "https://github.com/MadsLorentzen/ai-job-search"
source_platform: github
author: "Mads Lorentzen"
published: "2026-03-18"
captured_at: "2026-09-20T23:06:50Z"
captured_by: "routine:github-stars-sync"
canonical_id: "github:MadsLorentzen/ai-job-search"
engagement: "stars=43470 forks=14927"
tags: [ai, ai-agents, career, claude-code, cover-letter, cv, interview-preparation, job-application, job-hunting, job-search, latex, resume]
related: []
needs_manual_text: false
---

## 摘要
呢個係一套建立喺 Claude Code 之上嘅 AI 求職自動化框架,作者原本係地球物理學家,喺 2025 年尾被裁咗之後自己攞呢套工具嚟搵工:透過 `/scrape` 搜尋多個求職網嘅職位、`/apply` 評分職位合適度並自動生成度身訂造嘅 LaTeX CV 同求職信(有第二個 agent 做 reviewer 覆核),再用 `/interview` 準備面試。作者話用咗呢套流程投咗 69 份申請,攞到 20 個第一輪面試,最終喺 2026 年 6 月拎到 AI 工程師 offer。核心工作流(自我建檔、職位評估、CV/求職信生成)係語言同國家無關嘅,但求職網搜尋 skill 目前係做丹麥市場,設計上可以換成自己地區嘅求職網。

## Key facts
- Language: Python (+ Claude Code skills/commands)
- License: MIT
- Created: 2026-03-18
- Last pushed: 2026-09-16
- Stars: 43,470
- Forks: 14,927
- Requires: Claude Code CLI, Python 3.10+, Bun, LaTeX (lualatex/xelatex)
- Core commands: `/setup`, `/scrape`, `/apply`, `/interview`, `/outcome`, `/rank`

## 點解值得留意
呢個 repo 本身唔止係一個 skill,而係一整套用 Claude Code commands + skills 組成嘅完整應用範例(`.claude/skills/job-application-assistant`、`job-scraper`、`upskill` 等),對於想學點樣用多個 skill/command 夾埋做一條完整 agentic workflow 嘅人嚟講,係一個好完整嘅實戰參考架構,尤其係 drafter-reviewer(生成再由第二個 agent 覆核)嘅設計模式值得參考落去自己嘅 skill 度。

## Source
GitHub repository: https://github.com/MadsLorentzen/ai-job-search
Author: Mads Lorentzen
Published: 2026-03-18
Reader used: raw README via Exa (web_fetch_exa)

## Related
