---
title: "caveman"
slug: JuliusBrussee--caveman
type: repo
status: draft
source_url: "https://github.com/JuliusBrussee/caveman"
source_platform: github
author: "JuliusBrussee"
published: "2026-04-04"
captured_at: "2026-11-10T06:06:37Z"
captured_by: "routine:github-stars-sync"
canonical_id: "github:JuliusBrussee/caveman"
engagement: "stars=118720 forks=6906"
tags: ["claude-code", "skill", "tokens", "prompt-engineering", "llm"]
related: []
needs_manual_text: false
---
## 摘要

Caveman 係一套幫 AI coding agent 慳 token 嘅工具，4.0 版分六個部分：「Say less」令 agent 用簡短、答案先行嘅語氣回覆，程式碼、指令、路徑同錯誤訊息保持逐字不變；「Read less」喺 agent 讀 log、JSON、CSV、測試輸出前先壓縮，README 量度成個 session 輸入 token 減 33.2%；「Auto」按每個請求揀模型同 effort，宣稱比 Opus 5.5 xhigh 平 54% 而分數相若（結果仍屬中期）；「Blocks」令 agent 重用寫過嘅 script；另有保持 prompt cache 溫熱同壓縮網頁嘅 Browse。一行 `npx @caveman-ai/cli@latest` 安裝，支援 Claude Code、Codex、Gemini CLI 等 30 多個 agent，亦可只裝 skill。README 引用 Adobe Research 同 JetBrains 嘅測試，並坦白標明 HTML 壓縮暫時冇效果。

## Key facts

- **Repo**: [JuliusBrussee/caveman](https://github.com/JuliusBrussee/caveman)
- **Stars**: 118,720 | **Forks**: 6,906
- **Language**: Go
- **License**: Apache-2.0
- **Last push**: 2026-11-09
- **Install**: `npx @caveman-ai/cli@latest` (Node.js 22.13+); skill only: `npx skills add JuliusBrussee/caveman -g`; Claude Code: `/plugin marketplace add JuliusBrussee/caveman` then `/plugin install caveman@caveman`
- **Caveats**: Auto needs a free account and sends data (see README Privacy); the installer rewrites agent configs; review before running.

## 點解值得留意

Token 成本係長時間 agent session 最實際嘅開支，而 caveman 唔止係「講少啲」，仲針對 agent 讀入嘅內容同重複寫 script 嘅浪費，有量度數字同外部測試支持。對 vault 嚟講，可以同 model-tiering 同 CLAUDE.md 壓縮（`/caveman-compress`）一齊參考。裝落去前要留意佢會改寫多個 agent 設定，而且 Auto 需要登入，建議先過 scanning-agent-skills 掃描。已另外草擬 draft skill。

## Source

- URL: https://github.com/JuliusBrussee/caveman
- Created: 2026-04-04
- Reader: raw.githubusercontent.com README + Jina Reader (GitHub API JSON)
