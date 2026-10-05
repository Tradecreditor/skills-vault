---
slug: 20261004-crawlie-open-source-seo-geo-crawler-mcp
source_url: "https://www.threads.com/@arumwu/post/DeD1c2yEoBW"
canonical_id: "threads:DeD1c2yEoBW"
fetched_at: "2026-10-04T21:00:18Z"
reader: "jina"
---
{"author": "@arumwu", "author_name": "私は Arum です™", "platform": "threads", "published": "2026-10-04", "published_note": "date as given by the caller; the share page showed '15h' at fetch time and the post id DeD1c2yEoBW decodes to 2026-10-04T05:01:18Z", "engagement": {"likes": 4, "replies": 0, "reposts": 0, "shares": 7, "views": 434}, "engagement_order": "Threads hides zero counts: the pages showed only two bare numbers (4 and 7) plus '434 views'. likes=4 and shares=7 follow the caller's assignment (order inferred from Threads UI); replies=0 and reposts=0 are inferred from their absence", "post_url": "https://www.threads.com/@arumwu/post/DeD1c2yEoBW", "share_url": "https://www.threads.com/share/BAPkw4EzcM/", "author_replies": "none found in the share-page HTML", "text_note": "text is the caption stored in the share-page HTML JSON (original line breaks and bullets); the Jina clean-shape text is identical except that it flattens the line breaks and omits the final link line. The share-page shape shows that last line as a link card 'github.com/spron…' that points to github.com/spronta/crawlie. 434 views come from the share-page shape."}

Post 1 — @arumwu (https://www.threads.com/@arumwu/post/DeD1c2yEoBW):

用 AI 飛快生出網站，結果大半沒被搜尋引擎跟 AI 找到——crawlie 就是專門抓這件事的。

crawlie 是一套免費、開源、跑在本機的技術 SEO + GEO 爬蟲，附 CLI 跟 MCP server，讓 AI agent 自己能審站。

最有感的幾個：
• 57 條檢查規則：壞連結、4xx/5xx、redirect 鏈、title／description 缺漏或重複、canonical、noindex、漏 alt
• 每次爬取給三個分數：Health（技術 SEO）、GEO（AI 搜尋可引用度）、Accessibility（WCAG）
• 每個問題都附白話說明：為什麼重要、怎麼修、不管它會怎樣；JSON／HTML 報告能直接丟 CI 或給客戶

授權 MIT，引擎、CLI、MCP、桌面 App 全開源。作者也明講：Crawlie Cloud（託管爬取服務與官網）是另一個閉源產品，不在這個 repo；roadmap 的雲端 worker、SPA 渲染、跨次爬取比對、連結圖也都還沒做。

github.com/spronta/crawlie

[link card: github.com/spron… -> github.com/spronta/crawlie]

4

7

434 views

## GitHub (api, 2026-10-04)

Repo named in the post: https://github.com/spronta/crawlie

api.github.com (curl -s https://api.github.com/repos/spronta/crawlie, 2026-10-04T21:06Z) answered HTTP 403 in this cloud session, so stars, license metadata, pushed_at and topics were NOT retrieved. Response body:

{"message":"GitHub access to this repository is not enabled for this session. Use add_repo to request access. If add_repo answers that read access is already available and you need GitHub API or write access, call add_repo again with access:\"push\" to attach the repository with credentials.","documentation_url":"https://docs.anthropic.com/en/docs/claude-code/github-actions"}

README.md fetched from https://raw.githubusercontent.com/spronta/crawlie/HEAD/README.md (HTTP 200, 308 lines, 2026-10-04T21:06Z), verbatim:

~~~~markdown
<div align="center">

# crawlie

**The fast, free, open-source technical SEO + GEO crawler — built for humans and agents.**

Crawl any site for broken links, redirects, missing metadata, and 40+ SEO & Generative-Engine checks — with plain-English guidance on every fix. Runs locally, ships a CLI and an MCP server, and costs nothing.

[![npm](https://img.shields.io/npm/v/crawlie?color=cb3837&logo=npm&label=crawlie)](https://www.npmjs.com/package/crawlie)
[![CI](https://github.com/spronta/crawlie/actions/workflows/ci.yml/badge.svg)](https://github.com/spronta/crawlie/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

<p>
  <a href="#setup">Setup</a> ·
  <a href="#how-to-use-cli">CLI</a> ·
  <a href="#use-with-agents-mcp">MCP &amp; agents</a> ·
   <a href="https://crawlie.dev/changelog" target="_blank">Changelog</a> ·
  <a href="#use-cases">Use cases</a> ·
  <a href="#why-i-built-this">Why I built this</a> ·
  <a href="#desktop-app">Desktop app</a> ·
  <a href="#what-it-checks">Checks</a> ·
  <a href="#how-it-compares">Compare</a> ·
  <a href="#architecture">Architecture</a>
</p>

*[Read the docs → crawlie.dev](https://crawlie.dev/docs)* 

[💡Share feedback & suggestions here](https://github.com/spronta/crawlie/discussions/2)

</div>

![Showcase of the example app demonstrating a report](https://cdn.spronta.com/spronta-8d32a2/pretty_snap_2026_5_18_23_58%20(2).png)

---

## Setup

**The easy way — npm** (installs the `crawlie` CLI and the `crawlie-mcp` server):

```bash
npm i -g crawlie
```

**The macOS app** — grab the signed `.dmg` from [Releases](https://github.com/spronta/crawlie/releases).

**From source** — needs [Rust](https://rustup.rs) (engine/CLI/MCP) and, for the desktop app, [pnpm](https://pnpm.io) + Node:

```bash
git clone https://github.com/spronta/crawlie
cd crawlie
cargo build --release
# → target/release/crawlie  and  target/release/crawlie-mcp

# or install onto your PATH:
cargo install --path crates/crawlie-cli      # installs `crawlie`
cargo install --path crates/crawlie-mcp      # installs `crawlie-mcp`
```

> **How it ships:** the **CLI + MCP** come *only* through npm — the right native binary installs automatically as a platform package (nothing to download or unblock). The **desktop app** is the only direct download: a signed, notarized `.dmg` on [Releases](https://github.com/spronta/crawlie/releases).

---

## How to use (CLI)

```bash
# Crawl a whole site (respects robots.txt, seeds from sitemap.xml)
crawlie crawl https://example.com --format pretty

# Audit a single page, or a specific set of pages
crawlie audit https://example.com/pricing
crawlie audit https://example.com/a https://example.com/b

# Save a shareable, self-contained HTML report
crawlie crawl https://example.com --format html -o report.html

# Clean JSON on stdout (perfect for piping / scripting / agents)
crawlie crawl https://example.com --format json -o report.json

# Learn why any finding matters and how to fix it
crawlie explain geo-not-answerable
```

**Output formats:** `pretty` (terminal), `json` (machine-readable, the default), `csv` (issues), `html` (shareable file).

**Common flags:**

| Flag | What it does |
|---|---|
| `--max-pages <n>` | Cap pages fetched (default 500) |
| `--max-depth <n>` | Max click depth from the seed |
| `--concurrency <n>` | Parallel requests (default 16) |
| `--include <glob>` / `--exclude <glob>` | Scope the crawl by URL pattern |
| `--no-robots` / `--no-sitemap` / `--no-external` | Turn off robots.txt, sitemap seeding, external link checks |
| `--severity error\|warning\|notice` | Only output findings at/above a level |
| `--save` | Save to local report history (`crawlie reports`, `crawlie report <id>`) |
| `--fail-on error\|warning` | Non-zero exit code for CI gating |

Every crawl returns three scores: a **Health** score (technical SEO), a **GEO** score (AI-search readiness), and an **Accessibility** score (WCAG conformance) — each reported separately so one kind of problem never hides another.

---

## Use with agents (MCP)

crawlie ships a [Model Context Protocol](https://modelcontextprotocol.io) server so an LLM agent can run a full audit and act on it — no human in the loop. This is the part most SEO tools don't have.

### Connect it

After `npm i -g crawlie`, `crawlie-mcp` is on your `PATH`. For **Claude Desktop**, edit `claude_desktop_config.json`:

```jsonc
{
  "mcpServers": {
    "crawlie": {
      "command": "crawlie-mcp"
    }
  }
}
```

For **Claude Code**:

```bash
claude mcp add crawlie crawlie-mcp
```

(If you built from source instead, use the absolute path to `target/release/crawlie-mcp`.)

(Any MCP-compatible client works — Cursor, Cline, your own agent. It speaks JSON-RPC over stdio.)

### Hosted: the Crawlie Cloud MCP (no install)

Prefer not to install anything, or want crawls to run on our infrastructure? Point any MCP client at the hosted endpoint and authenticate with a Crawlie API key (create one in the dashboard under Settings, API keys). It speaks MCP Streamable HTTP.

**Endpoint:** `https://crawlie.app/mcp`

For **Claude Code**:

```bash
claude mcp add --transport http crawlie-cloud https://crawlie.app/mcp \
  --header "Authorization: Bearer crw_your_key"
```

For **Claude Desktop** (or any client that takes a JSON config):

```jsonc
{
  "mcpServers": {
    "crawlie-cloud": {
      "type": "http",
      "url": "https://crawlie.app/mcp",
      "headers": { "Authorization": "Bearer crw_your_key" }
    }
  }
}
```

Hosted crawls run on the same engine as the dashboard, are scoped to your team, and are metered against your plan. The tools mirror the local server (`crawl_site`, `audit_url`, `top_fixes`, `geo_gaps`, `affected_urls`, `diff_reports`, plus `crawl_status` to poll a long crawl and `get_report` / `list_reports` over your saved cloud reports). Every crawl returns a `reportId` you can re-slice later without re-crawling.

### One-step install: the Claude Code plugin

The fastest path. The [`crawlie` plugin](.claude-plugin/plugin.json) bundles the MCP server **and** a set of skills (audit playbooks) in a single install — the MCP server auto-runs via `npx`, so you don't even pre-install the binary:

```bash
# add this repo as a marketplace, then install the plugin
claude plugin marketplace add spronta/crawlie
claude plugin install crawlie@spronta
```

### Skills (works with *any* agent, even without the MCP)

The [`skills/`](skills/) folder holds standalone [Agent Skills](https://agentskills.io) that teach an agent how to run real audits — full-site SEO + GEO, broken-link fixes, pre-launch gates, and AI-search readiness. Each is **self-contained**: it needs neither this repo nor a pre-installed crawlie. Missing the binary? The skill runs it on demand via `npx -y -p crawlie …` (the install *is* the run), and automatically uses the MCP tools when they're present. See [skills/README.md](skills/README.md).

### Tools exposed

| Tool | Purpose |
|---|---|
| `crawl_site` | Crawl + audit a whole site (SEO + GEO), returns scores, issues, per-page data |
| `audit_url` | Audit a single page |
| `audit_urls` | Audit an explicit list of pages |
| `explain_issue` | Why a rule matters + how to fix it |
| `list_rules` | The full catalogue of checks |
| `list_reports` / `get_report` | Read saved crawl history |

### Example agent prompts

> *"Crawl crawlie.dev, then give me the top 5 fixes that would most improve my GEO score, with the exact change for each."*

> *"Audit these three landing pages and tell me which is least ready to be cited by AI search, and why."*

> *"Run a crawl with `--fail-on error` semantics — are there any broken links or 5xx pages blocking launch?"*

The agent calls `crawl_site`, reads the structured issues, and uses `explain_issue` to turn findings into a prioritized, actionable plan.

---

## Use cases

- **Pre-launch QA** — catch broken links, redirects, 4xx/5xx, and missing metadata before you ship.
- **GEO optimization** — make pages citable by AI search: structured data, semantic HTML, answer-ready content, authorship/E-E-A-T.
- **Agent workflows** — let a marketing/SEO agent audit a site and propose fixes autonomously via MCP.
- **CI/CD gating** — `crawlie crawl … --fail-on error` in a pipeline to block regressions.
- **Client reporting** — generate a polished, shareable HTML report in one command.
- **Auditing AI-generated sites** — verify that the site your agent just built is actually built for search.

---

## Why I built this

I'm **Sean Ryan**. I've spent 6+ years as a Lead Marketing Engineer, and on the side I build AI tooling for marketers.

With AI, it's faster than ever to ship a marketing site — but most of what gets generated is slop that was never built to be found. And the tools meant to catch that fall short: most SEO auditors cost money, don't play nicely with your agents, or tell you *what's* wrong without telling you *how to actually rank* for SEO **and** GEO (Generative Engine Optimization — being cited by AI search like ChatGPT, Perplexity, and Google AI Overviews).

crawlie fixes that. It's free, it's local-first, it's agent-native, and every issue it finds comes with *why it matters* and *how to fix it*.

**If this is useful to you, [connect with me on LinkedIn →](https://linkedin.com/in/sean-exe)** — I share what I'm learning building AI for marketers and SEO/GEO tooling, and I'd love to hear how you're using crawlie.

---

## Desktop app

A beautiful Tauri + React app (Geist design, light/dark, seamless window chrome):

```bash
cd apps/desktop
pnpm install
pnpm tauri dev          # live native crawls
pnpm dev                # preview the UI in a browser (demo data, no backend)
```

Whole-site / single-page / URL-list modes, live progress, **Health**, **GEO** & **Accessibility** score rings, issues with built-in *why-it-matters* guidance, a sortable pages table, a per-page drawer (GEO signals, headers, schema, hreflang…), auto-saved report history, and one-click shareable HTML export.

> First run, generate the icon set: `cd src-tauri/icons && python3 generate.py && cd .. && pnpm tauri icon icons/source.png`

---

## What it checks

*57 rules and counting.*

**Technical SEO** — broken links · 4xx/5xx · redirects & chains · titles & meta descriptions (missing / duplicate / length) · H1s · canonicals · noindex / nofollow / X-Robots-Tag · robots.txt blocking · images missing alt · thin & duplicate content · orphan & deep pages

**Performance & security** — slow responses · large pages · missing compression · HTTPS · mixed content · HSTS

**Accessibility (WCAG)** — links & buttons without an accessible name · form controls without a label · iframes missing a title · zoom-blocking viewport · positive `tabindex` · skipped heading levels

**Mobile, international & social** — viewport · `lang` · hreflang · Open Graph · Twitter cards · structured data

**Structured-data validation** — parses JSON-LD and checks each item against Google's rich-result requirements: invalid markup, missing required fields, and missing recommended fields (Product, Article, Recipe, Event, FAQ, Breadcrumb, and more)

**JavaScript rendering** — crawl with `--render` to audit each page's post-JavaScript DOM via headless Chrome, so client-rendered content (React/Next/Vue) is seen, and `content-requires-js` flags pages whose content only exists after JS runs

**GEO — Generative Engine Optimization** — structured data, semantic HTML, answer-readiness, authorship/E-E-A-T, dated content, question-style headings, and extractable blocks, rolled into a per-page **GEO score**.

Every finding links to plain-English guidance: **why it matters**, **how to fix it**, and **what happens if you ignore it**.

---

## How it compares

| | **crawlie** | Screaming Frog | Sitebulb |
|---|:---:|:---:|:---:|
| Price | **Free & open-source** | £259/yr to unlock | from £13.50/mo |
| Engine | **Rust, async, tiny binary** | Java (JVM) | .NET |
| CLI with JSON output | ✅ | partial | ❌ |
| JavaScript rendering | ✅ headless Chrome | ✅ | ✅ |
| **MCP server (agent-native)** | ✅ | ❌ | ❌ |
| **GEO — AI/answer-engine audit** | ✅ | ❌ | ❌ |
| **"Why it matters" built in** | ✅ every issue | ❌ | partial |
| Shareable HTML report | ✅ | paid | ✅ |
| Source you can read & extend | ✅ | ❌ | ❌ |

---

## Architecture

```
crates/
  crawlie-core    # the engine — crawl, audit, score, knowledge base, reports
  crawlie-cli     # `crawlie` — JSON / pretty / CSV / HTML output
  crawlie-mcp     # `crawlie-mcp` — Model Context Protocol server (stdio)
apps/
  desktop         # Tauri v2 + React (Geist) desktop app
```

`crawlie-core` has zero host dependencies — the same audited engine drops straight into a cloud worker (it already targets `wasm32`). One engine, every surface, identical results.

---

## Roadmap

- Cloud workers (shared Rust core) for scheduled/remote crawls
- JavaScript rendering for SPA-heavy sites
- Crawl-to-crawl comparison & regression alerts
- Internal-link graph visualization

---

## License & author

**MIT** © **[Spronta Ltd](https://crawlie.dev)** — the crawler engine, CLI, MCP
server, and desktop app: everything in this repository is MIT. Crawlie Cloud (the
hosted crawl service and the marketing site) is a separate, closed-source product
and is not part of this repository. Pull requests to the open engine, CLI, and
desktop app are very welcome.

Built by Sean Ryan — Lead Marketing Engineer at Pendo.io, building AI for marketers on the side. **[Connect on LinkedIn →](https://linkedin.com/in/sean-exe)**

If crawlie saves you time, a ⭐ on the repo and a hello on LinkedIn mean a lot.
~~~~
