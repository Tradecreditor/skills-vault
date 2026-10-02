---
title: "Claude Mods Overview：Function Hooks、Plugin 與 State 架構"
slug: 20261002-claude-mods-overview-hooks-state
type: post
status: draft
source_url: "https://www.facebook.com/638368594/posts/10163494558868595"
source_platform: facebook
author: "Sean Liu"
published: "2026-10-02"
captured_at: "2026-10-02T09:10:00Z"
captured_by: "routine:capture-link"
canonical_id: "facebook:10163494558868595"
engagement: ""
tags: [topic/agent-tooling, claude-code, claude-mods, plugins, function-hooks, javascript, typescript, state-management]
related: []
needs_manual_text: false
---

## 摘要

Claude Mods 是 Anthropic 於 2026 年 10 月 1 日正式發布的 Claude Code 擴充功能，讓開發者能以 JavaScript 或 TypeScript 直接介入 Claude Code 的事件處理流程。不同於提供任務指引的 Skill 和提供外部工具的 MCP，Mod 透過 function hooks 觀察、修改或攔截提示詞、工具呼叫與模型請求等事件，並可繪製操作介面。Plugin 是安裝與分發單位，可同時包含 Mod、Skill 與 MCP 等元件。多個 Mods 形成一條事件處理鏈，外層 Mod 先取得輸入並可阻止後續處理，適合做政策管理與日誌記錄。狀態管理分三層：模組變數（重新載入即重設）、`$.state`（Session 持久）、`$.store`（跨 Session JSON 儲存）。

## Key facts

- Released: 2026-10-01 by Anthropic
- Language: JavaScript or TypeScript
- Plugin = distribution/installation unit; can bundle Mod + Skill + MCP together
- Mod handles events via function hooks: observe, modify, or return results directly
- Use `next` to pass the event to the next handler in the chain
- Event data is frozen — must create a copy before modifying
- Multiple Mods form a processing chain; outer Mod gets input first, inner result last
- Outer Mod can block further processing (useful for policy enforcement, PII filtering)
- `$` interface: file I/O, process spawn, network requests, model calls
- Each `$` API call is itself an event — outer Mods can intercept or reject it
- Enterprise use: a policy Mod can programmatically restrict what other Mods can do
- State tiers: module variable (resets on reload) → `$.state` (session, supports UI reactivity) → `$.store` (cross-session JSON)
- Permissions: Mod runs with the executor's own file and process permissions

## 點解值得留意

- 比 Skill 和 MCP 更底層，可程式化控制 Claude Code 的每個請求與回傳，而不只是提示指引
- 企業場景：outer Policy Mod 攔截所有 `$` API 呼叫，實現 zero-trust 管控與審計日誌
- 實用個人場景：context enrichment（每次請求自動帶入 project data）、cost tracking（記錄 token 用量）
- `$.store` 可跨 session 保存 vault capture 狀態，是 skills-vault Routines 持久化小資料的新選項

## Source

- <https://www.facebook.com/638368594/posts/10163494558868595>
- Author: Sean Liu · Published: 2026-10-02 08:06 UTC
- Reader: exa (final paragraph truncated; last readable sentence: "Mod 可以使用執行者的權限操作檔案與程序。")

## Related

- [[pages/20260921-4-claude-code-plugins|4 Claude Code Plugins That Fix the Real Bottlenecks]]
- [[pages/20260920-fast-jev-compaction|fast-jev-compaction — verbatim Jev-scored compaction for Claude Code]]
