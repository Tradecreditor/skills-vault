---
title: "context7"
slug: upstash--context7
type: repo
status: draft
source_url: "https://github.com/upstash/context7"
source_platform: github
author: "Upstash"
published: "2025-03-26"
captured_at: "2026-09-20T23:06:50Z"
captured_by: "routine:github-stars-sync"
canonical_id: "github:upstash/context7"
engagement: "stars=62255 forks=3015"
tags: [llm, mcp, mcp-server, vibe-coding]
related: [vercel-labs--skills, openai--codex-plugin-cc, Fission-AI--OpenSpec, googleanalytics--google-analytics-mcp, pages/20260921-4-claude-code-plugins]
needs_manual_text: false
---

## 摘要
Context7 解決 LLM 寫程式時「訓練資料過時、亂噏冇存在過嘅 API」呢個老問題 —— 佢會即時由官方文件來源攞返最新、對應版本嘅程式碼文件同範例,直接塞入 agent 嘅 prompt context 度。用法好簡單,喺 prompt 尾加返 "use context7" 或者指名 library id,就可以叫 agent 攞最新版 Next.js、Supabase 呢類 library 嘅正確用法,唔使自己周圍搵文件。支援兩種安裝模式:CLI + Skills(裝一個 skill,用 `ctx7` command 攞文件,唔使 MCP)同埋傳統 MCP server 模式,一個指令 `npx ctx7 setup` 就搞掂晒設定。

## Key facts
- Language: TypeScript
- License: MIT
- Created: 2025-03-26
- Last pushed: 2026-09-20
- Stars: 62,255
- Forks: 3,015
- Install: `npx ctx7 setup` (or MCP server URL `https://mcp.context7.com/mcp`)
- Packages: `@upstash/context7-mcp`, `ctx7` CLI, `@upstash/context7-sdk`

## 點解值得留意
Context7 而家已經係 AI coding agent 生態入面數一數二熱門嘅文件檢索工具,亦都出咗 skill 模式(唔一定要用 MCP),同 skills-vault 嘅 agent skills 思路直接相關,值得留意佢點樣將「攞外部最新文件」呢件事包裝做一個 agent 隨手可用嘅工具。可以考慮攞嚟同 vault-capture 呢類 skill 比較設計手法。

## Source
GitHub repository: https://github.com/upstash/context7
Author: Upstash
Published: 2025-03-26
Reader used: raw README via Exa (web_fetch_exa)

## Related

- [[vercel-labs--skills|skills]] — 兩者都支援「CLI + Skills」模式，唔一定要用 MCP 先攞到能力。
- [[openai--codex-plugin-cc|codex-plugin-cc]] — 都係幫 coding agent 攞多一層外部資訊/工具嘅官方插件。
- [[Fission-AI--OpenSpec|OpenSpec]] — 兩者都係將外部/規格資訊塞入 agent context 嘅工具。
- [[googleanalytics--google-analytics-mcp|google-analytics-mcp]] — 都係將外部資料/文件即時塞入 agent context 嘅官方級工具。
- [[../pages/20260921-4-claude-code-plugins|4 Claude Code Plugins]] — 呢篇文章都提到 Context7，話佢同 Graphify 一樣係減少 agent 亂噏/重複讀檔嘅方案。
