---
title: "ponytail"
slug: DietrichGebert--ponytail
type: repo
status: draft
source_url: "https://github.com/DietrichGebert/ponytail"
source_platform: github
published: "2026-06-12"
captured_at: "2026-09-19T11:09:28.035525Z"
captured_by: "routine:github-stars-sync"
canonical_id: "github:DietrichGebert/ponytail"
engagement: "stars=142274 forks=7629"
tags: ["agent-skills", "ai-agents", "claude", "claude-code", "claude-code-plugin", "cursor-rules", "developer-tools", "llm", "prompt-engineering", "yagni"]
related: []
needs_manual_text: false
---
## 摘要

Ponytail 係一套令 AI agent 寫代碼變得「夠用就好」嘅 skill，靈感嚟自嗰種老練工程師：畀佢睇五十行代碼，佢一聲不響換成一行。核心係一條七級判斷梯：由「呢樣嘢使唔使存在（YAGNI）」到「用原生平台功能」到「一行搞掂」,逐級檢查先落手寫代碼，但唔會犧牲驗證、錯誤處理、安全性同無障礙呢啲底線。作者用真實 Claude Code session 喺 FastAPI+React 專案做十二個功能任務嚟量度效果,對比有冇裝呢個 skill。

## Key facts

- **Repo**: [DietrichGebert/ponytail](https://github.com/DietrichGebert/ponytail)
- **Stars**: 142,274 | **Forks**: 7,629
- **Language**: JavaScript
- **License**: MIT License
- **Numbers**: 相比無 skill 基線,代碼行數 -54%、token -22%、成本 -20%、時間 -27%，安全守則 100% 保留
- **Install (Claude Code)**: `/plugin marketplace add DietrichGebert/ponytail` 再 `/plugin install ponytail@ponytail`
- **Topics**: agent-skills, ai-agents, claude, claude-code, claude-code-plugin, cursor-rules, developer-tools, llm, prompt-engineering, yagni

## 點解值得留意

呢個 skill 直接解決 agent 「過度建構」嘅通病（例如求一個日期選擇器，agent 會裝成個 library 仲加埋 wrapper，Ponytail 就會直接用原生 `<input type="date">`）。跨十幾種 agent 平台（Claude Code、Codex、Cursor、Gemini CLI、OpenCode 等）都有安裝方式，且有真實 benchmark 數字支撐,唔止係得個講字。

## Source

- URL: https://github.com/DietrichGebert/ponytail
- Created: 2026-06-12
- Reader: routine:github-stars-sync

## Related
