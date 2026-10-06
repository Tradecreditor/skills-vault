---
title: "herdr: Claude Code and Codex working side by side (romanticamaj)"
slug: 20261005-herdr-claude-code-codex-side-by-side
type: video
status: draft
source_url: "https://www.instagram.com/reel/DeHE7FFSzUq/"
source_platform: instagram
author: "romanticamaj"
published: "2026-10-05"
captured_at: "2026-10-06T10:00:00Z"
captured_by: "routine:capture-link"
canonical_id: "instagram:DeHE7FFSzUq"
engagement: "not shown by reader"
tags: [topic/agent-tooling, herdr, claude-code, codex, multi-agent, code-review]
related: []
needs_manual_text: false
---
## 摘要
呢條 Instagram reel（Gary Hsieh / romanticamaj）介紹 herdr：用一行指令，Claude Code 就會開一個 Codex 視窗，兩個 AI 喺你面前直接對話，你睇得到亦可以隨時介入。同 Codex rescue 或 subagent 唔同，嗰啲過程無法直接插手。用途包括互相 code review，以及交叉驗證教學投影片、報告同報表。底層係 herdr 開一個 socket API，幫 AI 喺對方終端機打字，再將畫面讀返出嚟；作者認為呢種輕量做法日後會成為工程師同 AI 用家嘅基本環境。

## Key facts
- herdr exposes a socket API so one agent can type into another agent's terminal and read the screen back.
- Claude Code opens a Codex window; both agents converse visibly and the human can intervene at any time.
- Contrast with Codex rescue / subagents, where the exchange cannot be interrupted directly.
- Use cases named: mutual code review, cross-checking slides, reports and spreadsheets.
- The caption gives no install command or repo link; caption only, no audio transcript. Engagement counts not returned by the reader.

## 點解值得留意
- 同 vault 已有嘅 Codex 委派流程相關，herdr 提供可見、可介入嘅雙 agent 對話方式。
- 可試用於 code review 交叉驗證，同 OpenRig 一類持久多 agent 設定對照。

## Source
- https://www.instagram.com/reel/DeHE7FFSzUq/ — romanticamaj (Gary Hsieh), 2026-10-05. Reader: Jina (caption in Title and body).

## Related
- [[../pages/20261005-openrig-persistent-claude-code-codex-agent-team|OpenRig: persistent Claude Code + Codex agent team]]
- [[../../skills/delegating-to-codex/SKILL|skill: delegating-to-codex]]
