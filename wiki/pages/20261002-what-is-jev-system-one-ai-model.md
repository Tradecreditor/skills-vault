---
title: "What Is Jev? The AI Model That Doesn't Generate Text"
slug: 20261002-what-is-jev-system-one-ai-model
type: video
status: draft
source_url: "https://www.youtube.com/watch?v=YGgNBcIgI4s"
source_platform: youtube
author: "IBM Technology"
published: ""
captured_at: "2026-10-02T00:00:00Z"
captured_by: "routine:capture-link"
canonical_id: "youtube:YGgNBcIgI4s"
engagement: ""
tags: [topic/agent-tooling, jev, typesafe, system-one, classification, calibrated-probabilities, llm-routing, rlcd]
related: []
needs_manual_text: false
---

## 摘要

Jev 是 TypeSafe 推出的「系統一」（System 1）AI 模型——快速、自動，完全不生成任何文字。它的運作方式是：接收「狀態」資料加上一組預設選項，輸出每個選項的機率值，讓軟體根據閾值做路由決策，速度與成本均遠優於呼叫 LLM。Jev 採用 RLCD（Reinforcement Learning for Calibrated Decisions）訓練，使輸出的機率值與實際正確率真正吻合，解決了 RLHF 訓練下模型「過度自信」的問題。典型應用包括客服郵件分類路由、聊天機器人護欄（guardrail）、資料庫逐行標記等不需要生成回答的判斷任務。Jev 並非要取代 LLM，而是與 LLM 協作：Jev 做快速系統一判斷，LLM 做慢速系統二生成，正如 Kahneman 描述人類思維的雙系統架構。名稱源自 1865 年 Jevons Paradox：效率提升往往帶來更大總消耗，暗示當系統一模型夠便宜時，它將進入 LLM 過去太貴而無法部署的所有場景。

## Key facts

- **What it is**: "system one" AI model by TypeSafe — no text generation, outputs calibrated probability scores per option
- **Inputs**: `state` (the data to reason about, e.g. a support email + customer charge history) + questions defined as typed lists of options
- **Question types**:
  - `bool` — yes/no → single probability score (e.g. `refund: 0.9`)
  - `choice` — pick one from a list → probability per option (e.g. `team: {billing: 0.85, technical: 0.10, sales: 0.05}`)
  - `scale` — score on a range (e.g. `urgency: critical`)
- **All questions sent in one request; all answers returned at once** — faster and cheaper than streaming JSON tokens from an LLM
- **Training**: RLCD (Reinforcement Learning for Calibrated Decisions) — model rewarded when predicted probabilities match actual outcome rates; produces a truly calibrated model (80% confidence → correct ~80% of the time)
- **vs RLHF**: RLHF trains models to sound confident (rewarded by human preference for confident answers); RLCD rewards probability accuracy, not confidence
- **Threshold pattern**: `prob > 0.9` → auto-route; `0.1–0.9` → human review; `prob < 0.1` → ignore
- **Limitations**: text-only input; poor at math and counting; susceptible to prompt injection in input data
- **Designed to complement LLMs**, not replace them: Jev handles fast classification steps in a workflow, LLM handles generation steps
- **Use cases**: customer support routing, chatbot guardrails (jailbreak detection), log-file tagging, per-row DB classification at scale

## 點解值得留意

- 機率輸出讓 agent 工作流擁有真正的「信心閾值」邏輯，避免 LLM structured output 的過度自信陷阱，可應用於 vault-capture 路由、SEO agent 的關鍵字分類等步驟
- 「每行 log / 每條 DB record 都跑判斷」的場景對 LLM 來說太貴，Jev 的速度與成本讓這類大規模分類成為可行
- RLCD 訓練概念與 TypeSafe 的架構細節值得持續追蹤，目前未發表論文
- IBM Technology 發布解說影片，代表 Jev 已進入主流開發者社群視野，與 `fast-jev-compaction` 插件一起印證 Jev 生態系正在形成

## Source

- Video: https://www.youtube.com/watch?v=YGgNBcIgI4s
- Author: IBM Technology (@IBMTechnology)
- Published: unknown (captured 2026-10-02)
- Reader: exa

## Related

- [[../../wiki/pages/20260920-fast-jev-compaction|fast-jev-compaction: Jev-scored context compaction for Claude Code]]
- [[../../wiki/pages/20260928-claude-code-fable-advisor-jev-tree|Claude Code: Fable 5.1 Advisor + Jev Routing Tree]]
- [[../../skills/judging-with-jev/SKILL|skill: judging-with-jev]] — how the vault asks Jev typed questions in its own Routines; this video's threshold and prompt-injection points are folded into its rules.
