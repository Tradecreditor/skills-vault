---
title: "codex-plugin-cc"
slug: openai--codex-plugin-cc
type: repo
status: draft
source_url: "https://github.com/openai/codex-plugin-cc"
source_platform: github
author: "OpenAI"
published: "2026-03-30"
captured_at: "2026-09-21T23:07:37Z"
captured_by: "routine:github-stars-sync"
canonical_id: "github:openai/codex-plugin-cc"
engagement: "stars=33429 forks=2321"
tags: [claude-code-plugin, codex, code-review]
related: [skills/delegating-to-codex, upstash--context7, Fission-AI--OpenSpec, NousResearch--hermes-agent-self-evolution, pages/20260920-fast-jev-compaction]
needs_manual_text: false
---

## 摘要
呢個係 OpenAI 官方出嘅 Claude Code plugin,俾你直接喺 Claude Code 入面叫 Codex 做嘢 —— 可以攞 Codex 嚟做 code review,或者將任務直接交俾 Codex 處理。裝咗之後會有 `/codex:review`(普通唯讀 review)、`/codex:adversarial-review`(可引導嘅挑戰式 review,專門質疑設計決定同風險位)、同埋 `/codex:rescue`、`/codex:transfer`、`/codex:status`、`/codex:result`、`/codex:cancel` 呢班用嚟委派任務、交接 session、管理背景工作嘅指令。仲有一個可選嘅「review gate」,開咗之後每次 Claude 回覆前都會用 Codex 做針對性 review,查到問題就會擋住唔俾停,逼 Claude 先處理好先可以完成。

## Key facts
- Language: JavaScript
- License: Apache-2.0
- Created: 2026-03-30
- Last pushed: 2026-07-08
- Stars: 33,429
- Forks: 2,321
- Requires: ChatGPT 訂閱(包括免費版)或者 OpenAI API key、Node.js 18.18+
- Install: `/plugin marketplace add openai/codex-plugin-cc` → `/plugin install codex@openai-codex` → `/reload-plugins` → `/codex:setup`
- 底層用返本機安裝嘅 Codex CLI 同 Codex app server,唔係獨立 runtime

## 點解值得留意
OpenAI 同 Anthropic 兩間對頭公司嘅工具竟然官方互通 —— OpenAI 親自出 plugin 俾 Claude Code 用戶叫用 Codex,呢個對「一個 agent CLI 入面調用另一個 agent CLI」嘅 orchestration 模式好有參考價值,尤其係 `/codex:adversarial-review` 呢種專門質疑自己設計決定嘅 review 模式,同 skills-vault 講求嘅 agent 互相協作思路好夾。

## Source
GitHub repository: https://github.com/openai/codex-plugin-cc
Author: OpenAI
Published: 2026-03-30
Reader used: raw README via Exa (web_fetch_exa)

## Related

- [[../../skills/delegating-to-codex/SKILL|skill: delegating-to-codex]] — 呢個 skill 就係由呢個 repo 直接包裝出嚟。
- [[upstash--context7|context7]] — 兩者都係幫 coding agent 攞多一層外部資訊/工具嘅官方插件。
- [[Fission-AI--OpenSpec|OpenSpec]] — 兩個都係喺 coding agent 流程入面加一層審批/規劃步驟。
- [[NousResearch--hermes-agent-self-evolution|hermes-agent-self-evolution]] — 都係喺 agent 產出之後加一層自動審查/演化嘅迴路。
- [[../pages/20260920-fast-jev-compaction|fast-jev-compaction]] — 同屬本週留意緊嘅 Claude Code plugin 生態擴充。
