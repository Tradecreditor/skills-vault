---
title: "Rubric Data：封裝廠用評分規準資料逐項驗收 AI 成果"
slug: 20260929-rubric-data-semiconductor-packaging-ai-checks
type: post
status: draft
source_url: "https://www.facebook.com/share/1DtbvyMo4g/"
source_platform: facebook
author: "Sean Liu"
published: "2026-09-29"
captured_at: "2026-10-04T21:20:46Z"
captured_by: "claude-code-cloud"
canonical_id: "url:10ccd8e36a71094c4f7d7294d2eccc117d132dca"
engagement: "reactions=17 shares=2"
tags: [topic/agent-tooling, rubric-data, ai-evaluation, evals, semiconductor, manufacturing, quality]
related: [20260923-promptfoo, skills/judging-with-jev]
needs_manual_text: false
---

## 摘要
Sean Liu 喺 Facebook 發文介紹「Rubric Data」：將「點樣先算做啱」整理成可以逐項檢查嘅評分規準資料，令企業有根據去驗收 AI 嘅工作成果。以半導體封裝廠為例，即係把製程同品保主管審查異常分析、客訴報告或批次處置建議時會睇嘅條件、會追問嘅證據，以及不可接受嘅錯誤清楚記低，之後 AI 交出嘅良率分析、打線（#打線）拉力測試異常分析等，就可以逐項判定有冇達標。作者強調評分規準本身都要由製程同品保專家確認、核對案例並隨規格更新；引用錯誤規格、捏造檢測結果或繞過放行條件，應列為直接不合格項目。佢認為呢類資料可以將資深工程師嘅判斷累積成可交接嘅組織資產，亦方便比較或更換不同 AI 系統。全文係概念說明，冇附工具、repo 或實際數據，結尾只寫「說是這麼說，但...就之後講吧」。

## Key facts
- Personal Facebook post by Sean Liu. The page showed "5 days ago" when read on 2026-10-04, so about 2026-09-29. Counts shown: 17 reactions, 2 shares; comments not shown. One image attached (not described in the text).
- Definition (author's claim): Rubric Data turns "what counts as correct" into item-by-item checkable scoring criteria so a company has a basis to accept AI work, instead of judging only on fluent or professional-sounding text.
- Packaging-fab framing: record the conditions, the evidence reviewers ask for and the unacceptable errors that process and QA managers apply when reviewing anomaly analyses, customer-complaint reports or lot-disposition recommendations.
- Each item needs a judging condition and a scoring method; for a fab it also records applicable product, spec version and the basis for the judgement.
- Yield-analysis example: check input quantity, passing quantity and statistics period separately, plus whether the anomaly conclusion is supported by data, each with a clear pass condition.
- Optional calibration set: engineer-graded cases with the reasons for each score, so later graders know what counts as complete and which omissions must be sent back.
- Wire-bond (#打線) pull-test anomaly example: the rubric can require checking the test method, identifying the failure mode, comparing normal and abnormal lots, and proposing checks that confirm or exclude causes. A suggestion such as "raise bonding energy" is judged on whether those checks were done.
- Insufficient data should still pass if the AI says clearly which evidence is missing and what to check next, so the rubric does not reward guessing an answer.
- Rubric quality control: a wrong rubric keeps passing wrong answers; one item may not transfer across customers, package types or spec versions, so process and QA experts confirm scope, verify cases and update on spec changes.
- Auto-fail items (cannot be offset by other scores): citing a wrong spec, fabricating test results, bypassing required release conditions. The author adds that actual release still follows the plant's existing authority and sign-off process.
- Claimed value: turns senior engineers' judgement into a handover-able, checkable, revisable organisational asset; allows comparing different AIs and checking after a system update that nothing previously caught is now missed; the plant keeps its product conditions, evidence requirements and quality standards when it changes AI systems.
- No tool, repo, template or sample data is given, and no numbers beyond the example items; the post ends unfinished ("不過...說是這麼說，但...就之後講吧").

## 點解值得留意
- 同 Jeff 評估 agent 輸出質素嘅工作好貼身：「條件、必要證據、不可接受錯誤」三件頭，可以直接當作幫 HK 中小企客戶寫 AI 交付驗收清單嘅框架，唔使淨係靠「睇落專業」去評。
- 「證據不足時講明缺咩都算合格」同「捏造規格／檢測結果＝直接不合格（auto-fail）」兩個設計，可以抄入 Claude Code skill 或 agent 輸出嘅 checker，防止 AI 為求有答案而作嘢。
- 概念上同 vault 已有嘅 evals（promptfoo assertions）同 Jev 嘅 rubric `score` 問題相通，之後可以試將某個客戶流程寫成 rubric 再自動打分；但呢篇只係概念文，冇範例資料，封裝廠例子要由領域專家驗證，唔好當成已證實嘅做法。

## Source
- https://www.facebook.com/share/1DtbvyMo4g/ — Sean Liu, personal post (profile https://www.facebook.com/modeerf). Published date is not shown; the page said "5 days ago" when read on 2026-10-04, so `published` is the estimate 2026-09-29. Engagement as shown on the page: "All reactions: 17", "2 shares" (comments not shown).
- `canonical_id` is `url:<sha1>` of the share URL because the share link did not resolve to a numeric post id (the permalink carries only a `pfbid…` token, recorded in `raw/`).
- Reader: Jina Reader (`r.jina.ai`), full post text returned on this attempt (an earlier attempt had returned only a truncated title behind a CAPTCHA warning). Exa was not used. No Supadata (text post).
- Verbatim text in `raw/20260929-rubric-data-semiconductor-packaging-ai-checks.md`.

## Related
- [[../pages/20260923-promptfoo|promptfoo: LLM Evals & Red Teaming]]
- [[../../skills/judging-with-jev/SKILL|skill: judging-with-jev]]
