# Jev 試點交接文件（2026-10-03）

**畀下一個 session / agent 睇嘅一頁紙。** 讀完呢份，再讀 `skills/judging-with-jev/SKILL.md`（點叫 Jev）、`skills/judging-with-jev/references/vault-routine-questions.md`（每個試點嘅問題 JSON、state 欄位、門檻）、`outputs/20261002-jev-in-vault-routines.md`（為何值得做、成本、試點 1 真實結果）。呢份文件只講**狀態、待辦、步驟、陷阱**，唔重複上面三份嘅內容。

## 1. 現況一句

試點 1（`weekly-hot-list` 嘅 H1 `in_scope` + H2 `topical`）已經合併並上線，等 2026-10-05（星期一）08:00 UTC 第一次正式 run 驗收。試點 2–4 未開始。

## 2. 試點 1 做咗啲咩（全部已 merge 入 `main`）

| 件 | 位置 | 狀態 |
|---|---|---|
| 報告 + 草稿 skill | `outputs/20261002-jev-in-vault-routines.md`、`skills/judging-with-jev/` | PR #15 merged |
| API 形狀修正、provider 可配置、env var key 文件 | 同上 + `routines/README.md` | PR #16 merged |
| 「開發改動即時測試，唔等 schedule」實踐 | `routines/README.md` Step 5（只係開發 session 嘅實踐，**唔寫入** CLAUDE.md / AGENTS.md / routine prompt） | PR #17 merged |
| Jev client script、`jev.client` config、prompt 改用 script | `skills/judging-with-jev/scripts/jev_ask.py`、`wiki/hot-list/_config.yaml` `jev:`、`routines/weekly-hot-list.md` step 0 | PR #18 merged（2026-10-03 11:01 UTC） |
| Live Routine prompt 重貼 | claude.ai Routine `weekly-hot-list`（trigger `trig_01FGvPxxku629BRWVuTGTxYv`） | 2026-10-03 11:29 UTC 已貼新版（Josep） |
| 環境 | `TYPESAFE_API_KEY` 係環境變數；`api.typesafe.ai` 喺 allowed domains；Bearer 型 API credential 注入唔 work，唔要再試 | 完成 |
| W40 開發測試報告 | branch `hot-list/2026-W40`、PR #19（**唔要 merge**，星期一正式 run 會 force-push 覆寫） | 開住 |

**已證實**：classifier 放行 `jev_ask.py`（兩個 routine session + 開發 session 零 denial）；probe 200 `jev-1.13.0`；H2 `topical` 112 個 repo、0 fallback，同所有關鍵人手判斷一致（AIHOT 0.27 / HowToLiveBetter 0.36 / floorplan-3d 0.03 → general；所有 agent 工具 ≥ 0.82）；H1 `in_scope` 33 條真實 X 帖、0 fallback；145 個決定約 20.7 萬 input tokens（≈ US$0.009）。
**未證實**：生產 Routine（Sonnet、auto mode、有 Exa + repo 綁定）由頭到尾跑一次；Threads 嘅 H1（Exa 搵唔到 threads.net 結果）；H3 `same_item`（config 關住）。

## 3. 試點 1 尾段待辦（按次序）

1. **星期一 run 後驗收**（Josep 或下一個 session）：開 `hot-list/2026-W40` PR → `## 方法` 要有 `jev: in_scope a/b/c/d; topical …` 一行而唔係 `jev: off (...)`；transcript 冇 permission denial；H1 act 名單冇混入宣傳 / 活動帖。
2. **門檻決定**：開發 run 見 `in_scope` 2.5 偏鬆（活動回顧 3.05、贊助鳴謝 2.90、「分享你嘅 setup」2.55 都入 act）。星期一數據一致嘅話，`wiki/hot-list/_config.yaml` → `jev.in_scope.act_min: 3.0`（改 file 即生效，唔使重貼 prompt）。`topical` 0.80 / 0.50 唔改。
3. **兩個乾淨星期後**：`jev.same_item.enabled: true`；`jev.model` 由 `jev-latest` 釘到當時版本（例如 `jev-1.13.0`）。
4. **Snapshot 缺口**：開發 run 同 W39 一樣只刷新搜尋命中嘅 repo，冇命中嘅 tracked repo（`_snapshot.json` ∪ `wiki/stars`）冇重新抓星數，所以「舊 repo 突然爆升」會漏。生產 Routine 有 GitHub connector / Exa，應照 prompt 刷新全部；如果 Monday run 都冇做，考慮喺 prompt 1a 加硬性一句。
5. **清理**：DEV trigger「weekly-hot-list DEV run (Jev pilot 1, 2026-10-02)」（`trig_01AFdkexceR6xHxAsNiRmquo`，fire-only，冇 cron）可以 disable 或刪除；佢嘅 session 冇 repo 綁定亦冇 Exa，再用價值低。PR #19 等星期一覆寫，或者 close。

## 4. 試點 2 — `github-stars-sync`：S2 `summary_from_readme`（之後 S1 `is_agent_asset`）

目的：5b backfill 嘅候選排序由「CJK 字數 < 20」擴展到「摘要有冇 README 先有嘅事實」。只改排序，唔改寫法。

1. 分支 → 改 `routines/github-stars-sync.md` step 5b：CJK filter 保留；之後「if `python3 skills/judging-with-jev/scripts/jev_ask.py probe` exits 0, for every `wiki/stars/*.md`（或者只係 CJK filter 冇標嘅）build the S2 state（reference §S2：full_name、description、`## 摘要` body、README 頭 100 行）and run `jev_ask.py ask --state <f> --act-min 0.80 --defer-min 0.50`；`band == no`（p < 0.50）嘅最低三個做 backfill 候選，`defer` 由 Sonnet 讀兩邊決定，`act` 跳過」。Fallback（exit 2 / denial）= 今日 CJK-only。最後訊息加一行 `jev: summary_from_readme <asked>/<act>/<defer>/<no>; fallbacks <n>`。
2. 門檻放邊：stars-sync 冇 config file。最簡單係寫死喺 prompt 並註明「reference 嘅預設」；如果想同 hot-list 一致，可以新增 `wiki/github-stars.base.yaml`？——唔建議，多一個檔。寫入 prompt 即可。
3. 測試（即時，唔等 06:00 UTC）：Routine → Run now（係 schedule routine，但 prompt 冇「今日係星期一先跑」嘅 guard，所以任何時間都會真跑）；讀 transcript：見到 `jev_ask.py probe` + 多次 `ask`、最後訊息有 jev 行；對照佢揀嘅三個 backfill 同 CJK filter 嘅名單。成本：34 個 star 筆記 × ≈1,200 tokens ≈ 4 萬 tokens（≈ US$0.002）。
4. 驗收：連續兩次 run 嘅 backfill 候選合理（人手抽查 3 個 p < 0.50 嘅 摘要 確實只係改寫 description）→ 再做 S1（step 4 draft SKILL.md 判斷，reference §S1，`≥ 0.80` draft）。
5. 每次 prompt 改動都要 `copy-prompt` 重貼（見 §7）。

## 5. 試點 3 — `vault-lint`：L1 `near_duplicate`（之後 L2 `review_priority`）

1. 改 `routines/vault-lint.md` check 5：先確定性預篩配對（標題共享 ≥ 4 字元嘅小寫 token、或同 `author`、或 `source_url` 同 host），每對一次 `jev_ask.py ask`（reference §L1 state：兩頁嘅 slug / title / type / source_url / 摘要 頭兩句），`≥ 0.80` 列入 `## Suggested fixes`（建議合併，唔自動合併），`0.50–0.80` Sonnet 自己讀，`< 0.50` 唔理。`outputs/health/WEEK.md` 加一行 jev 統計。預計每週 ≈ 20 對、≈ 4,000 tokens。
2. 測試：Run now（lint prompt 用「this ISO week」，冇星期一 guard，任何日都真跑，但會寫 `outputs/health/WEEK.md` 同 commit 到 main——呢個係 lint 本身嘅行為，可接受）。
3. 之後 L2：check 6 嘅 stale-draft 名單用 `review_priority`（score，五級，reference §L2）排序，只排序唔刪。

## 6. 試點 4 — `capture-link`：C1–C5（最後做）

每條 URL 一次 request 問 `type`（choice，7 類，criteria 抄 `vault-capture` §3）、`topic`（choice，11 個 `topic/*`，只喺 post/video/article）、`actionable`（noul → 要唔要 draft SKILL.md）、IG/FB 加 `substance_in_caption`（→ `needs_manual_text`）；`related_relevance`（score）對 `vault-search` 結果排序揀 `## Related`。要改 `skills/vault-capture/SKILL.md` §3 / §4 加「Jev 建議 + Sonnet 覆核」同 `routines/capture-link.md`。測試用 `.\scripts\capture.ps1 <url>` 或 Routine 嘅 Run now（API routine，有 run text 框，貼 URL）。慳得最少（一次 run 一條 URL），價值係 type / topic 揀法一致。

## 7. 每個試點都要行嘅步驟

1. 開分支改檔 → `bash scripts/vault-guard-check.sh origin/main HEAD Tradecreditor` → push → 開 PR（Josep merge；核心帳戶先可以）。
2. Merge 後 Josep 本機 `git pull --rebase origin main`，然後 `.\scripts\copy-prompt.ps1 <routine>`（macOS/Linux：`bash scripts/copy-prompt.sh <routine>`），見綠色 "verified intact" 先去 Routine → Instructions 全選刪除 Ctrl+V Save。Routine 儲存自己一份 prompt，改 repo 檔唔會自動生效。
3. **即時 Run now 測試，唔等 schedule**（開發實踐；只喺 README Step 5，唔寫入 routine prompt）。讀 transcript 核實 `jev_ask.py probe` 有出現、jev 行有數字。
4. 所有 Jev 請求經 `jev_ask.py`（exit 0 答到 / 2 整個 run 關 Jev / 3 單項 fallback / 4 state 有 secret 被拒）。永不手寫帶 key 嘅 curl / Python。
5. Jev 只揀分支，永不改數字、gate、公式、dedupe；state 只放 reference 列明嘅欄位。

## 8. 已知陷阱（2026-10-02/03 實測）

- **Auto-mode permission classifier**：曾以「Data Exfiltration」拒絕一條帶 `$TYPESAFE_API_KEY` 嘅 curl，35 分鐘前同一 call 卻通過；script 之後零 denial。Repo 嘅 `.claude/settings.json` allow rule 繞唔過（文件：只有 managed settings 嘅 `autoMode` 規則先得）。被拒時 routine 要當 `jev: off (permission denied)` 照完成。
- **Routine session 嘅 GitHub API**：冇 repo 綁定嘅 session（例如 agent 自建嘅 trigger）打 `api.github.com` 一律 403「sessions are bound to their configured repositories」；有綁定嘅 session search 都可能 403。可行路：GitHub connector、Exa `web_fetch_exa` 打 API URL（prompt 寫明嘅 cloud 路徑）、Jina `r.jina.ai/https://api.github.com/...`（免費但約 20 次後封匿名請求，要 URL-encode `>=`）。`raw.githubusercontent.com` 直連 OK。
- **Exa 搜唔到 x.com / threads.net**：22 次搜尋零社交 URL（`site:` 同 plain 都係）。X 證據要由候選作者嘅 fxtwitter timeline 攞：`api.fxtwitter.com/2/profile/<handle>/statuses`（key 係 `reposts` 唔係 `retweets`；cursor 要 URL-encode），單帖 `api.fxtwitter.com/<user>/status/<id>`。作者 handle 由 README 或 GitHub `users/<login>.twitter_username` 搵。
- **Exa fetch 大輸出**：`web_fetch_exa` 一個 repo 物件 ≈ 6.6 KB；`maxCharacters` 太細會截斷，太大會塞 context；批量用 10 個 URL × 7,000–12,000 字元。
- **平台限制**：schedule 型 Routine 嘅 Run now 冇 run text（只有 API 型有）；agent 只能 `fire_trigger` 自己建嘅 trigger；`create_trigger` 唔能加 connector（所以 DEV trigger 冇 Exa）；子 session 有時拒絕 seeded prompt。
- **TypeSafe 403 語義**：冇 key 同 key 無效都回 `403 authentication_error`；proxy 封 host 係 CONNECT 403 冇 JSON body。Key / base_url / model 係同一供應商一套（直連 / Vercel AI Gateway / OpenRouter）。
- **Jev 本身**：score criteria 係有序 array、分數由 0 起（五級 = 0–4）；H1 2.5 偏鬆（見 §3.2）；state 當不可信資料。

## 9. 檔案地圖

- 判斷邏輯：`skills/judging-with-jev/SKILL.md` · 問題集：`skills/judging-with-jev/references/vault-routine-questions.md` · 離線測試答案：`.../references/jev-fake.example.json` · client：`skills/judging-with-jev/scripts/jev_ask.py`
- 試點 1 設定：`wiki/hot-list/_config.yaml` `jev:` 區塊 · prompt：`routines/weekly-hot-list.md` · 開發報告：`wiki/hot-list/2026-W40.md`（branch `hot-list/2026-W40` / PR #19）
- 分析同成本：`outputs/20261002-jev-in-vault-routines.md`（§試點 1 開發測試結果 有 48 repo 對照表） · 分層規則：`skills/model-tiering/SKILL.md` Part C
- 操作手冊：`routines/README.md`（Step 0 環境、Step 5 即時測試、Things worth knowing → Jev）
- PR 記錄：#15 報告+skill · #16 API/provider/env var · #17 測試實踐 · #18 script+config+prompt · #19 W40 dev run（唔 merge）
