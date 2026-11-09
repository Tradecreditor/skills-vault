---
title: "storytold/craft-anything — Craft Anything: study any website, app or game, then have a coding agent rebuild it"
slug: 20261109-craft-anything-rebuild-any-software-with-agents
type: repo
status: draft
source_url: "https://github.com/storytold/craft-anything"
source_platform: github
author: "storytold"
published: "2026-10-31"
captured_at: "2026-11-09T08:20:00Z"
captured_by: "routine:weekly-hot-list"
canonical_id: "github:storytold/craft-anything"
engagement: "stars=23395 forks=4655 (2026-11-09; 1858 in the 2026-11-02 snapshot, +21526 in 7 days)"
tags: [hot-list, 2026-W45, coding-agents, mcp-server, reverse-engineering, claude-code, rust, clean-room, app-cloning]
related: [hot-list/2026-W45]
needs_manual_text: false
---

## 摘要

Craft Anything 係 storytold（ArtCraft 團隊）2026-10-31 開源嘅 Rust 引擎：指住一個網站、桌面或手機 app、遊戲或者檔案，講一句「照住整一個」，佢就用真嘅檢查工具研究原版，再叫你電腦上嘅 coding agent（首選 Claude Code）用你指定嘅語言或框架起一個新 project，然後同原版比較、逐步修到似為止。流程分 Study → Build → Check → Ready 四步，有簡單模式同進階工作台。預設係 clean room：唔讀原版嘅 code、檔案或者網頁 source，只用肉眼睇到嘅嘢；開 Deep 模式先會反編譯同讀 JavaScript，只限私人用途。320 個工具每個都係 CLI 指令兼 MCP tool，所以任何 agent 都可以直接驅動。一星期由 1,858 升到 23,395 stars，係 2026-W45 hot list 第一名。

## Key facts

- **What**: a pure-Rust reverse-engineering engine plus desktop app (egui), CLI and MCP server. It inspects a target (pages at three widths, code, files, runs), has a coding agent build a new project in the stack you name, compares the build with the original and refines it.
- **Modes**: *Clean room* (default) works only from what a visitor can see (screenshots, visible text, measured layout, colours, fonts) and refuses tools that look inside; *Deep* uses every tool (built-in decoders, disassembler, decompiler, Ghidra when installed) for private use. Clean room is a product rule, not an OS sandbox: the coding agent still acts as you.
- **Agents**: Claude Code first (runs your own unmodified `claude` with your own sign-in); a Codex adapter exists but is unverified; GitHub Copilot CLI and Grok Build via ACP; other ACP agents (Gemini CLI, Qwen Code, opencode, goose, Hermes, Maki) can be switched in.
- **Install**: Rust 1.97+; `git clone https://github.com/storytold/craft-anything && cd craft-anything`, `cargo run --release -p craft-anything` (app), `cargo install --path apps/craft-anything-cli` (CLI), `craft-anything-cli doctor`. Agent use: `craft-anything-cli mcp` serves all tools to an MCP client; `craft-anything-cli rebuild https://example.com "Recreate this website"`.
- **Numbers**: 23,395 stars / 4,655 forks on 2026-11-09, created 2026-10-31 14:50 UTC; 1,858 in the 2026-11-02 snapshot, so **+21,526 in 7 days**. Apache-2.0. Clears the new-repo gate (10,000) and the gain gate (3,000).
- **X**: no post cleared the X gate. Largest verified: @huangyun_122 [2118948396589592786](https://x.com/huangyun_122/status/2118948396589592786) 495 likes / 76 reposts / 33,606 views; @HeLi8866 142 / 20 / 9,887; @0xk7ro 35 / 1 / 1,359 (fxtwitter). Several posts say it comes from the same team as REA (morluto/rea, W41 winner).

## 點解值得留意

- 2026-W45 hot list 第一名（heat 0.80，GitHub 單平台），一星期 +21,526 stars 係今個星期最大增幅，詳見 [[hot-list/2026-W45|hot-list/2026-W45]]。
- 「研究原版 → agent 重建 → 自動比對 → 修正」呢個 loop 係 coding agent 嘅一個完整用法示範，而且每個工具都開放做 MCP tool。
- 法律同道德風險要自己判斷：clean room 只係產品規則，Deep 模式會反編譯；用之前讀 `docs/claude-code.md` 同佢對 agent 權限嘅說明。
- 同 [[pages/20261012-rea-reverse-engineer-anything|REA]] 屬同一方向（逆向 + agent），今個星期 REA 再加 +24,718 stars。

## Source

- https://github.com/storytold/craft-anything — storytold — created 2026-10-31
- Reader: raw.githubusercontent.com README (curl), GitHub search API (`gh api`) for counts, api.fxtwitter.com for the X posts. Raw text in `raw/20261109-craft-anything-rebuild-any-software-with-agents.md`.

## Related

- [[hot-list/2026-W45]]
- [[pages/20261012-rea-reverse-engineer-anything]]: reverse engineering with agents (W41 winner)
