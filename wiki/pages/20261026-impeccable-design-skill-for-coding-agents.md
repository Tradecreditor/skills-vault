---
title: "pbakaus/impeccable — Impeccable: design skill, 24 commands and anti-slop detectors for coding agents"
slug: 20261026-impeccable-design-skill-for-coding-agents
type: repo
status: draft
source_url: "https://github.com/pbakaus/impeccable"
source_platform: github
author: "Paul Bakaus (pbakaus)"
published: "2025-11-16"
captured_at: "2026-10-26T08:20:00Z"
captured_by: "routine:weekly-hot-list"
canonical_id: "github:pbakaus/impeccable"
engagement: "stars=88193 forks=5267 (+5341 stars since 2026-10-19 snapshot); X @pbakaus 598 likes (2026-10-20)"
tags: [hot-list, 2026-W43, agent-skills, frontend-design, ui-design, anti-slop, claude-code, codex, cursor]
related: [hot-list/2026-W43]
needs_manual_text: false
---

## 摘要

Impeccable 係 Paul Bakaus 做嘅設計 skill（Apache-2.0），俾 Claude Code、Codex、Cursor、Gemini CLI、Grok Build 等 coding agent 用，目標係避開 AI 前端嘅老套樣：Inter 字體、紫藍漸變、卡片包卡片、彩色底灰字之類。一個 skill 有 24 個指令（`/impeccable polish`、`audit`、`critique`、`bolder`、`live` 等），`/impeccable init` 會先記低產品資料去 `PRODUCT.md`，之後指令就知受眾同限制。佢仲有 62 條唔使 LLM、唔使 API key 嘅確定性偵測規則，CLI 同瀏覽器擴充都行到。今個星期佢加咗一個自動 hillclimb 同 polish 前端嘅 sub-agent。佢係 2026-W43 hot list 第三名：一星期 +5,341 stars。

## Key facts

- **Install**: from the project root `npx impeccable install` (detects `~/.claude`, `~/.codex`, `~/.grok`, `~/.hermes`, `.cursor` and asks for project or global scope; `--providers=claude,codex,cursor,...` and `--scope=project|global` for scripts), then run `/impeccable init` inside the agent. Manual and Git installs work without Node; each skill copy ships a small launcher that runs a self-contained engine binary, downloaded once into `~/.impeccable/bin/` if it is not bundled.
- **Commands**: `craft`, `init`, `document` (writes `DESIGN.md`), `extract`, `shape`, `critique`, `audit`, `polish`, `bolder`, `quieter`, `distill`, `harden`, `onboard`, `animate`, `colorize`, `typeset`, `layout`, `delight`, `overdrive`, `clarify`, `adapt`, `optimize`, `live`, `generate`; `/impeccable pin <command>` makes a shortcut such as `/audit`.
- **Detectors**: 62 deterministic rules plus LLM-only critique checks; on Claude Code, Cursor, Codex, Copilot and Grok Build the installer also adds provider-native edit hooks.
- **Numbers (2026-10-26, GitHub search API)**: 88,193 stars / 5,267 forks, created 2025-11-16; 82,852 in the 2026-10-19 snapshot, so **+5,341 in 7 days** (W42: +2,839). Topical by README (an agent skill).
- **Social (fxtwitter)**: @pbakaus [2112646940278354248](https://x.com/pbakaus/status/2112646940278354248) (2026-10-20) 598 likes / 14 reposts / 75,043 views; [2113065895069368804](https://x.com/pbakaus/status/2113065895069368804) (2026-10-22, the new hillclimbing sub-agent) 368 / 7 / 20,412. Below every X gate. SkillsMP lists the skill in pbakaus's repo and copies in NousResearch's hermes-agent and nexu-io's open-design.

## 點解值得留意

- 2026-W43 hot list 第三名（heat 0.80，GitHub 單平台），同分項目入面實測增幅排第三，詳見 [[hot-list/2026-W43|hot-list/2026-W43]]。
- Jeff 已經收咗同類嘅 [[stars/Leonxlnx--taste-skill|taste-skill]] 同 [[stars/VoltAgent--awesome-design-md|awesome-design-md]]：Impeccable 嘅分別係有指令詞彙同唔使 LLM 嘅偵測規則，可以當 lint 咁行。
- 安裝器會喺專案加 edit hooks，第一次會下載一個 binary：喺 vault 以外嘅專案先試。佢本身已經係 skill，所以 vault 唔另外起 SKILL.md。

## Source

- https://github.com/pbakaus/impeccable — Paul Bakaus — created 2025-11-16
- Reader: raw.githubusercontent.com README (curl) + GitHub search API (connector) for counts; fxtwitter for the @pbakaus timeline. Raw text in `raw/20261026-impeccable-design-skill-for-coding-agents.md`.

## Related

- [[hot-list/2026-W43]]
- [[stars/Leonxlnx--taste-skill]]: agent skills that give coding agents taste, the closest neighbour
- [[stars/VoltAgent--awesome-design-md]]: DESIGN.md files that a coding agent can follow
- [[pages/20260924-4-free-design-sites-for-vibe-coders]]: design references for vibe coders
