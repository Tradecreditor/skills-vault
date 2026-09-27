# skills-vault 使用指南

呢份係俾**用家**睇嘅簡介：呢個系統係乜、做到啲乜、日常點用。
安裝同設定步驟睇 `README.md`；agent 要跟嘅規則睇 `CLAUDE.md`。

---

## 一句講晒

**見到有用嘅 AI 工具、教學、GitHub repo，分享條 link 入嚟，系統就會自動讀晒內容、寫好中文筆記、整理成 skill；之後喺任何 project、任何 agent 都搵得返、裝得返。**

---

## 做到啲乜

| 功能 | 你做乜 | 系統做乜 |
|---|---|---|
| 📥 **收藏連結** | 貼 / 分享一條 link（X、Threads、Instagram、YouTube、GitHub、任何網頁） | 自動讀原文，存一份原文、寫一篇繁中摘要筆記，教得出步驟嘅就順手草擬一個 skill |
| 🔎 **搵返收過嘅嘢** | 問「之前有冇收過關於 XXX 嘅嘢？」 | 搜目錄、skill、筆記，答你係乜、點解相關、原文 link 同安裝指令 |
| 💡 **開新 project 自動提示** | 乜都唔使做 | 開 Claude Code 嗰陣，睇你 project 用緊乜技術，提你 vault 入面邊啲 skill 用得着 |
| 🧩 **一句裝 skill** | 喺 Claude Code / Codex / Gemini CLI / Cursor / OpenClaw 打一行指令 | 將 vault 嘅 skill 裝落嗰個 agent |
| ⭐ **GitHub stars 同步** | 喺 GitHub 撳 star | 每日 07:00 自動幫每個新 star 寫一篇筆記 |
| 🔥 **每週熱門榜** | 乜都唔使做 | 逢星期一 09:00 掃 GitHub、X、Threads、skill 市集，揀出真正爆紅嘅 AI agent 工具，開 PR 俾你睇 |
| 🩺 **每週健康檢查** | 乜都唔使做 | 逢星期一 10:00 檢查格式、重複、斷 link，報告寫入 `outputs/health/` |

---

## 日常點用

### 1. 收藏一條 link

揀一個最就手嘅方法：

- **手機**：喺任何 app 撳「分享」→ 揀 **Save to Vault** 捷徑 → 可以加一句備註 → 幾分鐘後 repo 會多一個 `capture: …` commit。
- **電腦（Claude Code）**：喺 vault 資料夾開 `claude`，貼 link 再講「save」／「收」／「入庫」。
- **電腦（一句指令）**：`bash scripts/capture.sh <url>`（Windows：`scripts\capture.ps1 <url>`），交俾雲端 Routine 做。
- **瀏覽器**：Obsidian Web Clipper 剪落 `inbox/`，下次處理嗰陣會整理好。

同一條 link 收兩次唔會變兩份，系統只會喺原本嗰篇加備註。

### 2. 搵返之前收過嘅嘢

喺 Claude Code 直接問，例如：

> 有冇收過關於 Obsidian 嘅嘢？
> 之前收過邊個 browser 自動化工具？

`vault-search` skill 會答你：標題、點解相關、原文 link，同埋 skill 嘅安裝指令。

想自己睇：打開 Obsidian，由 `wiki/hot.md`（最近 20 項 + 本週熱門榜）開始，再睇 `wiki/index.md`（全部目錄）。

### 3. 將 skill 裝去其他 agent

```bash
# 睇有乜 skill
npx skills add Tradecreditor/skills-vault --list

# 裝其中一個（-a 揀 agent，-g 裝落全域）
npx skills add Tradecreditor/skills-vault --skill <name> -a claude-code -a codex -a cursor -g -y
```

Claude Code 亦可以用 plugin 方式一次過裝晒：

```
/plugin marketplace add Tradecreditor/skills-vault
/plugin install skills-vault@tradecreditor-vault
```

repo 係公開嘅，唔使 token 就裝到。全部 skill 列表見 `skills/README.md`。

### 4. 睇每週熱門榜

逢星期一，系統會開一個 `hot-list/YYYY-Www` 嘅 PR。你睇完覺得 OK 就 merge，報告會存入 `wiki/hot-list/`。
冇嘢夠熱嘅星期會寫「quiet week」，唔會為咗湊數降低門檻。想改門檻或者關注嘅題目，改 `wiki/hot-list/_config.yaml`。

---

## 收完一條 link 之後會出現乜

```
raw/<slug>.md              原文（一字不改，永久保留）
wiki/pages/<slug>.md       繁中筆記：摘要 · Key facts · 點解值得留意 · 來源 · 相關
skills/<name>/SKILL.md     （如果內容係可以跟住做嘅步驟）草擬 skill
wiki/index.md / log.md / hot.md   目錄、流水帳、最近清單各加一行
```

`<slug>` 係「日期-標題」，例如 `20260923-promptfoo`。GitHub stars 嘅筆記就放 `wiki/stars/<owner>--<repo>.md`。

---

## 資料夾速查

| 資料夾 | 用嚟做乜 |
|---|---|
| `inbox/` | 隨手放、未處理嘅嘢 |
| `raw/` | 原文存檔（只加不改） |
| `wiki/pages/` | 你收藏嘅筆記 |
| `wiki/stars/` | GitHub stars 筆記 |
| `wiki/hot-list/` | 每週熱門榜報告 |
| `skills/` | 可安裝嘅 skill |
| `outputs/` | AI 寫嘅長篇答案、每週健康報告 |
| `agents/` | 其他 agent（Codex、Gemini CLI 等）嘅草稿區 |

---

## 三條要記住嘅規矩

1. **唔刪、唔改名**：唔要嘅嘢改 `status: deprecated`，唔好刪檔。
2. **`raw/` 只加不改**：原文係證據，改錯就另開 `-v2` 新檔。
3. **新 skill 一律係 `draft`**：你 review 過先改做 `verified`；未 review 嘅 skill 唔好喺其他 project 直接跑入面嘅指令。

---

## 其他 agent 點用

- **Claude Code、雲端 Routine、Obsidian**：用 Josep 本人帳戶，可以直接寫入 `main`。
- **Codex、Gemini CLI、OpenClaw 等**：用機器帳戶 `tradecreditor-ui` 嘅 token，喺自己嘅 branch 做嘢再開 PR，要 Josep approve 先會合併。
  `guard` 檢查會擋刪檔、改名、改 `raw/` 同改受保護嘅設定檔。

詳細設定（機器帳戶 token、ruleset）睇 `CLAUDE.md` 嘅「Onboarding a non-core agent」。

---

## 出問題點算

| 情況 | 點處理 |
|---|---|
| 手機分享之後冇反應 | 去 claude.ai/code/routines 睇 `capture-link` 有冇跑；可能當日 Routine 次數用完 |
| 筆記寫住 `needs_manual_text: true` | 系統讀唔到原文（例如 IG 要登入），自己貼返文字入去補 |
| 搵唔到收過嘅嘢 | 試下換英文／中文關鍵字；或者直接睇 `wiki/index.md` |
| 其他 agent 嘅 PR 紅叉 | 多數係刪咗檔、改咗名或者掂咗 `raw/`，改返做 `status: deprecated` |

更多故障排除見 `README.md` 尾段。
