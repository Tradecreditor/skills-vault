---
title: "Clay: AI B2B Prospecting and Waterfall Enrichment"
slug: 20260910-clay-ai-b2b-sales-automation
type: tool
status: draft
source_url: "https://www.instagram.com/p/DdIruFJI9u5/"
source_platform: instagram
author: "touchdownmedia.ai (TouchDown 創·著陸)"
published: "2026-09-10"
captured_at: "2026-09-27T15:01:30Z"
captured_by: "claude-code-cloud"
canonical_id: "instagram:DdIruFJI9u5"
engagement: "comments=0"
tags: [clay, sales-automation, b2b, lead-generation, data-enrichment, gtm, ai-agents, mcp, hk-sme]
related: ["assafelovic--gpt-researcher", "ScrapeGraphAI--Scrapegraph-ai"]
needs_manual_text: false
---

## 摘要

香港商業媒體 TouchDown 創·著陸 報道，AI 銷售自動化平台 Clay 完成 1.15 億美元 D 輪融資，估值升至 71 億美元，Wellington Management 領投，CapitalG、紅杉資本及 Meritech 參投。Clay 針對 B2B 銷售最花時間的「搵潛在客」環節：銷售員用自然語言描述目標客群，AI 就會列出符合條件的買家。它的核心是 Waterfall 功能，一次過串連 200 多個外部數據源，逐個數據商查到有結果為止，再按公司規模、業務里程碑同收入潛力排序，並寫個人化開發郵件。Clay 現有超過 17,000 個客戶，包括 Anthropic 同 OpenAI。截至 2026-09-27，Clay 官網已經推出 MCP 連接器，同埋畀 Claude Code、Codex、Cursor 用的 agent plugin，所以佢亦都係一個可以喺 coding agent 入面直接調用嘅 GTM 數據工具。

## Key facts

- **What it is:** Clay (clay.com) is a go-to-market (GTM) data and automation platform for B2B sales and prospecting: search companies and people, enrich them, score them, write outreach and push the results to a CRM or email sequencer.
- **Funding (per the post, 2026-09-10):** US$115M Series D led by Wellington Management, with CapitalG (Alphabet), Sequoia and Meritech; valuation US$7.1B, up US$2.1B since the start of the year. Not cross-checked against a second source, because Exa search was out of credits at capture time.
- **Business numbers (per the post):** 17,000+ customers (Anthropic and OpenAI among them; both also appear on clay.com/customers). Annualised revenue is expected to reach about US$200M by the end of the quarter, and the company was briefly profitable earlier in the year. Co-founder and CEO: Kareem Amin.
- **Waterfall enrichment:** queries several data vendors in sequence until one returns the field (email, phone and so on), so one Clay account replaces separate contracts with each vendor. Clay's site says the marketplace has "200+ providers" and uses waterfall logic to validate emails and phone numbers across vendors.
- **AI features (clay.com, fetched 2026-09-27):** Claygents (AI research agents for companies and people), Account Agents, Signals (job changes, promotions, new hires, company news), Sequencer (email campaigns), Ads audience sync (LinkedIn, Meta, Google), Workflows and Functions (reusable GTM logic).
- **Agent access (clay.com/mcp, fetched 2026-09-27):** a Clay MCP connector for Claude, ChatGPT, Codex, Copilot and Glean. Reps can find contacts, pull verified emails and phone numbers, run Clay Functions and push contacts to CRMs or sequencers in natural language, with up to 1,000 People Search results per request.
- **Coding-agent plugin:** `github.com/clay-run/agent-plugins` provides skills plus the `clay` CLI for Claude Code, Codex and Cursor, in open beta on Mac and Linux. Sign-in uses `clay login`, and setup is described in the repo's `GETTING_STARTED.md`. Developer docs: https://developers.clay.com. This capture did not install or run it.
- **Pricing (clay.com/pricing, fetched 2026-09-27):** Free: 500 actions/mo and 100 data credits/mo, multi-provider waterfalls included, no phone enrichment. Launch: from $167/mo (15K actions/mo). Growth: from $446/mo (40K actions/mo), which adds CRM and HTTP API integrations. Enterprise: custom. "Actions" measure platform usage; "data credits" pay for third-party data and AI.

## 點解值得留意

- **AI 顧問 (HK SME)：** 好多香港中小企仲係靠人手搵客、買 list。Clay 嘅「自然語言描述 ICP → 自動 enrich → 排序 → 寫 outreach」可以直接做成一個顧問方案模板，免費 plan 夠做 demo。不過要留意，佢嘅數據源以歐美 B2B 為主，香港本地公司嘅覆蓋率要先實測。
- **Waterfall 概念本身可以抄：** 逐個數據源試到有結果先停，呢個 pattern 可以用喺任何 enrichment pipeline，例如用 Agent-Reach 或者 Scrapegraph-ai 自己砌一個平價版畀預算細嘅客。
- **Agent 化 GTM：** Clay 已經出咗 MCP 同 Claude Code、Codex 嘅 plugin，即係 coding agent 可以直接幫你搵客、寫 email。呢個係「AI agent 入侵銷售」嘅好例子，啱拎嚟拍短片。
- **內容題材：** TouchDown 用廣東話包裝外國 AI 融資新聞（標題「AI銷售獨角獸」、「OpenAI 都係佢客仔」），呢種 hook 格式可以參考嚟做 Jeff 自己嘅 AI 短片。

## Source

- URL: https://www.instagram.com/p/DdIruFJI9u5/
- Author: @touchdownmedia.ai (TouchDown 創·著陸, 撰文)
- Published: 2026-09-10
- Engagement: comments=0; the reader did not return a like count
- Reader: jina (r.jina.ai) for the post; product, pricing and plugin facts come from clay.com pages (/, /pricing, /mcp, /agent-plugin, /waterfall-enrichment) and the `clay-run/agent-plugins` README, all fetched through Jina Reader or raw.githubusercontent.com on 2026-09-27

## Related

- [[assafelovic--gpt-researcher|gpt-researcher]]: open-source research agent, a DIY counterpart to Claygent-style account research
- [[ScrapeGraphAI--Scrapegraph-ai|Scrapegraph-ai]]: LLM web data extraction, usable as one step in a home-made waterfall enrichment
- [[Panniantong--Agent-Reach|Agent-Reach]]: agent-side readers for social or web sources when building your own prospect research
