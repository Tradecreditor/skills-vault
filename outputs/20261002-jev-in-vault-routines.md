# Jev 點樣放入 vault 四個 Routines（2026-10-02）

**決定**：Jev 只用喺「對大量項目做 yes/no、揀一個、打分」嘅步驟，永遠唔用佢寫 摘要 或 Key facts。每個 Jev 呼叫都保留今日嘅路徑做 fallback：冇 `TYPESAFE_API_KEY`、HTTP 402 / 5xx、或者機率落入中間地帶，就照今日做法由 Sonnet / Opus 決定，並喺最後訊息講一次。第一個試點係 `weekly-hot-list` 嘅候選預篩（X / Threads 搜尋結果揀邊 40 個去 fxtwitter 驗證、GitHub 候選嘅 topical gate），之後係 `github-stars-sync` 嘅 backfill 篩選器同 `vault-lint` 嘅近似重複判斷。`capture-link` 一次 run 只有一條 URL，Sonnet 點都要讀全文寫 摘要，所以 Jev 喺呢度慳唔到幾多，只係令 `type` / `topic` 揀法一致，排最後。今次只出呢份報告加 draft skill `skills/judging-with-jev/`，唔改任何 routine prompt、`_config.yaml` 或 script。

## 摘要

Jev 係 TypeSafe AI 2026-09-15 推出嘅「System One」判斷模型：你送一個 state（文字或 JSON）加一組有名有類型嘅問題，佢回傳校準過嘅機率，唔會寫任何文字。三種問題：noul（命題為真嘅機率）、choice（每個選項一個機率）、score（喺你用文字定義嘅 2–10 級量表上嘅位置）。同一個 request 可以放多條問題共用 state，只收 input token 錢，Jev 自己網站引用嘅中位數大約每個判斷 US$0.000068。

Vault 四個 Routines 入面，寫作（摘要、Key facts、週報）一定要留喺 Sonnet / Opus，但有十幾個步驟其實係判斷：呢個搜尋結果同 vault scope 有冇關、呢個 repo 係唔係 agent skill / MCP server、兩個標題係唔係同一樣嘢、呢篇 摘要 係唔係照抄 description。今日呢啲判斷全部由 routine 本身嘅模型做，`weekly-hot-list` 仲係用 Opus 讀幾百個搜尋結果先揀邊 40 個值得花 fxtwitter 配額。將呢啲判斷交俾 Jev，Opus / Sonnet 只讀過關嘅項目，每星期 Jev 開支估計低於 US$0.10（見成本估算），而且判斷一致、每個機率都有紀錄、門檻可以事後調。

前置條件有三：Routine 環境加 `api.typesafe.ai` 做 allowed domain（呢個 sandbox 而家 curl 回 proxy 403）、`TYPESAFE_API_KEY` 用 Routine secret 存放、每個呼叫有固定 fallback。官方文件 madewithjev.com 同 api.typesafe.ai 喺呢個環境讀唔到，所以 API 細節來自 vault 入面 fast-jev-compaction 嘅 README、第三方站 jevmodel.org 同搜尋結果摘要；價錢同 response 欄位名要喺第一次 live 呼叫時核實，skill 已經標明邊啲係估。

## Jev 是咩

| 項目 | 事實 | 來源 | 狀態 |
|---|---|---|---|
| 推出 | 2026-09-15，TypeSafe AI（Diogo Almeida，@CompleteSkeptic），RLCD 訓練法；宣稱比 frontier chat 模型快 20–200 倍、平 40–400 倍，output token 免費 | madewithjev.com launch post（經 Exa 讀） | 已讀 |
| Endpoint | `POST https://api.typesafe.ai/v1/systemone`，`Authorization: Bearer $TYPESAFE_API_KEY`，model alias `jev-latest` | `raw/20260920-fast-jev-compaction.md`（README Options 表）| 已讀 |
| Request | `{ "state": <string / JSON / array>, "model": "jev-latest", "questions": { "<name>": { "type", "instructions", "criteria" } } }` | jevmodel.org/api（第三方站；request 形狀同 README 一致）| 已讀，欄位名未經官方文件核實 |
| 問題類型 | `noul`（命題為真嘅機率，機率本身就係信心值）· `choice`（每個 label 一個機率）· `score`（2–10 級有序量表上嘅位置，可以係小數）| jevmodel.org/api；DataCamp / LangChain 文章標題 | 已讀 |
| 批量 | 一個 request 多條問題，共用 state token，一齊答；60 條 rubric 問題同 1 條差唔多價 | jevmodel.org/api；madewithjev jev-for-seo（經 `20260925-jev-seo-geo-audit-cost-down-90`）| 已讀 / 轉述 |
| 上限 | 每個 request 約 32k tokens；只收文字 | fast-jev-compaction README（`maxRequestTokens` 30k 「under Jev's 32k request limit」）| 已讀 |
| 價錢 | 只收 input；中位數 US$0.000068 / 判斷（15 次量度）；1 問 × 1,000 URL ≈ $0.07；20 項 rubric × 1,000 URL ≈ $1.36 | madewithjev jev-for-seo，經 vault 頁轉述 | 轉述 |
| 價錢 | US$0.05 / 1M input tokens | apimodels.app 搜尋結果標題 | **未驗證**（內文被封）|
| 重試 | 加 `Idempotency-Key` header | jevmodel.org/api | 已讀 |
| 鎖版本 | 門檻調好後由 `jev-latest` 轉做固定版本（jevmodel.org 寫 `jev-1.13.0`）| jevmodel.org/api | 第三方站，寫法未核實 |
| 訓練 | RLCD（Reinforcement Learning for Calibrated Decisions）：預測機率同實際命中率吻合先有獎勵，所以 0.8 大約真係 80% 準；TypeSafe 未發表架構論文 | IBM Technology 解說片，vault 今日 capture（`wiki/pages/20261002-what-is-jev-system-one-ai-model.md`，`raw/` 有逐字稿）| 已讀 |
| 弱點 | 只收文字；數學同點算差；**input 入面藏嘅指令可以誤導佢**（prompt injection）| 同上 | 已讀 |
| 門檻示範 | IBM 例子：> 0.9 自動處理、0.1–0.9 人手覆核、< 0.1 忽略；「錯誤成本愈高，門檻愈高」。逐字稿叫三種問題做 noul / choice / score，同 jevmodel.org 一致（該頁 Key facts 寫 `bool` / `scale` 係轉述）| 同上 | 已讀 |
| 可靠做法 | 設門檻；中間地帶交大模型或人；記錄 input / output / 機率 / 模型版本；每個 Jev 動作後面都有 fallback | jevmodel.org/api；fast-jev-compaction（`keepThreshold` 0.5，失敗就 throw 交返 caller）| 已讀 |
| Sandbox | 環境冇 `TYPESAFE_API_KEY`；`curl https://api.typesafe.ai/v1/systemone` → `CONNECT tunnel failed, response 403` | 本 session 2026-10-02 | 已驗證 |

## 四個 Routine 入面嘅判斷步驟

規則先講：**Jev 永遠唔會刪走一個已經過咗數字 gate 嘅項目**。`_config.yaml` 嘅 gate 係確定性算式，照舊由 routine 計。Jev 只做三類事：決定「邊啲先讀 / 邊啲值得花配額」、做本來就要人判斷嘅 yes/no（topical、same item、actionable）、同埋排序。

### weekly-hot-list（Opus，每週一）— 最大慳位

| # | 步驟（prompt 原句）| 今日 | Jev 問題 | state | 門檻 → fallback | 結論 |
|---|---|---|---|---|---|---|
| H1 | 1b/1c：「only then fxtwitter-verify the in-window hits (the fxtwitter cap is 40, so never spend it on out-of-window posts)」；Threads「read each post via Jina」 | Opus 讀 13 topic × 25 個 X 結果 + Threads 結果嘅 snippet，自己揀邊 40 個去驗證 | `in_scope` score（五級，0–4）：呢個帖幾大程度係講 `_config.yaml` `scope:` 範圍內嘅新工具 / skill / MCP / repo | title + snippet + author + publishedDate（約 300 tokens）| ≥ 2.5 入驗證名單，按分排序取前 40；1.5–2.5 Opus 睇一眼；< 1.5 跳過，數目寫入 ## 方法 | **採用（試點 1）** |
| H2 | 1a：`min_stars_gained_7d_if_topical` gate 嘅 topical 判斷（「README/topics mention agent, skill, MCP, Claude Code, Codex, OpenClaw」）| Opus 逐個 repo 睇 description / topics / README 決定用 1,500 定 3,000 門檻 | `topical` noul：呢個 repo 係唔係 agent / agent skill / MCP server / coding-agent 工具 | name + description + topics + README 頭 60 行（約 1,500 tokens）| ≥ 0.80 topical；0.50–0.80 Opus 決定；< 0.50 用一般門檻 | **採用（試點 1）** |
| H3 | 1 末段：「Group candidates by item (canonical GitHub repo when one exists, otherwise normalised product name)」| Opus 憑名稱同描述配對 X 帖同 GitHub repo | `same_item` noul：呢個帖同呢個 repo 係唔係同一個產品 | 帖文 + repo name / description（約 600 tokens）| ≥ 0.80 合併；0.50–0.80 Opus 決定；< 0.50 分開 | 採用（試點 1，H1/H2 跑穩之後）|
| H4 | 3：「draft skills/<name>/SKILL.md only if it is an installable skill or a repeatable procedure」| Opus 寫報告時順手判斷 | `installable_skill` noul | 贏家嘅 README / 帖文頭 2k tokens | ≥ 0.80 draft；否則唔 draft，Opus 唔再諗 | 之後（每週只有 2–3 個贏家，慳得少）|
| H5 | 2：gate 同 heat 計算 | 算式 | — | — | — | **唔用 Jev**：確定性算式唔應該交俾機率模型 |

慳到：Opus 唔再讀 ~450 個 snippet 同 ~390 個 repo 物件嘅 topical 判斷，fxtwitter 40 次配額全部用喺有關嘅帖；run 時間跟住短。風險：H1 誤判漏走一個贏家 — 緩解係門檻設低（3.5/5）、中間地帶交 Opus、同埋 ## 方法 要列出被 Jev 跳過嘅數目，Josep 可以抽查。

### github-stars-sync（Sonnet，每日）

| # | 步驟（prompt 原句）| 今日 | Jev 問題 | state | 門檻 → fallback | 結論 |
|---|---|---|---|---|---|---|
| S1 | 4：「If the repo is itself an agent skill, Claude Code plugin, MCP server or OpenClaw skill, also draft skills/<gerund-name>/SKILL.md」| Sonnet 讀 README 時自己判斷 | `is_agent_asset` noul | description + topics + README 頭 100 行（約 1,200 tokens）| ≥ 0.80 draft；0.50–0.80 Sonnet 決定；< 0.50 唔 draft | 之後（每日 ≤ 6 個 repo，慳得少；價值在一致）|
| S2 | 5b backfill：「Every path it prints is a candidate, whatever that file's needs_manual_text says - an earlier run set that flag to false on notes whose README it had never read」| Python 數 CJK 字數，只捉到英文 摘要；捉唔到「繁中但照抄 description」 | `summary_from_readme` noul：呢篇 摘要 有冇 README 先有、description 冇嘅事實 | description + 摘要 + README 頭 100 行（約 1,200 tokens）| < 0.50 列為 backfill 候選（最多 3 個）；≥ 0.80 當合格；中間由 Sonnet 讀 | **採用（試點 2）**：補返一個已知盲點 |

### vault-lint（Sonnet，每週一）

| # | 步驟（prompt 原句）| 今日 | Jev 問題 | state | 門檻 → fallback | 結論 |
|---|---|---|---|---|---|---|
| L1 | 5：「near-duplicate titles」| Sonnet 逐週重新目測（W40 報告又再列 OpenSpec / OpenMAIC / OpenCLI 呢類表面相似）| `near_duplicate` noul：兩個條目係唔係同一樣工具 / 同一個來源 | 兩個條目嘅 title + type + source_url + 摘要 頭兩句（約 200 tokens）| 只對 token 重疊預篩出嘅配對問（約 20 對）；≥ 0.80 寫入 ## Suggested fixes；0.50–0.80 Sonnet 睇；< 0.50 唔提 | **採用（試點 3）** |
| L2 | 6：「draft entries older than 30 days (list them for Josep to review)」| 只列清單；而家 42 個 draft，9 月 19 日嗰批好快過 30 日 | `review_priority` score（五級，0–4）：呢篇值唔值得 Josep 先 verify（內容完整、有 Related、有 raw、同近期 capture 有關）| frontmatter + 摘要（約 800 tokens）| 用分數排清單，唔刪任何項 | 之後 |
| L3 | 1–4、7 嘅機械檢查 | 腳本 | — | — | — | **唔用 Jev**：確定性檢查 |

### capture-link（Sonnet，每條 URL 一次 run）— 排最後

| # | 步驟（vault-capture 原句）| 今日 | Jev 問題 | state | 門檻 → fallback | 結論 |
|---|---|---|---|---|---|---|
| C1 | §3 Type rules（skill / tool / repo / concept / post / video / article）| Sonnet 揀 | `type` choice，criteria 直接抄 Type rules | title + author + platform + raw 頭 2k tokens | 最高機率 ≥ 0.60 用；否則 Sonnet 決定 | 之後（一致性，唔係成本）|
| C2 | §3 Topic tag：「the first entry of tags is exactly one value from the fixed vocabulary」| Sonnet 揀 | `topic` choice，11 個 `topic/*`，只喺 type ∈ post / video / article 時問 | 同上 | 同上 | 之後 |
| C3 | §4：「Create skills/<gerund-name>/SKILL.md when the source teaches a repeatable procedure an agent could follow」| Sonnet 決定 | `actionable` noul | 同上 | ≥ 0.80 draft；0.50–0.80 Sonnet；< 0.50 唔 draft | 之後 |
| C4 | §1 Instagram / Facebook：「if the caption carries the substance set needs_manual_text: false; if it is only a teaser … set true」| Sonnet 決定 | `substance_in_caption` noul | caption + 帖文 metadata | ≥ 0.80 false；< 0.50 true；中間 Sonnet | 之後 |
| C5 | §3 Related：「wikilinks to existing pages found by vault-search」| Sonnet 讀 search 結果揀 | `related_relevance` score（五級，0–4），每個 hit 一問 | 新頁 title + 摘要；候選頁 title + tags + 摘要 頭句 | 取前 3 個 ≥ 2 | 之後 |

點解排最後：一次 run 只有一條 URL，Sonnet 一定要讀全文先寫得出 摘要，Jev 五條問題加埋大約 2k tokens、不足 US$0.001，慳嘅係一致性而唔係錢。等 hot-list 試點證明咗 fallback 同 log 格式先一次過加入。

### 唔採用 / 留待之後

- **Supabase `capture` edge function 預篩**（例如「呢條 URL 值唔值得 capture」）：手機路徑多一個網絡呼叫同一個 secret，而 dedupe 已經係確定性；Josep 貼嘅連結本來就係佢想收嘅。
- **`.claude/hooks/vault-suggest.sh` 用 Jev 重排建議**：SessionStart hook 只有 20 秒、laptop 要另外有 key；而家 keyword grep 嘅 6 條建議已經夠用。
- **fast-jev-compaction、Jev routing tree**：Claude Code session 層面嘅用法，vault 已有 `20260920-fast-jev-compaction`（verified）同 draft skill `configuring-fable-advisor-jev-tree`；唔喺今次「四個 Routines」範圍。
- **生意用途**：jev-seo 網站審核做 lead magnet、Iron Log / English Overload 內容 QA rubric、短片題材篩選 — 見 `wiki/pages/20260925-jev-seo-geo-audit-cost-down-90.md` 嘅 點解值得留意；同一個 `judging-with-jev` skill 嘅 request shape 可以直接套用。

## 成本估算

公式：每次 run 嘅判斷數 × 每個 state 嘅估算 tokens → 分別用兩個價位計。madewithjev 嘅每判斷中位數係喺短 SEO 頁面 state 上量度嘅，如果計費按 input token，大 state（README 1,500 tokens）每個判斷會貴過中位數；所以兩個數都只係量級。

| Routine | 每次 run 判斷數 | state tokens | 每次 run tokens | 按 $0.000068 / 判斷 | 按 $0.05 / M input（未驗證）| 取代咗啲咩 |
|---|---|---|---|---|---|---|
| weekly-hot-list | H1 ~450 × 1 · H2 ~390 × 1 · H3 ~50 × 1 | 300 · 1,500 · 600 | ≈ 0.75M | ≈ $0.06 | ≈ $0.04 | Opus 讀 ~450 個 snippet 同 ~390 個 repo 嘅 topical 判斷；fxtwitter 40 次配額用得準 |
| github-stars-sync | S1 ≤ 6 × 1 · S2 34 × 1（每週一次）| 1,200 | ≈ 50k | < $0.01 | < $0.01 | Sonnet 重讀 README 去判斷 backfill 候選 |
| vault-lint | L1 ~20 對 · L2 ~40 | 200 · 800 | ≈ 36k | < $0.01 | < $0.01 | Sonnet 逐對目測 |
| capture-link | C1–C5：1 URL × 5 問 | 2,000 | ≈ 2k | < $0.001 | < $0.001 | 幾乎冇 — Sonnet 照樣讀全文 |

每月合計約 US$0.30 以內。慳嘅主要係 `weekly-hot-list` 嘅 Opus input token 同 run 時間（Opus 讀幾百個 snippet 嘅 token 數同 Jev 嘅 state 數量相若，但單價差幾個數量級），其次係判斷一致、可追溯。

## 前置條件

1. **`TYPESAFE_API_KEY`** — 喺 Routine 環境用 **Add credential** 加：Name `TYPESAFE_API_KEY`、type Bearer、Allowed websites `api.typesafe.ai`、header `Authorization: Bearer <key>`。呢種 credential 係 proxy 注入：proxy 自己加 header，變數本身喺 run 入面通常見唔到（`SUPADATA_KEY` 一樣），所以 routine 同 skill 唔可以靠 `env` 判斷有冇 key，要用第一個請求判斷：TypeSafe 冇收到 key 會回 403 加 `authentication_error` JSON（2026-10-02 實測），proxy 封 host 就係 CONNECT 403 冇 body。Key、credential 嘅 Allowed websites、`jev.base_url`、`jev.model` 係同一個供應商嘅一套（TypeSafe 直連 / Vercel AI Gateway / OpenRouter），TypeSafe 對其他供應商嘅 key 回嘅 403 同冇 key 一模一樣（2026-10-02 實測）。本機 shell 就放 `~/.zshrc` / PowerShell profile，永不入 repo。
2. **Allowed domain** — 儲存 credential 時 Allowed websites 填 `api.typesafe.ai` 會自動建立 allow rule；Step 0 嗰張表再手動加一次係雙重保險。冇 allow 嘅話第一個呼叫 403，routine 整個 run 關 Jev 並喺 ## 方法 講明。
3. **固定 fallback 規則**（寫入 skill）：冇 key、402、5xx、timeout、或機率喺 0.50–0.80 → 照今日做法由 routine 本身嘅模型決定；最後訊息一行「jev: N asked, M fell back (reason)」。
4. **Log 格式**（run transcript）：`jev <question> p=0.93 model=jev-1.x state_sha=ab12cd34`，方便事後對照同調門檻。
5. **State 當作不可信資料**：captured 內容可能藏有指令（IBM 片明言 Jev 會被 input 入面嘅指令誤導），所以 `instructions` 寫死喺 code，`state` 只放資料欄位，Jev 嘅答案只用嚟揀分支，永遠唔直接執行；數字（stars、日期差）自己計，唔問 Jev。
6. **第一次 live 呼叫前**：喺 TypeSafe Playground 跑一條 noul、一條 choice、一條 score，核實 response 欄位名，再改 skill 入面 `parse_jev` 嘅對應。

## 下一步（Josep 批准後，每個一個 PR）

1. **hot-list 試點**：`wiki/hot-list/_config.yaml` 加 `jev:` 區塊（`enabled`、`in_scope_min: 3.5`、`topical_min: 0.80`、`defer_band: [0.50, 0.80]`、`max_decisions_per_run: 1500`）；`routines/weekly-hot-list.md` 1a–1c 各加一句「if jev.enabled and TYPESAFE_API_KEY is set, ask Jev first per skills/judging-with-jev」；## 方法 多一行 Jev 統計。跑兩個星期，對照 Watch 名單有冇被 Jev 跳過嘅項目。
2. **stars-sync 試點**：5b 嘅 Python 篩選器之後加 `summary_from_readme`，只係改候選排序，唔改寫法。
3. **lint 試點**：5 近似重複改成 token-overlap 預篩 + `near_duplicate`。
4. 三個試點穩定後，`capture-link` 一次過加 C1–C5，同時 `vault-capture` §3 / §4 加一句「Jev 建議 + Sonnet 覆核」。
5. 每一步都要：`bash scripts/vault-guard-check.sh`、routine 跑一次 Run now、讀 transcript 核實 Jev 行有出現。

## Verified / Unverified

**已驗證（今次 session）**
- Endpoint、auth header、model alias、request 形狀：`raw/20260920-fast-jev-compaction.md` README 同 jevmodel.org/api 一致。
- 三種問題類型、批量、`Idempotency-Key`：jevmodel.org/api 原文。
- 推出日期、作者、宣稱倍數：madewithjev.com launch post（經 Exa）。
- 環境 API credential 係 proxy 注入：本 session 嘅 `SUPADATA_KEY` 喺 `env` 入面完全唔存在，但 system prompt 列明 proxy 會為 `api.supadata.ai` 注入；其他 credential 只係佔位值。所以「有冇 key」只能用請求嘅 401 / 403 判斷。
- API reference（jevwiki.ai 鏡像 TypeSafe 嘅 OpenAPI，2026-10-02 經 Exa 讀）：`Authorization: Bearer`、response `{model, answers, usage}`、score `criteria` 係有序陣列而且分數由 0 起（五級 = 0–4）、每 request 64k tokens（state + 最長問題 32k）、`GET /v1/models` 免費列出可用模型；**TypeSafe 2026-09-24 起停收新註冊**，冇帳戶要用 gateway（OpenRouter `https://openrouter.ai/api`、Vercel AI Gateway `https://ai-gateway.vercel.sh/typesafe`）嘅 base URL 同 model id。
- 2026-10-02 加 domain 同 credential 之後，本 session 已經連到 `api.typesafe.ai`（GET 回 405），但 POST 回 403 `{"detail":{"error_type":"authentication_error","message":"Must supply an API key!"}}`：credential header 未有注入呢個已開始嘅 session（新 session / Routine run 先載入 credential，或者 Allowed websites 填法未對）。
- 本 sandbox：冇 `TYPESAFE_API_KEY`；`api.typesafe.ai` curl 回 proxy 403；madewithjev.com、jevmodel.org、datacamp.com、langchain.com、firecrawl.dev、hyperstack.cloud、marktechpost.com、apimodels.app 全部 egress 封鎖（WebFetch），只有 Exa 中繼讀到 jevmodel.org 同 madewithjev.com 首頁。

**未驗證**
- 每 1M input token 嘅價錢（只見搜尋結果標題）。
- 文件話冇 key 應該回 401，實測係 403 `authentication_error`；兩種都當「冇 key」處理。
- `jev-1.13.0` 鎖版本寫法（jevmodel.org 係第三方站，自稱 `jevmodel.org/v1/systemone` endpoint 同自己嘅 key；**唔要用佢**，用 `api.typesafe.ai`）。
- Routine 環境加 allowed domain 之後 curl 係否真正通到 TypeSafe（要 Run now 一次先知）。

## Sources（2026-10-02 讀）

- Vault：`wiki/pages/20260920-fast-jev-compaction.md`（verified）、`raw/20260920-fast-jev-compaction.md`（README 全文，含 Options 表同 How it works）、`wiki/pages/20260925-jev-seo-geo-audit-cost-down-90.md`（madewithjev jev-for-seo 價錢同 pattern 轉述）、`wiki/pages/20260928-claude-code-fable-advisor-jev-tree.md`、`wiki/pages/20260929-json-render-generative-ui-component-library.md`、`wiki/pages/20260925-5-github-repos-43k-stars-week.md`（jev-ultrafast、laya、hindsight Jev reranker）。
- Vault（2026-10-02 新 capture）：`wiki/pages/20261002-what-is-jev-system-one-ai-model.md` + `raw/20261002-what-is-jev-system-one-ai-model.md` — IBM Technology 影片 "What Is Jev? The AI Model That Doesn't Generate Text"（youtube:YGgNBcIgI4s）逐字稿：RLCD、三種問題、一次 request 全部答、門檻示範、弱點。
- Routines：`routines/weekly-hot-list.md`、`routines/github-stars-sync.md`、`routines/vault-lint.md`、`routines/capture-link.md`、`routines/README.md`、`wiki/hot-list/_config.yaml`、`skills/vault-capture/SKILL.md`、`outputs/health/2026-W40.md`。
- jevmodel.org/api — "Jev API Examples: Choice, Score, and Noul Requests"（經 Exa web_fetch_exa）。
- madewithjev.com — "What people are building with Jev"，launch post by @CompleteSkeptic（經 Exa）。
- 只有標題（內文被封）：datacamp.com/tutorial/jev-api-tutorial；datacamp.com/blog/system-one-models-jev；langchain.com/blog/building-a-harness-with-jev；firecrawl.dev/blog/what-is-jev；apimodels.app/docs/jev（"$0.05 per 1M input"）；marktechpost.com 2026-09-23 "A Coding Guide to TypeSafe AI Jev"；hyperstack.cloud "Jev: Inside TypeSafe AI's First System One Decision Model"。
