---
title: "Jev cuts agent SEO/GEO audit-and-fix cost by 90%"
slug: 20260925-jev-seo-geo-audit-cost-down-90
type: concept
status: draft
source_url: "https://www.threads.net/@krumjahn/post/Ddtiv16Gzxt"
source_platform: threads
author: "krumjahn"
published: "2026-09-25"
captured_at: "2026-09-27T15:02:34Z"
captured_by: "claude-code-cloud"
canonical_id: "threads:Ddtiv16Gzxt"
engagement: "likes=12 replies=2 reposts=1 shares=10 views=973"
tags: [seo, geo, jev, typesafe, site-audit, ai-search, consulting-pricing, mcp]
related: [20260920-fast-jev-compaction]
needs_manual_text: false
---

## 摘要

Keith Rumjahn（@krumjahn）喺 Threads 用中文轉述 Ryze AI 創辦人 Ira Bodnar 喺 X 嘅貼文：用 TypeSafe 嘅 Jev（「System One」判斷模型）做 SEO/GEO 審核同修正，成本大約減咗 90%。
重點唔係 Jev 識寫嘢，而係佢將「逐頁用 rubric 打分／分類」呢類判斷變到平到可以跑晒成個網站（官方中位數約 $0.000068 一個判斷），所以 agent 可以 audit 晒成千頁再逐頁提出修正。
Keith 嘅結論係：對接 case 嘅 AI builder 嚟講，呢個唔係慳工具錢，而係要重新諗報價；佢建議呢個星期揀一個客戶網站跑一次完整 audit，再決定報價要唔要跟住調。
要留意中文轉述有誤差：原文講「以前每次約 $250」，而家大約係十分之一；「30x」係指每個步驟快 30 倍，唔係報價差 30 倍。
開源方面已經有幾個 Jev 版 SEO/GEO 工具，例如可以當 Claude Code skill 用嘅 `AgriciDaniel/jev-seo`（每個網站約一仙美金），同 Rust CLI + 15 個 MCP tools 嘅 `AkashPriyadarshii/jev-seo`。

## Key facts

- **What it is**: a claim that Jev (TypeSafe AI's "System One" typed-judgment model, the same model behind `fast-jev-compaction`) makes agent-run SEO/GEO audit-and-fix work ~10x cheaper. Original claim by Ira Bodnar (Ryze AI), X, 2026-09-18: "Agents that audit and fix a client's SEO/GEO used to cost us ~$250" — now ~90% less. Ryze exposes it in its app and as an MCP / Claude Connector.
- **Correction to the Threads paraphrase**: ~$250 was the *old* per-client cost, not the new price; "30x" is per-step speed-up (Search Console reads, Bing/ChatGPT query checks, citation scans, gap analysis, bulk page fixes), not a 30x pricing gap.
- **The pattern (madewithjev.com/jev-for-seo)**: Jev *judges, it does not write*. Pair it with a data source (crawl, SERP scrape, Search Console export) and ask many yes/no or scored rubric questions per URL; questions in one call are answered in parallel, so a 60-question rubric costs about the same as one.
- **Published cost numbers** (median $0.000068 per decision, 15 runs): 1 question × 1,000 URLs ≈ $0.07; 20-point rubric × 1,000 URLs ≈ $1.36; × 10,000 URLs ≈ $13.60. Slop detector: 35 checks on a page in 243 ms for $0.00015.
- **Limits**: no index, no keyword volume, no backlink graph; cannot write titles/meta/copy (needs a writing model); text-only input.
- **Open-source builds to try** (not installed, not verified here):
  - `AgriciDaniel/jev-seo` (Python 3.10+, MIT, v0.1.1): live audit from one homepage URL, 52 rules tied to Google Search Central, Core Web Vitals via PageSpeed, 13 Jev page questions + 5 site questions; outputs PDF (client-facing), XLSX action tracker, Markdown. Runs as a Claude Code skill (`/jev-seo https://example.com`) or CLI (`bin/jevseo run https://example.com`). ~0.00015 USD/page in Jev; optional `--full` adds DataForSEO rankings/backlinks for ~0.30 USD/site. Budget caps `--jev-budget` (default 0.25 USD), `--dfs-budget` (default 1.00 USD). Needs `TYPESAFE_API_KEY`; page cap 60 by default.
  - `AkashPriyadarshii/jev-seo` (Rust, MIT, crates.io v0.1.2): `cargo install jev-seo`; 58-rule audits, live crawl, AI-citation readiness scores, rank drift in local SQLite, CI gate, `jev-seo mcp` exposes 15 MCP tools for coding agents; free path uses DuckDuckGo only.
- **Follow-up thread by Ira Bodnar** ("Jev killed 7 more SEO/GEO workflows"): score competitor pages to copy, keep/change verdict for title/meta/H1/FAQ/schema, match buyer questions to pages, per-URL citation chance + first fix, buyer-intent filter over the full Search Console export, internal-link map (15 nearest candidates per page), 20 yes/no checks on AI-written drafts.

## 點解值得留意

- 直接對應 Josep 嘅 AI 顧問生意：香港中小企好多都問「AI 搜尋搵唔搵到我」，一份用 `jev-seo` 出嘅 PDF 審核報告（每個網站成本幾毫子）可以做成低門檻 lead magnet 或者入門服務。
- Keith 嗰句「唔係慳工具錢，係重寫定價」值得認真諗：交付成本跌咗一個數量級，報價應該按結果／價值計，而唔係按工時。
- 「平價判斷模型逐 URL 打 rubric」呢個 pattern 可以搬去 Iron Log / English Overload 嘅內容 QA（例如用 yes/no 清單篩 AI 生成內容），亦可以做短片題材（「AI 幫你 audit 網站 GEO」）。
- 兩個 `jev-seo` repo 都未 review，指令同 API key 設定未驗證；要用之前先喺獨立環境試，唔好直接喺客戶網站上跑修正。

## Source

- Threads: https://www.threads.net/@krumjahn/post/Ddtiv16Gzxt (share link https://www.threads.com/share/_gQvsDHJj/)
- Author: Keith Rumjahn (@krumjahn); published 2026-09-25; likes=12 replies=2 reposts=1 shares=10 views=973 (at 2026-09-27)
- Upstream: Ira Bodnar (@irabukht), https://x.com/irabukht/status/2101090579127951694, 2026-09-18; likes=1557 retweets=98 views=377396 bookmarks=3041 (fxtwitter)
- Context: https://madewithjev.com/jev-for-seo (2026-09-22), https://github.com/AgriciDaniel/jev-seo, https://github.com/AkashPriyadarshii/jev-seo (READMEs via raw.githubusercontent.com)
- Reader: jina (r.jina.ai) for the post and replies; fxtwitter for the upstream tweet; Exa unavailable (credits exhausted); post image not retrievable (CDN blocked)

## Related

- [[20260920-fast-jev-compaction|fast-jev-compaction — verbatim Jev-scored compaction for Claude Code]] — same Jev "System One" model, used there for keep/drop decisions on Claude Code context; background on what Jev is and how it is priced.
- [[../../skills/judging-with-jev/SKILL|skill: judging-with-jev]] — the vault's own procedure for asking Jev typed questions, with the per-routine question sets where this cost pattern applies to the vault itself.
