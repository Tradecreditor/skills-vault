---
title: "OpenSpec"
slug: Fission-AI--OpenSpec
type: repo
status: draft
source_url: "https://github.com/Fission-AI/OpenSpec"
source_platform: github
author: "Fission AI"
published: "2025-08-05"
captured_at: "2026-09-20T00:00:00Z"
captured_by: "routine:github-stars-sync"
canonical_id: "github:Fission-AI/OpenSpec"
engagement: "stars=69664 forks=4772"
tags: [sdd, spec-driven-development, ai, planning, engineering]
related: [upstash--context7, openai--codex-plugin-cc, NousResearch--hermes-agent-self-evolution]
needs_manual_text: false
---

## 摘要
OpenSpec 係一套規格驅動（spec-driven）嘅開發框架，用嚟喺寫任何程式碼之前，先同 AI 一齊釘實「要做咩、點解要做」。流程係四個指令：`/opsx:explore` 同 AI 一齊摸索方向（佢會讀你現有嘅程式碼再提方案）、`/opsx:propose` 產生 proposal.md／specs／design.md／tasks.md、`/opsx:apply` 逐項實作、`/opsx:archive` 歸檔並更新規格。規格本身就係純 Markdown——用 WHEN／THEN 寫具體情境，冇特殊語法要學，由 AI 落筆、你審批。Beta 功能 Stores 再進一步，將規劃獨立成一個 repo，等跨 repo 嘅功能同跨團隊共用嘅需求有單一來源。
## Key facts
- Language: TypeScript
- License: MIT
- Created: 2025-08-05
- Last pushed: 2026-09-18
- Stars: 69,664
- Forks: 4,772
- Homepage: https://openspec.dev
- Topics: spec-driven-development, context-engineering, planning

## 點解值得留意
佢解決嘅唔係「AI 寫唔到程式碼」，而係「AI 唔清楚你想要乜就照寫」。規格係純 Markdown 又入咗 git，所以每個 coding agent 都讀得到，唔會好似 wiki 咁飄移。設計上明言針對 brownfield（現有專案）而唔係只服務新專案，呢點同大部分同類工具唔同。
## Source
GitHub repository: https://github.com/Fission-AI/OpenSpec
Author: Fission AI
Captured: 2026-09-20

## Related

- [[upstash--context7|context7]] — 兩者都係將外部/規格資訊塞入 agent context 嘅工具，一個攞文件一個攞規格。
- [[openai--codex-plugin-cc|codex-plugin-cc]] — 兩個都係喺 coding agent 流程入面加一層審批/規劃步驟。
- [[NousResearch--hermes-agent-self-evolution|hermes-agent-self-evolution]] — 都想將「點解會失敗/點解要咁做」講清楚先落手改。
