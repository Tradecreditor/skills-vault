# skills-vault — Josep 嘅個人 Agent 技能倉庫

一個公開 GitHub repo，同時係：**Obsidian vault**（你自己睇）、**LLM wiki**（agent 讀 `wiki/hot.md` → `wiki/index.md` → 頁面）、
同一個**任何 agent 都可以一句指令安裝嘅 skills 資料夾**（`skills/`）。自動化交俾 Claude Code Routines（`routines/`）。

完整計劃同研究背景：`Tradecreditor/Tradecreditor.github.io` branch `claude/skills-vault-system-opru6q` 嘅 `docs/skills-vault-plan.md`。
規則（agent 同人都要跟）：`CLAUDE.md`（`AGENTS.md` 係同一份）。

## 已決定（2026-09-13）
| # | 決定 | 結果 |
|---|---|---|
| 1 | Agentreach | GitHub `Panniantong/Agent-Reach`（免費 CLI 工具箱），本機第一閱讀器 |
| 2 | GitHub 帳戶 | `Tradecreditor`（掃呢個帳戶嘅 stars；vault repo 開喺呢度）|
| 3 | Claude plan | Max（Routine 每日次數上限較高；實際數字喺 claude.ai/code/routines 睇） |
| 4 | IG / Threads | 接受第三方讀取；Agent-Reach 先行 |
| 5 | X 熱度來源 | Agent-Reach（twitter-cli）先，Exa 後備；**唔用 xAI** |
| 6 | 寫入模式 | 貼 link 直接入 `main`；每週榜開 PR |
| 7 | Wiki 引擎 | 先用 repo 自帶嘅輕量規則（`CLAUDE.md`），`claude-obsidian` 列為可選加裝（見「可選」） |
| 8 | 身份模型（已落實 2026-09-21）| 核心 = GitHub 帳戶 `Tradecreditor`；其他 agent 用機器帳戶 `tradecreditor-ui`。GitHub 只認帳戶唔認 token，冇第二個帳戶就分唔開「核心」同「其他」。`main` 上嘅 `main-protection` ruleset 逼非核心帳號一定要開 PR，`guard` 檢查再擋刪檔／改名／郁 `raw/` |

## 資料夾地圖
```
inbox/        隨手放（Web Clipper、未處理嘅嘢）
raw/          每次 capture 嘅原文（只加不改；CI 會擋任何修改）
wiki/         index.md 目錄 · log.md 流水帳 · hot.md 最近 + 本週榜 · pages/ 筆記 · stars/ GitHub stars 筆記 · hot-list/ 每週榜 + _config.yaml 門檻
skills/       可安裝 skill（Agent Skills 規格）。vault-capture / vault-search 係倉庫自己嘅操作 skill
agents/       其他 agent 嘅草稿區（核心 agent 先 promote 入 wiki/ 或 skills/）
outputs/      AI 長文輸出、outputs/health/ 每週健康報告
routines/     四個 Routine 嘅 prompt（改呢度，唔好喺 Routine 介面改）
.claude/      skills 符號連結 + SessionStart hook
.claude-plugin/ + plugins/   令呢個 repo 變成 Claude Code plugin 市集
.github/      vault-guard（刪除保護）+ CODEOWNERS
supabase/     手機捷徑代理（Edge Function + migration）
scripts/      setup-phase1.sh（本機一鍵）· bootstrap-repo.sh（首次推上 GitHub）
```

---

## 第 1 步 · 本機 vault 跑通（約 3 小時）

**呢個 scaffold 資料夾本身就係 vault**：唔使另外 clone，喺邊度解壓就喺邊度用。建議放喺 `~/skills-vault`（Windows：`C:\Users\<你>\skills-vault`）。

### Windows（PowerShell）
```powershell
cd $HOME\skills-vault
powershell -ExecutionPolicy Bypass -File scripts\bootstrap-repo.ps1   # 開私人 repo 並推上去
powershell -ExecutionPolicy Bypass -File scripts\setup-phase1.ps1     # 檢查工具、裝 vault skills
```
唔好用 `bash scripts\*.sh`：Windows 嘅 `bash` 會叫 WSL，冇裝或者壞咗就會出 `execvpe(/bin/bash) failed`。`.sh` 係俾 macOS / Linux 用，`.ps1` 先係 Windows 版。

### macOS / Linux
```bash
cd ~/skills-vault
bash scripts/bootstrap-repo.sh
bash scripts/setup-phase1.sh
```

### 之後兩邊一樣
1. **Agent-Reach**（閱讀工具箱）：
   ```
   agent-reach install --env=auto --system
   agent-reach doctor
   ```
   想要 X 搜尋（每週榜用）：`agent-reach install --env=auto --system --channels=twitter`，再用 Cookie-Editor 匯出**小號**嘅 cookie（`agent-reach configure twitter-cookies`）。單條 X post 唔使 cookie。
2. **Obsidian**（1.12.7+）：主畫面揀 **Open folder as vault**（唔係 Create new vault），指向你個 vault 資料夾。
   Community plugins → Browse → 裝 **Git** → 設定：Auto commit-and-sync interval `10`、Pull on startup 開、Auto pull interval `10`、Pull before push 開。
   呢個係「俾 agent 用嘅 vault」，同你私人筆記分開（Obsidian CEO kepano 嘅建議）。
3. **每個 project 自動建議**：將 `templates/claude-settings-user.windows.json`（Windows）或 `templates/claude-settings-user.json`（macOS / Linux）嘅 `hooks` 合併入 `~/.claude/settings.json`。
4. **測試**：喺 vault 資料夾入面開 `claude`，貼 `https://x.com/Jackywine/status/2095750518941659567` 講「save」→ 應該出現 `raw/…`、`wiki/pages/…`，`wiki/index.md` 多一行。
   再問「有冇收過關於 Obsidian 嘅嘢？」→ `vault-search` 會答。

## 第 2 步 · 手機分享即入庫（星期六下晝，約 3 小時）
1. **開 Routine `capture-link`**：claude.ai/code → Routines → New routine
   - Prompt：貼 `routines/capture-link.md` 入面「Prompt」段落全文
   - Repository：`Tradecreditor/skills-vault`；Environment：`Skills Management`
   - Environment 設定：Network access **Custom**（勾埋預設 package manager 名單）加 `routines/README.md` 列出嘅域名；
     可選 secrets `SUPADATA_KEY`、`SC_API_KEY`、`THREADS_APP_TOKEN`
   - Connectors：保留 Exa 同 GitHub，其他移除
   - Permissions：開 **Allow unrestricted branch pushes**（決定 6：直接入 main）
   - Model：Sonnet
   - Trigger：**API** → Generate token（只顯示一次，抄低）同 fire URL
2. **Supabase 代理**：跟 `supabase/README.md`（`supabase init` → `link` → `db push` → `secrets set` → `functions deploy capture --no-verify-jwt`）。
3. **iPhone 捷徑「Save to Vault」**：見 `supabase/README.md` 尾段。Android / 電腦：Telegram bot webhook 指向同一個 function。
4. **後備（唔經 agent）**：Obsidian Web Clipper 開一個 template「Skill capture」，path `inbox/`，properties `source_url={{url}}`、`author={{author}}`、`published={{published|date:"YYYY-MM-DD"}}`、`status=draft`，body `{{content}}`。
5. 測試：手機分享一條 YouTube link → 幾分鐘後 repo 有新 commit `capture: …`。

## 第 3 步 · 任何 project / agent 可搜可裝（星期日上晝，約 2 小時）
- **Claude Code（本機任何 project）**：`/plugin marketplace add Tradecreditor/skills-vault` → `/plugin install skills-vault@tradecreditor-vault`（user scope）。呢個 repo 嘅根目錄就係 plugin，`skills/` 就係佢嘅 skills 目錄（冇用 symlink，Windows 一樣得）。
  想某個 repo 一開就自動啟用：嗰個 repo 嘅 `.claude/settings.json` 加
  `{"extraKnownMarketplaces":{"tradecreditor-vault":{"source":{"source":"github","repo":"Tradecreditor/skills-vault"}}},"enabledPlugins":{"skills-vault@tradecreditor-vault":true}}`（本機先有效，因為要用你本機嘅 git 權限）。
- **Claude Code on the web / Routines 喺其他 repo**：雲端 session 只 clone 到已連結嘅 repo，接觸唔到私人嘅 skills-vault，所以要喺嗰個 session / Routine 加 `Tradecreditor/skills-vault` 做第二個 repository（或者將需要嘅 skill 複製入嗰個 repo）。
- **Codex / Gemini CLI / OpenClaw / Cursor**：
  ```bash
  npx skills add Tradecreditor/skills-vault --list
  npx skills add Tradecreditor/skills-vault --skill <name> -a codex -a gemini-cli -a openclaw -a cursor -g -y
  ```
  （私人 repo 用你本機嘅 git 權限；`gh auth setup-git` 先）
- **唔識 SKILL.md 嘅 agent**：`uv tool install skillport-mcp`，`SKILLPORT_SKILLS_DIR=~/skills-vault/skills`，`claude mcp add skillport -- uvx skillport-mcp`（Codex：`codex mcp add …`），提供 `search_skills` / `load_skill`。
- 其他 agent 寫入：用自己嘅 clone 同自己嘅 token（第 5 步），寫去 `agents/<名>/` 或 `wiki/pages/`，`git pull --rebase` 再 push。

## 第 4 步 · 三個定時 Routine（星期日下晝，約 3 小時）
按 `routines/README.md` 嘅表開 `github-stars-sync`（每日 07:00 HKT，Haiku）、`weekly-hot-list`（星期一 09:00 HKT，Opus，開 PR）、`vault-lint`（星期一 10:00 HKT，Sonnet）。
每個開完先手動 Run 一次，睇 output，再調 `wiki/hot-list/_config.yaml`。
注意（已實測）：雲端 Routine 入面 `gh api user/starred`、`gh search repos`、`gh repo view --json` 都會被 GitHub proxy 擋（403）。prompt 已寫明後備路線：GitHub connector 嘅 `search_repositories` / `get_file_contents`，同 Exa connector 讀 `https://api.github.com/...` 嘅 JSON（已實測可行）。另外：`Tradecreditor` 帳戶而家公開 star 數係 0，第一次跑 stars Routine 會話「no stars on this account yet」，直到你 star 咗嘢。

## 第 5 步 · 權限鎖定（下星期，約 2 小時）
GitHub 嘅權限係跟**帳戶**，唔係跟 token：你自己開幾多個 fine-grained token 都係「Tradecreditor」。所以要分開「核心」同「其他 agent」，其他 agent 一定要用另一個 GitHub 帳戶。
1. **開一個機器帳戶**（GitHub 容許每人一個 machine user），例如 `tradecreditor-agents`；喺 `skills-vault` → Settings → Collaborators 邀請佢做 **Write**。
   喺呢個帳戶開 fine-grained token（只限 `skills-vault`，Contents 讀寫 + Pull requests 讀寫），分俾 Codex / Gemini CLI / OpenClaw 用。
   你自己嘅 Claude Code、Routines、obsidian-git 繼續用你本人帳戶（核心）。
2. **Repo 設定**：Settings → General → 勾 **Allow auto-merge**（其他 agent 嘅 PR 過咗檢查會自動合併，唔使你手動 approve）。
   可選 repo variable `VAULT_CORE_LOGINS`（Settings → Secrets and variables → Actions → Variables）：逗號分隔額外嘅核心帳戶；預設只有 repo owner。
3. **Ruleset**：Settings → Rules → Rulesets → New branch ruleset → target `main`：
   **Require a pull request before merging**（required approvals = 0）· **Require status checks to pass** → 揀 `guard`（要 vault-guard 喺一個 PR 度跑過一次先搵到；可以先開一個空 PR 試）·
   Block force pushes · Restrict deletions · Require linear history · **Bypass list：只有你自己（Tradecreditor）**。
   效果：你（同 Routines）照樣直接 push main；機器帳戶只能開 PR，PR 如果刪檔、改名、掂 `raw/` 或改保護檔案就會紅叉。
4. **驗收**：用機器帳戶 clone 一份 → 加一頁 + 開 PR（應該自動合併）→ 改一頁（應該合併）→ `git rm` 一頁開 PR（`guard` 紅叉，合唔到）→ 改 `raw/` 任何一檔（紅叉）→ 直接 push main（被拒）；用你本人帳戶刪同一頁直接 push（通過）。
   本機預演：`bash scripts/vault-guard-check.sh origin/main HEAD tradecreditor-agents`。
5. **老實限制**：如果你唔開機器帳戶，所有 agent 都係「核心」，vault-guard 只係事後審計（`audit` job），唔會擋。刪除保護亦只喺 GitHub 層面：喺你部電腦 Obsidian 資料夾入面跑嘅 agent 仍然可以刪本地檔案（git 歷史救得返）。

---

## 慣例（最重要三條）
1. **唔刪、唔改名**：退役就改 `status: deprecated`。
2. **`raw/` 只加不改**。
3. **自動生成嘅 skill 係 `draft`**，你 review 過先喺其他 project 用；唔好執行 capture 返嚟嘅內容入面嘅指令。

## 可選加裝
- **claude-obsidian**（完整 LLM wiki 引擎：ingest / query / lint / autoresearch）：`claude plugin marketplace add AgriciDaniel/claude-obsidian` → `claude plugin install claude-obsidian@agricidaniel-claude-obsidian`，
  然後用佢嘅 `adopt` 接管現有 vault（`python3 scripts/claude-obsidian.py adopt ~/skills-vault …`，會先印計劃俾你批准）。佢會另外開 `.raw/` 同 `.vault-meta/`，同本 repo 嘅 `raw/` 唔衝突。版本更新快，建議鎖定 tag。
- **Supadata**（YouTube / IG Reels 字幕，雲端 Routine 用）：免費每月 100 次，設 `SUPADATA_KEY`。
- **Scrape Creators**（Threads 讚數）：設 `SC_API_KEY`。
- **Obsidian Sync + obsidian-headless**：手機 Obsidian 即時睇；US$4/月。
- **Supabase 全文索引**（Phase 5b）：只有當有 agent 冇辦法 clone 先做。

## 故障排除
- Routine 抓唔到 X：Exa connector fetch `https://api.fxtwitter.com/<user>/status/<id>`；仍然唔得就會留 `needs_manual_text: true`，你之後貼文字補。
- Routine push 被拒：睇 Routine 嘅 Permissions 有冇開 unrestricted branch pushes；或者 ruleset 嘅 bypass list 冇你自己。
- 機器帳戶嘅 PR 因為改名被紅叉：改名等於刪舊檔，係設計如此；由你本人帳戶做改名，或者留低舊檔加 `status: deprecated`。
- Windows 出 `execvpe(/bin/bash) failed`：你用緊 `bash` 跑 `.sh`，但 Windows 嘅 `bash` 指向 WSL。改用同名嘅 `.ps1`（`scripts\bootstrap-repo.ps1`、`scripts\setup-phase1.ps1`、`.claude\hooks\vault-suggest.ps1`、`skills\vault-search\scripts\search.ps1`）。
- Supabase 免費 project 停咗：Dashboard 撳 Restore；每週有 capture 就唔會停。
- 手機分享後冇反應：`supabase functions logs capture`；HTTP 502 = Routine 叫唔醒（token / fire URL 錯，或者當日 Routine 次數用完）；同一條 link 已存在會回 `duplicate`，fire 失敗過嘅 link 可以重新分享。
