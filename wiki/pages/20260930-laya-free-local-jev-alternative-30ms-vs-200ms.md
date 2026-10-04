---
title: "Laya: free open-source local Jev alternative (~30 ms vs ~200 ms)"
slug: 20260930-laya-free-local-jev-alternative-30ms-vs-200ms
type: video
status: draft
source_url: "https://www.instagram.com/reel/Dd6P9YOB06z/"
source_platform: instagram
author: "nick_saraev"
published: "2026-09-30"
captured_at: "2026-10-04T21:18:42Z"
captured_by: "claude-code-cloud"
canonical_id: "instagram:Dd6P9YOB06z"
engagement: "likes=2.3K comments=2.5K"
tags: [topic/model-comparison, laya, jev, decision-models, fine-tuning, claude-code, open-source]
related: [20261002-what-is-jev-system-one-ai-model, 20260925-5-github-repos-43k-stars-week, 20260925-jev-seo-geo-audit-cost-down-90, 20260921-laya-pip-install-comment-fast-teaser, 20260920-jev-in-60-seconds-nate-herk-teaser, skills/judging-with-jev]
needs_manual_text: false
---

## 摘要
Nick Saraev（@nick_saraev）於 2026-09-30 的 reel（逐字稿約 164 字，說明文字另有較長的書面版）介紹 Laya，稱它是「Jev 的免費開源替代品」：一個可在本機執行的分類模型，據他所說回應約 30 毫秒，而 Jev 約 200 毫秒。他同時指出基礎模型並非開箱即用，需要針對自己的用途微調，並說借助 Claude Code「很輕易」就能做到，微調後準確度「甚至可以追平 Jev」，而且只需約十分之一的時間（這句只出現在口述）。「原裝引擎對整輛車」的比喻只出現在說明文字，影片口述沒有。完整設定指南要在留言區輸入「JEV」才領取，口述與說明文字都沒有 repo 連結、指令、授權或微調方法。語音辨識把 Laya 寫成「leia」，與說明文字及 #layaai 一致應讀作 Laya。以上速度與準確度說法全部是創作者自述，沒有基準測試佐證。

## Key facts
- Basis: the Supadata ASR transcript (lang en, mode=auto, 164 words, kept verbatim in `raw/20260930-laya-free-local-jev-alternative-30ms-vs-200ms.md`) plus the written caption (Jina). Everything below is Nick Saraev's own claim; no benchmark is cited.
- ASR name: the transcript writes "leia"; read it as Laya, as the caption and its hashtag #layaai spell it.
- Pitch (spoken): "someone just released a free open source version of jev and it's actually way faster and cheaper". Caption: "Someone just released a free and open source version of Jev, and it's actually way faster and cheaper. It's called Laya."
- What it is (spoken and caption): "a classifier model that you can run locally on your own computer" that "does the exact same job as jev".
- Speed claim (spoken): "takes only around 30 milliseconds to answer while jev takes closer to 200" (caption: "around 200"). No benchmark, hardware or batch size is given.
- Caveat (spoken): "the base model isn't good at everything out of the box so it needs to be fine-tuned and trained for your specific use case", which "you can do ... with the help of claude code really easily" (the caption says the same without "really easily"). Fine-tuning data, method and effort are not described.
- Accuracy and time claim (spoken only): "once you're done it can even match jev on accuracy except do it in a tenth of the time". The caption has only "it can even match Jev on accuracy". Note that 30 ms against 200 ms is about one seventh, so "a tenth" is loose rounding.
- Caption only (not in the speech): the raw-engine-versus-finished-car analogy, "Most people skip this step and end up disappointed with the base model's accuracy" and "Fine tuning is really where the real performance gap closes".
- Funnel: spoken "if you want a guide to set it up yourselves just comment jev below and I'll send you the link directly"; caption: comment "JEV" to get the setup guide for Laya. Neither gives a repo URL, install command, license, version or model size.
- Caption hashtags: #jevai #typesafeai #layaai #opensourceai #githubrepo.
- Transcript quirk: the last sentences ("do it in a tenth of the time. So if you want a guide ...") appear twice (ASR duplication).
- Vault cross-check: [[../pages/20260925-5-github-repos-43k-stars-week|@buildwithneej's post]] lists laya as "the free, open answer to Jev, released the same day Jev launched" at 24 to 29 ms per call on a laptop once loaded, and [[../pages/20260921-laya-pip-install-comment-fast-teaser|Albert Olgaard's reel]] says about 30 ms for Laya against about 250 ms for Jev. The Laya magnitudes agree; the Jev latency differs between creators (about 200 ms here, about 250 ms there). All are second-hand claims and none is verified here.
- Counts as shown by Jina: 2.3K likes, 2.5K comments (Instagram UI order, likes then comments).

## 點解值得留意
- 對 `judging-with-jev` 的新資訊：這是 vault 第一次出現「Jev 以外的自架選擇」的具體取捨（本機、免費、自述約 30 ms，但要自行微調）。skill 目前只覆蓋託管的 Jev（中位數約 US$0.000068 一個判斷，見 [[../pages/20260925-jev-seo-geo-audit-cost-down-90|SEO/GEO 成本頁]]），沒有自架方案；Jev 延遲的說法在兩位創作者之間也不一致（約 200 ms 對約 250 ms），沒有一手數字可供對照。
- 「微調後追平 Jev、只需十分之一時間」只是自述，前提是自備標註資料與評估集；Jev 的賣點是經 RLCD 校準的機率，使 skill 的 0.80 / 0.50 門檻有意義，微調後的本機分類器未必保留這種校準（推論，未驗證）。若 Laya 日後取代 Jev 作後備，門檻要重新量度。
- 「留言領取 setup guide」加上 skill 已警告的 Jev 仿冒轉售站（jevmodel.org 等），採用前應先找 Laya 的官方 repo 與授權，不要依賴留言區派發的指南；配合 Claude Code 微調的做法也值得在找到一手來源後再評估是否值得草擬 skill（本次不草擬）。

## Source
- https://www.instagram.com/reel/Dd6P9YOB06z/ — Nick Saraev (@nick_saraev), 2026-09-30 (from the cover alt-text "Video by Nick Saraev on September 30, 2026"), likes=2.3K comments=2.5K.
- Reader: Jina (full caption, cover alt-text, rounded counts) + Supadata transcript (lang en, mode=auto, 164 words), fetched 2026-10-04 by the main session one call at a time after the earlier parallel burst hit HTTP 429. The caption already carried most of the pitch (`needs_manual_text: false` before and after); the transcript adds the spoken-only "really easily" and "a tenth of the time" and confirms the caption's analogy is not in the audio. The transcript is automatic speech recognition ("leia" for Laya) and is kept verbatim in raw/. Supadata metadata was not re-fetched, so counts are Jina's rounded figures.

## Related
- [[../pages/20261002-what-is-jev-system-one-ai-model|What Is Jev? The AI Model That Doesn't Generate Text]]
- [[../pages/20260925-5-github-repos-43k-stars-week|5 GitHub Repos That Gained ~43k Stars in a Week]] — first mention of laya in the vault.
- [[../pages/20260925-jev-seo-geo-audit-cost-down-90|Jev cuts agent SEO/GEO audit-and-fix cost by 90%]] — the hosted-Jev per-decision cost this reel compares against.
- [[../pages/20260921-laya-pip-install-comment-fast-teaser|Albert Olgaard: Laya via pip install (comment 'Fast' teaser)]]
- [[../pages/20260920-jev-in-60-seconds-nate-herk-teaser|Nate Herk: Jev in under 60 seconds (comment 'JEV' teaser)]]
- [[../../skills/judging-with-jev/SKILL|skill: judging-with-jev]]
