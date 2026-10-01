---
title: "json-render: generative UI constrained to your own component library"
slug: 20260929-json-render-generative-ui-component-library
type: post
status: draft
source_url: "https://www.threads.com/@krumjahn/post/Dd2h9cGAueD"
source_platform: threads
author: "@krumjahn"
published: "2026-09-29"
captured_at: "2026-10-01T12:42:40Z"
captured_by: "claude-code-cloud"
canonical_id: "threads:Dd2h9cGAueD"
engagement: "likes=65 replies=5 reposts=8 shares=62 views=6.5K"
tags: [topic/agent-tooling, json-render, generative-ui, component-library, jev, agent-ui, constrained-output]
related: [20260925-jev-seo-geo-audit-cost-down-90, 20260928-claude-code-fable-advisor-jev-tree, 20260920-fast-jev-compaction]
needs_manual_text: false
---

## 摘要

Keith Rumjahn（@krumjahn）介紹 json-render，一個將「生成式介面」限制喺開發者自己定義嘅元件庫入面運作嘅項目。AI 只可以從你預先定義嘅元件入面揀，唔可以亂生成代碼，所以輸出更可控、風格更一致。帖文提到有一條實驗路徑可以接駁 Jev，而 GitHub 已有 18,331 顆星。呢類做法針對 agent 生成 UI 時容易失控、同設計系統唔一致嘅問題，適合做 agent UI 或 AI app 前端嘅開發者。帖文係影片貼文，影片內容未有擷取，只有文字說明。

## Key facts

- Tool name: **json-render** — generative UI that runs inside your own component library
- Core constraint: the AI can **only pick from components you define**, it cannot generate arbitrary code
- An experimental path can connect it to **Jev**
- GitHub stars at time of post: **18,331**
- Audience named by the author: people building agent UI
- No repo URL, install command or version is given in the post text
- Engagement: 65 likes, 62 shares, 6.5K views (order inferred from Threads UI)
- The author's reply is a promo for his own AI community on skool.com (no extra content)

## 點解值得留意

- **Iron Log / English Overload 可以參考**：如果日後想畀 AI 生成頁面或元件，限制喺自己 design system 內，可以避免生成不一致嘅 UI。
- **客戶 agent 前端**：香港 SME 嘅內部 AI 助手如果要顯示表格、卡片、表單，用受限元件庫比自由生成 HTML 安全得多。
- **Jev 話題延續**：呢帖再次將 Jev 同 agent 工作流連埋一齊，同 vault 內已有 Jev 相關筆記互相對照。
- **待查證**：帖文冇附 repo 連結，「實驗路徑可接 Jev」嘅具體做法要自己再搵出處。

## Source

- Post: https://www.threads.com/@krumjahn/post/Dd2h9cGAueD
- Author: @krumjahn (Keith Rumjahn) · Published: 2026-09-29 (derived from "2d" at fetch time 2026-10-01T12:42Z)
- Engagement: likes=65 replies=5 reposts=8 shares=62 views=6.5K (order inferred from Threads UI)
- Reader: Jina Reader (r.jina.ai)
- Share URL: https://www.threads.com/share/BAXaN96TIc/
- Not captured: the attached video content, the repo itself, replies and "Related threads" by other accounts

## Related

- [[pages/20260925-jev-seo-geo-audit-cost-down-90|Jev cuts agent SEO/GEO audit-and-fix cost by 90%]] — Jev as a typed-judgment model, same author
- [[pages/20260928-claude-code-fable-advisor-jev-tree|Claude Code: Fable 5.1 Advisor + Jev Routing Tree]] — Jev used for routing in Claude Code
- [[pages/20260920-fast-jev-compaction|fast-jev-compaction — verbatim Jev-scored compaction for Claude Code]] — another Jev tool in the vault
