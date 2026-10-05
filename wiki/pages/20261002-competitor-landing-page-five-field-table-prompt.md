---
title: "Competitor Landing Page Research: 5-Field Table + Agent Prompt"
slug: 20261002-competitor-landing-page-five-field-table-prompt
type: post
status: draft
source_url: "https://www.threads.com/@ai.marketing.hk/post/Dd_mKONFA2-"
source_platform: threads
author: "@ai.marketing.hk"
published: "2026-10-02"
captured_at: "2026-10-04T21:08:38Z"
captured_by: "claude-code-cloud"
canonical_id: "threads:Dd_mKONFA2-"
engagement: "likes=9 replies=6 reposts=0 shares=11"
tags: [topic/marketing-content, competitor-analysis, landing-page, manus, prompt, hk-sme]
related: [20260927-seo-purchase-intent-ai-agent-ecom, 20260929-newsletter-subject-line-generator-prompt, skills/researching-competitor-landing-pages]
needs_manual_text: false
---

## 摘要

AiMarketingHK（@ai.marketing.hk）認為研究競爭對手 landing page 唔應該只係收藏 screenshot，而係用同一套框架逐頁對照，睇出市場上嘅溝通空位。方法係每個 landing page 只睇五樣：目標客、第一個承諾、證據類型、CTA、可能阻力，搵唔到嘅資料標「未見」，唔好推測。作者建議揀 5 個同一市場嘅公開 landing page，將網址交畀 AI agent（例如 Manus）按五欄整理成表格，並提供一段可直接 copy & paste 嘅任務指令，最後人手逐頁核對「證據類型」一欄。表格完成後先只問一條問題：邊啲承諾人人都講、邊啲證據仍然罕見。作者強調呢啲只係待驗證嘅假設，要回到自己嘅客服查詢、銷售對話同客戶評價去驗證，先值得投放資源。

## Key facts

- Author: @ai.marketing.hk (AiMarketingHK), Traditional-Chinese Threads post, 2026-10-02. The root post only sets up the idea and ends with "給他一張表👇"; the method and prompt are in the author's own 5 replies (Post 2 to Post 6 in `raw/`)
- Claim: do not just collect screenshots of competitor pages; compare every page against the same framework to find gaps in market communication ("溝通空位"). The author likens it to briefing a new colleague with a table to fill in
- The five fields, looked at for every landing page:
  1. 目標客 (target customer): who is this page talking to
  2. 第一個承諾 (first promise): what the first screen promises the visitor
  3. 證據類型 (evidence type): what backs the promise, e.g. customer reviews, data, certifications, demos
  4. CTA: what the page wants the visitor to do next
  5. 可能阻力 (likely resistance): what could make the visitor hesitate
- Rule: data that cannot be found is marked 「未見」 (not seen); do not infer ("不要推測")
- Procedure as written by the author:
  1. Pick 5 public landing pages from the same market
  2. Give the URLs to an AI agent (the author's example: Manus) and have it fill the five fields into a table, with the original URL attached
  3. Task prompt, "直接 Copy & Paste 使用" (copied verbatim, NOT run):
  4. Open each page yourself once to check, especially the 證據類型 column
- Prompt text (verbatim from the post):

```
你是 landing page 分析師。分析以下 5 個競爭對手網址：[網址1]-[網址5]
以表格輸出：網址／目標客／第一個承諾／證據類型／CTA／可能阻力。
每格須引用對應網址的內容；頁面沒有的資料寫「未見」，不要猜測。
```

- Reading the table: answer one question first, "哪些承諾人人都在說？哪些證據仍然罕見？" (which promises does everyone make, which evidence is still rare). Per the author, promises everyone makes rarely let you stand out, while evidence that is still rare often marks the communication gap
- Validation: the author says these are only hypotheses; go back to your own customer data (support enquiries, sales conversations, customer reviews) to check the gap is real before spending budget
- The thread closes with a question to readers ("你最想看清楚哪一個市場的溝通空位？") and Post 6, a newsletter promo with a buff.ly short link (not followed, not summarised)
- No tool pricing, accuracy test or example output is given; Manus is only named as an example agent
- Engagement: likes=9 replies=6 reposts=0 shares=11

## 點解值得留意

- **可直接做客戶交付**：五欄框架加現成 prompt，可以變成幫香港中小企做「競品 landing page 審查」嘅標準流程；帖文只提 Manus，但同一段指令亦可交畀 Claude Code 或其他有瀏覽能力嘅 agent 試跑。
- **防幻覺設計**：「未見」規則、要求每格引用對應網址內容、再人手核對證據欄，係低成本約束 agent 亂作嘅做法，可以搬去其他研究 prompt。
- **由競品表走到定位**：「人人都講嘅承諾 vs 罕見證據」再用自己客戶資料驗證，可以接去 landing page 文案、定位同 SEO 項目（已草擬成 skill，見 Related）。
- **同系列內容**：同一作者另有 Newsletter 主題行 copy-paste prompt，屬香港 AI 營銷系列，值得持續跟進。

## Source

- Post: https://www.threads.com/@ai.marketing.hk/post/Dd_mKONFA2-
- Author: @ai.marketing.hk (AiMarketingHK) · Published: 2026-10-02
- Engagement: likes=9 replies=6 reposts=0 shares=11
- Reader: jina (share link resolved via r.jina.ai; counts order inferred from Threads UI)
- Replies (Post 2 to Post 6): recovered from the embedded JSON of the share-page HTML, because Jina returned only the root post
- Share URL: https://www.threads.com/share/BAEFDz9Vjc/
- Not captured: the newsletter promo link, other accounts' comments

## Related

- [[../pages/20260927-seo-purchase-intent-ai-agent-ecom|AI Agent SEO: Purchase-Intent Keywords for $100k/mo E-com Organic Revenue]] — another post about handing marketing research to an AI agent
- [[../pages/20260929-newsletter-subject-line-generator-prompt|Newsletter 主題行生成器 (Subject Line Prompt)]] — same author, another copy-paste prompt for Hong Kong marketing
- [[../../skills/researching-competitor-landing-pages/SKILL|skill: researching-competitor-landing-pages]] — draft skill built from this post
