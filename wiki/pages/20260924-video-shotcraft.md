---
title: "Video Shotcraft — Cinematic Product Videos with Claude Code & Remotion"
slug: 20260924-video-shotcraft
type: post
status: draft
source_url: "https://facebook.com/share/p/19YgQuaaCb"
source_platform: web
author: "Brian Jhang"
published: "2026-09-24"
captured_at: "2026-09-27T00:00:00Z"
captured_by: "routine:capture-link"
canonical_id: "url:e14ea4c61b6c92d7ea867765b3445de350d9d62f"
engagement: "likes=34 comments=2 shares=27"
tags: [video-generation, remotion, agent-skills, claude-code, codex, cinematic, product-video, typescript]
related: [20260829-higgsfield-hell-grind-ai-film-consistency-workflow]
needs_manual_text: false
---

## 摘要

Video Shotcraft 是建立在 Remotion 上的 Agent Skill，讓 Claude Code 和 Codex 不只會寫動畫程式碼，還具備鏡頭語言、節奏與驗收標準。它不是一鍵成片的工具，而是把「專業製作流程」轉化成 Agent 可執行的規則，包含 157 張鏡頭配方卡、214 種樣式和 214 段動態預覽。每張配方卡都有用途說明、節奏指引、建議時長、參數設定與調校過的 TSX 實作。截至 2026-09-24，GitHub 已有 9,308 Stars 和 847 Forks，適合用於 SaaS、網頁與桌面產品的功能展示影片。

## Key facts

- **GitHub**: https://github.com/Vincentwei1021/video-shotcraft
- **License**: Apache-2.0 (note: underlying Remotion has its own license)
- **Stars / Forks**: 9,308 ⭐ / 847 forks (as of 2026-09-24)
- **Built on**: Remotion (React-based video rendering)
- **Shot recipe cards**: 157 cards with purpose, rhythm, recommended duration, params, FAQs, and TSX implementation
- **Styles / previews**: 214 styles + 214 motion previews
- **Production workflow** (8 phases):
  1. Understand product & audience
  2. Decide visual direction
  3. Map features to shot types
  4. Create storyboard
  5. Capture real product screenshots
  6. Build shot by shot
  7. Design audio
  8. Final frame-by-frame QA (render, check specific frames, re-render if needed)
- **Rules enforced**:
  - One primary action per shot
  - Leave reading time for key info
  - Use real UI screenshots, not AI-redrawn
  - Each shot outputs designated frames for review
- **Post-production**: browser workbench for reordering shots, adjusting length/speed/styles; export to CapJian (剪映) for further editing
- **Best for**: SaaS, web and desktop product demos, launch videos, promo shorts
- **Not for**: talking-head vlogs, documentaries, long narrative films

## 點解值得留意

- AI 做動畫的關鍵障礙不是模型能力，而是缺乏鏡頭語言——Video Shotcraft 把這個缺口填補了，對 Josep 用 Claude Code 製作任何產品展示影片直接有用。
- 157 張已調校的 TSX 配方卡等於現成的鏡頭庫，可以直接插入 Remotion 專案，大幅縮短製作週期。
- 「逐鏡驗收」框架（輸出指定影格、修改後重新渲染整片）是可以移植到其他 Agent 視覺任務的通用品質控制模式。
- 9,308 stars 且持續更新，社群活躍度高，是值得長期追蹤的基礎設施專案。

## Source

- **Post**: https://facebook.com/share/p/19YgQuaaCb
- **Author**: Brian Jhang (Admin, AI 生活運用｜Brian Jhang's Edge 社群)
- **Published**: 2026-09-24
- **Engagement**: 34 reactions · 2 comments · 27 shares
- **Reader**: jina (r.jina.ai)

## Related

- [[../../skills/making-product-videos/SKILL|skill: making-product-videos]]
- [[20260829-higgsfield-hell-grind-ai-film-consistency-workflow|拆解 Higgsfield《Hell Grind》AI 長片三大一致性技巧]] — AI 影片嘅角色同場景一致性技巧，產品片同短劇都用得著。
