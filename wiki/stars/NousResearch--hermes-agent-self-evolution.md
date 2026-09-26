---
title: "hermes-agent-self-evolution"
slug: NousResearch--hermes-agent-self-evolution
type: repo
status: draft
source_url: "https://github.com/NousResearch/hermes-agent-self-evolution"
source_platform: github
author: "Nous Research"
published: "2026-03-09"
captured_at: "2026-09-20T00:00:00Z"
captured_by: "routine:github-stars-sync"
canonical_id: "github:NousResearch/hermes-agent-self-evolution"
engagement: "stars=5380 forks=637"
tags: [hermes, agent, ai, dspy, gepa, self-improvement]
related: [openai--codex-plugin-cc, Fission-AI--OpenSpec, pages/20260923-promptfoo, OWASP--secure-coding-practices-quick-reference-guide]
needs_manual_text: false
---

## 摘要
用 DSPy 加 GEPA（Genetic-Pareto Prompt Evolution）自動演化 Hermes Agent 嘅 skill 檔案、工具描述、system prompt 同程式碼。核心思路係：讀現有 skill → 產生評估資料集 → GEPA 睇住實際執行軌跡去理解「點解會失敗」而唔係淨係知道「失敗咗」→ 提出針對性變體 → 評分 → 最好嗰個開 PR。唔使 GPU，全程靠 API 呼叫，一次優化大約 US$2–10。每個演化出嚟嘅版本都要過五道關卡：完整測試、體積上限、快取相容、語義冇偏離、真人審 PR——永遠唔會直接 commit。
## Key facts
- Language: Python
- License: (Unknown)
- Created: 2026-03-09
- Last pushed: 2026-06-17
- Stars: 5,380
- Forks: 637
- Tools: DSPy, GEPA
- Focus: Self-evolution, optimization

## 點解值得留意
呢個係「版本 → 評分 → 下一版」呢條迴路嘅現成實作，同任何 prompt 管理系統嘅核心價值完全對口。而家 Phase 1（skill 檔案）已完成，Phase 2–5（工具描述、system prompt、工具程式碼、持續改進迴路）仲係規劃中，即係啱睇架構多過即刻攞嚟用。
## Source
GitHub repository: https://github.com/NousResearch/hermes-agent-self-evolution
Author: Nous Research
Captured: 2026-09-20

## Related

- [[openai--codex-plugin-cc|codex-plugin-cc]] — 兩者都係喺 agent 產出之後加一層自動審查/演化嘅迴路。
- [[Fission-AI--OpenSpec|OpenSpec]] — 都想將「點解會失敗/點解要咁做」講清楚先落手改。
- [[../pages/20260923-promptfoo|promptfoo]] — 演化流程要靠評估資料集打分，同 promptfoo 嘅 LLM eval 思路直接對應。
- [[OWASP--secure-coding-practices-quick-reference-guide|secure-coding-practices-quick-reference-guide]] — 兩者都用「過五關」式嘅檢查清單先俾改動通過。
