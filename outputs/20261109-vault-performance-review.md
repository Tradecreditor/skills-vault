# Skills Vault 表現報告（2026-09-18 → 2026-11-09）

Vault 喺 2026-09-18 先開始，所以「過去 3 個月」即係佢成個生命週期（約 7.5 星期）。
數據來源：`git log origin/main`（287 commits，PR #1–#42）、`wiki/index.md`、page frontmatter、`outputs/health/` W39–W46、
`outputs/skill-reviews/`、`wiki/hot-list/` W38–W45，同 Notion **Skill Installs**（2026-11-09 讀取）。

## 一句總結
**收集同管理做得好，交付做得差。** 捕捉、審核、Routine 全部準時穩定，但入面嘅 skill 好少俾 agent 真正用到。
而家係一個「圖書館」，仲未係會主動推介 skill 嘅資料庫。

## 關鍵數字
| 指標 | 數字 | 評價 |
|---|---|---|
| 條目總數 | 133（96 pages + 37 stars），97 個 raw | ✅ |
| 每月新增 | 9 月 51 · 10 月 76 · 11 月（到 9 號）6 | ⬇️ |
| Jeff 自己貼 link 嘅 capture | W40 37 → W43 10 → W44 2 → W45–W46 **0** | ⬇️⬇️ |
| Skills | 22 個：2 verified · 12 reviewer-approved · 8 draft | ✅ |
| 新 skill 速度 | 20 個喺 10/6 之前建立；之後 5 星期得 **1** 個 | ⬇️ |
| Capture → skill 轉化 | 14 個網上 skill ÷ 96 pages ≈ **15%**；hot list 24 個 winner → **0** 個 skill | ⚠️ |
| Routine 準時率 | hot list 8/8 星期、lint 8/8 星期、Jev fallback 0 | ✅ |
| Review gate | 12 個 approved；7 個 rejected draft 無人修（最舊 36 日） | ⚠️ |
| **真實使用**（Skill Installs） | Jeff PC 92 個安裝入面 vault skill 只有 **4 個（≈4%）**，全部係 vault 自己嘅運作 skill（vault-capture、vault-search、keeping-handoff-docs、model-tiering） | ❌ |
| 網上捕捉 skill 喺其他 project 嘅安裝 | **0**（14 個之中） | ❌ |
| 另一個 marketing project | 7 個安裝，**0** 個來自 vault（vault 有 3 個已批 SEO / marketing skill） | ❌ |
| Orphan pages | 0（W39）→ 29（W46） | ⬇️ |
| Draft > 30 日 | 94（≈71% 條目），無機制令佢哋變 verified | ❌ |
| Board violations | 1（W42）→ 16（W46，本 repo 4 張 stale） | ⬇️ |

## 做得好
- **自動化穩定**：5 個 Routine 準時跑，hot list 同 lint 一個星期都無甩過；Jev prefilter 0 fallback（W45 篩咗 108 個 candidate）。
- **安全同治理**：review gate + `review_hash` 鎖、`guard`、`raw/` 不可改；lint check 1 / 2 / 3 / 5 每週全綠。
- **主動發現已有雛形**：hot list 每週自動揀 3 個熱門，加埋「你貼嘅 link」section。
- **第一次有用量數據**：Skill Installs（11/9 上線）。

## 主要問題（按嚴重程度）
1. **收藏 ≠ 使用。** 14 個網上 skill 喺其他 project 安裝數係 0；marketing project 無用到 vault 嘅 SEO / marketing skill。
2. **入口萎縮。** Jeff 貼 link 跌到 0；新 skill 停咗 5 星期；而家只靠 hot list 每週 3 個。
3. **Hot list 唔產出 skill。** 有啲 winner 本身就係可安裝 skill（impeccable、stageshow、cloudflare security-audit、anatomy isometric），但只寫咗 page，無收入 skill 目錄，所以 `vault-search` 推介唔到。
4. **積壓越嚟越多。** 94 個 draft 永遠唔會變 verified（status 欄失去意義）；7 個 rejected skill 無人修；29 個 orphan。
5. **Board 過時。** 「Hot list straight to main」嗰張 card 其實已經完成（PR #40 / #41 喺 10/30 merge 咗，W44 / W45 都直接推上 `main`，有「你貼嘅 link」section），但仍然寫住 Waiting on Jeff。

## 點樣變成 pro-active skill database（按優先次序）
| # | 做咩 | 效果 | 工作量 |
|---|---|---|---|
| 1 | **Project 配對推介**：每日（或 SessionStart hook）用 Skill Installs 加 project 嘅 stack（CLAUDE.md、package.json）對比已批 skill，推介「呢個 project 應該裝 X」，寫入 Notion 或者喺 session 開頭提示 | 直接解決「用唔到」 | 中 |
| 2 | **外部 skill 目錄**：hot list / capture 見到本身係 skill 嘅 repo，就加一行 registry（name、install 指令、review 狀態），過 `skill-review` 掃描上游 | `vault-search` 可以推介可安裝嘅 skill；已有 ≥6 個候選 | 低 |
| 3 | **入冊 PC 上 64 個非 vault skill**：一次過登記同 review | vault 變成真正嘅 single source of truth | 中 |
| 4 | **用量回饋**：hook 記錄每次 Skill tool 被 invoke（skill 名、project），每週報熱門同零使用；60 日零使用就建議 deprecate | 知道邊個有用、邊個係死貨 | 低 |
| 5 | **自動清積壓**：rejected draft 14 日無人修，`skill-review` 自動試修一次，再 fail 就 deprecate；pages 改做「lint 無問題 + 30 日 → auto-verified」，或者取消 pages 嘅 draft / verified | 94 → 接近 0 | 低 |
| 6 | **按需求捕捉**：每週由 Projects HQ cards 抽出需要（例如 SEO、video），hot list 加一個「你需要嘅」section 搵相關 skill，唔淨係睇星數熱度 | 入口由被動變主動 | 中 |

## Quick wins（今個星期）
- 關閉 hot-list In flight card（Done，證據：PR #40 / #41 + commits `9e38e6c`、`4eddcd2`）→ stale 減 1。
- Jev pilot 1 判 Done（W41–W45 全部 0 fallback）。
- 嗰個 marketing project 裝 3 個已批 marketing skill：`targeting-purchase-intent-keywords`、`auditing-seo-with-crawlie`、`researching-competitor-landing-pages`。
- `model-tiering`（draft，已裝喺 PC）：修好再過 review，或者 uninstall（lint check 10 已經 flag 咗）。
- Notion：刪 test row `global:cloud-test`；check 另一個 global label 嘅 170 行全部 Removed（係咪同一部機用咗 hostname label？）。
  （2026-11-09 Jeff 確認：test row 已刪；嗰 170 行係同 `global:jeff-pc` 重複，Removed 係正確。）

## 下次量度嘅 KPI
| KPI | 而家 | 目標（4 星期後） |
|---|---|---|
| Vault skill 安裝率（vault 安裝 ÷ 總安裝） | 4% | 25% |
| 每個 active project 有 ≥1 個 vault skill | 1 / 2 | 全部 |
| 網上 skill 被安裝數 | 0 | ≥3 |
| Capture → skill（包括外部 registry） | 15% | ≥30% |
| Draft > 30 日 | 94 | <20 |
| 本 repo board violations | 4 | 0 |
