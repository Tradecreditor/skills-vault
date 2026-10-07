---
title: "Decision Models After Jev: Strands Decider, Clef and Other Routes"
slug: 20261002-decision-models-strands-decider-clef-jev
type: article
status: draft
source_url: "https://techorange.com/2026/10/02/ai-jev-decisions-api-strands-decider-clef/"
source_platform: web
author: "廖紹伶 (TechOrange 科技報橘)"
published: "2026-10-02"
captured_at: "2026-10-04T21:18:29Z"
captured_by: "claude-code-cloud"
canonical_id: "url:7e4e3966fba23661505e6d512661a5fa4d9ccc90"
engagement: "n/a"
tags: [topic/model-comparison, decision-models, jev, typesafe, openai-decisions-api, strands-decider, clef, cloudflare, aws]
related: [20261002-what-is-jev-system-one-ai-model, skills/judging-with-jev, 20260925-jev-seo-geo-audit-cost-down-90]
needs_manual_text: false
---

## 摘要

TypeSafe 喺 9 月中推出 Jev 後，「決策模型」（直接為預設答案集評分、唔逐字生成文字）迅速成為熱點。呢篇科技報橘文章整理不到三週內嘅主要跟進者：OpenAI 在 DevDay（9/29）推出以 Luna 模型驅動、託管式嘅 Decisions API；AWS 在 10/1 推出基於 Qwen3.5-2B、約 20 億參數、權重程式碼數據全開放嘅 Strands Decider 2B；Cloudflare 同日推出走多模態、Workers AI 託管、可做強化學習微調而且相容 Jev API 嘅 Clef 同 Clef-flash。文章亦點出 Laya、Kev、Bespoke Nimble 9B、史丹佛與 NVIDIA 嘅 CLM-8B 等更多路線，並引述 TechCrunch 指市場已有數十個類似模型，各自嘅獨立價值有待檢視。文章主要轉述 VentureBeat、TechCrunch 同 The Register 嘅報道，冇獨立測試，所以只能當格局地圖。

## Key facts

- Concept (article, citing VentureBeat): for questions with a fixed answer set ("should this tool run?", "which path should this request take?"), having an LLM generate an explanation first adds time and cost. A decision model scores the pre-allowed answers directly, so it fits gating, routing and tool-call checks around AI agents; writing, coding and complex reasoning stay with fuller generative models.
- Jev (TypeSafe, 9/15): reads the current state plus predefined questions and returns an option, a score or a yes/no judgment, plus a probability per answer, instead of generating text token by token.
- Comparison, as reported in the article (blank means the article does not say):

| Model | Maker | Date | Size | Open? | Hosting | Notable |
|---|---|---|---|---|---|---|
| Jev | TypeSafe | 9/15 | not stated | not stated | not stated | The template: state + predefined question in; option, score or yes/no + per-answer probabilities out |
| Decisions API | OpenAI | 9/29 (DevDay) | runs on OpenAI's "Luna" model | not stated | OpenAI hosted API | Not a standalone decision model; developer defines the question and finite options; works from text or images to classify, route requests or pick an agent's next action |
| Strands Decider 2B | AWS | 10/1 | about 2B params (Qwen3.5-2B base, text-generation part removed) | Weights, code, training data and method published | Self-host on CPU, GPU or PC | VentureBeat: main difference is openness, self-hosting and reproducibility, not proven better accuracy than Jev |
| Clef / Clef-flash | Cloudflare | 10/1 | larger Qwen-series bases; self-host about 85 GB (Clef) / 41 GB (Clef-flash) VRAM per The Register | Open-weight, not fully open-source (full training data not published, per The Register) | Workers AI, or self-host | Text, image and video input, longer inputs, RL fine-tuning service, compatible with Jev's API |
| Laya | not stated | weeks after Jev | 421M params | not stated | not stated | Smallest model named |
| Kev | not stated | weeks after Jev | offered in several sizes | not stated | not stated | |
| Bespoke Nimble 9B | not stated | weeks after Jev | 9B (from name) | not stated | not stated | |
| Mapika decider, FLock this-that-model | not stated | weeks after Jev | not stated | not stated | not stated | Named only |
| CLM-8B | Stanford + NVIDIA | not stated | "8B" in name | not stated | not stated | Architecture separates current state from candidate actions so repeated actions can be precomputed, to cut the cost of repeatedly choosing among the same tools |

- Strands Decider demo (AWS): placed before an agent calls a tool. When an agent about to look up weather guesses a city although the user gave no location, Decider judges whether the parameter has grounding and whether now is the right time, and the system then allows, blocks or asks for confirmation.
- Marc Brooker (AWS distinguished engineer), per the article citing TechCrunch: AWS found the need while discussing agent workflows with customers, since many steps do not need a full LLM's capability and cost. The article also reports him saying the real technical challenge is balancing speed, accuracy, probability calibration and general understanding, and that these small models may cost only hundreds to thousands of dollars to develop, so he does not assume frontier labs will dominate.
- Clef is directly compatible with Jev's API: applications using Jev need not rewrite the call interface to switch. The article reads this as Jev's input, question and probability-output format being reused by others.
- TechCrunch (per the article): dozens of Jev-like models have appeared since launch, which raises the question of how much independent value each adds.
- Open question the article ends on: which agent jobs should really be split out of large LLMs, and whether the specialised models keep enough judgment quality while cutting latency and cost.
- Article's source list: Strands Agents blog (https://strandsagents.com/blog/introducing-strands-decider/), VentureBeat x2, TechCrunch x2 (2026-09-30 and 2026-10-01), The Register (2026-10-01). Links are in raw/; none were fetched.

## 點解值得留意

- Jeff 嘅 vault routines 已經用 Jev 做低成本判斷（見 judging-with-jev）。文章指 Clef 相容 Jev API，將來想加第二個引擎做 fallback 或對比，理論上唔使重寫呼叫介面；但呢點係文章轉述，真係切換前要自己試。
- 做 AI 顧問時，可以拎呢份清單做「gate / 路由類判斷未必要叫大模型」嘅選型表：想放喺自己環境、避免每次判斷都叫外部雲端模型，睇 Strands Decider 2B（CPU 都跑得）；想託管同要圖片或影片輸入，睇 Clef（Workers AI）；已經用 OpenAI 就睇 Decisions API。Clef 自行部署要約 41 至 85 GB VRAM，香港中小企多數唔現實。
- 呢篇係二手整理，冇 benchmark；VentureBeat 都話 Strands 未證明比 Jev 更準。轉用任何一款之前，應該用自己嘅分類或 gate 任務做小型 eval，唔好單憑呢份文章換模型。

## Source

- URL: https://techorange.com/2026/10/02/ai-jev-decisions-api-strands-decider-clef/
- Title (original): Jev 爆紅後 Strands Decider、Clef 接連登場，決策模型正走出哪些不同路線？
- Author: 廖紹伶 (TechOrange 科技報橘) · Published: 2026-10-02 (Jina Published Time 2026-10-02T17:13:19+08:00)
- Engagement: none shown
- Reader: Jina Reader (r.jina.ai)
- Not captured: images, site navigation, trending and related-article lists, footer. The article's six cited sources were listed in raw/ but not fetched. The article states it is open for partner reprint.

## Related

- [[../pages/20261002-what-is-jev-system-one-ai-model|What Is Jev? The AI Model That Doesn't Generate Text]] - explains Jev, the model that set the template for this wave.
- [[../../skills/judging-with-jev/SKILL|skill: judging-with-jev]] - how the vault asks Jev typed questions in its routines.
- [[../pages/20260925-jev-seo-geo-audit-cost-down-90|Jev cuts agent SEO/GEO audit-and-fix cost by 90%]] - a cost-reduction use case for Jev-style decisions.
