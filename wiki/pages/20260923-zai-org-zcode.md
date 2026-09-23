---
title: "ZCode — Z.ai's open-sourced coding agent harness"
slug: 20260923-zai-org-zcode
type: repo
status: draft
source_url: "https://github.com/zai-org/ZCode"
source_platform: github
author: "zai-org (Z.ai / Zhipu AI)"
published: "2026-09-20"
captured_at: "2026-09-23T01:18:14Z"
captured_by: "routine:weekly-hot-list"
canonical_id: "github:zai-org/ZCode"
engagement: "stars=6302 forks=1832"
tags: [hot-list, coding-agent, glm, desktop-app, cli, typescript]
related: []
needs_manual_text: false
---

## 摘要

`ZCode` 係中國 AI 公司 Z.ai（前身 Zhipu AI）為自家 GLM 模型出嘅「Agentic Development
Environment」：一個 Electron 桌面應用、瀏覽器介面同終端機 Agent 三合一,支援 macOS／Windows／
Linux,重可以喺微信、飛書、Telegram 用機械人遠端操控編程任務。呢個產品其實喺 2026 年 7 月已經
以「ZCode 3.0／GLM-5.2 官方開發環境」名義公開發佈過,但今個星期（2026-09-20）先至將原始碼開喺
GitHub（Apache 2.0 授權），3 日內就攞到 6,302 stars,係一個「產品舊、代碼新公開」嘅個案 ——
記低嘅係呢個 GitHub 倉庫本身今個星期先出現、先開始儲 star,唔係話呢個產品今個星期先推出。

## Key facts

- **是咩**：Monorepo，包含 `packages/desktop`（Electron 桌面版）、`packages/web`（瀏覽器版）、
  `packages/server`（HTTP/WebSocket 後端）、`apps/zcode-cli`（Agent CLI／TUI／runtime）等。
- **點解特別**：定位為 Cursor、Claude Code、GitHub Copilot 嘅競品,主打對 GLM-5.2/5.3 模型深度
  優化嘅 multi-agent 協作、"Goal" 模式（規劃 → 執行 → 驗證持續循環）,同支援 BYOK 接第三方模型。
- **點裝**（CLI 版）：
  ```sh
  zcode              # 終端互動介面
  zcode --web        # 開瀏覽器介面
  zcode --web --workspace /path/to/project --port 3030 --no-open
  ```
  桌面版：`pnpm bootstrap` → `pnpm dev:desktop`。
- **數字**（2026-09-23 擷取，見 `raw/20260923-zai-org-zcode.md`）：
  - GitHub：6,302 stars · 1,832 forks · 11 open issues（3 日大，2026-09-20 建立）
- 冇搵到呢個 GitHub 倉庫／今次開源動作專屬嘅 X 或 Threads 貼文（有搵到嘅報導全部係講 7 月個
  產品發佈,唔係今次 GitHub release）,所以呢單嘢淨係用 GitHub 一個平台嘅數字嚟計分。

## 點解值得留意

GitHub 增長門檻用「topical」版本（因為 repo 描述明講自己係 "coding agent harness"）：門檻
1,500，佢 3 日就有 6,302，metric/threshold = 4.2，用 single-source 公式 cap 喺 2.0 之後
heat = 0.40 × 2.0 = 0.80——係本週三個贏家入面 heat 第二高,顯示中國大模型廠商加緊將自家編程
agent 開源化去搶佔 Cursor／Claude Code／Copilot 呢個賽道嘅速度幾快。

## Source

- https://github.com/zai-org/ZCode （GitHub connector + Exa web_fetch_exa README）
- https://zcode.z.ai/en （官方產品頁，7 月舊發佈,作對照用）
- Reader used: Exa web_fetch_exa（README + 官方頁面）+ GitHub connector（repo search）

## Related

- [[../hot-list/2026-W39|hot-list/2026-W39]]
- [[20260923-browser-use-jev-ultrafast|20260923-browser-use-jev-ultrafast]]
- [[20260923-nandhakishorm-laya|20260923-nandhakishorm-laya]]
