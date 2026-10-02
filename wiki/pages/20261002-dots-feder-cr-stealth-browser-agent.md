---
title: "dots — open-source web agent on a patched Firefox that does not get blocked"
slug: 20261002-dots-feder-cr-stealth-browser-agent
type: repo
status: draft
source_url: "https://github.com/feder-cr/dots"
source_platform: github
author: "feder-cr"
published: "2026-09-29"
captured_at: "2026-10-02T23:22:00Z"
captured_by: "claude-code-cloud"
canonical_id: "github:feder-cr/dots"
engagement: "stars=2465 forks=433"
tags: [hot-list, 2026-W40, agent-tooling, browser-agent, anti-detect, firefox, openrouter, mcp, python]
related: [hot-list/2026-W40]
needs_manual_text: false
---

## 摘要

dots（feder-cr）係開源版「dots for the web」：一個 web agent 配一個喺 C++ 層面改過嘅 Firefox 引擎，fingerprint 喺引擎內部決定而唔係用 JavaScript 蓋住，一個 `--seed` 一個前後一致嘅身份（螢幕、字型、GPU、時區、語言），冇 WebDriver 旗、冇 DevTools 協定、冇 automation globals，滑鼠會真係移去目標、鍵一個一個按，`--profile-dir` 保留登入，`--proxy` 令時區語言跟出口。模型係 OpenRouter 上任何一個，`--model` 換。安裝用 uv：`uvx --from git+https://github.com/feder-cr/dots dots --openrouter-key sk-or-...`，開 http://127.0.0.1:8765 左邊對話右邊實時瀏覽器。同一個瀏覽器經 invisible_playwright_mcp 可以俾 Claude Code、Codex、Gemini CLI 用。2026-09-29 建立，10-02 有 2,465 stars。

## Key facts

- **What**: web agent + patched Firefox engine (C++), fingerprint decided in-engine; one identity per `--seed`; no WebDriver / DevTools / automation globals; human-like pointer and key events; `--profile-dir`, `--proxy`. MIT, not affiliated with OpenAI.
- **Install**: `curl -LsSf https://astral.sh/uv/install.sh | sh` then `uvx --from git+https://github.com/feder-cr/dots dots --openrouter-key sk-or-...` (Windows: `irm https://astral.sh/uv/install.ps1 | iex`); UI at http://127.0.0.1:8765.
- **Model**: any OpenRouter model via `--model`.
- **For coding agents**: the same browser as an MCP server through github.com/feder-cr/invisible_playwright_mcp (Claude Code, Codex, Gemini CLI or any MCP client).
- **GitHub (2026-10-02)**: 2,465 stars, 433 forks, created 2026-09-29; no in-window X post by @feder_cr. Jev `topical` 0.93.

## 點解值得留意

Hot list 2026-W40（開發測試 run）入選第三位，詳見 [[hot-list/2026-W40|hot-list/2026-W40]]。對 vault 嘅意義：browser agent 嘅「被封」問題由瀏覽器層解決，同 moli（Rust headless）、OpenBot 係同一個熱點；invisible_playwright_mcp 可以直接接入 Claude Code 嘅 browser 工作流。注意 anti-detect 瀏覽器嘅用途要自己把關。

## Source

- https://github.com/feder-cr/dots — feder-cr — 2026-09-29
- Reader: raw.githubusercontent.com README (curl); star/fork counts from the GitHub repos API through the Exa / Jina relay; X counts from fxtwitter. Raw text in `raw/20261002-dots-feder-cr-stealth-browser-agent.md`. Captured by a Claude Code development run of the weekly-hot-list routine on 2026-10-02.

## Related

- [[hot-list/2026-W40]]
- [[pages/20260930-ui-ux-pro-max]]
