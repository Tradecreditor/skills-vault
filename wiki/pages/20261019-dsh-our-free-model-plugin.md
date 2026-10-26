---
title: "Ebony-Vinyl/dsh-our-free-model — DeepSeek Harness plugin with free model lanes and no API key"
slug: 20261019-dsh-our-free-model-plugin
type: repo
status: draft
source_url: "https://github.com/Ebony-Vinyl/dsh-our-free-model"
source_platform: github
author: "Ebony-Vinyl"
published: "2026-09-24"
captured_at: "2026-10-19T08:21:37Z"
captured_by: "routine:weekly-hot-list"
canonical_id: "github:Ebony-Vinyl/dsh-our-free-model"
engagement: "stars=26054 forks=564 (+15863 stars since 2026-10-12 snapshot)"
tags: [hot-list, 2026-W42, deepseek-harness, dsh-plugin, free-model, model-provider, openai-compatible, llm-gateway]
related: [hot-list/2026-W42]
needs_manual_text: false
---

## 摘要

dsh-our-free-model 係 DeepSeek Harness（dsh）嘅模型插件：裝咗之後唔使登入、註冊或者填 API Key，模型選擇器就會多咗 DeepSeek V4.1 Flash、Kimi K3 等「免費車道」模型。免費車道直連 OpenCode 嘅 Zen gateway 同 Kilo AI 嘅公共 gateway；2.0 之後再加十三個「白嫖」帳號渠道（CodeArts、CodeBuddy / WorkBuddy、Qoder、TRAE、Cline 等），連帳號池同每日積分領取。佢仲會開一個 OpenAI 兼容兼識講 Anthropic Messages 嘅本地 gateway，所以 Claude Code、Codex 都可以指住佢用，另外有降級鏈路由、工具輸出壓縮同本地用量看板。佢係 2026-W42 hot list 第一名：一星期 GitHub +15,863 stars，單平台入選。

## Key facts

- **Install** (README; do not use the npm package of the same name, which the author says is a third-party repack with modified files): `dsh plugin --profile web add /absolute/path/dsh-our-free-model`, then restart once. Directory sites also list `dsh plugin --profile web add github:Ebony-Vinyl/dsh-our-free-model`.
- **What it adds**: a free lane (OpenCode Zen gateway + Kilo AI free pool), an EAC "co-pay" lane on desktop hosts, 13 account channels, a bring-your-own-key aggregator (75+ providers), fallback chains (`combo:` virtual models), RTK tool-output compression, and a local gateway with `/v1/chat/completions`, `/v1/responses` and `POST /v1/messages` (Anthropic) on `127.0.0.1`.
- **Limits stated in the README**: "no usage cap" means no quota system, but the free lane rate-limits per session (429). The Kilo free pool says prompts may be logged by the upstream provider: do not send secrets or sensitive data.
- **Star mechanics**: the EAC lane unlocks only after the user signs in with GitHub **and stars the repo** (server-side check), and every settings page carries a Star button. Part of the star growth is therefore incentivised, not organic interest.
- **Numbers (2026-10-19)**: 26,054 stars / 564 forks; 10,191 in the 2026-10-12 snapshot, so **+15,863 in 7 days**. Created 2026-09-24, so it also clears the new-repo gate (25 days, >= 10,000). Jev `topical` 0.80. No in-window X or Threads post about it was found.

## 點解值得留意

- 2026-W42 hot list 第一名（heat 0.80，GitHub 單平台）。今個星期 0.80 嗰級有六個項目同分，按實測七日增幅排，佢最高，詳見 [[hot-list/2026-W42|hot-list/2026-W42]]。
- 呢個係 DeepSeek Harness 生態爆發嘅縮影：dsh 本體（deepseek-ai/deepseek-harness）已經 25 萬 stars，插件市場、目錄網站一個接一個出現。
- **唔建議喺 Jeff 嘅項目用**：免費車道同帳號渠道靠第三方 gateway 同各家廠商嘅免費額度，有服務條款風險，Kilo 池會記錄 prompt，EAC 渠道仲要 star 先用得。當新聞同趨勢睇就夠，唔好放 production 或者有客戶資料嘅工作。
- 同 [[pages/20261002-magpie-agent-model-switcher|magpie]]（同一班人關注嘅「agent 換模型」工具）係同一類需求。

## Source

- https://github.com/Ebony-Vinyl/dsh-our-free-model — Ebony-Vinyl — created 2026-09-24
- Reader: raw.githubusercontent.com README (curl; first 300 of 771 lines) + GitHub search API (connector) for counts. Raw text in `raw/20261019-dsh-our-free-model-plugin.md`.

## Related

- [[hot-list/2026-W42]]
- [[pages/20261002-magpie-agent-model-switcher]]: routes Codex / Claude Code to other models from the menu bar; same "any agent, any model" demand

## Notes

- also trending 2026-W43 (43,692 stars / 1,238 forks on 2026-10-26, +17,638 since 2026-10-19; GitHub search API; see [[hot-list/2026-W43]]). The star-to-unlock EAC lane noted above still applies, so read the number as incentivised.
