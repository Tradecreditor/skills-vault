---
title: "Benji Taylor: Stageshow, a skill that helps your agent make better faux product UI"
slug: 20261102-benji-taylor-stageshow-faux-ui-skill
type: post
status: draft
source_url: "https://x.com/benjitaylor/status/2116593247854453244"
source_platform: x
author: "benjitaylor"
published: "2026-10-31"
captured_at: "2026-11-02T08:50:00Z"
captured_by: "routine:weekly-hot-list"
canonical_id: "x:tweet:2116593247854453244"
engagement: "likes=12651 reposts=622 views=1187405 bookmarks=22900"
tags: [topic/agent-tooling, hot-list, 2026-W44, agent-skills, faux-ui, product-demo, react, motion-design, frontend-design]
related: [hot-list/2026-W44]
needs_manual_text: false
---

## 摘要

X 設計主管 Benji Taylor 喺 2026-10-31 發佈 Stageshow：一個教 coding agent 整「假產品 UI」嘅 skill，例如 landing page hero 嘅示範動畫、feature card、bento grid、有游標嘅操作 demo。佢將自己手整呢類圖時嘅大量細微決定寫低，核心一句係「睇落似真產品、簡化到觀眾需要嘅程度、構圖有意圖、每個動作都有原因」，並列出五種常見失敗（太多、似線框圖、成個窗縮入卡片、平、悶）。skill 附幾十個金標準例子、一套 React 部件，仲有 `film.mjs` 等工具將 demo 拍成 contact sheet 俾 agent 自己檢查。用 `npx skills add` 一句就裝到 Claude Code、Codex、Gemini 等。呢個 post 一個人就過晒 X 三條門檻（1.2 萬 like、622 轉推、119 萬瀏覽），係今個星期唯一過 X gate 嘅項目，排 2026-W44 hot list 第三。

## Key facts

- **Install**: `npx skills add benjitaylor/skills --skill stageshow` (works for Claude Code, Codex, Gemini, Grok Build and other agents). Then ask for something small: one interaction, in one product, at one size, e.g. "A small looping demo for our homepage hero: someone assigns an issue to a teammate."
- **What the agent gets**: SKILL.md with the one idea, five failure modes, a seven-step workflow and a table of gold examples; references for framing, craft, motion, verify and rehearse; dozens of gold examples; a small React kit (stage, windows, phones, motion); `film.mjs` (films the demo, contact sheet, measurements), `jumps.mjs` (one-frame snaps), `layout.mjs` (text fits its boxes). Output is an ordinary React component.
- **Playground**: `npm install && npm run dev` in the skill folder shows every example, kit parts, and bad-vs-good comparisons.
- **Numbers (fxtwitter, 2026-11-02)**: 12,651 likes / 622 reposts / 1,187,405 views / 22,900 bookmarks, posted 2026-10-31. Clears all three X thresholds (2,000 / 500 / 1,000,000). The repo benjitaylor/skills (created 2026-10-26) has 591 stars, below every GitHub gate. SkillsMP lists the `stageshow` skill (no install count).
- **Caveat** (author): the first pass is a big step up, but most demos still take a few rounds of feedback; the taste encoded is his own.

## 點解值得留意

- 2026-W44 hot list 第三名（X 單平台 heat 0.70），亦係今個星期唯一滿足「至少一個社交入選」嘅項目，詳見 [[hot-list/2026-W44|hot-list/2026-W44]]。
- 「agent 自己拍片再自己檢查」嘅閉環（film → contact sheet → fix）係一個可以借用落其他視覺 skill 嘅模式。
- 同 Impeccable、taste-skill 一樣係「俾 agent 品味」嘅 skill，但專攻 marketing 用嘅產品示意圖同動畫。

## Source

- https://x.com/benjitaylor/status/2116593247854453244 — @benjitaylor (Benji Taylor) — 2026-10-31
- https://benji.org/stageshow (write-up) · https://github.com/benjitaylor/skills (repo)
- Reader: api.fxtwitter.com (post and counts), Jina Reader (benji.org), raw.githubusercontent.com (README, SKILL.md). Raw text in `raw/20261102-benji-taylor-stageshow-faux-ui-skill.md`.

## Related

- [[hot-list/2026-W44]]
- [[pages/20261026-impeccable-design-skill-for-coding-agents]]: design skill for coding agents (W43 winner)
- [[stars/Leonxlnx--taste-skill]]: agent skills that give coding agents taste
