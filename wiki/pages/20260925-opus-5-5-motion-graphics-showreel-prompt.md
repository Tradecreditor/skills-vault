---
title: "Opus 5.5 One-Prompt Motion-Graphics Showreels"
slug: 20260925-opus-5-5-motion-graphics-showreel-prompt
type: post
status: draft
source_url: "https://www.instagram.com/p/Ddt893riBb7/"
source_platform: instagram
author: "learnaifaster"
published: "2026-09-25"
captured_at: "2026-09-27T15:03:15Z"
captured_by: "claude-code-cloud"
canonical_id: "instagram:Ddt893riBb7"
engagement: "likes=1543 comments=1573"
tags: [claude-opus-5-5, motion-graphics, video-generation, prompt-engineering, short-form-content, comment-to-dm]
related: [LottieFiles--motion-design-skill, motion-canvas--motion-canvas, greensock--gsap-skills, nolangz--pixel2motion, 20260924-4-free-design-sites-for-vibe-coders]
needs_manual_text: true
---

## 摘要

@learnaifaster（Learn AI Faster，約 6.9 萬 followers）喺 2026-09-25 出咗一個 5 條短片嘅 carousel，每條約 15 秒，caption 只有「Comment "Motion" and I'll send the link to your DM」，係典型嘅留言換連結引流帖。IG 自己為呢個帖生成嘅 SEO 關鍵字係「motion graphics、ai-generated graphics、claude opus 5.5、résumé」，加上每條片 15 秒，對得上當日早幾個鐘喺 X 爆紅嘅 Claude Opus 5.5「履歷 showreel」prompt：一句 prompt 就叫 Opus 5.5 寫出一條 15 秒專業級 motion graphics 片。Opus 5.5 本身只係文字/圖片入、文字出，影片其實係佢寫嘅渲染代碼（HTML/Canvas/WebGL/p5.js/Manim 等）或者佢指揮其他影片模型做出嚟。呢頁記低嗰條 prompt、可參數化版本，同埋社群整理出嚟嘅開源製作套件；DM 入面嘅連結本身攞唔到。

## Key facts

- **The post:** carousel of 5 videos (1080×1350, 4:5, ~15.07 s each, with audio). Caption is only `Comment "Motion" and I’ll send the link to your DM.` — a comment-to-DM funnel; comments (1,573) outnumber likes (1,543) because of the keyword gate.
- **Subject is inferred, not stated:** Instagram's own meta keywords for the post are `motion graphics, ai-generated graphics, claude opus 5.5, résumé, … video production, animation`; the 15-second clip length matches the viral prompt below, posted on X ~5.5 h earlier. The DM link and on-screen text could not be retrieved (Instagram CDN blocked, link gated behind a comment).
- **The viral prompt** (@ajith_io on X, 2026-09-25, 531K views, 3.7K likes, 4.4K bookmarks), verbatim:
  `make a dynamic 15-second motion graphics video that shows what an incredible motion designer you are, like it's your showreel for a résumé. go all out.`
- **Parametrised variant** (@polydao, 2026-09-26) — run in stock Claude Code, Opus 5.5 on max reasoning, memory off:
  `Make a dynamic [24]-second motion graphics video that shows what an incredible motion designer you are, like it's your showreel for a resume. Go all out. Only about [TOPIC]. Style: [BRAND COLORS], sound synced to the cuts.`
- **How the pixels get made:** Opus 5.5 takes text + images and outputs text, so a video comes from code it wrote (rendered to frames), a program it controlled and screen-recorded, footage it edited, or an external video model it directed. `athemeroy/awesome-opus-5-5-videos` catalogues 1,401 distinct MP4s / 168 reviewed cases; largest styles are motion graphics / UI (350 files) and 3D render (324).
- **Reusable open-source production kits** (listed in that repo, checked 2026-09-27): `lemomo-ai/lemo-opuscar` (39 styles, Canvas/WebGL, DIRECTOR.md + TECHNIQUE.md, MIT code / CC BY 4.0 guides), `francozanardi/papermotion` (paper-cut animation engine with deterministic physics and sound checks), `JohnHeibel/ClaudeAnimationBase` (p5.js + p5.brush starter with storyboard/contact-sheet steps), `makevoid/motion-graphics-music-video-skill` (Claude Code plugin + Ruby toolkit; can call Fal image/video/audio models).
- **Model context:** Opus 5.5 shipped 2026-09-22; pricing $4 input / $20 output / $0.20 cache reads per million tokens (vs Opus 5 at $5 / $25 / $0.50), per Charlie Hills, who calls motion graphics "the biggest jump".
- **Limits:** good at designed animation (text, logos, shapes, data visuals, UI), not realistic camera footage; results still need iteration and human polish, especially sound.

## 點解值得留意

- Josep 做 AI 短片內容：一句 prompt 出 15 秒 motion graphics，可以直接做 reel 開場、hook 畫面，或者「AI 識做 motion design」呢類示範片，本身就係好嘅 content 題材。
- 香港中小企顧問：用參數化版本（`[TOPIC]`、`[BRAND COLORS]`）幫客戶出 launch video / 廣告短片，係可以即場 demo 嘅服務賣點；Iron Log、English Overload 上架都可以用嚟整 launch 片。
- 呢個帖本身係 comment-to-DM 引流嘅教科書例子（留言數多過 like 數），同 `shortform-growth-system` 嘅 lead magnet 做法一致，可以參考佢點樣用「片 + 一句 CTA」收名單。
- 配合 vault 已有嘅 motion-design-skill、gsap-skills、Motion Canvas，可以令 agent 寫動畫代碼時有節奏同品味，唔止靠一句 prompt 碰運氣。

## Source

- URL: https://www.instagram.com/p/Ddt893riBb7/
- Author: @learnaifaster (Learn AI Faster | Artificial Intelligence (AI), verified)
- Published: 2026-09-25 (17:03 UTC)
- Engagement: likes=1543 comments=1573 (at fetch, 2026-09-27)
- Reader: jina (r.jina.ai markdown + HTML of the post and of `/embed/captioned/`); Exa returned 402 (credits exhausted). Context: fxtwitter for https://x.com/ajith_io/status/2103449416325890146 and https://x.com/polydao/status/2103783134206566862; raw.githubusercontent README of https://github.com/athemeroy/awesome-opus-5-5-videos; Jina for https://charliehills.substack.com/p/claude-code-motion-graphics and https://navigotechsolutions.com/blog/claude-opus-5-5-motion-graphics/
- needs_manual_text: the DM link and the videos' on-screen text were not retrievable; paste them under `## Notes` if you have them.

## Related

- [[LottieFiles--motion-design-skill|motion-design-skill]] — 教 agent 先諗時序、緩動同編舞再寫動畫代碼，正好補 one-prompt showreel 嘅品味。
- [[greensock--gsap-skills|gsap-skills]] — Opus 寫 web 動畫代碼時常用嘅 GSAP，有現成 agent skill。
- [[motion-canvas--motion-canvas|Motion Canvas]] — code-first 動畫庫，適合將 prompt 出嚟嘅片變成可重用模板。
- [[nolangz--pixel2motion|pixel2motion]] — 另一個將靜態設計轉成 motion 嘅 agent 工具。
- [[20260924-4-free-design-sites-for-vibe-coders|4 Free Design Sites for Vibe-Coded Apps]] — 同樣係 IG 留言換連結帖，animos.app 都係出 launch video。
- [[../../skills/providing-design-references/SKILL|skill: providing-design-references]] — 喺 prompt 加品牌色 / 參考畫面，令出片唔會千篇一律。
