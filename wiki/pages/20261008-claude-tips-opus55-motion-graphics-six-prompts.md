---
title: "Claude Tips & Tricks：Opus 5.5 用代碼做 motion graphics 嘅 6 個 prompt"
slug: 20261008-claude-tips-opus55-motion-graphics-six-prompts
type: post
status: draft
source_url: "https://www.instagram.com/p/DeOuCSrDCj8/"
source_platform: instagram
author: "claudetipsandtricks"
published: "2026-10-08"
captured_at: "2026-10-09T00:00:00Z"
captured_by: "routine:capture-link"
canonical_id: "instagram:DeOuCSrDCj8"
engagement: ""
tags: [topic/video-gen, motion-graphics, opus-5-5, headless-browser, claude-tips]
related: []
needs_manual_text: true
---

## 摘要
呢個 Instagram 輪播介紹 Opus 5.5 點樣做 motion graphics：Claude 將每個動畫寫成代碼，再用 headless browser 逐格 render 成影片，所以每次輸出都完全一致。帖文列出 6 個 prompt 主題，包括 kinetic 標題、landing page hero 動畫、同音訊同步嘅標題、由 CSV 生成動畫圖表。作者最推薦第 5 張：畀 SaaS 網站連結，Claude 會抽取產品資料同 CTA，規劃場景並做出完整 intro。實際 prompt 全文只喺圖片 slide 入面，caption 冇。

## Key facts
- Claude writes each animation as code; a headless browser renders it to video frame by frame, so exports are deterministic.
- Six prompt topics: scenes are just code; kinetic titles on the beat; hero motion for a landing page; full SaaS intro from a website link; titles synced to audio; animated charts from a CSV.
- Slide 5 flow: website link -> pull product details + CTA -> plan scenes -> build intro.
- The prompt texts are in the carousel images only; not captured (needs_manual_text: true). No skill drafted.

## 點解值得留意
- 同 vault 已有嘅 motion graphics / HyperFrames 材料屬同一路線（代碼驅動、可重現 render）。
- 「網站連結 -> SaaS intro 影片」可用於產品宣傳片流程。

## Source
https://www.instagram.com/p/DeOuCSrDCj8/ — claudetipsandtricks, 2026-10-08. No engagement counts available. Reader: Jina (caption only; slide images not read).

## Related
- [[20260925-opus-5-5-motion-graphics-showreel-prompt]]
- [[20260927-hyperframes-camera-3d-captions-skill]]
- [[20260924-video-shotcraft]]
