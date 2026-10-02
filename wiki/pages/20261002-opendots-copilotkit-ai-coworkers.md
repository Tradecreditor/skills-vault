---
title: "OpenDots — CopilotKit's self-hostable always-on AI coworkers (open-source OpenAI Dots)"
slug: 20261002-opendots-copilotkit-ai-coworkers
type: repo
status: draft
source_url: "https://github.com/CopilotKit/OpenDots"
source_platform: github
author: "CopilotKit"
published: "2026-09-29"
captured_at: "2026-10-02T23:22:00Z"
captured_by: "claude-code-cloud"
canonical_id: "github:CopilotKit/OpenDots"
engagement: "stars=1428 forks=172 x_likes=4548 x_reposts=429 x_views=786864 (@ataiiam)"
tags: [hot-list, 2026-W40, agent-platforms, ai-coworkers, copilotkit, ag-ui, slack, voice, template, typescript]
related: [hot-list/2026-W40]
needs_manual_text: false
---

## 摘要

OpenDots 係 CopilotKit 推出嘅開源 template，對應 OpenAI 嘅 dots：每個「Dot」係一個長駐 AI coworker，有自己嘅名字、角色、指令同工具權限，可以有自己一部電腦（用 OpenBot 嘅 container supervisor，瀏覽器 profile 同檔案跨重啟保留），喺 Space 入面寫同儲存文件，經 Channels SDK 入 Slack thread，亦可以語音通話（WebRTC 語音 + 另一個 compute agent 並行做長任務）。前後端用 AG-UI 串流訊息、tool call 同狀態，human-in-the-loop 卡片喺儲存前暫停等人批准。強調係 template 唔係 hosted 產品，自己跑自己配置；alpha 狀態。2026-09-29 建立，10-01 由 @ataiiam 喺 X 公佈（4,548 likes、78.7 萬 views），10-02 有 1,429 stars。

## Key facts

- **What**: open-source template for persistent AI agents ("Dots") with Spaces, specialist Dots, per-Dot computers (OpenBot), Slack via Channels SDK, realtime calls, background work, memory and Automatic Learning; MIT, alpha.
- **Stack**: CopilotKit React SDK + runtime, AG-UI for agent↔UI streaming, TanStack AI for model streaming, Intelligence / Threads for durable conversations, OpenAI-compatible model provider.
- **Run**: Node.js 24 + npm; `git clone https://github.com/CopilotKit/OpenDots.git && cd OpenDots && npm ci && cp .env.example .env && npm run dev` → http://127.0.0.1:5173; `docs/SETUP.md` for Slack, calls, browser service, Docker; `docs/COMPUTERS.md` for Dot computers.
- **X (fxtwitter, 2026-10-01)**: @ataiiam 4,548 likes / 429 reposts / 786,864 views (quoting OpenAI's dots launch); @tannerlinsley 479 likes; @CopilotKit 395 likes / 49 reposts / 33,151 views.
- **GitHub (2026-10-02)**: 1,428 stars, 172 forks, created 2026-09-29. Jev `topical` 0.82.

## 點解值得留意

Hot list 2026-W40（開發測試 run）入選第二位，亦係本週唯一過 X gate 嘅項目（三個作者各 ≥ 300 likes），詳見 [[hot-list/2026-W40|hot-list/2026-W40]]。GitHub 差 71 stars 先過 1,500 嘅 topical gate，過到就變雙平台 0.94。對 vault 嘅意義：係「開源 dots」嘅參考實作，agent 自己有電腦、Slack、語音同人批准卡片呢套 pattern，同 OpenMuse / OpenBot 一齊睇。

## Source

- https://github.com/CopilotKit/OpenDots — CopilotKit — 2026-09-29
- Reader: raw.githubusercontent.com README (curl); star/fork counts from the GitHub repos API through the Exa / Jina relay; X counts from fxtwitter. Raw text in `raw/20261002-opendots-copilotkit-ai-coworkers.md`. Captured by a Claude Code development run of the weekly-hot-list routine on 2026-10-02.

## Related

- [[hot-list/2026-W40]]
