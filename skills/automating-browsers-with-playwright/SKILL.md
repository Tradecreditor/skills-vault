---
name: automating-browsers-with-playwright
description: Connects an agent to a real browser via the Playwright MCP server, driving pages through structured accessibility snapshots instead of screenshots. Use when asked to browse, click, fill forms, or test a web page without a vision model.
metadata:
  source_url: "https://github.com/microsoft/playwright-mcp"
  source_platform: github
  author: "Microsoft"
  captured_at: "2026-09-21T23:07:37Z"
  engagement: "stars=37448 forks=3183"
  origin_type: "repo"
  vault_status: "draft"
---

# automating-browsers-with-playwright

Draft, unreviewed. Wraps `microsoft/playwright-mcp`, an MCP server exposing Playwright browser automation to any MCP client. Requires Node.js 18+.

## When to use MCP vs the CLI
Microsoft's own README steers coding agents (Claude Code, Codex) toward the sibling project [`microsoft/playwright-cli`](https://github.com/microsoft/playwright-cli) (CLI + Skills) instead: CLI invocations are more token-efficient because they skip loading large tool schemas and full accessibility trees into context. Reach for this MCP server instead when the task needs persistent browser state across many turns — exploratory automation, self-healing tests, long-running autonomous workflows — where continuity outweighs token cost.

## Install (Claude Code)
```
claude mcp add playwright npx @playwright/mcp@latest
```
Standard MCP config for other clients (VS Code, Cursor, Windsurf, Claude Desktop, Goose, Grok, Junie, …):
```json
{
  "mcpServers": {
    "playwright": {
      "command": "npx",
      "args": ["@playwright/mcp@latest"]
    }
  }
}
```

## Why it's fast
Uses Playwright's accessibility tree, not pixel/screenshot input — no vision model needed, and tool application is deterministic (no ambiguity from interpreting a screenshot).

## Useful flags
Passed inside the config's `"args"` list (each also has a `PLAYWRIGHT_MCP_*` env var):
- `--browser <chrome|firefox|webkit|msedge>` — engine to use
- `--headless` — headless mode (headed by default)
- `--device "<name>"` / `--mobile` — emulate a specific device or a generic mobile device (lighter pages, fewer tokens)
- `--caps <vision,pdf,devtools>` — enable extra capabilities
- `--allowed-origins` / `--blocked-origins` — origin allow/block lists (not a security boundary; doesn't affect redirects)
- `--allow-unrestricted-file-access` — lift the default restriction to workspace-root files and `file://` URLs
- `--cdp-endpoint <url>` — connect to an existing browser over CDP instead of launching one
- `--codegen <typescript|python|java|csharp|none>` — generate reusable automation code alongside the run

## Notes
- Origin allow/block lists and `--ignore-https-errors` are explicitly not security boundaries per the README — don't rely on them to sandbox untrusted sites.
- `--idle-timeout` closes an idle headless browser (default 1h); headed browsers never auto-close unless set to 0/disabled.
