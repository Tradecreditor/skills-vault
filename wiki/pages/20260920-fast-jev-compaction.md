---
title: "fast-jev-compaction — verbatim Jev-scored compaction for Claude Code"
slug: 20260920-fast-jev-compaction
type: repo
status: draft
source_url: "https://github.com/tamaratran/fast-jev-compaction"
source_platform: github
author: "tamaratran"
published: "2026-09-17"
captured_at: "2026-09-20T22:15:03Z"
captured_by: "routine:weekly-hot-list"
canonical_id: "github:tamaratran/fast-jev-compaction"
engagement: "stars=5089 forks=281 x_likes=10686 x_retweets=657 x_views=3693140"
tags: [hot-list, claude-code, claude-code-plugin, context-management, compaction, typescript, 2026-W38]
related: []
needs_manual_text: false
---

## 摘要

`fast-jev-compaction` 係一個 Claude Code function-hook plugin（同埋可獨立用嘅 npm package），
用嚟取代 Claude Code 內建嘅「摘要式」context compaction。傳統壓縮做法係叫模型將舊對話寫成摘要，
呢個過程有損：一個檔案路徑、一句 error message、一個限制條件，隨時喺摘要入面被靜靜地漏走。
呢個 plugin 完全唔改寫內容——佢淨係揀邊啲 tool call / tool result 要刪，判斷交俾 TypeSafe 嘅
「Jev」System One 模型嚟做,每個非釘選（non-pinned）嘅 tool call 問兩條 yes/no 問題（call 本身留唔留、
result 要唔要逐字留），留低嘅嘢保證同原文一模一樣。倉庫喺 2026-09-17 建立，三日內就衝到 5,089 stars，
創作者 @tamarajtran 嘅發佈貼文喺 X 攞到 1 萬幾個 like、369 萬 views，係呢個星期熱度榜第一。

## Key facts

- **是咩**：Claude Code plugin（`hooks/` + `.claude-plugin/`）+ 獨立 npm library（`src/`），
  提供 `compactMessages` / `compact` / `reductionRatio` 等公開 API。
- **點解特別**：唔做摘要（lossy），淨係逐個 tool call 決定「留 / 截斷 / 刪」，文字訊息永遠逐字保留。
- **點裝**（Claude Code，需要 2.1.274+ 嘅 early-access function hooks）：
  ```json
  { "env": { "CLAUDE_CODE_ENABLE_FUNCTION_HOOKS": "1", "TYPESAFE_API_KEY": "<your key>" } }
  ```
  ```sh
  claude plugin marketplace add tamaratran/fast-jev-compaction
  claude plugin install fast-jev-compaction@fast-jev-compaction
  ```
- **點裝**（npm library）：`npm install fast-jev-compaction`，設定 `TYPESAFE_API_KEY`。
- **關鍵參數**：`keepThreshold`（預設 0.5）、`preserveRecentMessages`（預設 6）、`maxStateTokens`
  （25k）、`maxRequestTokens`（30k）、`truncateHeadChars`（300）。
- **數字**（2026-09-20 擷取，見 `raw/20260920-fast-jev-compaction.md` 底部「Verified engagement」）：
  - GitHub：5,089 stars · 281 forks · 56 open issues（3 日大，2026-09-17 建立）
  - X（創作者原帖 @tamarajtran，fxtwitter 驗證）：10,686 likes · 657 retweets · 3,693,140 views
- 報導同 HN 討論指出，呢類「retroactive pruning」同另一種「input hygiene」（單次 tool output 過濾）
  係唔同問題，唔好混淆。

## 點解值得留意

呢個係本週 hot-list 嘅第一名：GitHub（新倉 3 日破 5k stars，遠超「topical」門檻 1,500）同 X
（創作者貼文 過萬 like、369 萬 views，遠超門檻）雙平台都清晒 gate，heat 分數大約 0.94（含
multi-platform ×1.25 bonus）。對比之下，本週另外幾個 GitHub 爆款（cloudflare/security-audit-skill、
opencodex、codex-security）雖然 star 數更誇張，但今個星期搵唔到對應嘅高互動 X/Threads 貼文嚟做第二
平台佐證,所以留喺 Watch 名單，冇入選正式贏家（詳見 `wiki/hot-list/2026-W38.md`）。

## Source

- https://github.com/tamaratran/fast-jev-compaction （GitHub API，透過 mcp__github__search_repositories）
- https://x.com/tamarajtran/status/2100694549362553153 （fxtwitter 驗證）
- Reader used: Exa web_fetch_exa（README）+ GitHub connector（repo metadata）+ fxtwitter API（X 互動數字）

## Related

- [[../hot-list/2026-W38|hot-list/2026-W38]]
