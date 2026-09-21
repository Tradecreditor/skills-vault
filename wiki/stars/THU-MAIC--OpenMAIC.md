---
title: "OpenMAIC"
slug: THU-MAIC--OpenMAIC
type: repo
status: draft
source_url: "https://github.com/THU-MAIC/OpenMAIC"
source_platform: github
author: "THU-MAIC"
published: "2026-03-11"
captured_at: "2026-09-21T23:07:37Z"
captured_by: "routine:github-stars-sync"
canonical_id: "github:THU-MAIC/OpenMAIC"
engagement: "stars=38431 forks=6024"
tags: [ai, ai-agents, education, multi-agent]
related: []
needs_manual_text: false
---

## 摘要
OpenMAIC(Open Multi-Agent Interactive Classroom)係一個開源 AI 平台,一句 prompt 或者一份文件就可以生成一個完整嘅互動課堂:自動整投影片、測驗、互動模擬同埋 project-based learning,仲有 AI 老師同 AI 同學識講嘢、識喺白板度畫圖,同你即時討論。v1.0.0 加咗一個 Pro workbench,可以同 agent 對話式咁規劃課程大綱、逐頁修改,重可以由你自己嘅文件、音頻、影片建構課堂內容。佢仲自帶一個標準 SKILL.md 格式嘅 skill 包,可以喺 OpenClaw、Codex、DeepSeek 呢類 agent workbench 入面直接用,甚至喺 Feishu、Slack、Telegram 呢啲聊天軟件度生成課堂。

## Key facts
- Language: TypeScript
- License: MIT
- Created: 2026-03-11
- Last pushed: 2026-09-21
- Stars: 38,431
- Forks: 6,024
- Requires: Node.js >= 22.19, pnpm >= 10
- Install: `git clone` + `pnpm install` + configure `.env.local` with an LLM provider key + `pnpm dev`
- Ships a `skills/openmaic/SKILL.md` package for agent workbenches (OpenClaw, Codex, DeepSeek, WorkBuddy)

## 點解值得留意
一個學術團隊(清華大學 MAIC)出品嘅開源多 agent 教學平台,將「一鍵生成教材」呢個概念做到相當完整 —— 由劇本理解、投影片、測驗到互動模擬全部包晒。佢隨機附帶嘅 agent-skill 包裝手法(`skills/openmaic/SKILL.md`)同呢個 vault 嘅 skill 收藏思路直接相關,可以參考佢點樣將一個大型應用包裝成一個可以喺唔同 agent workbench 通用嘅 skill。

## Source
GitHub repository: https://github.com/THU-MAIC/OpenMAIC
Author: THU-MAIC
Published: 2026-03-11
Reader used: raw README via Exa (web_fetch_exa)

## Related
