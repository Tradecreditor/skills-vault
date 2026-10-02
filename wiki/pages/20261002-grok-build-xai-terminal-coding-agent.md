---
title: "Grok Build — SpaceXAI's open-source terminal coding agent (Rust TUI, ACP, headless)"
slug: 20261002-grok-build-xai-terminal-coding-agent
type: repo
status: draft
source_url: "https://github.com/xai-org/grok-build"
source_platform: github
author: "xai-org"
published: "2026-07-14"
captured_at: "2026-10-02T23:22:00Z"
captured_by: "claude-code-cloud"
canonical_id: "github:xai-org/grok-build"
engagement: "stars=27197 forks=5117"
tags: [hot-list, 2026-W40, coding-agent, harness, cli, tui, rust, acp, mcp, xai]
related: [hot-list/2026-W40]
needs_manual_text: false
---

## 摘要

Grok Build（指令 `grok`）係 SpaceXAI 開源嘅終端 coding agent：Rust 寫嘅全螢幕 TUI，識讀整個 codebase、改檔、跑 shell 指令、搜網同管理長時間任務，可以互動用、headless 用於腳本同 CI，或者經 Agent Client Protocol（ACP）嵌入編輯器。Repo 係由 SpaceXAI monorepo 定期同步出嚟嘅 Rust 原始碼（根目錄 `SOURCE_REV` 記住 monorepo commit），用家指南涵蓋快捷鍵、slash commands、設定、主題、MCP servers、skills、plugins、hooks、headless 同 sandboxing。2026-07-14 建立，10-02 已有 27,197 stars、5,117 forks，係今個星期 hot list 以 new-repo gate（90 日內、過萬 star）入選嘅項目；因為冇窗口前 snapshot，7 日增長未知。

## Key facts

- **What**: SpaceXAI's `grok` CLI/TUI and agent runtime, Rust, synced periodically from the SpaceXAI monorepo (`SOURCE_REV` records the commit).
- **Install**: `curl -fsSL https://x.ai/cli/install.sh | bash` (macOS / Linux / Git Bash) or `irm https://x.ai/cli/install.ps1 | iex` (Windows); `grok --version`. First launch opens the browser to authenticate.
- **Build**: pinned Rust toolchain, DotSlash for hermetic `bin/protoc`; `cargo run -p xai-grok-pager-bin`; the binary is `xai-grok-pager`, shipped as `grok`.
- **Modes**: interactive TUI, headless for scripting/CI, embedded in editors via ACP; docs cover MCP servers, skills, plugins, hooks, sandboxing (docs.x.ai/build/overview).
- **Numbers (2026-10-02)**: 27,197 stars, 5,117 forks (GitHub API via relay); created 2026-07-14; last push 2026-09-29. 7-day gain unknown (no pre-window snapshot). Jev `topical` 0.93.

## 點解值得留意

Hot list 2026-W40（開發測試 run）入選第一位，詳見 [[hot-list/2026-W40|hot-list/2026-W40]]。入選靠 new-repo gate（建立 80 日、27k stars），唔係一週增長，所以「今個星期有幾熱」其實未知；入 snapshot 之後下星期先有 delta。對 vault 嘅意義：又一個大廠開源 coding agent harness，同 Claude Code / Codex / ZCode 同一個賽道，ACP 嵌入同 skills / plugins / hooks 體系值得同 Claude Code 對照。

## Source

- https://github.com/xai-org/grok-build — xai-org — 2026-07-14
- Reader: raw.githubusercontent.com README (curl); star/fork counts from the GitHub repos API through the Exa / Jina relay; X counts from fxtwitter. Raw text in `raw/20261002-grok-build-xai-terminal-coding-agent.md`. Captured by a Claude Code development run of the weekly-hot-list routine on 2026-10-02.

## Related

- [[hot-list/2026-W40]]
- [[pages/20261002-zcode-zai-harness]]
