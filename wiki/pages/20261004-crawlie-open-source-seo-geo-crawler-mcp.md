---
title: "crawlie: open-source local SEO + GEO crawler with CLI and MCP"
slug: 20261004-crawlie-open-source-seo-geo-crawler-mcp
type: post
status: draft
source_url: "https://www.threads.com/@arumwu/post/DeD1c2yEoBW"
source_platform: threads
author: "@arumwu"
published: "2026-10-04"
captured_at: "2026-10-04T21:09:15Z"
captured_by: "claude-code-cloud"
canonical_id: "threads:DeD1c2yEoBW"
engagement: "likes=4 replies=0 reposts=0 shares=7 views=434"
tags: [topic/seo-geo, crawlie, mcp, geo, technical-seo, open-source, cli]
related: [20260930-openseo-open-source-semrush-alternative, 20260925-jev-seo-geo-audit-cost-down-90, skills/auditing-seo-with-crawlie]
needs_manual_text: false
---

## 摘要

Arum（@arumwu）介紹 crawlie：一套免費、開源、跑喺本機嘅技術 SEO + GEO 爬蟲，附 CLI 同 MCP server，等 AI agent 自己審站。帖文由一個痛點開頭：用 AI 快速生成嘅網站，大半冇被搜尋引擎同 AI 搜尋找到。據帖文，crawlie 有 57 條檢查規則，每次爬取分開俾 Health（技術 SEO）、GEO（AI 搜尋可引用度）同 Accessibility（WCAG）三個分數，每個問題附白話說明，JSON／HTML 報告可以交俾 CI 或客戶。授權係 MIT；託管嘅 Crawlie Cloud 係另一個閉源產品，雲端 worker、SPA 渲染等 roadmap 項目亦未做。對照 repo README，主要說法吻合，但 GitHub API 喺呢個環境回 403，星數同維護狀況未核實。

## Key facts

- What it is: crawlie, `github.com/spronta/crawlie`. README tagline: "The fast, free, open-source technical SEO + GEO crawler — built for humans and agents." Runs locally, ships a CLI (`crawlie`) and an MCP server (`crawlie-mcp`), plus a Tauri desktop app (a signed macOS `.dmg` on Releases).
- Poster's claims checked against the README: free, open source and local (yes); CLI plus MCP (yes); 57 rules (README "What it checks": "57 rules and counting"; its intro says "40+"); three separate scores Health, GEO and Accessibility (yes); every finding explains why it matters, how to fix it and what happens if ignored (yes); JSON and HTML reports (yes, plus `pretty` and `csv`); MIT for engine, CLI, MCP and desktop app (yes, "MIT © Spronta Ltd"); Crawlie Cloud is a separate closed-source product (yes); roadmap items cloud workers, SPA JavaScript rendering, crawl-to-crawl comparison and link-graph visualisation (yes, listed under Roadmap).
- GitHub verification (2026-10-04): api.github.com answered HTTP 403 ("GitHub access to this repository is not enabled for this session"), so stars, pushed_at and topics were not retrieved. README fetched fine via raw.githubusercontent.com (308 lines) and is stored verbatim in the raw file. README author: Sean Ryan (describes himself as a Lead Marketing Engineer); this is not the Threads poster.
- Install, copied verbatim from the README (NOT run): `npm i -g crawlie` (installs the `crawlie` CLI and the `crawlie-mcp` server). From source it needs Rust: `cargo build --release`.
- CLI commands from the README: `crawlie crawl https://example.com --format pretty`, `crawlie audit https://example.com/pricing`, `crawlie crawl https://example.com --format html -o report.html`, `crawlie crawl https://example.com --format json -o report.json`, `crawlie explain geo-not-answerable`. Flags include `--max-pages` (default 500), `--max-depth`, `--concurrency` (default 16), `--include` / `--exclude`, `--no-robots`, `--severity`, `--save`, `--fail-on error|warning`.
- MCP from the README: Claude Code `claude mcp add crawlie crawlie-mcp`; Claude Desktop config `{"mcpServers": {"crawlie": {"command": "crawlie-mcp"}}}`; any stdio MCP client works. Tools: `crawl_site`, `audit_url`, `audit_urls`, `explain_issue`, `list_rules`, `list_reports`, `get_report`. Claude Code plugin: `claude plugin marketplace add spronta/crawlie` then `claude plugin install crawlie@spronta`.
- Hosted option (closed source): Crawlie Cloud MCP at `https://crawlie.app/mcp` needs a Crawlie API key and is metered against a plan. The local tools do not need any key.
- README check areas: technical SEO, performance and security, accessibility (WCAG), mobile / international / social, structured-data validation, JavaScript rendering with `--render` (headless Chrome), and GEO signals.
- Open question: the README documents `--render`, yet its Roadmap lists JavaScript rendering for SPA-heavy sites and the poster says SPA rendering is not built. Test on a client-side-rendered page before relying on it.
- README's comparison table against Screaming Frog and Sitebulb is the author's own marketing claim, not independently checked.
- Engagement is low: 4 likes, 7 shares, 434 views; Threads hides zero counts, so replies and reposts are 0 (order inferred from Threads UI).
- A draft skill was written from the README: `skills/auditing-seo-with-crawlie/SKILL.md`.

## 點解值得留意

- **客戶 SEO／GEO 審核工具**：Josep 做 SEO／GEO，crawlie 免費、跑本機、可出 HTML／JSON 報告，可以補充或取代付費爬蟲嚟降低交付成本；同 vault 內 OpenSEO、Jev 審核成本兩篇互補。
- **Agent 自己審站**：MCP server 令 Claude Code 可以自己 crawl、讀 issue、列出修正清單，啱用喺「AI 生成網站上線前檢查」呢類中小企服務；已草擬 skill `auditing-seo-with-crawlie`（draft，仍要經 skill-review）。
- **三個分數分開報**：Health、GEO、Accessibility 分開，方便向香港中小企客戶解釋「搜尋引擎排名」同「AI 搜尋可見度」係兩件事，亦可做 baseline、修正、重測嘅前後對比。
- **風險要記住**：只爬自己或客戶授權嘅網站；Crawlie Cloud 閉源兼要 API key，客戶網站唔好隨便交俾第三方；帖文互動低，真正值得睇嘅係 repo 本身，星數未核實前唔好當成熟工具介紹。

## Source

- Post: https://www.threads.com/@arumwu/post/DeD1c2yEoBW
- Author: @arumwu (display name 私は Arum です™) · Published: 2026-10-04
- Engagement: likes=4 replies=0 reposts=0 shares=7 views=434 (order inferred from Threads UI; zero counts are not displayed)
- Reader: Jina Reader (r.jina.ai) for the post; caption line breaks and the final repo link read from the share-page HTML; GitHub README via raw.githubusercontent.com (api.github.com 403)
- Share URL: https://www.threads.com/share/BAPkw4EzcM/
- Repo: https://github.com/spronta/crawlie
- Not captured: "Related threads" by other accounts; the author posted no replies under this post

## Related

- [[../pages/20260930-openseo-open-source-semrush-alternative|OpenSEO: self-hosted open-source Semrush alternative]] — another open-source SEO tool in the same topic/seo-geo
- [[../pages/20260925-jev-seo-geo-audit-cost-down-90|Jev cuts agent SEO/GEO audit-and-fix cost by 90%]] — agent-driven SEO/GEO audit over MCP, the cost side of the same service
- [[../../skills/auditing-seo-with-crawlie/SKILL|skill: auditing-seo-with-crawlie]] — draft skill written from this capture
