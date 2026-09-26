---
title: "diagram-design"
slug: cathrynlavery--diagram-design
type: repo
status: draft
source_url: "https://github.com/cathrynlavery/diagram-design"
source_platform: github
author: "cathrynlavery"
published: "2026-04-16"
captured_at: "2026-09-19T11:09:28.035450Z"
captured_by: "routine:github-stars-sync"
canonical_id: "github:cathrynlavery/diagram-design"
engagement: "stars=41245 forks=2637"
tags: ["agent-skills", "claude-code", "codex", "data-visualization", "diagrams", "drawio", "mermaid", "svg"]
related: [slidevjs--slidev, LottieFiles--motion-design-skill, vercel-labs--skills, VoltAgent--awesome-design-md]
needs_manual_text: false
---
## 摘要

Diagram Design 係一套幫 Claude Code、Codex、Factory Droid、Pi 等 Agent Skills 相容工具畫「編輯級」圖表嘅 skill，賣點係自成一體嘅 HTML + SVG，唔靠 Mermaid 嗰種千篇一律圓角框，亦唔使開 Figma 慢慢揀色。內置三十幾種版面文法（架構圖、流程圖、時序圖、狀態機、燃盡圖、Sankey、魚骨圖、Wardley map、UML class、資料庫 schema 等），每種都有淺色、深色、全編輯三個靜態版本,亦可以讀入現有 draw.io / Mermaid / Excalidraw 圖再重畫。作者話設計原則係「刪減先係最高質素嘅動作」,每個節點都要有存在理由，強調識別密度控制喺 4/10。

## Key facts

- **Repo**: [cathrynlavery/diagram-design](https://github.com/cathrynlavery/diagram-design)
- **Stars**: 41,245 | **Forks**: 2,637
- **Language**: HTML
- **License**: MIT License
- **Install (Claude Code)**: `/plugin marketplace add cathrynlavery/diagram-design` 再 `/plugin install diagram-design@diagram-design`
- **Gallery**: https://cathrynlavery.github.io/diagram-design/
- **Topics**: agent-skills, claude-code, codex, data-visualization, diagrams, drawio, mermaid, svg

## 點解值得留意

同呢個 vault 已裝嘅 `artifact-diagramming` 類技能屬同一路數,但呢個係跨平台獨立 skill（Claude Code / Codex / Copilot / Factory Droid / Pi / Kiro / OpenCode 都有安裝方式），版面文法齊全兼且持續加新類型（v2.5.10 一次過加十種），對要出「畀客戶睇」而唔係「畀開發者睇」嘅圖表特別有用。

## Source

- URL: https://github.com/cathrynlavery/diagram-design
- Created: 2026-04-16
- Reader: routine:github-stars-sync

## Related

- [[slidevjs--slidev|Slidev]] — diagram-design 出嘅自足 HTML+SVG 圖可以直接嵌入 Slidev 呢類 HTML 簡報。
- [[LottieFiles--motion-design-skill|motion-design-skill]] — 兩者都係「先講原則後落手畫」嘅視覺設計 skill。
- [[vercel-labs--skills|skills]] — 都係將 skill 分發到多個 agent client 嘅方式：diagram-design 行 plugin marketplace，skills 行 CLI。
- [[VoltAgent--awesome-design-md|awesome-design-md]] — 都用純 markdown/HTML 檔案取代 Figma 嚟教 agent 做視覺嘢。
