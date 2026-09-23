---
source_url: "https://github.com/zai-org/ZCode"
captured_at: "2026-09-23T01:18:14Z"
captured_by: "routine:weekly-hot-list"
reader_used: "exa web_fetch_exa"
---

# zai-org/ZCode

Z.ai's coding agent harness. Powerful, intelligent, extensible.

- Stars: 6302
- Forks: 1832
- Watchers: 6302
- Open issues: 11
- License: Apache License 2.0
- Homepage: https://zcode.z.ai/
- Default branch: main
- Created: 2026-09-20T12:01:16Z

## Languages

C#, CMake, CSS, Dockerfile, HTML, JavaScript, NSIS, Shell, Swift, TypeScript

## Top Contributors

- MBearo (1 contribution)
- zRzRzRzRzRzRzR (1 contribution)

---

## README (translated highlights; original is Simplified Chinese / English bilingual)

ZCode is an AI coding workbench shipping a desktop app, a browser UI, and a terminal agent. This repository holds the client, backend service, shared UI, and the Agent CLI/runtime source.

| Entry point | Purpose | Dev command |
| --- | --- | --- |
| Desktop | Electron desktop app | `pnpm dev:desktop` |
| Web / ZCode CLI build | Terminal + browser workbench; bundles TUI, Web, backend and Agent into a standalone release | `pnpm dev:web` |
| Agent CLI | `zcode` on the terminal; also the Agent runtime for Desktop and Web | `pnpm --filter @zcode/cli dev` |

Setup: Git, Node.js 24.14.0, pnpm 10.33.2 (see mise.toml), then `pnpm bootstrap`.

Repo layout: `packages/desktop` (Electron), `packages/web` (web client), `packages/server` (HTTP/WebSocket + remote connections), `packages/ui` (shared React components/hooks/Zustand state), `packages/services`, `packages/shared`/`rpc`/`client` (shared protocol, RPC framework, Agent client SDK), `packages/provider`(-node), `apps/zcode-cli` (Agent CLI, TUI, runtime, tools).

The CLI build ships a single `zcode` binary: no args opens a TUI; `--web` opens a browser UI proxying to a local backend; other args pass through to the Agent CLI.

Note: this GitHub repository (zai-org/ZCode, created 2026-09-20) is the newly-public source for the ZCode product; Z.ai's ZCode desktop app itself was first announced publicly in July 2026 as "the official development environment for GLM-5.2/5.3" — this week's news is the source going up on GitHub and its rapid star growth, not the product's original launch.

---

## Verified engagement (source-of-record numbers)

GitHub (mcp__github__search_repositories / web_fetch_exa on github.com, live 2026-09-23T01:1xZ):
- stargazers_count: 6302, forks_count: 1832, open_issues_count: 11
- created_at: 2026-09-20T12:01:16Z (3 days old at time of capture; repo is topical — description itself says "coding agent harness")

No X or Threads post specific to this GitHub repository/release was found with a resolvable status link within the routine's search budget; coverage found (LinkedIn, VentureBeat, Business Insider, TechieTricks, Let's Data Science, PithWire, Digital Applied) is all about the July 2026 ZCode 3.0 product launch, not this GitHub repo. Not used as an X/Threads gate signal.
