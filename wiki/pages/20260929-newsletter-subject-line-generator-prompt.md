---
title: "Newsletter 主題行生成器 (Subject Line Prompt)"
slug: 20260929-newsletter-subject-line-generator-prompt
type: post
status: draft
source_url: "https://www.threads.com/@ai.marketing.hk/post/Dd5iIXgjgBd"
source_platform: threads
author: "@ai.marketing.hk"
published: "2026-09-29"
captured_at: "2026-10-01T12:59:40Z"
captured_by: "claude-code-cloud"
canonical_id: "threads:Dd5iIXgjgBd"
engagement: "likes=7 replies=2 reposts=2 (root post; order inferred from Threads UI; no views shown)"
tags: [topic/marketing-content, newsletter, email-marketing, subject-line, copy-paste-prompt, hong-kong, psychology-triggers]
related: [20260927-seo-purchase-intent-ai-agent-ecom, 20260919-linkedin-skills-for-claude, 20260923-promptfoo]
needs_manual_text: false
---

## 摘要

@ai.marketing.hk（AiMarketingHK）喺 Threads 分享一個即用 AI 行銷 Prompt：《Newsletter 主題行生成器》，一次為 Newsletter 出 8 個 subject line，再為最好嘅 3 個配 preview text。每個 subject line 各用一種心理觸發點（好奇缺口、具體數字、緊迫感、FOMO、爭議性等），並限制字數、禁止作者發明數據或保證。解決嘅問題係 Newsletter 內容寫好後，主題行成日到發送前先臨時諗，影響開信率。適合做電郵行銷、經營電子報嘅香港中小企同內容創作者。作者提醒 AI 初稿仍要人手檢查字數。

## Key facts

- Thread by @ai.marketing.hk: root post (Dd5iIXgjgBd) = pitch; reply Dd5iJeEDlOj (the share target) = full copy-paste prompt; reply Dd5iLBnjrLa = newsletter CTA.
- Root post claim: 8 subject lines in one go, then preview text for the top 3. Author caveat: "AI 初稿仍要人手檢查字數" (AI drafts still need a human length check).
- The prompt, verbatim (fill the three bracketed fields):

```
你是 Email Marketing 專家，熟悉讀者心理。

為以下 Newsletter 生成 8 個 subject line： 本期主題：[本期核心內容] 目標受眾：[訂閱者描述] Newsletter 風格：[專業資訊型／輕鬆故事型／實用教學型]

8 個 subject line 各用一個心理觸發點： 1. 好奇缺口 2. 具體數字（只用我提供的資料） 3. 個人化對話 4. 緊迫感 5. 利益驅動 6. FOMO 7. 爭議性 8. 故事開場

輸出要求： - 編號 1-8，每個 subject line 30 字以內，標明觸發點 - 推薦前 3 個，各配一條 preview text（45 字以內）補充懸念或資訊 - 用 1-2 句說明為何推薦這 3 個（針對我的受眾） - 不要發明數據、價錢、成效或保證 - 資料不足先列出需要補充的資料
```

- Built-in guardrails: numbers only from user-supplied data, no invented prices/results/guarantees, ask for missing info first.
- CTA reply: author promotes a newsletter and a free "Grok Bot AI MKT 入門體驗包" (one Chief of Staff configured, opens 4 managers for research through copy drafts); "每週只需 5 分鐘". Link not captured.
- Engagement shown (order inferred from Threads UI): root 7 · 2 · 2; prompt reply 3 · 1 · 5. Only three counts appeared per post, no views line.

## 點解值得留意

- 可以直接放入 Jeff 幫香港中小企做電子報 / EDM 嘅工作流程，一次出 8 個唔同角度嘅主題行，客人揀得快。
- 「只用我提供嘅資料、唔好發明數據」呢類防幻覺指令，值得抄入自己其他行銷 prompt 同客戶培訓教材。
- 做短影音內容時，可以拆解成「8 個心理觸發點」一集，Comment 領 prompt 都好有引流潛力。
- 可以用 promptfoo 類評測工具，測試輸出有無超字數（30 / 45 字）或發明數字。

## Source

- Post: https://www.threads.com/@ai.marketing.hk/post/Dd5iIXgjgBd
- Share link: https://www.threads.com/share/_xasBKG0y/ (lands on reply Dd5iJeEDlOj)
- Author: @ai.marketing.hk (AiMarketingHK)
- Published: 2026-09-29 (the root post showed age "1d" in a read of the share link on 2026-09-30; the 2026-10-01 read showed no age)
- Engagement: likes=7 replies=2 reposts=2 for the root post (order inferred from Threads UI; no views shown)
- Reader: Jina Reader (r.jina.ai); Exa not used
- Not captured: the newsletter link behind the CTA, images/profile picture.

## Related

- [[pages/20260927-seo-purchase-intent-ai-agent-ecom|AI Agent SEO: Purchase-Intent Keywords for $100k/mo E-com Organic Revenue]] - another AI-for-marketing workflow post for SME clients.
- [[pages/20260919-linkedin-skills-for-claude|LinkedIn Skills for Claude: Free LinkedIn Automation Tool]] - marketing-copy skills that pair with this prompt.
- [[pages/20260923-promptfoo|promptfoo: LLM Evals & Red Teaming]] - way to test the prompt's length and no-invented-numbers constraints.
