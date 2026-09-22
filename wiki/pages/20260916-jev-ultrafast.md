---
title: "jev-ultrafast — Browser Use's decision-only web agent on TypeSafe's Jev"
slug: 20260916-jev-ultrafast
type: repo
status: draft
source_url: "https://github.com/browser-use/jev-ultrafast"
source_platform: github
author: "browser-use"
published: "2026-09-16"
captured_at: "2026-09-22T02:15:00Z"
captured_by: "routine:weekly-hot-list"
canonical_id: "github:browser-use/jev-ultrafast"
engagement: "stars=15806 forks=988 x_likes=8956 x_retweets=643 x_views=3070384"
tags: [hot-list, browser-agent, jev, typesafe, web-automation, python]
related: []
needs_manual_text: false
---

## 摘要

`jev-ultrafast` 係 Browser Use（開源瀏覽器自動化框架嘅團隊）出嘅一個極簡瀏覽器 agent，用 TypeSafe 嘅
「Jev」決策模型嚟揀操作（CLICK / TYPE_TEXT / SELECT / SCROLL 等）同目標元素，淨係 `TYPE_TEXT` 呢個
operation 先會叫細 LLM 生成文字，其餘全部一個 network round trip 搞掂,所以速度快好多。示範片段係
Google Flights 搵蘇黎世去倫敦嘅機票,7.1 秒完成（真係生成文字、真係等待載入,仲有獨立驗證結果,唔係砌返
出嚟嘅片）。六次交替測試,中位數任務時間由 9.45 秒降到 7.09 秒（-25%）,瀏覽器協定調用由 1,092 次降到
101 次。倉庫 2026-09-16 建立,4-6 日內衝到 15,806 stars,創辦人 @gregpr07 嘅發佈貼文喺 X 攞到 8,956
likes、643 retweets、307 萬 views,GitHub 同 X 雙平台都清晒 gate,係本週熱度榜第一,heat 分數 0.9375。

## Key facts

- **是咩**：開源瀏覽器 agent（Python, MIT license），依賴 Browser Use 自己嘅 `browser-harness`（Chrome
  remote-debugging 橋接）同 TypeSafe 嘅 Jev API（同上星期贏家 `tamaratran/fast-jev-compaction` 用緊
  同一間決策模型公司）。
- **核心設計**：每次觀察產生一個新嘅 element table,operation 頭同 target 頭喺同一個請求入面回答,
  只有 `TYPE_TEXT` 先觸發細 LLM（`inception/mercury-2.5` 喺 demo 入面用,亦支援 Gemini/GLM/DeepSeek）
  生成文字。冇 screenshot 落 default loop,execution 前後有 DOM freshness/occlusion 檢查。
- **點裝**：
  ```bash
  git clone https://github.com/browser-use/jev-ultrafast.git
  cd jev-ultrafast && uv sync
  cp .env.example .env   # TYPESAFE_API_KEY + TEXT_MODEL_API_KEY
  uv run jev             # http://127.0.0.1:8766 inspector
  ```
- **限制**（作者自己講明）：MVP,冇 shadow-DOM / iframe / canvas / 上傳支援;`DONE` 判斷仍需要獨立
  結果驗證(demo 本身有做);6 次重複測試唔係通用可靠度 benchmark。
- **數字**（2026-09-22 擷取）：
  - GitHub：15,806 stars · 988 forks · 108 open issues（created 2026-09-16,~6 日大）
  - X（創辦人原帖 @gregpr07,fxtwitter 驗證,2026-09-17 貼）：8,956 likes · 643 retweets · 3,070,384 views

## 點解值得留意

- 本週 GitHub + X 雙平台都清晒 gate 嘅贏家（新倉超過 10,000-star 門檻,X 三個子指標全部超標),
  heat = (0.40×1 + 0.35×1) × 1.25 = **0.9375**,同上星期贏家 `fast-jev-compaction` 打成平手嘅公式結果。
- 同上星期嘅 `fast-jev-compaction` 屬同一個「Jev」決策模型生態系:一個做 context compaction,一個做
  瀏覽器自動化,反映 TypeSafe 嘅 System One／Jev API 呢排喺 agent 工具鏈度快速擴散緊。
- 本週亦見到一個「Laya」決策模型陣營喺競爭同一個位（`NandhaKishorM/laya`、`mizorewww/laya-mlx`,
  見 Watch 名單）,值得留意呢場「決策模型」路線之爭。

## Source

- https://github.com/browser-use/jev-ultrafast （GitHub API,透過 mcp__github__search_repositories）
- https://x.com/gregpr07/status/2100411066966749359 （fxtwitter 驗證）
- Reader used: Exa web_fetch_exa（README）+ GitHub connector（repo metadata）+ fxtwitter API（X 互動數字）

## Related

- [[20260920-fast-jev-compaction|fast-jev-compaction]]（上星期嘅 Jev 生態系贏家）
- [[../hot-list/2026-W39|hot-list/2026-W39]]
