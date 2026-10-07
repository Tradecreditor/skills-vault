---
title: "Claude Opus 5.5 tutorial-animation prompt (research, compare, build, deliver)"
slug: 20260928-claude-opus-5-5-tutorial-animation-prompt
type: post
status: draft
source_url: "https://www.threads.com/@pin._.wen/post/Dd0VbUxDRZv"
source_platform: threads
author: "@pin._.wen"
published: "2026-09-28"
captured_at: "2026-10-04T21:08:08Z"
captured_by: "claude-code-cloud"
canonical_id: "threads:Dd0VbUxDRZv"
engagement: "likes=1.5K replies=59 reposts=277 shares=2K"
tags: [topic/video-gen, claude, opus-5-5, animation, prompt, tutorial-video]
related: [20260925-opus-5-5-motion-graphics-showreel-prompt, 20260924-video-shotcraft, motion-canvas--motion-canvas]
needs_manual_text: false
---

## 摘要

張品妏（@pin._.wen）話自己冇時間研究，所以直接叫 Claude 生成一部教學影片，認為對懶得睇文章嘅人好有幫助，帖文只寫「Prompt 放留言」。佢喺自己嘅留言（分成幾則）貼出完整四階段 prompt：先叫 Claude Opus 5.5 上網研究大家點用佢做動畫，再分類比較各種做法（HTML/CSS/JS、SVG、Canvas、GSAP、Three.js、Remotion、Manim、Motion Canvas 等），然後製作一部約 2–4 分鐘、可自動播放並有暫停／上一段／下一段控制嘅教學動畫，最後交付研究報告、分鏡腳本、網頁版動畫同完整原始碼。有網友問係咪要接駁影片 MCP，作者回覆話冇串 MCP，係直接將 prompt 貼入 Claude Code 生成，而且呢個 prompt 本身都係 Claude 幫佢整理出嚟。以上全部係作者自述，成品影片未有睇到。

## Key facts

- Post by 張品妏 (@pin._.wen), 2026-09-28. Root text: she had no time to research, so she asked Claude to generate a tutorial video, which she says helps people who dislike reading articles; "Prompt 放留言" (prompt in the comments). One video is attached (cover frame only was visible; the video was not watched).
- The full prompt is in the author's own replies, split over 3 replies (phase 1, phase 2, phase 3 + 4 + notes). It targets "Claude Opus 5.5". Verbatim (copied exactly, NOT run):

```text
請幫我上網研究大家怎麼用 Claude Opus 5.5 製作動畫，整理成一套清楚的操作流程，再用這套流程親手做一部「如何用 Opus 5.5 做動畫」的教學動畫。
第一階段：資料收集

1. 搜尋範圍：YouTube 教學影片（可讀字幕或說明欄）、X/Twitter、Reddit（r/ClaudeAI 等）、個人部落格、Medium、GitHub 範例專案，以及 Anthropic 官方文件。
2. 關鍵字用中英文都搜，例如：「Claude Opus 5.5 animation」「Claude 做動畫」「Claude Remotion」「Claude Manim」「Claude SVG animation」「Claude HTML animation prompt」「Claude artifact animation」。
3. 以最近三月內的資料為主，至少參考 【10】 個以上不同來源。
4. 每個來源記下：作者、網址、用的工具或技術、他們的提示詞寫法、遇到的問題和解法。

第二階段：整理分析

1. 先分類大家的做法。我不確定是用動畫工具還是寫程式碼，請幫我釐清，可能包括：
 * 程式碼類：HTML/CSS/JS、SVG、Canvas、GSAP、Three.js、Remotion（React 影片）、Manim（Python 數學動畫）、Motion Canvas 等
 * 工具搭配類：Claude 寫腳本或分鏡，再交給其他動畫或影片工具
2. 比較各做法的難易度、適合對象、成品效果和優缺點，做成表格。
3. 歸納出一套「新手也能照做」的標準流程，例如：構想 → 寫腳本/分鏡 → 下提示詞 → 生成程式碼 → 預覽修改 → 匯出影片。每一步都附上實際可用的提示詞範例。
4. 列出大神們共同提到的技巧，以及常見的錯誤。

第三階段：製作教學動畫

1. 內容：用動畫呈現第二階段整理出的流程，讓沒有經驗的人看完就知道怎麼開始。
2. 長度：約 【2-4】 分鐘，分成 【5–7】 個段落（開場 → 各步驟 → 小技巧 → 結尾總結）。
3. 風格由你決定，以清楚易懂為最高原則。可以是扁平插畫、資訊圖表或簡約動態文字，配色統一、畫面不要太雜。
4. 語言：畫面文字用繁體中文，專有名詞保留英文。
5. 製作方式：請採用你研究後認為最適合的方法，最好就是教學裡介紹的方法，讓這部動畫本身也是示範。
6. 動畫要能自動播放，也要有暫停、上一段、下一段的控制。

第四階段：交付內容

1. 一份研究報告，包含來源列表（附連結）、做法比較表和標準流程。
2. 分鏡腳本：每一段的畫面描述、文字、秒數。
3. 成品動畫：可直接播放的網頁版。如果做得到，也請附上 MP4 或匯出影片的方法。
4. 完整原始碼和使用說明，讓我之後能自己修改。

注意事項

* 如果某些資訊查不到或不確定，請直接說明，不要編造。
* 開始製作動畫前，先把第二階段的流程和分鏡給我確認。
```

- Structure in one line: phase 1 research (sources: YouTube, X, Reddit, blogs, Medium, GitHub, Anthropic docs; at least 【10】 sources from the last 3 months) → phase 2 classify and compare methods in a table, then derive a beginner-proof standard flow (idea → script/storyboard → prompt → generate code → preview/revise → export video) → phase 3 build a 【2-4】 minute animation in 【5–7】 segments, Traditional Chinese on-screen text with English terms kept, autoplay plus pause / previous / next controls → phase 4 deliver a research report with source links, a storyboard (visual, text, seconds per segment), a playable web version (MP4 or export method if possible), and full source code with usage notes.
- Built-in guardrails: say so if information cannot be found or is uncertain, do not fabricate; and confirm the phase-2 workflow and storyboard with the user before starting to build. The 【】 values are tunable parameters.
- Author's Q&A (author claims): asked whether Claude Code generates video natively or via a video MCP (question by @lojomate, not the author), she replied "沒有串mcp喔～" (no MCP connected) and that she pasted these prompts straight into Claude Code with no other software.
- Author's claim: the prompt itself was drafted by Claude; she only told it she wanted to ask AI to collect people's Opus 5.5 animation tutorials (YouTube included), organise their workflows (animation tool vs. code, she was unsure which), and build a how-to tutorial animation in a style of its own choosing, then asked it to turn that into a fuller prompt.
- Not verified: the resulting video, its quality, and whether the research step produces real sources; the post shows no output in text form.
- Engagement: 1.5K likes, 59 replies, 277 reposts, 2K shares (order inferred from Threads UI).

## 點解值得留意

- **可直接改用嘅 meta-prompt**：「先研究 → 比較做法 → 做成品 → 交付報告＋分鏡＋原始碼」呢個四步結構唔限於動畫，Jeff 可以換個題目（例如客戶培訓影片、YouTube 教學）再用 Claude Code 跑，亦啱做短影音「AI 自己教你點用 AI」嘅示範。
- **設計細節值得抄**：中途要先確認流程同分鏡（human checkpoint）、「查唔到就講，唔好作」條款、`【】` 參數位、要求交付來源連結同完整原始碼令客戶之後可以自己改——全部都可以放入 HK 中小企項目嘅交付 SOP。
- **同 vault 已有題材互補**：vault 已有 Opus 5.5 一句 prompt 出 motion-graphics showreel，同 Video Shotcraft 嘅 Remotion 產品片流程；呢個帖係「叫 agent 自己研究方法再做」嘅另一種進路，三者可以對比。
- **用前要核實**：作者所講嘅「冇接 MCP、Claude Code 直接生成」係自述，成品未睇到；prompt 要 agent 上網搜資料，來源品質要人手抽查。

## Source

- Post: https://www.threads.com/@pin._.wen/post/Dd0VbUxDRZv
- Author: @pin._.wen (張品妏) · Published: 2026-09-28
- Engagement: likes=1.5K replies=59 reposts=277 shares=2K (order inferred from Threads UI)
- Reader: jina (share link resolved via r.jina.ai; counts order inferred from Threads UI)
- Share URL: https://www.threads.com/share/BAdRbSMGiN/
- Author replies (the prompt) read from the embedded JSON of the share-page HTML; the attached video was not watched; "Related threads" by other accounts not captured.

## Related

- [[../pages/20260925-opus-5-5-motion-graphics-showreel-prompt|Opus 5.5 One-Prompt Motion-Graphics Showreels]] — 同樣係用 Opus 5.5 叫 agent 出動畫／影片嘅 prompt，一句版對比呢個四階段版
- [[../pages/20260924-video-shotcraft|Video Shotcraft — Cinematic Product Videos with Claude Code & Remotion]] — Remotion + Claude Code 嘅固定流程，呢個 prompt 亦提到 Remotion 係可選做法
- [[../stars/motion-canvas--motion-canvas|Motion Canvas: Visualize Your Ideas With Code]] — prompt 清單入面列出嘅 code-first 動畫工具之一
