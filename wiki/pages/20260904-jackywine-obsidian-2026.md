---
title: "2026 我的 Obsidian 完整分享"
slug: 20260904-jackywine-obsidian-2026
type: article
status: draft
source_url: "https://x.com/Jackywine/status/2095750518941659567"
source_platform: x
author: "Jackywine"
published: "2026-09-04"
captured_at: "2026-09-13T00:00:00Z"
captured_by: "claude-code-local"
canonical_id: "x:tweet:2095750518941659567"
engagement: "likes=1070 retweets=244 views=414258 bookmarks=2673"
tags: [obsidian, llm-wiki, knowledge-management, evergreen-notes, karpathy]
related: []
needs_manual_text: false
---

## 摘要

Jackywine 是 Obsidian VIP 支持者，用了六年 Obsidian，這篇萬字長文是他對自身知識管理歷程的完整回顧。文章從「工具崇拜」陷阱（47 個插件、刪庫重建十次）講起，整理了他收藏的所有入門教程、深度研究文件，以及 Karpathy 的 LLM-Wiki 方法論。核心爭論是 Karpathy（讓 AI 做編譯器，你只負責餵資料）vs. Kepano（保持個人庫純淨，AI 產物必須隔離）兩種哲學的對立。作者最終的錨點是常青筆記（Evergreen Notes）：原子化、概念性、靠鏈接而非標籤組織，且不把思考本身外包給 AI。

## Key facts

**Obsidian 背景**
- 2020 年由 Shida Li（CTO）& Erica Xu（COO）在新冠隔離期間創建；CEO 為 Kepano（Steph Ango，Minimal 主題作者）
- 團隊約 7 人；估值 $350M；150 萬+ 月活用戶；從未接受外部融資
- 商業模式：核心免費，Sync $4/月，Publish $8/月，Catalyst 一次性 $25 起
- 2026/03 社區插件超過 2,500 個，每週 6–14 個新插件、80–100 個插件更新

**Karpathy LLM-Wiki 架構（作者已落地到自己的 Vault）**
```
軟體工程         →  知識庫工程
src/             →  raw/      (原始資料，immutable)
build/           →  wiki/     (LLM 編譯產物)
logs/            →  outputs/  (問答歸檔)
編譯器           →  LLM
IDE              →  Obsidian
Lint/CI          →  Health Check (weekly, outputs/health/)
增量編譯         →  只處理新增/變更的 raw
```
- 攢 5–10 篇 raw → 讓 Claude 逐篇摘要、抽概念、更新索引（第一次 30–60 分鐘，之後增量很快）
- AI Output 落文件：每次複雜提問，結果存到 `outputs/`，帶問題、時間、來源、結論、不確定性
- Health Check 三項：一致性（概念定義衝突）、完整性（缺定義/例子/來源）、孤島（入鏈出鏈 <2）

**別一上來就搭 RAG**
- 知識庫 < 100 篇文章 / 40 萬詞：維護索引文件就夠，LLM 先讀索引再直接閱讀
- 超過 1 萬條筆記且搜不全時，再考慮 RAG

**Kepano 的回應（一句話）**
> Keep your personal vault clean and create a messy vault for your agents.

- 個人產物 vs. Agent 產物必須分離
- Agent 工作流產出有用的東西時，才引入主庫，放進 `clippings/`

**常青筆記三原則（Andy Matuschak 2020）**
1. 概念性——一條講一個想法/洞察
2. 原子化——一條只說一件事
3. 靠鏈接組織，而非標籤

**公開資源（飛書）**
- 踩坑經驗 + 知識庫匯總：https://my.feishu.cn/wiki/PPW4w6eEYi01dfkUgc3cGYsVnkh
- 作者 Obsidian 庫（插件、主題、Agent 提示詞、記憶存檔、自定義 CSS）：https://my.feishu.cn/wiki/GccZwP13MikuGJk07mTcOXAfnAg

## 點解值得留意

- **這個 vault 就是 Karpathy LLM-Wiki 的實作**：`raw/` → `wiki/pages/` → `outputs/` 的三層架構與作者描述的完全對應，可用此文驗證設計決策是否正確。
- **Kepano「乾淨庫 vs. 髒庫」原則直接影響 vault 政策**：AI 捕獲的內容放 `raw/`，人工審核後才進 `wiki/`，與本庫現有規則一致——這篇文章是支持現有設計的外部佐證。
- **「別一上來搭 RAG」是對 Josep 的直接提醒**：庫還小，索引檔案優先，等規模到了再加向量搜尋。
- **作者的公開 Obsidian 庫**可直接參考插件清單、Agent 提示詞範本，值得在需要擴充 skills 時查閱。

## Source

- 連結：https://x.com/Jackywine/status/2095750518941659567（X Article）
- 作者：@Jackywine（Obsidian VIP，Prompt Engineer）
- 發佈：2026-09-04
- 互動：likes=1070 retweets=244 views=414,258 bookmarks=2,673
- Reader：fxtwitter-api

## Related

（首次入庫，尚無相關頁面）
