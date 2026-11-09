---
title: "JuliusBrussee/caveman — terse caveman voice skill plus a token-saving proxy for coding agents"
slug: 20261109-caveman-terse-voice-and-token-proxy
type: repo
status: draft
source_url: "https://github.com/JuliusBrussee/caveman"
source_platform: github
author: "JuliusBrussee"
published: "2026-04-04"
captured_at: "2026-11-09T21:50:13Z"
captured_by: "claude-code-cloud"
canonical_id: "github:JuliusBrussee/caveman"
engagement: "stars=118625 forks=6907"
tags: [agent-skills, token-saving, prompt-engineering, claude-code, codex, proxy, caveman]
related: [20261019-dsh-our-free-model-plugin]
needs_manual_text: false
---

## 摘要

caveman 係一個令 coding agent「講少啲、讀少啲」嘅 skill 加工具組，118k stars。核心係 `/caveman` 呢個 skill：答案行先、刪晒客套說話，但 code、指令、路徑、數字同錯誤訊息一隻字都唔改；仲有 `/ultracave`（更短）同 `/megacave`（文言文）兩個版本。4.0 之後佢變成「六塊石」：除咗個 voice，仲有一個本地 proxy 壓縮 log／JSON／測試輸出、自動揀 model 嘅 Auto、保存 agent 寫過嘅 script 嘅 Blocks、壓縮網頁嘅 Browse 等。淨係用 skill 唔會傳送任何資料；完整 CLI 預設會傳使用統計，Auto 登入後會將你嘅提問傳去 Caveman Cloud。

## Key facts

- **Skill only (no proxy)**: `npx skills add JuliusBrussee/caveman -g`, then `/caveman` (`$caveman` in Codex); `stop caveman` to end. The `skills/caveman/` folder is two Markdown files, no scripts.
- **Full install**: `npx @caveman-ai/cli@latest` (Node.js 22.13+); finds your agents and logins and puts a local proxy in front of them. `caveman status`, `caveman off browse`, `caveman telemetry off`. Uninstall: `npx -y github:JuliusBrussee/caveman -- --uninstall`.
- **Numbers (upstream)**: ten prompts on claude-opus-5-5, output tokens: none 6,983 · "Answer concisely." 4,334 · `/caveman` 4,119 · `/ultracave` 2,693 (3.1.0 rules, single run). Read-less proxy: 33.2% fewer input tokens over 54 Claude Code runs. The rules cost ~1,160 input tokens.
- **Outside results cited**: Adobe Research (1.4–2.4× cost cut, eight models), Elastic (63.6% fewer response tokens), JetBrains A/B (no measurable quality loss, p = 0.82, 8.5% fewer output tokens).
- **Privacy**: the skill sends nothing. The CLI sends usage stats by default (commands, token counts, install ID, OS, IP; not prompts or code). Auto, after `caveman login`, sends the latest ask plus attached CLAUDE.md / memory / files to Caveman Cloud.
- **Claude Code plugin**: v4.1.0, four Node hooks (SessionStart, SubagentStart, UserPromptSubmit, SessionEnd) that switch the voice on for every session and subagent. `{"defaultMode":"manual"}` in `.caveman.json` keeps normal prose by default.
- Apache-2.0; Go + Node; created 2026-04-04, last push 2026-11-09.

## 點解值得留意

- 淨係裝 skill 已經夠：純 Markdown、冇 script、唔傳資料，係最細風險嘅省 token 方法；vault 嘅 static scan 只有兩個誤報（R6 "tokens" 字眼、R7 `defaultMode` 設定）。
- 完整 CLI／proxy 會攔住所有 agent 嘅流量、預設開 telemetry，同 Jeff「no-login、no cookies」嘅原則有衝突，裝之前要逐項決定。
- 同 [[pages/20261019-dsh-our-free-model-plugin|DSH 免費模型插件]] 入面嘅 caveman／ponytail prompt 瘦身係同一個概念。
- Jeff 用廣東話回覆嘅 preference 仍然有效：caveman 只壓縮風格，唔會轉語言。

## Source

- https://github.com/JuliusBrussee/caveman — JuliusBrussee — created 2026-04-04, commit `3dc497a7` (2026-11-09)
- Engagement: stars=118625 forks=6907 (2026-11-09)
- Reader: raw.githubusercontent.com README (curl), api.github.com via r.jina.ai for counts, shallow git clone for the skill files. Raw text in `raw/20261109-caveman-terse-voice-and-token-proxy.md`.

## Related

- [[../../skills/using-caveman-mode/SKILL|skill: using-caveman-mode]]
- [[pages/20261019-dsh-our-free-model-plugin|DSH 免費模型插件]]
- [[pages/20261019-chase-h-ai-ponytail-carousel|Ponytail]]
- [[../../skills/scanning-agent-skills/SKILL|skill: scanning-agent-skills]]
