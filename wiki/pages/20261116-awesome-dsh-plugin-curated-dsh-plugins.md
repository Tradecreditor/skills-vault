---
title: "awesome-dsh-plugin/awesome-dsh-plugin — Awesome DSH Plugin: curated list (and plugin-market index) of 11,000+ DeepSeek Harness plugins"
slug: 20261116-awesome-dsh-plugin-curated-dsh-plugins
type: repo
status: draft
source_url: "https://github.com/awesome-dsh-plugin/awesome-dsh-plugin"
source_platform: github
author: "awesome-dsh-plugin"
published: "2026-08-13"
captured_at: "2026-11-16T08:20:00Z"
captured_by: "routine:weekly-hot-list"
canonical_id: "github:awesome-dsh-plugin/awesome-dsh-plugin"
engagement: "stars=24837 forks=8617 (2026-11-16; 23912 in the 2026-11-09 snapshot, +923 in 7 days)"
tags: [hot-list, 2026-W46, deepseek-harness, dsh, dsh-plugin, awesome-list, coding-agents, agent-harness, plugin-market]
related: [hot-list/2026-W46, 20261026-deepseek-harness-everything-is-a-plugin, 20261109-dsh-go-android-client-for-deepseek-harness]
needs_manual_text: false
---

## 摘要

Awesome DSH Plugin 係 DeepSeek Harness（dsh）社群插件嘅精選清單：收錄嘅插件要宣告 `dsh.bundle` manifest、可以用 `dsh plugin add` 安裝，分類涵蓋 agent 架構、UI、用量計費、主題、模型供應商、記憶、工具、瀏覽器等，2026-11-16 抓取時已有 11,332 個條目。份清單同時係一個插件市場 index：dsh 0.2.1 以上可以喺 Plugins → Discover → Index sources 加入佢經 npm / jsDelivr 發佈嘅 `index.json`，亦推薦配合 dsh-market 一鍵安裝。README 明確警告：插件會用你嘅權限跑第三方代碼，上榜唔等於安全審查。

## Key facts

- **What**: an awesome-list (CC0-1.0) of community DeepSeek Harness plugins, English and Chinese READMEs, website awesome-dsh-plugin.com. Listing bar: installs with `dsh plugin add`, does what its one-line description says, right category, maintained; it explicitly does not rank or judge quality.
- **Use as a market index**: on dsh 0.2.1+, Plugins → Discover → Index sources → add `https://cdn.jsdelivr.net/npm/dsh-plugin-catalog/index.json`. Or install the market UI with `dsh plugin --profile web add dshmarket`, or let the agent search with `dsh plugin --profile web add dsh-find-plugin`.
- **Warning** (README): installing a plugin runs third-party code with your own permissions; tool approvals do not sandbox plugin code; being listed is not a security review.
- **Numbers**: 24,837 stars / 8,617 forks on 2026-11-16, created 2026-08-13; 23,912 in the 2026-11-09 snapshot, so +923 in 7 days. It qualifies on the new-repo total alone (24,837 / 10,000 = 2.48, capped at 2.0 → heat 0.80) and takes the third slot on the tie-break among 0.80 items (see the report). 11,332 list entries in the README fetched 2026-11-16.

## 點解值得留意

- 2026-W46 hot list 第三名（heat 0.80，GitHub 單平台，只靠新 repo 總星數），詳見 [[hot-list/2026-W46|hot-list/2026-W46]]。佢今個星期實測只多咗 923 star，入選係因為規則（0.80 同分，排喺佢前面嗰兩個已經佔咗位），唔係因為今個星期特別熱。
- dsh 插件生態已經大到一萬幾個插件，同 W43 嘅 DeepSeek Harness、W44 嘅 dsh-superagent、W45 嘅 DSH Go 係同一條線；想喺 dsh 搵插件，用呢份清單或 dsh-market 比自己搜 GitHub 快。
- 一萬個插件冇人逐個做過安全審查，裝之前要自己睇 source。

## Source

- https://github.com/awesome-dsh-plugin/awesome-dsh-plugin — awesome-dsh-plugin — created 2026-08-13
- Reader: raw.githubusercontent.com README.md (curl), GitHub search API (`gh api`) for counts. Raw text in `raw/20261116-awesome-dsh-plugin-curated-dsh-plugins.md`: verbatim except the 4 MB plugin list itself (README lines 79–11479), which a capture note in the file names with the full file's sha256.

## Related

- [[hot-list/2026-W46]]
- [[pages/20261026-deepseek-harness-everything-is-a-plugin]]: the harness these plugins extend (W43 winner)
- [[pages/20261109-dsh-go-android-client-for-deepseek-harness]]: Android client for the same harness (W45 winner)
- [[pages/20261102-dsh-superagent-proactive-coding-agent]]: another dsh bundle (W44 winner)
