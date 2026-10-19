---
title: "stablyai/orca — Orca ADE: run a fleet of coding agents side by side, each in its own worktree"
slug: 20261019-orca-ade-parallel-coding-agents
type: repo
status: draft
source_url: "https://github.com/stablyai/orca"
source_platform: github
author: "Stably (stablyai)"
published: "2026-03-17"
captured_at: "2026-10-19T08:21:37Z"
captured_by: "routine:weekly-hot-list"
canonical_id: "github:stablyai/orca"
engagement: "stars=97239 forks=6201 (+7130 stars since 2026-10-12 snapshot); skills.sh orchestration 8.4K installs, orca-cli 8.1K"
tags: [hot-list, 2026-W42, agent-ide, coding-agents, claude-code, codex, worktrees, orchestration, agent-skills]
related: [hot-list/2026-W42]
needs_manual_text: false
---

## 摘要

Orca 係 Stably（YC 投資）出嘅開源 ADE（Agent Development Environment，MIT），專門用嚟同時行一隊 coding agent：Claude Code、Codex、OpenCode、Pi、Grok、DeepSeek Harness 等任何喺 terminal 行得嘅 CLI agent 都得，每個 agent 有自己嘅 git worktree，唔會互相踩腳，最後比較結果再 merge 最好嗰個。佢有 WebGL terminal、Design Mode（喺 Chromium 揀 UI 元素，HTML/CSS 同截圖直接入 prompt）、GitHub / Linear 整合、SSH worktree、手機 app 遙控，仲有 `orca` CLI 等 agent 反過嚟操控 Orca。用嘅係你自己嘅訂閱，唔使另外買 API。佢係 2026-W42 hot list 第二名：一星期 +7,130 stars，W41 已經喺 Watch（+4,849）。

## Key facts

- **Install**: download from https://onorca.dev/download, or `brew install --cask stablyai/orca/orca` (macOS), `yay -S stably-orca-bin` (Arch). Mobile companion on iOS App Store and Android APK.
- **Core model**: fan one prompt across several agents, each in an isolated git worktree; compare diffs, merge the winner. Built-in orchestration lets one coordinator agent delegate to workers.
- **Agent-facing pieces**: `orca` CLI (`orca worktree create`, `snapshot`, `click`, `fill`), Computer Use, account switcher with Claude / Codex usage and rate-limit tracking. Its own agent skills (`orchestration`, `orca-cli`, `orca-linear`, ...) are on skills.sh and SkillsMP.
- **Numbers (2026-10-19)**: 97,239 stars / 6,201 forks; 90,109 in the 2026-10-12 snapshot, so **+7,130 in 7 days**. Jev `topical` 0.94. skills.sh trending: `orchestration` 8.4K and `orca-cli` 8.1K weekly installs (registry corroboration). Best in-window X post: @orca_build 2111227669920756188 (2026-10-16) 247 likes / 9 reposts / 13,338 views; @lxfater 2110731820429946883 (2026-10-15) 245 likes / 41 / 27,171 (fxtwitter), below every X gate.
- Telemetry: anonymous usage data with an opt-out (README links the privacy docs).

## 點解值得留意

- 2026-W42 hot list 第二名（heat 0.80，GitHub 單平台，加上 skills.sh 安裝量佐證）。同 dsh-our-free-model 同分，按實測增幅排第二，詳見 [[hot-list/2026-W42|hot-list/2026-W42]]。
- Jeff 而家用 Claude Code 為主，有時開 Codex：Orca 可以將兩個放埋一齊、各自一個 worktree 跑同一個任務再揀，同 [[pages/20261005-herdr-claude-code-codex-side-by-side|herdr]] 係同一個方向，不過係完整桌面 app。
- 嚟緊試嘅話留意：每個 agent 用你自己帳號嘅額度，平行跑會快啲燒完 rate limit。

## Source

- https://github.com/stablyai/orca — Stably — created 2026-03-17
- Reader: raw.githubusercontent.com README (curl) + GitHub search API (connector) for counts; skills.sh trending via Exa. Raw text in `raw/20261019-orca-ade-parallel-coding-agents.md`.

## Related

- [[hot-list/2026-W42]]
- [[pages/20261005-herdr-claude-code-codex-side-by-side]]: terminal panes for Claude Code and Codex side by side; Orca does the same in a desktop app with worktrees
- [[pages/20261005-openrig-persistent-claude-code-codex-agent-team]]: another way to keep a Claude Code + Codex team running
