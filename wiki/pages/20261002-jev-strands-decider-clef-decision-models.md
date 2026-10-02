---
title: "Jev 爆紅後 Strands Decider、Clef 接連登場，決策模型正走出哪些不同路線？"
slug: 20261002-jev-strands-decider-clef-decision-models
type: article
status: draft
source_url: "https://techorange.com/2026/10/02/ai-jev-decisions-api-strands-decider-clef"
source_platform: web
author: "廖紹伶"
published: "2026-10-02"
captured_at: "2026-10-02T12:00:00Z"
captured_by: "routine:capture-link"
canonical_id: "url:bfae13dd06651cbb844828503010c2ffce0a1099"
engagement: ""
tags: [topic/model-comparison, jev, typesafe, decision-model, strands-decider, aws, cloudflare, clef, openai, decisions-api, agent-tooling, llm-routing]
related: []
needs_manual_text: false
---

## 摘要

TypeSafe 9 月中推出 Jev 後，「決策模型」迅速成為 AI 領域新熱點，OpenAI、AWS、Cloudflare 在不到三週內相繼發布 Decisions API、Strands Decider 2B 與 Clef。決策模型的核心邏輯是：對於答案範圍明確的判斷（工具選擇、路由、操作檢查），讓大型語言模型逐字生成回答既耗時又昂貴，直接對候選答案評分則更高效。AWS 的 Strands Decider 2B 押注小型化（20 億參數）與可自行部署，全面開放權重、訓練資料與程式碼；Cloudflare 的 Clef 則押注多模態能力與企業強化學習微調，且直接相容 Jev 的 API 格式，顯示 Jev 的介面設計正在成為事實標準。市場上已出現 Laya、Kev、Bespoke Nimble 9B 等十數個類似模型，設計方向開始從參數大小、架構與部署方式分化。核心問題仍在於哪些 AI 代理工作真正值得從大型語言模型拆出來，以及專門模型能否同時兼顧延遲、成本與判斷品質。

## Key facts

- **Jev (TypeSafe)**: launched 2026-09-15; reads current state + predefined question, returns option scores and calibrated probabilities; no autoregressive text generation
- **OpenAI Decisions API**: launched 2026-09-29 at DevDay; uses OpenAI Luna model; classify text/images, route requests, pick next agent action from finite option sets
- **AWS Strands Decider 2B**: launched 2026-10-01; 2B params; based on Qwen3.5-2B (Alibaba); autoregressive decoder removed, replaced with direct candidate scoring; runs on CPU, GPU, or consumer PC; fully open: weights + code + training data + methodology
- **Cloudflare Clef / Clef-flash**: launched 2026-10-01; based on larger Qwen series; multimodal (text, images, video); longer context; deployed on Workers AI; supports RL fine-tuning service; Jev API-compatible; Clef-flash ~41 GB VRAM, full Clef ~85 GB VRAM; open weights only (training data not released)
- **Other models in the ecosystem**: Laya (421M params), Kev (multiple sizes), Bespoke Nimble 9B, Mapika decider, FLock this-that-model
- **CLM-8B (Stanford + NVIDIA)**: separates state and candidate action processing, enabling KV-cache pre-computation for repeated action sets to cut agent decision costs
- **Development cost**: small decision models reported in hundreds to thousands of USD range (per Marc Brooker, AWS Distinguished Engineer)
- **Use-case boundary**: decision models handle narrow-range judgments (tool selection, routing, operation checks); generation, coding, complex reasoning remain for full LLMs

## 點解值得留意

- Clef 直接相容 Jev 的 API 格式，意味著 Jev 的輸入/問題/機率輸出介面正在成為事實標準，vault 中的 `judging-with-jev` skill 的邏輯可能無需修改即可遷移到其他模型
- AWS Strands Decider 的全開放路線（權重 + 訓練資料 + 代碼）使決策層本地部署成本大幅降低，適合不願每次判斷都呼叫外部雲端 API 的私有部署場景
- 模型開發成本數百至數千美元，整個生態快速擴張，對 vault 中現有的 Jev 相關 skill（fast-jev-compaction、jev-seo-geo-audit）提供了更廣的市場背景與替代方案參考
- 決策模型的真正挑戰在於速度、準確率、機率校準與通用理解四者的平衡，這是評估是否在 Josep 的 agent 流程中引入此類模型的核心考量框架

## Source

- **Link**: https://techorange.com/2026/10/02/ai-jev-decisions-api-strands-decider-clef
- **Author**: 廖紹伶
- **Published**: 2026-10-02
- **Engagement**: (not shown)
- **Reader**: exa (web_fetch_exa, maxCharacters=50000)

## Related

- [[../pages/20261002-what-is-jev-system-one-ai-model|What Is Jev? The AI Model That Doesn't Generate Text]]
- [[../pages/20260920-fast-jev-compaction|fast-jev-compaction]]
- [[../pages/20260925-jev-seo-geo-audit-cost-down-90|Jev SEO/GEO Audit Cost Down 90%]]
- [[../pages/20260928-claude-code-fable-advisor-jev-tree|Claude Code Fable Advisor Jev Tree]]
- [[../../skills/judging-with-jev/SKILL|skill: judging-with-jev]]
