---
title: "ZCode — Z.ai open-sources its Claude Code rival after a git-history upload scandal"
slug: 20260920-zcode-open-source
type: repo
status: draft
source_url: "https://github.com/zai-org/ZCode"
source_platform: github
author: "zai-org"
published: "2026-09-20"
captured_at: "2026-09-22T01:15:53Z"
captured_by: "routine:weekly-hot-list"
canonical_id: "github:zai-org/ZCode"
engagement: "stars=5633 forks=1609 open_issues=11"
tags: [hot-list, coding-agent, z.ai, glm, privacy-incident, typescript]
related: []
needs_manual_text: false
---

## 摘要

Z.ai（前 Zhipu AI,港股上市,市值約 620 億美元,出 GLM 系列模型）將自家嘅 Claude Code 對手 ZCode
（桌面 app + 瀏覽器介面 + 終端 agent 全部一個 monorepo）用 Apache-2.0 全部開源。呢次開源嘅時機唔尋常:
2026-09-18 有開發者 ferstar 發現 ZCode 會靜靜將本地工作目錄（包括 `.git` 完整歷史,佔一個 345MB、
42,411 檔案封存包嘅 86.6%）上傳去阿里雲 OSS,未經用戶同意。Z.ai 同日道歉,話係一個做 session
recovery/版本回退/自動 Repo Wiki 嘅索引功能觸發,已經修復;三日後(09-20/21)就將成個 ZCode 工作台開源,
仲附上一份異常坦白嘅 `NOTICE.md`,逐項列晒有咩功能會讀寫檔案、聯網、傳送去邊。倉庫 24 小時內衝到
5,600+ stars、1,600+ forks（fork ratio 接近 29%,異常高,反映好多人係真係想拎嚟跑/改,唔係純粹標星）。

## Key facts

- **是咩**：AI 編程工作台,單一 repo 包含 Desktop（Electron）、Web、Server（HTTP/WebSocket）、
  Agent CLI（`apps/zcode-cli`）,官方稱為 GLM-5.3 嘅「official harness」。
- **點裝**（命令行版）：
  ```bash
  zcode          # 終端交互界面
  zcode --web    # 瀏覽器界面
  ```
  開發環境需要 Node.js 24.14.0、pnpm 10.33.2、`pnpm bootstrap`。
- **NOTICE.md 揭露重點**：共享執行配置預設 `build` 權限模式;獨立 CLI 用 `--prompt` 跑非交互任務、
  冇指定 `--mode` 會預設 `yolo`(冇 OS sandbox);Computer Use 喺開源版係「不可用佔位實現」;
  兩個官方 Anthropic-compatible 端點會被自動改發去 ZCode 自己嘅網關,連認證 header 都保留轉發。
- **時機背景**：Anthropic 09-14 削減 Claude Code 每週用量 17%,Codex 用戶嗰陣都喺度投訴額度用晒;
  Z.ai 由 09-03 到 09-20 有個 GLM Coding Plan 無限用量優惠,開源 commit 就係優惠最後一日落嘅。
- **數字**（2026-09-22 擷取）：GitHub 5,633 stars · 1,609 forks · 11 open issues（created 2026-09-20,
  ~2 日大）。冇搵到過門檻嘅 X/Threads 貼文（ZCode 官方賬號 @zRdianjiao 個開源公告帖只有 1,329
  likes/153 retweets/224,310 views,遠低於 X gate）。

## 點解值得留意

- 本週 GitHub-only 贏家:呢個新倉未夠 10,000 stars 門檻(唔清 new-repo gate),但佢係 topical
  （coding agent 工具）,用 gain gate 嘅 topical 門檻 1,500 stars 計:5,633/1,500 = 3.76,套用
  single-source escape hatch 嘅 2.0 上限,component = 2.0,heat = 0.40 × 2.0 = **0.80**。
- 呢單「上傳緊 `.git` 歷史去阿里雲」嘅私隱風波,加上一份坦白到罕見嘅 `NOTICE.md`,同上個月 xAI
  Grok Build 都出現過類似「coding agent 靜靜上傳成個 workspace」嘅事故,係 coding-agent 呢個
  category 一個值得持續留意嘅風險模式(agent 需要廣泛檔案存取,先天就同私隱難以兩全)。
- SkillsMP 第三方鏡像有個 `zcode-delegate` skill 顯示 45,632★（呢個係鏡像自己嘅 star 數,唔係
  官方 GitHub star,只作旁證,唔計入 gate)。

## Source

- https://github.com/zai-org/ZCode （GitHub API,透過 mcp__github__search_repositories）
- https://runtimewire.com/article/zai-open-sources-zcode-security-remediation-git-history-upload
- https://www.cryptopolitan.com/z-ai-zcode-tool-uploaded-local-files/
- Reader used: Exa web_fetch_exa（README + NOTICE.md via raw.githubusercontent.com）+ GitHub connector
  （repo metadata）+ fxtwitter API（X 互動數字核實,未達門檻）

## Related

- [[../hot-list/2026-W39|hot-list/2026-W39]]
