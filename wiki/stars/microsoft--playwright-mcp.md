---
title: "playwright-mcp"
slug: microsoft--playwright-mcp
type: repo
status: draft
source_url: "https://github.com/microsoft/playwright-mcp"
source_platform: github
author: "Microsoft"
published: "2025-03-21"
captured_at: "2026-09-21T23:07:37Z"
captured_by: "routine:github-stars-sync"
canonical_id: "github:microsoft/playwright-mcp"
engagement: "stars=37448 forks=3183"
tags: [mcp, playwright, browser-automation]
related: []
needs_manual_text: false
---

## 摘要
Playwright MCP 係一個 Model Context Protocol server,俾 LLM 用 Playwright 做瀏覽器自動化。特別之處係佢唔靠截圖或者要 vision model,而係用 Playwright 嘅 accessibility tree(結構化資料)俾 agent 睇網頁,所以快、輕量、仲可以避免截圖式方法常見嘅歧義問題。README 特登提醒:如果你用嘅係 coding agent(例如 Claude Code、Codex),官方建議改用佢哋出嘅 Playwright CLI + SKILLS 版本,因為 CLI 用 command 形式,唔使成個 accessibility tree 塞入 context,對省 token 嚟講更加化算;MCP 版就啱一啲需要持續維持瀏覽器狀態嘅場景,例如探索式自動化、自我修復測試、長時間運行嘅自主流程。

## Key facts
- Language: TypeScript
- License: Apache-2.0
- Created: 2025-03-21
- Last pushed: 2026-09-18
- Stars: 37,448
- Forks: 3,183
- Install: `npx @playwright/mcp@latest`(或者 Claude Code 用 `claude mcp add playwright npx @playwright/mcp@latest`)
- Requires: Node.js 18+
- Related tool: Playwright CLI + SKILLS(https://github.com/microsoft/playwright-cli),官方講明啱 coding agent 用,更省 token

## 點解值得留意
微軟官方出品,係目前 MCP 瀏覽器自動化嘅事實標準之一,直接支援 Claude Code、VS Code、Cursor 等十幾種 client 嘅一鍵安裝。README 入面「MCP vs CLI+SKILLS」嗰段對呢個 vault 特別有參考價值 —— 官方親自解釋咗點解 coding agent 場景應該用 CLI+Skill 而唔係 MCP(token 效率),同呢個 vault 「capture 一個 URL 就變成一個可安裝 skill」嘅方向完全對應。

## Source
GitHub repository: https://github.com/microsoft/playwright-mcp
Author: Microsoft
Published: 2025-03-21
Reader used: raw README via Exa (web_fetch_exa)

## Related
