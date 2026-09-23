---
title: "jev-ultrafast — Browser Use's Jev-powered browser agent"
slug: 20260923-browser-use-jev-ultrafast
type: repo
status: draft
source_url: "https://github.com/browser-use/jev-ultrafast"
source_platform: github
author: "browser-use (Gregor Zunic)"
published: "2026-09-16"
captured_at: "2026-09-23T01:18:14Z"
captured_by: "routine:weekly-hot-list"
canonical_id: "github:browser-use/jev-ultrafast"
engagement: "stars=18079 forks=1163 x_likes=9046 x_retweets=650 x_views=3149666"
tags: [hot-list, browser-agent, jev, typesafe, mcp, ai-agents, python]
related: []
needs_manual_text: false
---

## 摘要

`jev-ultrafast` 係瀏覽器自動化公司 Browser Use 出品嘅開源瀏覽器 agent，用 TypeSafe 嘅「Jev」
System One 決策模型嚟揀「做咩操作」同「揀邊個網頁元素」，一次 API 請求就搞掂兩個決定，淨係
輸入文字（`TYPE_TEXT`）先至叫細 LLM 幫手生成文字。官方 demo 展示喺 Google Flights 用一句自然語言
目標，蘇黎世飛倫敦航班搜尋 7.1 秒內完成，仲有一個經六輪交替測試嘅細規模數字：中位任務時間由
9.45 秒降到 7.09 秒（快 25%），瀏覽器協議調用由 1,092 次降到 101 次（少 90.8%）。倉庫喺
2026-09-16 建立，一星期內衝到 18,079 stars；創辦人 @gregpr07 嘅發佈貼文喺 X 攞到 9,046 個 like、
650 個轉發、315 萬 views，GitHub 同 X 雙平台都清晒 gate，係本星期熱度榜第一。

## Key facts

- **是咩**：MIT 授權嘅開源瀏覽器 agent（Python），一個 goal 就可以喺真實網頁完成任務，唔靠逐格
  截圖畀 vision model 睇，改用結構化 DOM snapshot + indexed element table。
- **點解特別**：Jev 喺同一個 request 入面揀 operation（`CLICK`/`TYPE_TEXT`/`SELECT`/`SCROLL_UP`/
  `SCROLL_DOWN`/`WAIT`/`DONE`/`BLOCKED`）同對應嘅目標元素，細 LLM 淨係喺打字先出手，模型輸出永遠
  唔會變成 selector、座標或者可執行 code。
- **點裝**：
  ```sh
  git clone https://github.com/browser-use/jev-ultrafast.git
  cd jev-ultrafast && uv sync
  cp .env.example .env   # 填 TYPESAFE_API_KEY 同 TEXT_MODEL_API_KEY
  uv run jev              # 開 127.0.0.1:8766
  ```
- **數字**（2026-09-23 擷取，見 `raw/20260923-browser-use-jev-ultrafast.md`）：
  - GitHub：18,079 stars · 1,163 forks · 117 open issues（7 日大，2026-09-16 建立）
  - X（創辦人原帖 @gregpr07，fxtwitter 驗證）：9,046 likes · 650 retweets · 315 萬 views
- README 自己都老實列出限制：DOM reader 冇實現完整 accessible-name 規格，shadow root、frame、
  canvas、上傳、彈出分頁、巢狀捲動同任意鍵盤 widget 全部未支援；6 輪測試嘅 sign test p=0.25，
  作者自己都話呢個唔算強嘅統計結論。

## 點解值得留意

本週熱度榜第一名：GitHub（一星期新倉破 1.8 萬 star，遠超 new-repo 門檻 1 萬）同 X（創辦人貼文
9,046 like / 650 retweet / 315 萬 views，三個 sub-metric 全部過 gate）雙平台都清 gate，
heat 分數 0.9375（含 multi-platform ×1.25 bonus），係目前為止呢個 vault 記錄過最高嘅一次。
同一個 "Jev" 決策模型生態呢星期仲催生咗另外兩個贏家（NandhaKishorM/laya、zai-org/ZCode），
反映呢類「唔生成文字、淨係做決策」嘅細模型正喺度快速滲透去 agent tooling（compaction、
browser automation、classification 都有）。

## Source

- https://github.com/browser-use/jev-ultrafast （GitHub connector + Exa web_fetch_exa README）
- https://x.com/gregpr07/status/2100411066966749359 （fxtwitter 驗證）
- Reader used: Exa web_fetch_exa（README/repo metadata）+ GitHub connector（repo search）+ fxtwitter API（X 互動數字）

## Related

- [[../hot-list/2026-W39|hot-list/2026-W39]]
- [[20260923-nandhakishorm-laya|20260923-nandhakishorm-laya]]
- [[20260923-zai-org-zcode|20260923-zai-org-zcode]]
- [[20260920-fast-jev-compaction|20260920-fast-jev-compaction]]
