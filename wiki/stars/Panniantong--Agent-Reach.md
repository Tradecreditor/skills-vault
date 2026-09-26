---
title: "Agent-Reach"
slug: Panniantong--Agent-Reach
type: repo
status: draft
source_url: "https://github.com/Panniantong/Agent-Reach"
source_platform: github
author: "Panniantong"
published: "2026-02-24"
captured_at: "2026-09-19T11:09:28.035252Z"
captured_by: "routine:github-stars-sync"
canonical_id: "github:Panniantong/Agent-Reach"
engagement: "stars=83273 forks=7296"
tags: ["agent-infrastructure", "ai-agent", "ai-search", "automation", "bilibili", "claude-code", "cli", "cursor", "free-api", "llm-tools", "mcp", "python", "reddit-scraper", "twitter-scraper", "web-scraper", "xiaohongshu", "youtube-transcript"]
related: []
needs_manual_text: false
---
## 摘要

Agent-Reach 係一套「能力層」工具，畀 AI agent 一鍵裝上讀取全網嘅能力，唔使逐個平台自己踩坑裝配置。佢用「首選 + 備選」嘅有序後端路由：讀網頁用 Jina Reader、讀推特用 twitter-cli 加 OpenCLI 兜底、YouTube 用 yt-dlp、B站用 bili-cli、GitHub 用官方 gh CLI，全網搜索就經 mcporter 接 Exa。裝一次之後 `agent-reach doctor` 一條命令就話你知邊個渠道通、邊個要修。作者強調完全免費、開源，Cookie 只存本機唔上傳,亦都建議登入類平台用小號以防封號。

## Key facts

- **Repo**: [Panniantong/Agent-Reach](https://github.com/Panniantong/Agent-Reach)
- **Stars**: 83,273 | **Forks**: 7,296
- **Language**: Python
- **License**: MIT License
- **Install**: 對 AI agent 講一句「帮我安装 Agent Reach：https://raw.githubusercontent.com/Panniantong/agent-reach/main/docs/install.md」
- **Diagnose**: `agent-reach doctor`
- **Topics**: agent-infrastructure, ai-agent, ai-search, automation, bilibili, claude-code, cli, cursor, free-api, llm-tools, mcp, python, reddit-scraper, twitter-scraper, web-scraper, xiaohongshu, youtube-transcript

## 點解值得留意

呢個項目正正就係呢個 vault 自己 capture 流程都要靠嘅底層工具（Agent-Reach upstream tools 排喺 reader order 第一位），一鍵幫任何 agent 裝好讀 Twitter/Reddit/YouTube/GitHub/小紅書嘅能力，慳返自己逐個平台踩坑嘅時間。可插拔架構加持續換代嘅承諾（邊個接入方式死咗會自動換路由）令佢維護成本低，適合長期依賴。

## Source

- URL: https://github.com/Panniantong/Agent-Reach
- Created: 2026-02-24
- Reader: routine:github-stars-sync

## Related
