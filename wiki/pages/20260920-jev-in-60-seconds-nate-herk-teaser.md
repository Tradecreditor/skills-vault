---
title: "Nate Herk: Jev in under 60 seconds (comment 'JEV' teaser)"
slug: 20260920-jev-in-60-seconds-nate-herk-teaser
type: video
status: draft
source_url: "https://www.instagram.com/reel/DdhR21VBfQH/"
source_platform: instagram
author: "nateherkai"
published: "2026-09-20"
captured_at: "2026-10-04T21:18:41Z"
captured_by: "claude-code-cloud"
canonical_id: "instagram:DdhR21VBfQH"
engagement: "likes=14.5K comments=3.3K"
tags: [topic/model-comparison, jev, typesafe, decision-models, agent-gating, teaser]
related: [20261002-what-is-jev-system-one-ai-model, 20260925-5-github-repos-43k-stars-week, 20260921-laya-pip-install-comment-fast-teaser, 20260930-laya-free-local-jev-alternative-30ms-vs-200ms, skills/judging-with-jev]
needs_manual_text: false
---

## 摘要
Nate Herk（@nateherkai）於 2026-09-20 的 reel（逐字稿約 327 字）以「六十秒內講清楚 Jev」為題：他稱 Jev 是由 Diogo（語音辨識的拼寫；他說此人是 ChatGPT 的共同發明人之一，未經核實）創造的 AI 模型，「據說」比一般 AI 模型快 200 倍、平 400 倍，而且不會對話，只會答是／否、分類或打分，並附信心分數。他示範把 1,000 封電郵用 7 條問題跑過 Jev，自稱 7 秒、9 美仙完成；同一工作換成另一個模型（語音辨識寫成「luna」，身份不明）要 5 分鐘、62 美仙，他說貴 12 倍、慢 46 倍，但這兩個倍數與他說的絕對數字對不上。他另展示一個在 X 上即時把貼文標成 AI slop／golden nuggets／breaking news 的 Chrome 擴充功能，以及一個讓 Jev 每秒判斷比特幣升跌並自動落單的示範。結尾是留言「Jev」領取「the tool」，但沒有說明那個 tool 是甚麼。以上全部是創作者自述的示範，沒有獨立驗證。

## Key facts
- Basis: the Supadata ASR transcript (lang en, mode=auto, 327 words), kept verbatim in `raw/20260920-jev-in-60-seconds-nate-herk-teaser.md` under `## Transcript (supadata)`. Everything below is Nate Herk's own claim or his narration of an on-screen demo; nothing was checked here.
- Framing (speaker): "I'm gonna explain Jev clearly in under 60 seconds".
- Origin claim (speaker): Jev is "an AI model created by Diogo who co-invented ChatGPT". "Diogo" is the ASR spelling; the vault's launch note (`outputs/20261002-jev-in-vault-routines.md`) records TypeSafe AI and Diogo Almeida (@CompleteSkeptic). The "co-invented ChatGPT" credential is the speaker's claim and was not verified here.
- Speed and price claim (speaker): "apparently 200 times faster and 400 times cheaper than regular AI models", hedged with "apparently". That is the top end of the 20-200x faster / 40-400x cheaper range recorded for the launch post in the same outputs note.
- Interface (speaker): "an AI model that doesn't actually talk to you"; given an input it "can say yes or no, it can categorize, or it can give something a score", and each decision comes with a confidence score. This matches the noul / choice / score types in `skills/judging-with-jev`.
- Email demo (speaker): "a thousand emails through Jev on these seven questions", "categorized a thousand emails in seven seconds for nine cents". The same job on a comparison model took "five minutes and 62 cents", which he calls "12 times more expensive and 46 times slower". The comparison model's name is garbled by the ASR ("luna") and cannot be identified from the transcript. His multiples do not follow from his numbers (62 / 9 is about 6.9x; 300 s / 7 s is about 43x), so either the on-screen figures differ or the ASR mis-heard a number: treat 12x / 46x as unreliable.
- Other uses shown (speaker): YouTube comments and "school posts" (probably Skool posts, ASR); a Chrome extension that, while he scrolls X, labels posts "AI slop", "golden nuggets" or "breaking news", all with Jev on the back end, "essentially real time".
- Trading demo (speaker): Jev "trading bitcoin for me", deciding every second whether the price goes up, goes down or is unclear, and "placing all of these trades". No profit, risk, data or latency figure is given.
- CTA (speaker): "just comment Jev and I'll send you over the tool." Which tool (email classifier, Chrome extension, trading demo) is not said.
- Transcript quirk: the "categorized a thousand emails in seven seconds" clause appears twice (ASR duplication).
- Posted 2026-09-20, five days after Jev's launch on 2026-09-15 (launch date as recorded in `skills/judging-with-jev`), so it belongs to the first wave of creator explainers.
- Counts as shown by Jina: 14.5K likes, 3.3K comments (Supadata metadata was not re-fetched, so no exact figures).
- Background on what Jev is (typed noul / choice / score questions, calibrated probabilities, no text generation) is in [[../pages/20261002-what-is-jev-system-one-ai-model|the IBM Technology explainer]], a fuller and more neutral source than this reel.

## 點解值得留意
- 對 `judging-with-jev` 的新資訊：用法本身不新（是／否、分類、打分，附信心分數，正是 skill 的 noul / choice / score），但這是第一份有批量數字的示範：1,000 封電郵 × 7 條問題約 7 秒、9 美仙，即每個判斷約 US$0.000013，低於 skill 引用的中位數約 US$0.000068，與 skill 所說「同一 state 的多條問題共用成本」的設計一致（推論；他的電郵長度和計費方式不明，未驗證）。
- 電郵分類、貼文分類、即時決策與 skill 的 type / topic 標籤、hot-list 預篩同類，屬旁證而不是新能力；他拿來比較的模型被 ASR 弄花（「luna」），12 倍／46 倍又與自己的數字對不上，不要把這些倍數寫進 skill 或 Routine 文件。
- 比特幣交易示範沒有績效或風險數字，只當展示「每秒判斷」的速度，不應作為策略參考。
- 這是引流漏斗，「the tool」是甚麼仍然不明。skill 已警告 Jev 仿冒轉售站，引用 Jev 資料時優先用 TypeSafe 與 IBM 等一手來源。

## Source
- https://www.instagram.com/reel/DdhR21VBfQH/ — Nate Herk (@nateherkai), 2026-09-20 (from the cover alt-text "Video by Nate Herk on September 20, 2026"), likes=14.5K comments=3.3K.
- Reader: Jina (caption, cover alt-text, rounded counts) + Supadata transcript (lang en, mode=auto, 327 words), fetched 2026-10-04 by the main session one call at a time after the earlier parallel burst hit HTTP 429. The caption ("Comment "JEV" and I'll send you the tool.") was only a teaser; the transcript carries the substance, so `needs_manual_text: false`. The transcript is automatic speech recognition and garbles some names ("Diogo", "luna", "school posts"); it is kept verbatim in raw/. Supadata metadata was not re-fetched, so counts are Jina's rounded figures.

## Related
- [[../pages/20261002-what-is-jev-system-one-ai-model|What Is Jev? The AI Model That Doesn't Generate Text]]
- [[../pages/20260925-5-github-repos-43k-stars-week|5 GitHub Repos That Gained ~43k Stars in a Week]]
- [[../pages/20260921-laya-pip-install-comment-fast-teaser|Albert Olgaard: Laya via pip install (comment 'Fast' teaser)]]
- [[../pages/20260930-laya-free-local-jev-alternative-30ms-vs-200ms|Laya: free open-source local Jev alternative (~30 ms vs ~200 ms)]]
- [[../../skills/judging-with-jev/SKILL|skill: judging-with-jev]]
