---
title: "browser-use"
slug: browser-use--browser-use
type: repo
status: draft
source_url: "https://github.com/browser-use/browser-use"
source_platform: github
author: "browser-use"
published: "2024-10-31"
captured_at: "2026-10-10T06:10:37Z"
captured_by: "routine:github-stars-sync"
canonical_id: "github:browser-use/browser-use"
engagement: "stars=117459 forks=12994"
tags: [ai-agents, browser-automation, playwright, python, llm]
related: []
needs_manual_text: false
---

## 摘要
browser-use 係一個讓 AI 代理像真人一樣操作瀏覽器嘅開源項目，可以自動搵空檔、揀日期時間、處理 CAPTCHA 甚至完成預約。README 提供三條使用路線：全託管雲端 API、俾 Claude Code／Codex 等代理用嘅 CLI（`browser-use skill install`），以及可以喺自己 Python 程式碼入面運行嘅開源函式庫。函式庫只需 `uv add browser-use`，用 `Agent(task=..., llm=...)` 就能跑，支援 OpenAI、Anthropic、Google、Ollama 等模型，亦有自家針對瀏覽器優化嘅 BU2 模型。另外仲有「Browser Use toolsets for Claude」整合，以及支援自訂工具、本機 Chrome 登入狀態同雲端 stealth 瀏覽器。

## Key facts
- Language: Python (>= 3.11); license MIT; last push 2026-10-09
- Install: `uv add browser-use`; CLI route: `browser-use skill install`
- Cloud browser from $0.02 per browser-hour; new signups get $15 credit
- Related repos: browser-harness, browser-harness-js, cloud SDK, video-use, macOS harness
- Stars 117k, forks 13k

## 點解值得留意
呢個係瀏覽器代理類別入面星數最高嘅項目之一，同 Jeff 已 star 嘅 Agent-Reach、OpenCLI、playwright-mcp 屬同一個「俾代理操作網頁」方向，可以互相比較。佢有現成嘅 Claude Code skill 同 Claude toolset 整合，容易接入 vault 嘅工作流程。要留意嘅係雲端瀏覽器同 BU2 模型要付費，登入狀態同 CAPTCHA 處理亦視乎網站而定。

## Source
- https://github.com/browser-use/browser-use — browser-use — created 2024-10-31 — reader: Exa (raw README)

## Related
- [[Panniantong--Agent-Reach]] · [[jackwener--OpenCLI]] · [[microsoft--playwright-mcp]]
