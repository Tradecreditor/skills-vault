---
title: "OpenDots — CopilotKit's open-source, self-hosted template for always-on AI coworkers"
slug: 20261005-opendots-copilotkit-ai-coworkers
type: repo
status: draft
source_url: "https://github.com/CopilotKit/OpenDots"
source_platform: github
author: "CopilotKit"
published: "2026-09-29"
captured_at: "2026-10-05T08:19:24Z"
captured_by: "routine:weekly-hot-list"
canonical_id: "github:CopilotKit/OpenDots"
engagement: "stars=3325 forks=442; X launch post likes=6035 reposts=570 views=1031751"
tags: [hot-list, 2026-W40, ai-agents, ag-ui, copilotkit, computer-use, slack, self-hosted]
related: [hot-list/2026-W40]
needs_manual_text: false
---

## 摘要

OpenDots 係 CopilotKit 喺 OpenAI 2026-09-29 推出 Dots 之後兩日開源（MIT）嘅對應版本：一個可以自己 host 嘅「always-on AI 同事」template。每個 Dot 有自己名、角色、指示同權限，可以有獨立電腦（browser、檔案、terminal，經 OpenBot container supervisor），喺 web、手機、語音通話同 Slack 之間延續同一段對話；工作成果落喺可編輯嘅 Spaces / Pages，存檔前可以用 human-in-the-loop 卡片批准。佢用 AG-UI 協議，可以接任何 agent harness 同 OpenAI-compatible model。項目自稱 alpha、單一擁有者，Slack 同語音委派仲未完成連線測試。佢係 2026-W40 hot list 嘅 GitHub + X 雙平台入選項目。

## Key facts

- **What**: self-hostable template (not a hosted product), MIT, alpha. Built on CopilotKit, AG-UI and CopilotKit Intelligence (Threads, Channels SDK).
- **Features (README)**: specialist Dots with per-Dot browser/file/shell/memory permissions; Dot computers via OpenBot (persistent browser profile and files, human takeover); Spaces and Pages editor; review-before-save cards (Approve & save / Decline); realtime calls with a separate compute agent; Slack via Channels SDK with allowlists; recurring schedules.
- **Requirements**: Node.js 24 and npm; calls, Slack and Dot computers each need their own setup guide; an unconfigured template does not execute commands on the host.
- **Numbers**: GitHub 3,325 stars / 442 forks on 2026-10-05 (created 2026-09-29, total = in-window gain). X launch post [@ataiiam 2105710796198322659](https://x.com/ataiiam/status/2105710796198322659): 6,035 likes, 570 reposts, 1,031,751 views (fxtwitter, 2026-10-05). CopilotKit's own announcement 2105714964023685148: 407 likes.
- **Naming**: unrelated to `feder-cr/dots` (stealth browser agent), also trending this week.

## 點解值得留意

- Hot list 2026-W40 第二名（heat 0.94，GitHub topical gate + X 單帖 gate），詳見 [[hot-list/2026-W40|hot-list/2026-W40]]。
- 「每個 agent 有自己電腦 + 存檔前人手批准」係可以抄落 Jeff 自己 agent 項目嘅模式；比 OpenAI Dots 更易 self-host 同改。
- 產品 template 而唔係 procedure，所以冇 draft SKILL.md。

## Source

- https://github.com/CopilotKit/OpenDots — CopilotKit — 2026-09-29
- X: https://x.com/ataiiam/status/2105710796198322659 (2026-10-01)
- Reader: raw.githubusercontent.com README (curl) + GitHub search API (connector) + fxtwitter (curl); raw text in `raw/20261005-opendots-copilotkit-ai-coworkers.md`.

## Related

- [[hot-list/2026-W40]]
- [[pages/20261002-zcode-zai-harness]]
