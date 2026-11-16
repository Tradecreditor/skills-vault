---
title: "milind-soni/OpenMausBot — OpenMausBot: open-source Grok Bot alternative, a chat app of local Claude / Codex agents that each get a computer"
slug: 20261116-openmausbot-open-source-grok-bot-alternative
type: repo
status: draft
source_url: "https://github.com/milind-soni/OpenMausBot"
source_platform: github
author: "milind-soni"
published: "2026-08-11"
captured_at: "2026-11-16T08:20:00Z"
captured_by: "routine:weekly-hot-list"
canonical_id: "github:milind-soni/OpenMausBot"
engagement: "stars=23725 forks=3304 (2026-11-16; 18885 in the 2026-11-09 snapshot, +4835 in 7 days)"
tags: [hot-list, 2026-W46, ai-agents, computer-use, claude-code, codex, multi-agent, electron, self-hosted, composio]
related: [hot-list/2026-W46]
needs_manual_text: false
---

## 摘要

OpenMausBot 係一個開源、本機優先嘅「AI bot 聊天 app」：側邊欄每一個 bot 都係一個真嘅 agent，底層用你部機已經登入咗嘅 `claude`、`codex` 或 `grok` CLI 去跑，唔使開新帳戶，亦冇 proxy 喺中間。每個 bot 有自己嘅性格、模型同一部電腦（雲端 Linux 桌面、隔離嘅本機 VM，或者明確 opt-in 之後用你自己部機），仲可以經 Composio 連 Gmail、Slack、GitHub、Notion 等 500 幾個 app。Shell 指令、改檔同問題會變成對話入面嘅 Allow / Deny 卡，由你批准先做。佢自稱係 xAI Grok Bot、Meta Muse、OpenAI dots、Manus Cue 呢類封閉個人 agent 產品嘅開源版本（Apache-2.0，Electron 桌面 app，macOS / Windows / Ubuntu）。

## Key facts

- **What**: an Electron + React + TypeScript desktop app (macOS Apple silicon / Intel, Windows x64, Ubuntu 24.04) that presents agents as chat contacts. One small harness server on `127.0.0.1` owns every agent process; transcripts, keys and events live in `~/.openmausbot`.
- **Engines**: bring-your-own agent CLIs (`claude`, `codex`, `grok`) with your existing logins; any engine can point at a custom CLI binary (Settings → Engines). Per-bot model picker, switchable mid-conversation.
- **Computers**: each bot can use a cloud Linux desktop (live preview, "Open desktop" to take over), an isolated local VM, or the host machine after explicit opt-in (macOS and Ubuntu Xorg; Ubuntu Wayland host control disabled pending issue #345).
- **Safety**: a permission broker turns shell commands, file edits and questions into inline approval cards. Apps connect over OAuth through Composio Sessions.
- **Install**: signed and notarized `.dmg` (Apple silicon / Intel), `OpenMausBot-setup.exe`, `OpenMausBot-amd64.deb` from GitHub Releases or openmausbot.com/download. Apache-2.0. The README states it is independent of xAI and has no crypto token.
- **Numbers**: 23,725 stars / 3,304 forks on 2026-11-16, created 2026-08-11; 18,885 in the 2026-11-09 snapshot, so **+4,835 in 7 days**. Clears the gain gate (3,000) and the new-repo gate (10,000: 23,725 / 10,000 = 2.37, capped at 2.0 → heat 0.80). It qualified without winning in W44 (+5,252) and W45 (+8,008).

## 點解值得留意

- 2026-W46 hot list 第二名（heat 0.80，GitHub 單平台，同分以實測增長排序），詳見 [[hot-list/2026-W46|hot-list/2026-W46]]。
- 「一隊 agent 擺喺聊天 app 入面、每個有自己電腦」係今年 Grok Bot / Muse / dots / Cue 帶起嘅產品形態；呢個係用你自己 Claude Code / Codex 訂閱去跑嘅開源版，連續三個星期合資格。
- 權限好大（可以控制本機、連 500 個 app），用之前睇清楚 host control 嘅 opt-in 同 approval 設定；OAuth token 經 Composio。

## Source

- https://github.com/milind-soni/OpenMausBot — milind-soni — created 2026-08-11
- Reader: raw.githubusercontent.com README.md (curl), GitHub search API (`gh api`) for counts. Raw text in `raw/20261116-openmausbot-open-source-grok-bot-alternative.md`.

## Related

- [[hot-list/2026-W46]]
- [[hot-list/2026-W44]], [[hot-list/2026-W45]]: earlier weeks where it qualified and lost the tie-break
