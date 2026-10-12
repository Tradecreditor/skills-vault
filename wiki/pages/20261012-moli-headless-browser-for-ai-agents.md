---
title: "lexmount/moli — structure-first Rust headless browser for AI agents"
slug: 20261012-moli-headless-browser-for-ai-agents
type: repo
status: draft
source_url: "https://github.com/lexmount/moli"
source_platform: github
author: "Lexmount"
published: "2026-08-10"
captured_at: "2026-10-12T08:20:10Z"
captured_by: "routine:weekly-hot-list"
canonical_id: "github:lexmount/moli"
engagement: "stars=16732 forks=409 (+8633 stars since 2026-10-05 snapshot)"
tags: [hot-list, 2026-W41, browser-agent, headless-browser, rust, cdp, webdriver, agent-skills]
related: [hot-list/2026-W41]
needs_manual_text: false
---

## 摘要

Moli 係 Lexmount 用 Rust 寫嘅開源 headless browser（Apache-2.0 或 MIT），專為 AI agent 而設：預設只處理 DOM、CSS、JavaScript 同網絡呢啲頁面結構，要 layout、截圖或者 PDF 先至即場計，所以比長期維持完整畫面嘅 Chrome headless 慳資源。Agent 可以用 `moli fetch` 將網頁轉成 Markdown 或者精簡嘅 semantic tree，亦可以用 `moli serve` 開一個同時支援 CDP、WebDriver Classic 同 WebDriver BiDi 嘅 endpoint，Playwright 可以直接 `connectOverCDP`。Repo 仲附帶 `moli-webfetch` 等 agent skills，叫 agent「裝 skills 再用 moli-webfetch」就可以開始。佢係 2026-W41 hot list 第三名：一星期 +8,633 stars，GitHub 單平台入選。

## Key facts

- **Install**: Linux / macOS `curl --proto '=https' --tlsv1.2 -fsSL https://github.com/lexmount/moli/releases/latest/download/moli-installer.sh | sh`; Windows PowerShell installer `moli-installer.ps1`. Or tell the agent to install the skills under `lexmount/moli/tree/main/skills` and follow them.
- **Use**: `moli fetch --dump markdown --wait-until done <url>`; `--dump semantic_tree_text` for a model-friendly tree; `--layout --dump screenshot|screenshot_full|pdf` for pixels; `--eval '<js>'` to interact before export. `moli serve [--layout] [--resource]` starts the automation server (port 9222 in the Playwright example).
- **Design**: structure first, pixels on demand: most agent requests never need layout or paint. Ships a WebMCP playground that lists and calls a site's native WebMCP tools.
- **Platforms**: Linux, macOS, Windows. Licence Apache-2.0 OR MIT.
- **Numbers (2026-10-12)**: 16,732 stars / 409 forks; 8,099 in the 2026-10-05 snapshot, so **+8,633 in 7 days**. Created 2026-08-10, so it also clears the new-repo total gate (63 days, >= 10,000). Best in-window X post found: @vicky_grok 2107101100138725821 (2026-10-05) 268 likes / 51 reposts / 12,386 views (fxtwitter), below every X gate. SkillsMP lists `moli-webfetch`, `moli-websearch` and `moli-cdp-server`.

## 點解值得留意

- 2026-W41 hot list 第三名（heat 0.80，GitHub 單平台）。今個星期有九個項目同分 0.80，按實測七日 stars 增幅排序，佢最高，詳見 [[hot-list/2026-W41|hot-list/2026-W41]]。
- Vault 嘅 capture / reader 流程可以考慮用佢：如果 Jina 或者 Exa 唔用得，可以用佢喺本地將網頁轉 Markdown（今個星期 Exa 就無晒 credits）。
- 同 [[stars/browser-use--browser-use|browser-use]] 係唔同層面：browser-use 係 agent 框架，Moli 係底層瀏覽器引擎，兩樣可以一齊用。

## Source

- https://github.com/lexmount/moli — Lexmount — created 2026-08-10
- Reader: raw.githubusercontent.com README (curl) + GitHub search API (connector). Raw text in `raw/20261012-moli-headless-browser-for-ai-agents.md`.

## Related

- [[hot-list/2026-W41]]
- [[stars/browser-use--browser-use]]: agent framework that drives a browser; Moli is a browser engine it could connect to over CDP
