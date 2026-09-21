---
title: "OpenCLI"
slug: jackwener--OpenCLI
type: repo
status: draft
source_url: "https://github.com/jackwener/OpenCLI"
source_platform: github
published: "2026-03-14"
captured_at: "2026-09-19T11:09:28.036140Z"
captured_by: "routine:github-stars-sync"
canonical_id: "github:jackwener/OpenCLI"
engagement: "stars=29456 forks=2875"
tags: ["ai-agent", "ai-agents", "ai-tools", "browser-automation", "browser-use", "cli", "playwright"]
related: []
needs_manual_text: false
---
## 摘要

OpenCLI 將網站、瀏覽器 session、Electron 桌面程式同本機工具全部變做一個統一、確定性(deterministic)嘅 CLI 介面,俾人類同 AI agent 一齊用。三種主要玩法:(1)用內建 adapter 直接攞 Bilibili、知乎、小紅書、Reddit、HackerNews、Twitter/X 等 100+ 網站嘅資料;(2)裝 `opencli-browser` skill 落 Claude Code / Cursor,俾 AI agent 用你已登入嘅 Chrome session 直接操作任何網站(navigate、click、fill、extract);(3)自己用 `opencli-adapter-author` skill 一步步寫新 adapter。仲可以做 CLI hub,將 `gh`、`docker`、`longbridge` 呢類本機命令行工具統一喺同一個發現介面之下。

## Key facts

- **Repo**: [jackwener/OpenCLI](https://github.com/jackwener/OpenCLI)
- **Stars**: 29,456 | **Forks**: 2,875
- **Language**: JavaScript
- **License**: Apache License 2.0
- **Requires**: Node.js >= 20.18.1(或者裝 OpenCLIApp 桌面版)
- **Install**: `npm install -g @jackwener/opencli` + 裝 Chrome Web Store 嘅 Browser Bridge extension + `opencli doctor` 驗證
- **裝 agent skills**: `npx skills add jackwener/opencli`(或者只裝某個 skill,例如 `--skill opencli-browser`)
- **Topics**: ai-agent, ai-agents, ai-tools, browser-automation, browser-use, cli, playwright

## 點解值得 star

將「攞網站資料」呢件事拆做三層(內建 adapter / AI agent 即場操作瀏覽器 / 自己寫新 adapter),仲提供一套完整嘅 skill 套件(`opencli-browser`、`opencli-adapter-author`、`opencli-autofix` 等)俾 agent 用,skill 拆分粒度同呢個 vault 收藏嘅其他 agent-skill 項目(例如 Agent-Reach)有得直接比較。用「你已登入嘅瀏覽器」嚟做自動化,對唔想成日重新登入嘅場景(小紅書、LinkedIn 呢類要登入先睇到資料嘅網站)幾實用。

## Source

- URL: https://github.com/jackwener/OpenCLI
- Created: 2026-03-14
- Reader: routine:github-stars-sync

## Related
