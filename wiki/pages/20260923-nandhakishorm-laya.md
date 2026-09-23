---
title: "Laya — open-source System 1 decision engine, pitched as Jev's open alternative"
slug: 20260923-nandhakishorm-laya
type: repo
status: draft
source_url: "https://github.com/NandhaKishorM/laya"
source_platform: github
author: "NandhaKishorM (Nandakishor Mukkunnoth, ConvAI Innovations)"
published: "2026-09-18"
captured_at: "2026-09-23T01:18:14Z"
captured_by: "routine:weekly-hot-list"
canonical_id: "github:NandhaKishorM/laya"
engagement: "stars=16609 forks=1390 hn_points=560 hn_comments=310"
tags: [hot-list, decision-model, jev, typesafe, classification, agent-memory, python, apache-2.0]
related: []
needs_manual_text: false
---

## 摘要

`laya` 係一個開源、非自回歸（non-autoregressive）嘅「System 1 決策引擎」：畀佢一個 state
（一段文字、email、工單或 JSON）同幾條 typed questions（`choice`/`score`/`noul` 三種），佢一次
forward pass（33 毫秒）就答哂,唔生成文字所以冚唪唥冇幻覺。作者 Nandakishor Mukkunnoth 喺
Dev.to／Hacker News 發文話,呢個非自回歸決策模型嘅思路佢喺 2025 年 3 月已經發咗 arXiv 論文
（arXiv:2503.23303）並開源咗權重,結果 2026 年 9 月由 TypeSafe AI（ChatGPT 共同發明人 Diogo
Almeida 創辦、攞咗 4000 萬美元種子輪）推出嘅「Jev」被吹捧成突破性技術,但冇技術論文、冇開源
權重、冇開源訓練集。佢決定用返呢一年學到嘅嘢重新起一個完全開源版本 Laya,同 Jev 對比基準話快
7.8 倍、細20+選項嘅分類任務準確度更高,但作者自己都承認喺 20 個以上選項嘅分類（Banking77）
上輸畀 Jev。呢篇文喺 Hacker News 攞到 560 分、310+ comments,但呢件事本身喺 HN 社群都有爭議
（有留言話個 project「係啱啱先 vibe code 出嚟」、質疑兩者其實唔係同一樣嘢）。GitHub 倉庫
2026-09-18 開，5 日內衝到 16,609 stars。

## Key facts

- **是咩**：Apache 2.0 開源 Python library（`pip install laya`），Router 會自動偵測語言／文字
  script,揀岩英文（ModernBERT-large 421M）、多語言（mmBERT-base 322M，覆蓋 100+ 種語言）定
  typed-decisions 三個 checkpoint 之一。
- **點解特別**：三個決策原語 `choice`（分類）、`score`（等級評分）、`noul`（0-1 校準機率）,
  用嚟做 email/工單分流、urgency scoring、churn risk、jailbreak/prompt guard、內容審核等,
  訓練用 RLCD（策略梯度 + strictly proper scoring rule），令輸出機率有統計意義,可以直接用嚟做
  confidence-gated 自動化（高信心自動處理、低信心先升級俾人）。
- **點裝**：
  ```py
  import laya
  from laya import Router
  router = Router(preload=True)
  result = router.predict(state, questions)
  ```
- **數字**（2026-09-23 擷取，見 `raw/20260923-nandhakishorm-laya.md`）：
  - GitHub：16,609 stars · 1,390 forks · 122 open issues（5 日大，2026-09-18 建立）
  - Hacker News：560 分、310+ comments（"Laya beats Jev with 33ms open-source decision engine"）
  - X（作者原帖 @Nandakishorm1）：140 likes · 21 retweets · 12,132 views —— 遠低於呢個 vault 嘅
    X gate 門檻，證明呢單嘢主要靠 HN／blog 傳播，唔係靠 X。
- 「邊個先做出嚟」呢個優先權爭議未有定論：TypeSafe 官方未就此公開回應,兩者嘅實際模型架構、
  權重同訓練細節都冇公開比對過,呢度記低嘅係作者自己嘅講法同公開討論,唔係呢個 vault 獨立驗證
  過嘅結論。

## 點解值得留意

單靠 GitHub 一個平台就清 gate（new-repo 門檻 1 萬 star，佢有 1.66 萬），用 single-source path
計出 heat = 0.40 × min(2.0, 16609/10000) = 0.664，過咗 single_source_min_heat（0.60）門檻,
所以入選正式贏家,即使 X 冧檔（只有 140 個 like）。同 browser-use/jev-ultrafast、
zai-org/ZCode 一齊,呢個星期出現咗三個獨立團隊各自圍住「Jev」呢個 TypeSafe 決策模型做開源競品／
應用嘅例子,值得下個星期繼續追蹤呢個生態嘅發展（同埋呢場優先權爭議會唔會有下文）。

## Source

- https://github.com/NandhaKishorM/laya （GitHub connector + Exa web_fetch_exa README）
- https://news.ycombinator.com/item?id=49765348 （Hacker News 討論帖）
- https://dev.to/nandakishor_m_6cc0adfde9f/... 、 https://aetos.ai/posts/5ca891cfdfce11b9 （作者原文）
- https://x.com/Nandakishorm1/status/2100451354670195196 （fxtwitter 驗證，未過 gate）
- Reader used: Exa web_fetch_exa（README + 部落格文章）+ GitHub connector（repo search）+ fxtwitter API

## Related

- [[../hot-list/2026-W39|hot-list/2026-W39]]
- [[20260923-browser-use-jev-ultrafast|20260923-browser-use-jev-ultrafast]]
- [[20260923-zai-org-zcode|20260923-zai-org-zcode]]
- [[20260920-fast-jev-compaction|20260920-fast-jev-compaction]]
