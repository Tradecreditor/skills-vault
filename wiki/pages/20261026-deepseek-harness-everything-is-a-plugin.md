---
title: "deepseek-ai/deepseek-harness — DeepSeek Harness (dsh): open-source agent harness where everything is a plugin"
slug: 20261026-deepseek-harness-everything-is-a-plugin
type: repo
status: draft
source_url: "https://github.com/deepseek-ai/deepseek-harness"
source_platform: github
author: "DeepSeek AI (deepseek-ai)"
published: "2026-08-13"
captured_at: "2026-10-26T08:20:00Z"
captured_by: "routine:weekly-hot-list"
canonical_id: "github:deepseek-ai/deepseek-harness"
engagement: "stars=261866 forks=31651 (+8093 stars since 2026-10-19 snapshot)"
tags: [hot-list, 2026-W43, agent-harness, coding-agents, deepseek, dsh, dsh-plugin, cordis, plugins]
related: [hot-list/2026-W43]
needs_manual_text: false
---

## 摘要

DeepSeek Harness（指令 `dsh`）係 DeepSeek AI 開源嘅 agent harness（MIT），即係將語言模型變成可以讀檔、行指令、做多步任務嘅 agent 嘅嗰層 runtime。佢嘅設計係「everything is a plugin」，建基於 Cordis 框架，連桌面同 Web UI 本身都係插件，所以身邊已經長出一整個 `dsh-plugin` 生態（上星期第一名 dsh-our-free-model 就係其中一個）。一句 `npx @deepseek-ai/dsh web` 就喺本機 3080 port 開 Web UI。官方講明仍然係 developer preview，會有唔兼容嘅改動，行之前要睇 SAFETY.md。佢係 2026-W43 hot list 第一名：一星期 +8,093 stars，W42 已經排喺 Watch 第一。

## Key facts

- **Run**: `npx @deepseek-ai/dsh web` (needs Node.js) starts the Web UI at `http://127.0.0.1:3080`; `--no-open` runs the server without opening a browser. From source: `git clone`, `pnpm install`, `pnpm run build`, `pnpm dsh web`.
- **Architecture**: everything-is-a-plugin, powered by Cordis (paper *A Programming Paradigm for Spatiotemporal Composability*, arXiv 2608.25512). Plugin authors tag their repos `dsh-plugin` for discovery; desktop builds (`anywhere-labs/dsh-desktop` 33,228 stars, `dataelement/dsh-desktop` 16,959) and the `awesome-dsh-plugin` list (20,784) are themselves community plugins.
- **Status**: developer preview, "THERE WILL BE COMPATIBILITY-BREAKING CHANGES"; read `SAFETY.md` first. MIT licence, third-party notices in `THIRD_PARTY_NOTICES.md`.
- **Numbers (2026-10-26, GitHub search API)**: 261,866 stars / 31,651 forks, created 2026-08-13 (74 days before the window started); 253,773 in the 2026-10-19 snapshot, so **+8,093 in 7 days**. It also clears the new-repo gate on its total.
- **Social**: no in-window post about it was found. @DeepSeekHarness has posted three times in total (its 0.2.1 release post on 2026-10-17, 4,591 likes, was last week); @deepseek_ai's posts in the window were about DeepInfer, a separate inference framework.
- **Registries**: SkillsMP lists the repo's own `dsh-*` agent skills (`dsh-translate-docs`, `dsh-client-ui-ux`, ...) and a third-party `deepseek-harness-setup` skill; no install counts.

## 點解值得留意

- 2026-W43 hot list 第一名（heat 0.80，GitHub 單平台）。六個 0.80 同分項目入面，佢有最大嘅實測一週增幅，詳見 [[hot-list/2026-W43|hot-list/2026-W43]]。
- 星數大得離譜（26 萬），而且周邊插件 repo（dsh-desktop、awesome-dsh-plugin、dsh-our-free-model）都好快爆星，部分插件仲要你 star 先解鎖功能，所以星數唔好當質素指標，當「生態熱度」睇。
- 對 Jeff 嚟講：佢同 Claude Code / Codex 屬同一類工具，社群報道話可以將 Claude Code 同 Codex 當 subagent 掛入去。想試就喺獨立資料夾行 `npx`，唔好喺 Obsidian vault 入面行；preview 版本隨時改 API。

## Source

- https://github.com/deepseek-ai/deepseek-harness — DeepSeek AI — created 2026-08-13
- Reader: raw.githubusercontent.com README (curl) + GitHub search API (connector) for counts; fxtwitter for the X check. Raw text in `raw/20261026-deepseek-harness-everything-is-a-plugin.md`.

## Related

- [[hot-list/2026-W43]]
- [[pages/20261019-dsh-our-free-model-plugin]]: last week's winner, a dsh plugin that adds free model lanes
- [[pages/20261002-zcode-zai-harness]]: Z.ai's coding agent harness, the same category from another lab
- [[pages/20260924-model-vs-harness-claude-code-explained]]: what a harness is, as opposed to the model
