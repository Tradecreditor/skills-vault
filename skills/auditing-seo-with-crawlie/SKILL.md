---
name: auditing-seo-with-crawlie
description: Runs crawlie, an open-source local SEO + GEO crawler with CLI and MCP server, to audit a site's technical SEO, AI-search citability and WCAG accessibility and return fixes. Use when asked for an SEO audit, GEO score, site health check, or to wire an SEO crawler into an agent.
metadata:
  source_url: "https://www.threads.com/@arumwu/post/DeD1c2yEoBW"
  source_platform: "threads"
  author: "@arumwu"
  captured_at: "2026-10-04T21:09:15Z"
  engagement: "likes=4 replies=0 reposts=0 shares=7 views=434"
  origin_type: "post"
  vault_status: "draft"
---

# auditing-seo-with-crawlie

Crawl a site with crawlie (free, MIT, runs locally, ships a CLI and an MCP server), read its three scores, and turn the findings into a prioritised fix list. Commands below are copied from the crawlie README (github.com/spronta/crawlie) and were not run when this skill was drafted.

## When to use

- Pre-launch or post-build QA of a site, especially one an AI tool generated: broken links, 4xx/5xx, redirect chains, missing or duplicate titles and descriptions, canonicals, noindex, images without alt.
- A GEO check (is the page easy for AI search to cite) alongside classic technical SEO, for a client or for your own site.
- A WCAG-style accessibility pass in the same crawl.
- A CI gate that fails on new SEO errors, or a client-ready HTML/JSON report.
- Wiring an SEO crawler into Claude Code or another MCP client so the agent can audit and propose fixes itself.

## Prerequisites

- Node.js and npm. The README says the CLI and MCP server ship only through npm; the right native binary installs as a platform package.
- Permission to crawl the target: your own site, or a client site you are hired to audit.
- No API key is needed for local mode. Do not use the hosted Crawlie Cloud unless the client has agreed (see Pitfalls).
- Optional: Claude Code, for the `claude mcp add` and plugin commands.

## Steps

### 1. Check the package, then install

Confirm the npm package `crawlie` links back to github.com/spronta/crawlie before installing (look-alike package names are a common npm risk).

```bash
npm i -g crawlie
```

Installs two binaries: the `crawlie` CLI and the `crawlie-mcp` server.

### 2. Crawl or audit

```bash
crawlie crawl https://example.com --format pretty
```

Crawls the whole site (respects robots.txt, seeds from sitemap.xml) and prints a readable report in the terminal.

```bash
crawlie audit https://example.com/pricing
crawlie audit https://example.com/a https://example.com/b
```

Audits one page, or an explicit list of pages, without crawling the rest.

```bash
crawlie crawl https://example.com --format html -o report.html
crawlie crawl https://example.com --format json -o report.json
```

Writes a self-contained shareable HTML report, or machine-readable JSON (the default format) for scripts and agents. A `csv` format lists issues only.

```bash
crawlie explain geo-not-answerable
```

Prints why a rule matters and how to fix it (`geo-not-answerable` is the README's example rule id).

Useful flags (README table): `--max-pages <n>` (default 500), `--max-depth <n>`, `--concurrency <n>` (default 16), `--include <glob>` / `--exclude <glob>`, `--severity error|warning|notice`, `--save` (keeps local history for `crawlie reports` and `crawlie report <id>`), `--fail-on error|warning` (non-zero exit for CI).

### 3. Read the three scores

Every crawl returns three separate scores so one kind of problem never hides another:

1. Health: technical SEO (links, status codes, redirects, metadata, canonicals, robots, thin or duplicate content).
2. GEO: AI-search readiness (structured data, semantic HTML, answer-ready content, authorship, dated content, question-style headings).
3. Accessibility: WCAG-style checks (names for links and buttons, form labels, iframe titles, heading order).

Each finding carries why it matters, how to fix it, and what happens if ignored. Fix errors first, then warnings, then GEO gaps. Report to the person: the three scores, the top five fixes with the exact change for each, and the list of affected URLs.

### 4. Gate CI (optional)

```bash
crawlie crawl https://example.com --fail-on error
```

Exits non-zero when error-level findings exist, so a pipeline can block a release. The README shows this as `crawlie crawl ... --fail-on error`.

### 5. Wire the MCP server into an agent

Claude Code:

```bash
claude mcp add crawlie crawlie-mcp
```

Registers the local stdio server (after `npm i -g crawlie`, `crawlie-mcp` is on PATH).

Claude Desktop, in `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "crawlie": {
      "command": "crawlie-mcp"
    }
  }
}
```

Codex and other clients: the README gives no Codex-specific snippet. It says any MCP-compatible client works (Cursor, Cline, your own agent) and that the server speaks JSON-RPC over stdio, so register a stdio server whose command is `crawlie-mcp` using that client's own MCP configuration.

Tools exposed: `crawl_site` (whole site, returns scores, issues, per-page data), `audit_url`, `audit_urls`, `explain_issue`, `list_rules`, `list_reports`, `get_report`.

Example agent prompt from the README: "Crawl crawlie.dev, then give me the top 5 fixes that would most improve my GEO score, with the exact change for each."

One-step alternative for Claude Code: the plugin bundles the MCP server and audit-playbook skills, and the MCP server auto-runs via npx:

```bash
claude plugin marketplace add spronta/crawlie
claude plugin install crawlie@spronta
```

Adds the repo as a marketplace, then installs the `crawlie` plugin from it.

## Pitfalls

- Crawlie Cloud (hosted crawling service, dashboard, website and the hosted MCP endpoint that needs an API key and is metered) is a separate closed-source product, not part of the MIT repo. Use local mode for client work unless the client has agreed to a third party crawling their site. Never write an API key into a file or a prompt.
- Roadmap items are not built yet: cloud workers, JavaScript rendering for SPA-heavy sites, crawl-to-crawl comparison and regression alerts, internal-link graph. The README also documents a `--render` flag (headless Chrome) in its checks section, so run `crawlie crawl --help` and test on a client-side-rendered page before promising SPA coverage.
- The default crawl respects robots.txt. Do not pass `--no-robots` on a site you do not own or are not hired to audit. Lower `--concurrency` for small or shared hosting; the default is 16 parallel requests and 500 pages.
- The README says "40+ checks" in its intro and "57 rules" in its checks section; the Threads post says 57. Treat the number as approximate.
- Scores are heuristics. A high GEO score does not guarantee that ChatGPT, Perplexity or Google AI Overviews will cite the page.
- Stars, release cadence and maintenance were not verified (the GitHub API was blocked when this was captured). Check the repo before recommending it to a client.
- The desktop app is a signed macOS `.dmg` from GitHub Releases; the CLI and MCP do not need it.

## Source

- Threads post by @arumwu: https://www.threads.com/@arumwu/post/DeD1c2yEoBW (2026-10-04)
- Repo and README: https://github.com/spronta/crawlie (MIT, Spronta Ltd; README author Sean Ryan)
- Vault note: wiki/pages/20261004-crawlie-open-source-seo-geo-crawler-mcp.md and raw/20261004-crawlie-open-source-seo-geo-crawler-mcp.md (README verbatim)
