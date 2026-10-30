---
title: "morluto/rea — REA: Reverse Engineer Anything, one MCP for agent-driven reverse engineering"
slug: 20261012-rea-reverse-engineer-anything
type: repo
status: draft
source_url: "https://github.com/morluto/rea"
source_platform: github
author: "morluto"
published: "2026-04-14"
captured_at: "2026-10-12T08:20:10Z"
captured_by: "routine:weekly-hot-list"
canonical_id: "github:morluto/rea"
engagement: "stars=122874 forks=27598 (+119603 stars since 2026-10-05 snapshot); X @MatthewBerman likes=37504 reposts=3280 views=3233963"
tags: [hot-list, 2026-W41, mcp, reverse-engineering, coding-agents, claude-code, codex, binary-analysis]
related: [hot-list/2026-W41]
needs_manual_text: false
---

## 摘要

REA（Reverse Engineer Anything）係 morluto 開源（MIT）嘅 MCP server 加 CLI，令 Claude Code、Codex、Cursor、Gemini CLI 等 coding agent 可以喺冇 source code 嘅情況下拆解一個 app：睇 native binary 嘅 pseudocode / assembly、JavaScript / Electron app 嘅模組同 IPC、.NET assembly、Android APK、網站同網絡 capture，然後解釋某個功能點運作、列出證據，再幫你喺自己項目重做一個版本。`npx rea-agents setup` 會幫你揀 agent、註冊 MCP 同裝埋對應 workflow 指示。Native 分析會用你已有嘅 Hopper、Ghidra 或 IDA。佢係 2026-W41 hot list 第一名：一星期內 GitHub 由 3,271 升到 122,874 stars，加上 Matthew Berman 一條 X 帖 37,504 likes / 323 萬 views。

## Key facts

- **What it is**: `github.com/morluto/rea`, npm package `rea-agents`. "One MCP for reverse engineering across binaries, applications, and runtime behavior." Analysis runs locally; results include evidence and stated limitations.
- **Install**: `npx rea-agents setup` (pick agents, review proposed config changes, approve; backs up existing config; restart the agent). Global CLI: `npm install --global rea-agents`, then `rea --help`; update with `rea update` or `npx rea-agents@latest setup`.
- **Use**: ask the agent e.g. "Understand how search works in the Notes app, show me the evidence, and build a similar feature for my project." Terminal: `npx -y rea-agents@latest analyze-javascript-application /abs/path/to/app --json`.
- **Targets**: native binaries (Hopper / Ghidra / IDA), Go binaries, WASM, EVM bytecode, JavaScript / Electron / ASAR, websites (Chrome-family browser), HAR captures, .NET, Android APKs and devices (JADX, adb), firmware (Binwalk / Unblob), process behaviour capture.
- **Requirements**: Node.js 22.19+, 24.11+ or 26+; extra tools per target. Supported agents: Claude Code, Codex, Cursor, Gemini CLI, Grok Build and others.
- **Numbers (2026-10-12)**: 122,874 stars / 27,598 forks; 3,271 in the 2026-10-05 snapshot, so **+119,603 in 7 days**. X: [@MatthewBerman 2108245653843509415](https://x.com/MatthewBerman/status/2108245653843509415) (2026-10-08) 37,504 likes / 3,280 reposts / 3,233,963 views (fxtwitter). SkillsMP lists its `reverse-engineer-anything` skill; it is not on the skills.sh 24h trending page.

## 點解值得留意

- 2026-W41 hot list 第一名（heat 0.94，GitHub + X 兩個平台過關），詳見 [[hot-list/2026-W41|hot-list/2026-W41]]。
- 一星期 +119,603 stars、forks 27,598，呢個增幅極之罕見；分數照計，但唔好當佢係用家數量，可能有一部分係病毒式傳播或者灌星。
- 「睇到人哋 app 有個功能，叫 agent 拆嚟睇再自己整」係實用嘅 workflow，但要留意目標軟件嘅授權條款，同埋 runtime capture 會用你自己嘅權限執行目標程式。

## Source

- https://github.com/morluto/rea — morluto — created 2026-04-14
- X amplification: https://x.com/MatthewBerman/status/2108245653843509415 (2026-10-08)
- Reader: raw.githubusercontent.com README (curl) + GitHub search API (connector); fxtwitter for X counts. Raw text in `raw/20261012-rea-reverse-engineer-anything.md`.

## Related

- [[hot-list/2026-W41]]
- [[pages/20261005-universal-modder-claude-code-game-modding]]: another repo that gives Claude Code reverse-engineering tools, for game modding

## Notes

- also trending 2026-W42 (327,790 stars on 2026-10-19, +204,916 since 2026-10-12; 82,965 forks; numbers from [[hot-list/2026-W42]], written here by the W43 run because the page was not on `main` then)
- also trending 2026-W43 (386,840 stars / 96,900 forks on 2026-10-26, +59,050 since 2026-10-19; GitHub search API; see [[hot-list/2026-W43]])
