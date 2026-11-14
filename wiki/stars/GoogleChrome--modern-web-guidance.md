---
title: "modern-web-guidance"
slug: GoogleChrome--modern-web-guidance
type: repo
status: draft
source_url: "https://github.com/GoogleChrome/modern-web-guidance"
source_platform: github
author: "GoogleChrome"
published: "2026-03-23"
captured_at: "2026-11-14T06:02:37Z"
captured_by: "routine:github-stars-sync"
canonical_id: "github:GoogleChrome/modern-web-guidance"
engagement: "stars=11626 forks=405"
tags: ["agent-skills", "web-platform", "css", "accessibility", "chrome"]
related: []
needs_manual_text: false
---
## 摘要

Modern Web Guidance 係 Google Chrome、Microsoft Edge、Mozilla Firefox 同 MDN 團隊同社群一齊維護嘅一套 skills，將網頁平台嘅專業知識、最佳做法同瀏覽器相容性資料直接放入 coding agent 嘅 context。原因係 LLM 訓練資料充斥舊式寫法，agent 往往會寫出臃腫嘅 JavaScript，而原生 API 其實已經可以做到同樣嘅事。佢嘅 CLI 會按需要回傳經過精選、盡量慳 token 嘅指引，並用 eval 剔走模型本身已經識嘅內容。內容涵蓋約 250 個現代網頁功能，包括 View Transitions、container queries、Anchor Positioning、Popover API、INP 診斷，以及內置 AI API 等。

## Key facts
- Install: `npx modern-web-guidance@latest install` (interactive wizard)
- Try without installing: `npx modern-web-guidance@latest search "<query>"`, `retrieve "<guide-id>"`, `legacy-scan .` (scans a codebase for legacy patterns)
- Disciplines: user experience, CSS layout, performance, forms & UI, accessibility, built-in AI
- Language: none detected (guides are Markdown); License: Apache-2.0
- Last push: 2026-11-10; source code lives in GoogleChrome/modern-web-guidance-src

## 點解值得留意

對經常叫 agent 寫前端嘅人嚟講，呢個係官方級嘅「反舊寫法」補丁：由瀏覽器廠商自己維護，比一般 prompt 技巧可靠。佢嘅 legacy-scan 可以幫舊專案搵出可以原生化嘅位置。同 vault 內嘅 frontend、design 類 skills 可以互相補充。星數只有約 1.1 萬，但屬於新近星標，值得留意之後嘅更新。

## Source
- https://github.com/GoogleChrome/modern-web-guidance (author: GoogleChrome, created 2026-03-23)
- Reader: exa (web_fetch_exa on raw README; Jina needs a key and the GitHub proxy blocked direct API)
