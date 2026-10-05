---
name: researching-competitor-landing-pages
description: Compares competitor landing pages on five fields (target customer, first promise, evidence type, CTA, likely objection) with a ready agent prompt that fills the table for up to 5 URLs. Use when researching competitors, writing a landing page, positioning an offer, or asked for a competitor table.
metadata:
  source_url: "https://www.threads.com/@ai.marketing.hk/post/Dd_mKONFA2-"
  source_platform: "threads"
  author: "@ai.marketing.hk"
  captured_at: "2026-10-04"
  engagement: "likes=9 replies=6 reposts=0 shares=11"
  origin_type: "post"
  vault_status: "reviewer-approved"
  reviewed_at: "2026-10-05T07:49:32Z"
  reviewed_by: "routine:skill-review"
  review_hash: "45ca274a6d7486238ac74810c336dc7f1dc3ed052a942f9a4723ff68f1eb48ae"
  review_report: "outputs/skill-reviews/2026-10-05-researching-competitor-landing-pages.md"
---

# researching-competitor-landing-pages

Research competitor landing pages with one fixed framework instead of a folder of screenshots. Every page is read against the same five fields, an AI agent fills the table, and the table is used to find communication gaps in the market (promises everyone makes versus evidence that is still rare).

## When to use

- You are about to write or rewrite a landing page and want to know what competitors already promise
- You need a positioning angle for an offer, a client pitch or an ad campaign
- Someone asks for a "competitor table" or "competitor analysis" of web pages
- You catch yourself opening many tabs and saving screenshots without a question to answer

## The five fields

| Field | What it records |
|---|---|
| Target customer (目標客) | Who the page is talking to |
| First promise (第一個承諾) | What the first screen promises the visitor |
| Evidence type (證據類型) | What backs the promise: customer reviews, data, certifications, demos |
| CTA | What the page wants the visitor to do next |
| Likely resistance (可能阻力) | What could make the visitor hesitate |

Anything not found on the page is recorded as 「未見」 (not seen). Never infer it.

## Steps

1. **Pick the pages.** Choose 3 to 5 public landing pages from the same market (the source post uses exactly 5). Collect their URLs. Skip pages behind a login.
2. **Run the prompt.** Give the URLs to an AI agent that can open web pages (the source post names Manus as its example) and paste the prompt below, replacing `[網址1]-[網址5]` with the real URLs. If you have fewer than 5, change the number in the first line.

   Prompt, copied verbatim from the source post:

   ```
   你是 landing page 分析師。分析以下 5 個競爭對手網址：[網址1]-[網址5]
   以表格輸出：網址／目標客／第一個承諾／證據類型／CTA／可能阻力。
   每格須引用對應網址的內容；頁面沒有的資料寫「未見」，不要猜測。
   ```

   English rendering (this vault's translation, not from the post):

   ```
   You are a landing-page analyst. Analyse these 5 competitor URLs: [URL1]-[URL5]
   Output a table with columns: URL / target customer / first promise / evidence type / CTA / likely resistance.
   Every cell must cite content from the matching URL; where the page has no such information write "未見" (not seen) and do not guess.
   ```

3. **Spot-check the table.** Open each page yourself once and compare it with its row, especially the evidence-type column. Fix or blank any cell you cannot confirm.
4. **Read the table for one question first.** Which promises does everyone make, and which evidence is still rare? A promise everyone makes will hardly set you apart; evidence that is still rare often marks the gap in how the market communicates.
5. **Treat the gap as a hypothesis.** Check it against your own customer data (support enquiries, sales conversations, customer reviews) before spending any budget on it.
6. **Write the positioning note.** Keep it short:
   - Promises everyone makes (do not lead with these)
   - Evidence that is rare in the market and that you can honestly show
   - What your own customer data confirmed or contradicted
   - The one thing to test next (headline, proof block or CTA)

## Pitfalls

- **Agent fills gaps with guesses.** Keep the "未見" / "not seen" rule and the requirement to cite each page; if a cell has no citation, treat it as unverified. The human spot-check in step 3 is part of the method, not optional.
- **Pages the agent cannot see.** Login walls, geo-targeted variants, heavy client-side rendering and A/B tests can make the agent read a different page from your customers. Mark such cells 「未見」 or inspect them by hand.
- **Mixed markets.** Comparing pages that serve different customers makes "everyone promises X" meaningless. Keep the five pages in one market.
- **The gap is not a conclusion.** The source author stresses that the output is a set of hypotheses to validate against your own customer data.
- **"Likely resistance" is partly judgement.** Ask the agent to base it on what the page shows or omits (price, refund terms, proof) and to write 「未見」 when the page gives no basis.
- **Stale tables.** Landing pages change; redo the table every quarter or before a major campaign (this skill's suggestion, not from the source post).
- **Keep secrets out of the prompt.** Only public URLs go to the agent; do not paste logins or private client data.

## Source

- @ai.marketing.hk (AiMarketingHK) on Threads, 2026-10-02: https://www.threads.com/@ai.marketing.hk/post/Dd_mKONFA2-
- The method and the prompt are in the author's five replies under the root post; the root post only sets up the idea.
- Wiki note: `wiki/pages/20261002-competitor-landing-page-five-field-table-prompt.md`
