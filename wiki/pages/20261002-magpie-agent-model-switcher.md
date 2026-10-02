---
title: "magpie — one menu-bar panel and local gateway for every coding agent's model"
slug: 20261002-magpie-agent-model-switcher
type: repo
status: draft
source_url: "https://github.com/yetone/magpie"
source_platform: github
author: "yetone"
published: "2026-09-23"
captured_at: "2026-10-02T16:20:00Z"
captured_by: "routine:weekly-hot-list"
canonical_id: "github:yetone/magpie"
engagement: "stars=4232 forks=281"
tags: [hot-list, 2026-W39, coding-agent, claude-code, codex, llm-gateway, go, menu-bar]
related: [hot-list/2026-W39]
needs_manual_text: false
---

## 摘要

magpie（yetone）係 Go 寫嘅 menu bar app + CLI：一個畫面列出機器上每個 coding agent（Claude Code、Codex、Gemini CLI、OpenCode、Cursor CLI…）同佢用緊嘅 model，點一下就轉。底層係 127.0.0.1:3425 嘅本地 gateway，講 OpenAI Chat / Responses / Anthropic Messages，所以 Codex 可以行 DeepSeek、Claude Code 可以行 Kimi；已登入嘅 Claude / ChatGPT / Copilot 訂閱亦會變成其他 agent 可用嘅 provider。2026-09-23 開源，MIT。本週屬 GitHub 單平台入選：窗口內冇驗證到過 gate 嘅 X 貼文。

## Key facts

- **What**: Go (Wails) menu-bar app, terminal TUI (`magpie tui`), browser UI (`magpie web`) and plain CLI; MIT; under 15 MB.
- **Gateway**: `http://127.0.0.1:3425/v1` speaks OpenAI Chat Completions, OpenAI Responses and Anthropic Messages and translates streaming and tool calls between them.
- **Use**: `magpie provider add deepseek sk-…`, then `magpie codex deepseek/deepseek-v4-pro` or `magpie claude moonshot/kimi-k3`; `magpie save work` / `magpie use work` for profiles.
- **Safety**: edits only the key you change in each agent config (settings.json, config.toml), atomic writes, stash for switch-back; keys never read from env vars.
- **Numbers (2026-10-02)**: 4,232 stars, 281 forks (GitHub search API); created 2026-09-23. Third-party reports: 470 stars after ~1 day (Sep 24), 1,584 on Sep 29, so the in-window gain is below the 4,232 total.

## 點解值得留意

Hot list 2026-W39 入選項目，詳見 [[hot-list/2026-W39|hot-list/2026-W39]]。注意本次 run 喺 2026-10-02 執行，stars 為當日數字（建立至今累計），唔係窗口結束（09-27）嗰刻。

## Source

- https://github.com/yetone/magpie — yetone — 2026-09-23
- Reader: raw.githubusercontent.com README + GitHub search API (connector); raw text in `raw/20261002-magpie-agent-model-switcher.md`.

## Related

- [[hot-list/2026-W39]]
- [[pages/20260920-fast-jev-compaction]]
