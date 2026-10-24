# 決策模型對比測試包：Jev vs Clef vs 其他（2026-10-24）

**用途**：用 vault 真實用緊 Jev 嘅判斷，比較 Jev 1.13 / 1.14、Cloudflare Clef / Clef-flash、Strands Decider 同一般 LLM（Claude Haiku / Sonnet 等）。258 題，全部係 Jev 原生 `{state, questions}` 格式，問題原文照抄 `skills/judging-with-jev/references/vault-routine-questions.md`，門檻用 `wiki/hot-list/_config.yaml` 嘅現行數值。

## 四組測試

| 組 | 問題 | 類型 | vault 點用 | 題數 | 輸入從邊度嚟 |
|---|---|---|---|---|---|
| A | `topical`（H2） | noul | weekly-hot-list：GitHub 候選用 1,500 定 3,000 star 門檻。**2026-10-05 起生產中** | 61（正 39 / 負 22；11 題 borderline） | W39–W42 hot list 候選 repo；description、topics、README 頭 60 行 2026-10-24 由 GitHub 重新抓 |
| B | `in_scope`（H1） | score 0–4 | weekly-hot-list：X / Threads 搜尋結果邊啲值得用 40 次 fxtwitter 驗證。**生產中**，act ≥ 3.0 | 81（act 41 / defer 19 / skip 21） | 63 個用 routine 同一方法（DuckDuckGo 經 Jina，`<topic> site:x.com`）2026-10-24 搜到嘅真實結果；18 個 vault 收錄過嘅 X / Threads 帖 |
| C | `type` + `topic` | 兩條 choice 同一 request | capture-link：新收錄項目嘅 type 同 topic tag。**計劃中**（C1/C2） | 83（topic 計 53 題） | 全部 `wiki/pages`，輸入係 `raw/` 頭 3,000 字 |
| D | `same_item`（H3） | noul | weekly-hot-list：X 帖同 GitHub repo 係咪同一樣嘢。**已設定，暫時關閉** | 33（正 16 / 負 17） | hot list 用過嘅 X 帖（fxtwitter 原文）配真 repo 或者易混淆嘅 repo |

## 答案（gold label）點嚟，要知嘅偏差

| 來源 | 題數 | 說明 |
|---|---|---|
| `vault frontmatter` | 83 | C 組：vault 自己嘅 `type` 同 `tags[0]`（Sonnet 收錄 + vault-lint 檢查；7 頁 Jeff verified） |
| `w39-pre-jev` | 9 | A 組：W39 報告嘅判斷，嗰陣 pipeline 仲未用 Jev |
| `opus-report-W40/41/42` | 18 | A / D 組：hot-list 報告入面 Opus 讀完 README 之後嘅決定（例如 Jev defer 之後佢點判） |
| `label-1024` | 148 | 本 session（Claude Code，2026-10-24）按 vault 定義逐題標 |

**偏差**：A 組標籤時睇得到 Jev 1.13 喺報告入面嘅生產數值，可能偏向 Jev。所以 (1) 每組都有 `borderline` 標記，主要指標只計 `clear`；(2) `prompts/20-gold-review.md` 係盲標 prompt，想穩陣可以搵唔參賽嘅模型或者人再標一次。

## 檔案

| 檔案 | 內容 |
|---|---|
| `cases.jsonl` | 258 行，每行 `{id, suite, request, gold, ref, meta}`。**只可以將 `request` 送去模型** |
| `cases.csv` | 答案總覽（id、題目、gold、來源、Jev 1.13 生產數值、短文字），方便人睇 |
| `baselines/jev-1.13.0-production.jsonl` | A 組 54 題 Jev 1.13.0 喺 W40–W42 生產 run 真實回傳嘅機率，可以當一個參賽者計分 |
| `pack.py` | `split`（每題一個 request JSON）、`csv`、`score`（計分）。Python 3.8+，冇 dependency |
| `prompts/00-run-comparison.md` | **主 prompt**：貼落 agent（例如喺呢個 folder 開 Claude Code）就會 probe、跑 3 次、計分、寫 report |
| `prompts/10-llm-baseline.md` | 叫一般 LLM 用 Jev 同款格式答（noul 機率 / choice 機率 / score 分佈）嘅 system prompt |
| `prompts/20-gold-review.md` | 盲標 prompt（可選） |

## 點樣匯入 lab

1. **一次收一個 request 嘅 lab**（例如 Playground、`jev-lab ask <file.json>`）：
   ```sh
   python3 pack.py split --out requests                         # TypeSafe 直連 / Workers AI（Clef）
   python3 pack.py split --out requests-or --flatten --model typesafe/jev-1.14   # OpenRouter：criteria 要轉做字串
   ```
2. **收 JSONL / CSV 批量嘅 lab**：直接用 `cases.jsonl`，將 `request` 欄當輸入，`gold` 欄當答案；或者 `cases.csv`。
3. **用 agent 跑**：喺呢個 folder 開 Claude Code，貼 `prompts/00-run-comparison.md` 下半部份（先改好參賽者表）。

每次 call 寫一行落 `runs/<label>.jsonl`（格式見 `pack.py` 開頭），然後：

```sh
cp baselines/jev-1.13.0-production.jsonl runs/
python3 pack.py score --runs runs --out report-scores.md --json summary.json
```

## 指標點睇

- **auto-wrong**（A / D）：模型直接 act 或者直接否決，但答錯。呢個係最貴嘅錯：routine 唔會再覆核。越低越好，主要睇呢個。
- **deferred**：落入 0.50–0.80，交返 Opus 判斷。冇錯但要錢；borderline 題 defer 反而係好事。
- **missed act items / noise acted**（B）：值得驗證嘅帖被跳過 / 垃圾帖被拎去驗證。前者會漏贏家，後者浪費 40 次配額。
- **Brier / ECE**：校準。ECE 0.10 以上即係「話 80% 但唔係真係 80% 啱」。
- **repeat std / band flips**：同一題跑 3 次嘅穩定度；flip = 3 次之間由 act 跳去 defer 之類。
- **vs Jev 1.13 prod**：同生產數值差幾多、幾多題轉咗 band。用嚟決定好唔好將 pin 由 1.13.0 轉去 1.14.0。

## 已知限制

- README、star 數係 2026-10-24 重新抓，同 routine 當時見到嘅版本可能有少少分別（所以生產數值放喺 `ref`，唔當答案）。
- B 組嘅搜尋結果日期由 tweet ID 計，部份 snippet 係 DuckDuckGo 截斷版本，同生產一樣。
- Clef、Strands Decider 嘅實際 model id 同 endpoint 要喺你帳戶確認；主 prompt 叫 agent 唔好估。
- 只得 258 題，差 1–2 題唔好當顯著；睇錯題清單比睇百分比更有用。
