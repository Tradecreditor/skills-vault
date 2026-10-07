---
title: "AI 評估：用可重複測試驗收 AI（Sean Liu 轉述 Sergii Makarevych）"
slug: 20261006-ai-evals-repeatable-tests-sean-liu
type: post
status: draft
source_url: "https://www.facebook.com/638368594/posts/10163515237828595"
source_platform: facebook
author: "Sean Liu"
published: "2026-10-06"
captured_at: "2026-10-07T00:00:00Z"
captured_by: "routine:capture-link"
canonical_id: "facebook:10163515237828595"
engagement: "reactions=9 shares=1"
tags: [topic/agent-tooling, ai-evaluation, evals, llm-as-judge, test-cases]
related: []
needs_manual_text: false
---

## 摘要
貼文轉述 Sergii Makarevych 的原文，指 AI 評估核心是用可重複執行的測試，確認系統有否完成工作，以及每次修改後變好定變差。展示時成功一次不代表日常可靠。做法：整理貼近實況同過往失敗嘅測試案例、寫明合格條件、留一部分案例驗收用；先由人睇回答歸納錯誤類型，再設計評分。用 AI 評分要驗證評分者本身：客服例子中人工判 26 則不合格，AI 評分者只抓到 10 則。

## Key facts
- Test cases: realistic, include past failures and edge cases; each has explicit pass conditions (required facts, source documents, outcome); hold out some cases for acceptance only.
- Read outputs by hand first and list real failure modes (missing info, unsupported claims, wrong document retrieved, question not answered) before building automated graders.
- Format/number checks via code; faithfulness to documents needs a meaning-aware (LLM) grader given the documents as evidence.
- Validate the grader: in the small support example humans failed 26 answers, the AI grader caught only 10.
- Compare versions on the same cases, report pass rate with uncertainty, and see which cases improved or regressed (equal averages can hide both).
- RAG: score retrieval and answering separately. Agents: check the task was actually done and rules followed; repeat runs (once-in-N vs every-time reliability); cost per correct completion.
- Public leaderboards only shortlist models; validate on your own data. Evaluate before launch, after every change, and by sampling in production.
- Owner metrics: pass rate + uncertainty, grader/human agreement, smallest detectable change, how many cases the latest change broke.

## 點解值得留意
- 可直接用於 skill 審核同 agent 輸出驗收：held-out 案例、grader 同人工對照。
- 同 [[20260929-rubric-data-semiconductor-packaging-ai-checks|Rubric Data]] 一脈相承（評分規準式驗收）。
- 原文未見，只係二手轉述；數字（26 / 10）未經核實。

## Source
- https://www.facebook.com/638368594/posts/10163515237828595 — Sean Liu, ~2026-10-06, reactions=9 shares=1; reader: jina. 原文作者 Sergii Makarevych，連結未提供。

## Related
- [[20260929-rubric-data-semiconductor-packaging-ai-checks|Rubric Data]]
