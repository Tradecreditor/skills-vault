---
title: "Claude HTML+SVG animation: 3 practice cases and a 5-part prompt"
slug: 20261002-claude-html-svg-animation-5-part-prompt
type: post
status: draft
source_url: "https://www.threads.com/@aiposthub/post/Dd_5unfATy9"
source_platform: threads
author: "@aiposthub"
published: "2026-10-02"
captured_at: "2026-10-04T21:10:23Z"
captured_by: "claude-code-cloud"
canonical_id: "threads:Dd_5unfATy9"
engagement: "likes=41 replies=5 reposts=4 shares=34 views=3.3K"
tags: [topic/video-gen, svg-animation, html, claude, prompting, tutorial]
related: [stars/nolangz--pixel2motion, 20260925-opus-5-5-motion-graphics-showreel-prompt, stars/LottieFiles--motion-design-skill]
needs_manual_text: false
---

## 摘要

AI郵報（@aiposthub）分享用 Claude 製作 HTML＋SVG 動畫嘅入門教學：作者話只要把需求講清楚，Claude 就可以輸出一個可以直接開啟嘅動畫，唔使先學 After Effects，亦唔使自己研究動畫程式碼。帖文用 3 個練習案例示範，分別係 Logo 描邊動畫、三個圓點依序跳動嘅 Loading 動畫，同由 0 逐條長到指定數值嘅動態長條圖。作者指關鍵在於 Prompt 要交代「主體、畫布、動作、順序、輸出」五件事，並建議用細步修改（例如「把移動距離減半」）取代每次整份重新生成。輸出格式可按用途揀 HTML/SVG、MP4 或 GIF。帖末附完整教學連結，亦順帶宣傳作者嘅付費課程。

## Key facts

- Claim (author): Claude can produce a ready-to-open **HTML + SVG animation** from a clearly written request, with no After Effects and no hand-written animation code. The linked tutorial was not fetched, so none of this is verified.
- **Case 1, logo stroke animation**: the logo's lines are slowly "drawn", then the brand name fades in. Suggested uses: website intro, brand logo animation, presentation opener.
- **Case 2, loading animation**: e.g. three dots that bounce, fade in and scale in sequence. Author's tip: rhythm matters; if all three elements move at once it looks messy, so stagger each element's start time.
- **Case 3, animated bar chart**: give Claude the data directly, e.g. `A = 20 B = 40 C = 60`, and the bars grow from 0 to their values in order. Suggested uses: data presentations, product demos, landing pages.
- The prompt must state 5 things: 主體 subject, 畫布 canvas, 動作 motion, 順序 sequence, 輸出 output.
- Weak prompt (verbatim): 「幫我做一個有質感的 Logo 動畫。」
- Better prompt (verbatim): 「16:9 深色背景，Logo 線條用 2 秒描繪完成，再用 0.5 秒淡入品牌名稱，最後停止，輸出成單一 HTML。」
- Iteration examples (verbatim): 「把移動距離減半，其他設定保持原樣。」 · 「最後 0.4 秒加入減速。」 · 「手機版不要超出畫面。」 The author claims small step-by-step edits are much steadier than regenerating the whole file each time.
- Output by use (author): HTML / SVG for websites and interactive charts; MP4 for Reels, video and presentations; GIF for short looping animations. The thread does not explain how to get MP4 or GIF out of Claude.
- Full tutorial (not fetched): https://www.aiposthub.com/claude-svg-animation-logo-loading-chart-tutorial/ — the author says it holds the full workflow, 3 copy-ready prompts and animation-editing methods.
- The last author reply also promotes a paid course (Skill Shot 11, AI music monetisation, early-bird to 10/15, academy.aiposthub.com); unrelated to the animation topic.
- A reply by another account (@human_control_plane.17932) says 「香港不能使用😭」; what it refers to is not stated and is unverified.
- Engagement: 41 likes, 5 replies, 4 reposts, 34 shares, 3.3K views (order inferred from Threads UI).

## 點解值得留意

- **客戶 demo 快速原型**：「主體、畫布、動作、順序、輸出」呢個 Prompt 結構，Jeff 可以直接用喺 Claude Code，為香港中小企快速出 Logo 開場、Loading 動畫或動態圖表，交付單一 HTML 檔。
- **Prompt 要具體到秒數同停止條件**：例子入面有比例、背景、2 秒描繪、0.5 秒淡入、最後停止、輸出格式，啱做成可重用嘅 prompt checklist（呢次只係筆記，未起草 skill）。
- **同 vault 現有動畫素材互補**：pixel2motion 同 motion-design-skill 係「裝工具／skill」路線，呢個帖係純 Prompt 路線，可以對照邊個更適合客戶情境。
- **先核實可用性**：MP4／GIF 點輸出帖中冇交代，留言又有人話香港用唔到（原因不明），推薦畀客戶之前要自己試過。

## Source

- Post: https://www.threads.com/@aiposthub/post/Dd_5unfATy9
- Author: @aiposthub (AI郵報) · Published: 2026-10-02
- Engagement: likes=41 replies=5 reposts=4 shares=34 views=3.3K (order inferred from Threads UI)
- Reader: jina (share link resolved via r.jina.ai; counts order inferred from Threads UI)
- Share URL: https://www.threads.com/share/BARpqpl7Fq/
- Thread captured: root post plus the author's 3 replies (Dd_5vE2gf0y, Dd_5vm4AUlZ, Dd_5wAWgeqh) and 2 short replies by other accounts
- Not captured: the tutorial page, the course page, "Related threads" by other accounts

## Related

- [[../stars/nolangz--pixel2motion|pixel2motion]] — logo to SVG animation skill; the tool route to the same logo-animation use case
- [[../pages/20260925-opus-5-5-motion-graphics-showreel-prompt|Opus 5.5 One-Prompt Motion-Graphics Showreels]] — another prompt-driven Claude motion-graphics post
- [[../stars/LottieFiles--motion-design-skill|motion-design-skill]] — motion principles (timing, easing, choreography) for agents; fits the "stagger the timing" tip
