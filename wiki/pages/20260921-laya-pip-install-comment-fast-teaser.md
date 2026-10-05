---
title: "Albert Olgaard: Laya via pip install (comment 'Fast' teaser)"
slug: 20260921-laya-pip-install-comment-fast-teaser
type: video
status: draft
source_url: "https://www.instagram.com/reel/DdjdN0CCcU8/"
source_platform: instagram
author: "albert.olgaard"
published: "2026-09-21"
captured_at: "2026-10-04T21:18:40Z"
captured_by: "claude-code-cloud"
canonical_id: "instagram:DdjdN0CCcU8"
engagement: "likes=8325 comments=1479"
tags: [topic/model-comparison, laya, jev, decision-models, classifier, local-model, teaser]
related: [20261002-what-is-jev-system-one-ai-model, 20260925-5-github-repos-43k-stars-week, 20260930-laya-free-local-jev-alternative-30ms-vs-200ms, 20260920-jev-in-60-seconds-nate-herk-teaser, skills/judging-with-jev]
needs_manual_text: false
---

## 摘要
Albert Olgaard（@albert.olgaard）於 2026-09-21 的 reel（逐字稿約 139 字）說有人剛發佈了 Jev 的免費開源版本 Laya，是一個「可在自己電腦本機執行的 system one 模型」，和 Jev 一樣不能寫程式碼；他稱 Jev 回應約需 250 毫秒，Laya 只需 30 毫秒，原因是本機執行不必往返雲端。他同時承認基礎模型並非樣樣精通，要針對特定用途調校訓練，並說可以用 Claude 去做。結尾是「留言 fast 就把模型連結傳給你」的引流，口述中沒有安裝指令、授權、準確度數字或 repo；封面畫面的終端機 `pip install laya` 只出現在畫面上，沒有被唸出來。語音辨識把名稱聽成「Jeb」和「Naya」，這裡按 Jev 和 Laya 理解：封面畫面是 `pip install laya`，vault 內 Nick Saraev 那條 reel 的 hashtag 也是 #jevai #layaai。所有速度說法都是創作者自述，沒有基準測試佐證。

## Key facts
- Basis: the Supadata ASR transcript (lang en, mode=auto, 139 words), kept verbatim in `raw/20260921-laya-pip-install-comment-fast-teaser.md` under `## Transcript (supadata)`. Everything below is Albert Olgaard's own claim; nothing was benchmarked or verified here.
- ASR names: the transcript writes "Jeb" and "Naya". The ASR mis-hears the names; read them as Jev and Laya. Support: the cover frame shows `pip install laya`, and the other Laya reel in the vault ([[../pages/20260930-laya-free-local-jev-alternative-30ms-vs-200ms|Nick Saraev]]) carries the hashtags #jevai #layaai. This reel's own caption has no hashtags.
- Pitch (speaker): "Someone just released a free and open source version of Jeb [Jev], and it's actually much faster." It is "a local system one model that you can run on your own computer". "System One" is the term TypeSafe uses for Jev's model family ([[../pages/20261002-what-is-jev-system-one-ai-model|IBM explainer]]). He adds "Same as Jeb [Jev], it cannot write code" (the explainer says Jev generates no text at all).
- Speed claim (speaker): Jev "takes around 250 milliseconds to respond, this model only takes 30 milliseconds". His reason: "it's running local, so it doesn't have to go to the cloud and back". No hardware, model size or benchmark is given, so the gap mixes model speed with network round-trip. The other Laya reel quotes about 200 ms for Jev, so the Jev figure itself differs between creators.
- Caveat (speaker): "the base model isn't good at everything, so it needs to be tuned and trained for specific use cases, but we can actually do that with Claude." No training data, method, effort or resulting accuracy is given. The transcript repeats a fragment ("cases. But we can actually do that."), which is ASR duplication, not missing content.
- Funnel (speaker): "If you want the link to the model, just comment fast and I'll send it to you." No repo URL, license, version or install steps are spoken.
- On screen only (not in the speech): the cover frame shows a terminal with `pip install laya` and the words "System One" (Instagram alt-text, noisy). Not verified against PyPI or GitHub and not run; the package owner is unknown, so find the official source before installing anything called laya.
- Counts (Supadata metadata): likes=8325, comments=1479, views and shares null. The same metadata says `hasAudio: false`, which is wrong (a transcript with speech exists).
- Same cluster: [[../pages/20260930-laya-free-local-jev-alternative-30ms-vs-200ms|Nick Saraev's reel]] makes the same kind of claim (about 30 ms against about 200 ms, fine-tune with Claude Code).

## 點解值得留意
- 對 `judging-with-jev` 的新資訊：這是 vault 內第二條講「本機 Laya」的創作者來源。skill 假設的是付費託管 API（`api.typesafe.ai`、需要 key），這條 reel 指向本機執行的另一種部署形態；但數字全是自述，而且 Jev 的延遲在兩位創作者之間不一致（約 250 ms 對約 200 ms），不足以改動 skill。
- 他自己給的原因是「本機不用往返雲端」，所以 30 ms 對 250 ms 的差距有一部分來自網絡而不是模型本身；Routine 在雲端 sandbox 運行，要用本機模型就得先把模型裝進 sandbox（推論，未驗證）。
- 若日後驗證 Laya 可用，可考慮作 Jev 被限流或離線時的本機後備（對應 skill 的 402/429/5xx fallback）；但 skill 的 0.80 / 0.50 門檻是配合 Jev 的校準機率設計，換成另一個模型要重新調校（推論，未驗證）。
- 採用前應先找 Laya 的官方 repo、套件頁與授權，不要依賴留言區派發的連結。

## Source
- https://www.instagram.com/reel/DdjdN0CCcU8/ — Albert Olgaard (@albert.olgaard), 2026-09-21 (from the cover alt-text "Video by Albert Olgaard on September 21, 2026"), likes=8325 comments=1479 (Jina showed 8.3K / 1.5K).
- Reader: Jina (caption, cover alt-text) + Supadata metadata (exact counts) + Supadata transcript (lang en, mode=auto, 139 words), fetched 2026-10-04 by the main session one call at a time after the earlier parallel burst hit HTTP 429. The caption ("Comment “Fast” for the link") was only a teaser; the transcript carries the substance, so `needs_manual_text: false`. The transcript is automatic speech recognition and mis-hears the names (Jeb / Naya); it is kept verbatim in raw/.

## Related
- [[../pages/20261002-what-is-jev-system-one-ai-model|What Is Jev? The AI Model That Doesn't Generate Text]]
- [[../pages/20260925-5-github-repos-43k-stars-week|5 GitHub Repos That Gained ~43k Stars in a Week]] — first mention of laya in the vault (24–29 ms per call claim).
- [[../pages/20260930-laya-free-local-jev-alternative-30ms-vs-200ms|Laya: free open-source local Jev alternative (~30 ms vs ~200 ms)]]
- [[../pages/20260920-jev-in-60-seconds-nate-herk-teaser|Nate Herk: Jev in under 60 seconds (comment 'JEV' teaser)]]
- [[../../skills/judging-with-jev/SKILL|skill: judging-with-jev]]
