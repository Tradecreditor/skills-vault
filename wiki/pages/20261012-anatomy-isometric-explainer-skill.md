---
title: "wheresryan22/anatomy — agent skill that explains an idea as an interactive isometric machine"
slug: 20261012-anatomy-isometric-explainer-skill
type: repo
status: draft
source_url: "https://github.com/wheresryan22/anatomy"
source_platform: github
author: "wheresryan22"
published: "2026-10-08"
captured_at: "2026-10-12T08:20:10Z"
captured_by: "routine:weekly-hot-list"
canonical_id: "github:wheresryan22/anatomy"
engagement: "stars=4232 forks=330 (created 2026-10-08); X @wheresryan22 likes=13292 reposts=1121 views=1447839"
tags: [hot-list, 2026-W41, agent-skills, claude-code, svg, webgl, visualization, explainer]
related: [hot-list/2026-W41]
needs_manual_text: false
---

## 摘要

Anatomy 係 @wheresryan22 開源（MIT）嘅 Agent Skill，主要畀 Claude Code 用，亦支援 OpenCode 同 Codex。佢用「整一部真正會運作嘅機器」嚟解釋技術概念：例如 cache key 變成一把所有 pin 對齊先扭得開嘅鎖。Claude 會用幾十個細小、有陰影嘅零件砌出一張等軸測（isometric）卡片，配標題、提示同即時讀數，可以用滑鼠同鍵盤互動，最後仲會放大逐個接位自己檢查。輸出有三種：SVG（核心）、SVG 加 WebGL shader（火、水、等離子、焦散），同埋 beta 嘅 3D 模式。佢係 2026-W41 hot list 第二名：10-08 開 repo，四日內 4,232 stars，加上作者發佈帖 13,292 likes / 145 萬 views。

## Key facts

- **Install**: `npx skills add wheresryan22/anatomy -g -a claude-code` (or `-a opencode` / `-a codex`; drop `-g` for one project). Git: `git clone https://github.com/wheresryan22/anatomy.git ~/.claude/skills/anatomy`.
- **Use**: in Claude Code `/anatomy explain how a token bucket rate limiter works, interactive`; OpenCode uses `/anatomy`, Codex uses `$anatomy`.
- **Output**: a standalone HTML page, a lone `.svg` with embedded styles, or React / Next.js components; light or dark theme (light is designed first).
- **Requirements**: Node 20.10+, zero dependencies, no API keys. The kit ships its own `scripts/capture.mjs` and `scripts/drive.mjs` for screenshots and self-checks.
- **Examples**: `raptor-engine` (11 assemblies that come apart, with an audit that no pipe passes through anything), `ripple-tank` (SVG plus two WebGL layers), `turning-dial` (3D beta, about 90 parts re-shaded per frame), `dial-indicator` (smallest, about 300 lines).
- **Numbers (2026-10-12)**: 4,232 stars / 330 forks, created 2026-10-08T10:12Z, so the whole total is in-window gain. X launch post [@wheresryan22 2108948624004526516](https://x.com/wheresryan22/status/2108948624004526516) (2026-10-10): 13,292 likes / 1,121 reposts / 1,447,839 views (fxtwitter).

## 點解值得留意

- 2026-W41 hot list 第二名（heat 0.94，GitHub + X 兩個平台過關），詳見 [[hot-list/2026-W41|hot-list/2026-W41]]。
- 同 vault 入面嘅 motion graphics / 解說片 skill（Opus 5.5 code-drawn video）同一個潮流，不過呢個係互動圖解而唔係影片，適合寫技術文章或者教學。
- 係可以直接裝嘅 skill，裝之前跟 [[../../skills/scanning-agent-skills/SKILL|scanning-agent-skills]] 掃一次。今次 routine 冇 draft vault SKILL.md：改 `skills/` 要同時更新 `handoff.md`，而 routine 唔可以改 handoff。

## Source

- https://github.com/wheresryan22/anatomy — @wheresryan22 — created 2026-10-08
- X: https://x.com/wheresryan22/status/2108948624004526516 (2026-10-10)
- Reader: raw.githubusercontent.com README (curl) + GitHub search API (connector); fxtwitter for X counts. Raw text in `raw/20261012-anatomy-isometric-explainer-skill.md`.

## Related

- [[hot-list/2026-W41]]
- [[pages/20261008-claude-tips-opus55-motion-graphics-six-prompts]]: code-drawn motion graphics with Opus 5.5, the same "draw it in code" trend

## Notes

- also trending 2026-W42 (github:wheresryan22/anatomy 16,390 stars on 2026-10-19, +12,158 since the 2026-10-12 snapshot; skills.sh 1.1K installs) — [[hot-list/2026-W42]]
