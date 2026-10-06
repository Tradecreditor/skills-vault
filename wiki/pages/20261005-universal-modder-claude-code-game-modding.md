---
title: "universal-modder — skills, um CLI and fal MCP that let coding agents mod almost any PC game"
slug: 20261005-universal-modder-claude-code-game-modding
type: repo
status: draft
source_url: "https://github.com/rehan-remade/universal-modder"
source_platform: github
author: "rehan-remade (Rehan Sheikh, @rehan_shei)"
published: "2026-09-30"
captured_at: "2026-10-05T08:19:24Z"
captured_by: "routine:weekly-hot-list"
canonical_id: "github:rehan-remade/universal-modder"
engagement: "stars=3419 forks=297; X launch post likes=14124 reposts=878 views=3686837"
tags: [hot-list, 2026-W40, claude-code-plugin, agent-skills, game-modding, reverse-engineering, mcp, fal]
related: [hot-list/2026-W40]
needs_manual_text: false
---

## 摘要

universal-modder 係 fal 工程師 Rehan Sheikh 喺 2026-09-30 開源（MIT）嘅一套 Agent Skills + `um` CLI + fal MCP server，等 Claude Code、Codex、Cursor、Gemini CLI、Copilot、OpenCode 呢類 coding agent 可以幫你 mod 幾乎任何你擁有嘅 PC 遊戲。Agent 會先查共享知識庫、偵測遊戲引擎同 anti-cheat、揀 modding 路線、備份存檔、讀真正嘅 code（ILSpy / Ghidra / Frida 等），做一個可行切片，再用 fal 生成 sprite / 3D / 音效，喺真遊戲入面驗證，最後剪 showcase 片同寫 field note 畀下一個 agent。示範包括 Terraria 武器 mod、Age of Empires II 新文明同 Minecraft × GTA V。佢係 2026-W40 hot list 嘅 GitHub + X 雙平台入選項目。

## Key facts

- **Install (Claude Code)**: `/plugin marketplace add rehan-remade/universal-modder`, then `/plugin install universal-modder@universal-modder`.
- **Other agents**: Codex `codex plugin marketplace add rehan-remade/universal-modder` + `codex plugin add universal-modder@universal-modder`; Gemini CLI `gemini extensions install https://github.com/rehan-remade/universal-modder`; skills only `npx skills add https://github.com/rehan-remade/universal-modder`.
- **CLI elsewhere**: `uv tool install git+https://github.com/rehan-remade/universal-modder` (or pipx). Needs Python 3.10+, ffmpeg; Blender for 3D→sprite; `FAL_KEY` for fal assets (paid), or `um comfy` with a local ComfyUI server.
- **Skills**: `mod-any-game` (loop + 12 engine playbooks), `game-recon`, `reverse-engineering`, `fal-assets`, `asset-pipeline`, `game-automation`, `showcase-video`, `mashup-mods`, `publish-mod`, `share-field-notes`.
- **Safety rules (README)**: refuses anti-cheat injection, cheats against other players, DRM/ownership bypass; never ships game files or decompiled code; backs up saves; asks before driving mouse/keyboard, installing loaders or publishing.
- **Numbers**: GitHub 3,419 stars / 297 forks on 2026-10-05 (repo created 2026-09-30, so the total is the in-window gain). X launch post [@rehan_shei 2105161487509852622](https://x.com/rehan_shei/status/2105161487509852622): 14,124 likes, 878 reposts, 3,686,837 views (fxtwitter, 2026-10-05).

## 點解值得留意

- Hot list 2026-W40 第一名（heat 0.94，GitHub topical gate + X 單帖 gate），詳見 [[hot-list/2026-W40|hot-list/2026-W40]]。
- 「知識庫由 AI 寫畀 AI」（field notes + PR）同呢個 vault 嘅 LLM-wiki 思路一樣，可以參考佢點樣要求 agent 記錄 symptom → cause → fix。
- 冇另外 draft SKILL.md：repo 本身已經係可安裝 skills，vault 包一層冇增值；要用就直接裝原 repo（先用 `skills/scanning-agent-skills` 掃）。

## Source

- https://github.com/rehan-remade/universal-modder — Rehan Sheikh (rehan-remade) — 2026-09-30
- X: https://x.com/rehan_shei/status/2105161487509852622 (2026-09-30)
- Reader: raw.githubusercontent.com README (curl) + GitHub search API (connector) + fxtwitter (curl); raw text in `raw/20261005-universal-modder-claude-code-game-modding.md`.

## Related

- [[hot-list/2026-W40]]
- [[../../skills/scanning-agent-skills/SKILL|skill: scanning-agent-skills]]
- [[pages/20260921-4-claude-code-plugins]]
