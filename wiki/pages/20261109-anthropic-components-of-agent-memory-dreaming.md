---
title: "Anthropic: The components of agent memory, and how dreaming lets Claude organize and correct it"
slug: 20261109-anthropic-components-of-agent-memory-dreaming
type: post
status: draft
source_url: "https://x.com/AnthropicAI/status/2118814753154064501"
source_platform: x
author: "@AnthropicAI"
published: "2026-11-06"
captured_at: "2026-11-09T08:20:00Z"
captured_by: "routine:weekly-hot-list"
canonical_id: "x:tweet:2118814753154064501"
engagement: "likes=13976 reposts=1289 views=1969091 replies=1012 bookmarks=12727"
tags: [topic/knowledge-mgmt, hot-list, 2026-W45, agent-memory, dreaming, llm-wiki, claude, managed-agents, anthropic]
related: [hot-list/2026-W45]
needs_manual_text: false
---

## 摘要

Anthropic 喺 2026-11-06 發佈 Engineering Blog〈The components of agent memory〉，解釋 Claude 點樣用「dreaming」（閒時重溫 session transcript）整理記憶、改正錯誤同更易搵返要用嘅嘢。文章用 CL-Bench、Pokémon Red、Stainless 內部文件同 Harvey LAB 做評估：新模型識判斷乜嘢值得記、應該話畀佢知記憶係做咩而唔係點樣記；dreaming 可以用 transcript 核對並改正錯嘅筆記、逐步建立同修剪 wiki（128 個 session 由 13% 升到 48%）、將重要筆記升到每次開 session 都載入嘅一層，同埋圍繞特定目標組織記憶。文中直接引用 Karpathy 嘅 LLM wiki 做法，同呢個 vault 嘅設計好相近。X 帖文 13,976 like、1,289 轉推、197 萬瀏覽，係 2026-W45 唯一過 X gate 嘅項目。

## Key facts

- **What**: an Anthropic Engineering Blog post (https://www.anthropic.com/research/components-of-agent-memory), announced on X on 2026-11-06. "Agent memory" = knowledge Claude gains from experience and keeps between sessions as readable context (not weights, not in-context learning).
- **Findings**: memory is a prediction of what future sessions need; newer models judge salience better (on Pokémon Red, Fable 5 kept nine files plus `global.md` and progressed much further than Sonnet 3.7's sprawling archive); tell the model what memory is for, not how to use it (a "record only failures" rule cut Opus 5's gain); steering helps older models most (prompting Sonnet 4.6 to read memory and test theories nearly doubled its CL-Bench score).
- **Dreaming**: checks notes against the original transcripts and corrects them (the Mt. Moon example); builds wiki representations incrementally (Stainless corpus, ~350,000 files / 420M tokens: 13% → 48% of graded criteria as dreaming scaled from 2 to 128 sessions); promotes notes to an always-loaded top layer (Claude Code auto memory loads only the first 200 lines / 25 KB of `MEMORY.md`); can be steered toward a goal (a contract-terms wiki first captured 41 of 57 facts because parallel agents overwrote a shared table).
- **Try it**: cookbooks for dreaming with Claude Managed Agents (platform.claude.com cookbook `managed-agents-cma-dreaming-with-a-dynamic-workflow`) and knowledge wikis (`anthropics/claude-quickstarts/managed-agents/knowledge-wiki`).
- **Numbers** (fxtwitter, 2026-11-09): 13,976 likes / 1,289 reposts / 1,969,091 views / 12,727 bookmarks. Clears all three X thresholds (2,000 / 500 / 1,000,000).

## 點解值得留意

- 2026-W45 hot list 第三名（heat 0.70，X 單平台），係今個星期唯一社交入選，詳見 [[hot-list/2026-W45|hot-list/2026-W45]]。
- 呢個 vault 本身就係一個 LLM wiki：文中「wiki + 搜尋」「細小嘅頂層 index」「用 transcript 核對筆記」都可以直接對照 `wiki/index.md`、`wiki/hot.md` 同 lint routine 嘅做法。
- 「話畀模型知記憶係做咩，唔好規定點記」對寫 CLAUDE.md、handoff.md 同 skill 都有參考價值。

## Source

- https://x.com/AnthropicAI/status/2118814753154064501 — @AnthropicAI — 2026-11-06
- Linked: https://www.anthropic.com/research/components-of-agent-memory
- Reader: api.fxtwitter.com for the post; `scripts/read-url.sh` (jina) for the blog post. Raw text in `raw/20261109-anthropic-components-of-agent-memory-dreaming.md`.

## Related

- [[hot-list/2026-W45]]
- [[pages/20261024-aiposthub-memhub-cross-tool-ai-memory]]: cross-tool shared memory for AI agents
