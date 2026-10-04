---
title: "Backlog.md: Markdown-native Task Manager and Kanban for AI Agents"
slug: 20261004-backlog-md-markdown-kanban-for-agents
type: repo
status: draft
source_url: "https://github.com/MrLesk/Backlog.md"
source_platform: github
author: "MrLesk"
published: "2026-09-24"
captured_at: "2026-10-04T21:22:27Z"
captured_by: "claude-code-cloud"
canonical_id: "github:MrLesk/Backlog.md"
engagement: "stars=6.9k forks=441"
tags: [kanban, task-management, markdown, agents, claude-code, codex, gemini-cli, mcp, cli, obsidian]
related: [skills/tracking-tasks-with-backlog-md, skills/keeping-handoff-docs, 20260918-obsidian-skills, skills/using-obsidian-skills, stars/Fission-AI--OpenSpec, skills/scanning-agent-skills]
needs_manual_text: false
---

## 摘要

Backlog.md 是一個開源（MIT）、以 Markdown 為核心的任務管理工具兼 Kanban 看板，可以把任何 Git 倉庫（或一個普通資料夾）變成自足的專案看板。每一項任務都是倉庫內一個獨立的 `.md` 檔案（附 YAML frontmatter），所以任務會跟程式碼一同進 Git，亦可以直接放進 Obsidian vault，用一般 Markdown 工具閱讀和搜尋。它提供 CLI（`backlog task ...`）、終端機 Kanban（`backlog board`）、只綁定本機 `127.0.0.1` 的網頁看板（`backlog browser`），以及可選的 MCP 伺服器。專為 Claude Code、Codex、Gemini CLI（亦支援 Kiro）等 AI agent 設計：agent 先把想法拆成任務、寫驗收條件和實作計劃，人先審閱 spec 與 plan 才開始寫程式，貫徹「一個任務 = 一個 context window = 一個 PR」。README 同時強調本機優先：沒有伺服器、帳戶或 telemetry。

## Key facts

- **What it is:** "Markdown-native Task Manager & Kanban visualizer for any Git repository"; tagline "AI agents write the code. You review the tasks: before, during, and after." MIT licence. npm package `backlog.md`, binary `backlog`.
- **Install (copied from README):**
  ```bash
  npm i -g backlog.md
  # or: bun add -g backlog.md
  # or: brew install backlog-md
  # or: nix run github:MrLesk/Backlog.md
  ```
- **One-off with npx:** `npx backlog.md init "My Project"` and `npx backlog.md board`. Plain `npx backlog` resolves to an unrelated third-party npm package, not this tool.
- **Init:** `backlog init "My Awesome Project"`; without Git: `backlog init "Personal Planning" --no-git` (saved config forces `checkActiveBranches=false`, `remoteOperations=false`, `autoCommit=false`). Other documented init flags: `--task-prefix`, `--defaults`, `--agent-instructions`, `--backlog-dir <path>`, `--config-location <folder|root>`.
- **Init wizard asks how to connect AI tools:** CLI instructions (recommended; writes a short instruction file telling agents to run `backlog instructions overview`; non-interactive default target is AGENTS.md), MCP connector (auto-configures Claude Code, Codex, Gemini CLI, Kiro or Cursor), or Skip.
- **Board:** `backlog board` (live terminal Kanban), `backlog board export [file]` (shareable markdown). **Web UI:** `backlog browser` (listens on `127.0.0.1`, default port 6420), `backlog browser --port 8080`, `backlog browser --no-open`.
- **MCP setup (README):** `claude mcp add backlog --scope user -- backlog mcp start` · `codex mcp add backlog -- backlog mcp start` · `gemini mcp add backlog -s user backlog mcp start` · `kiro-cli mcp add --scope global --name backlog --command backlog --args mcp,start`. Manual JSON uses `"command": "backlog"`, `"args": ["mcp", "start"]` and optional `BACKLOG_CWD`. The project's MANIFESTO calls MCP "a legacy, optional adapter" and the CLI "canonical".
- **Agent workflow:** `backlog instructions overview`, then `task-creation`, `task-execution`, `task-finalization` guides. Three human review checkpoints: spec (tasks + acceptance criteria), plan (written into the task before coding), code (one task = one PR).
- **Task file layout:** plain `.md` files in a project-local backlog folder (`backlog/`, `.backlog/` or a custom `backlog_directory` set in `backlog.config.yml`). In the project's own repo they sit in `backlog/tasks/` as `back-697 - Keep-the-Nix-AVX2-check-independent-of-the-selected-Bun-package.md`; default ID prefix gives `TASK-1`-style IDs, `backlog init --task-prefix` changes it (this repo uses `back`).
- **Frontmatter observed in one sample task file (BACK-697, not a documented spec):** `id`, `title`, `status` (default columns To Do / In Progress / Done), `assignee` (list), `created_date`, `updated_date`, `labels`, `dependencies`, `references`, `modified_files`, `type`, `ordinal`. Body uses marker comments: `<!-- SECTION:DESCRIPTION:BEGIN -->`, `<!-- AC:BEGIN -->` (checklist `- [x] #1 ...`), `<!-- DOD:BEGIN -->`, `<!-- SECTION:PLAN:BEGIN -->`, `<!-- SECTION:NOTES:BEGIN -->`, `<!-- SECTION:FINAL_SUMMARY:BEGIN -->`.
- **Edit through the CLI, not by hand:** the README says to prefer Backlog.md commands (CLI/MCP/Web) over hand-editing task files so field types and metadata stay consistent. Stable JSON: `--json` on `task list`, `task view`, `search`.
- **Versions and dates:** npm latest `1.53.0`, published 2026-09-24T17:28:54Z (registry); 232 versions since `0.1.0` on 2025-06-13. Latest commit shown for the `backlog/tasks` folder: 2026-09-28 (BACK-706).
- **Numbers, verified vs not:** README text and npm fields were fetched directly. Stars 6.9k (rounded display), forks 441, 61 open issues and 15 open pull requests are as shown by the GitHub page via Jina on 2026-10-04. The GitHub REST API answered 403, so stars are unverified via API. Repo creation date, exact star count and npm download numbers were not obtained.
- **Not run:** nothing was installed and no `backlog` command was executed during capture.

## 點解值得留意

- Josep 想為自己的 agent 找一個 kanban：Backlog.md 的任務就是倉庫內的 `.md` 檔，本機優先、無帳戶無 telemetry，與 Obsidian vault 的做法一致；Claude Code、Codex、Gemini CLI 都有現成接法（CLI 指引或 MCP）。
- Vault 目前用 `handoff.md`（見 `keeping-handoff-docs`）記錄 session 交接，用 Obsidian Bases（`wiki/reads.base`）檢視資料；Backlog.md 補的是「逐項任務 + 驗收條件 + 看板」，兩者角色不同，不一定要取代 `handoff.md`。
- `backlog/` 資料夾不在 CLAUDE.md 的 folder-role 表內，採用前要先做一次 `docs:` 修改；而且 `backlog init` 預設會寫入 AGENTS.md，在本 vault 內 AGENTS.md 是 CLAUDE.md 的受保護複本，所以應先在獨立專案試行，或手動合併指引。
- 安裝前先用 `scanning-agent-skills` 掃描，並確認 npm 套件 `backlog.md` 指向 github.com/MrLesk/Backlog.md；星數和維護狀況只是頁面顯示，未經 API 驗證。

## Source

- **Repo:** https://github.com/MrLesk/Backlog.md
- **Author:** MrLesk (npm author field: Alex Gavrilescu)
- **Published:** 2026-09-24, the date of the latest npm release (1.53.0); the repo creation date was not visible (GitHub API 403), so this is not the creation date. The npm package's first version `0.1.0` is dated 2025-06-13.
- **Engagement:** `stars=6.9k forks=441`, per GitHub page via Jina on 2026-10-04 (read from the page header of `https://github.com/MrLesk/Backlog.md/tree/main/backlog/tasks`; the repo root page rendered via Jina shows only badge images; 6.9k is GitHub's rounded display). Stars unverified via API.
- **Reader:** `raw.githubusercontent.com` (README.md, CLI-INSTRUCTIONS.md, ADVANCED-CONFIG.md, AGENTS.md, MANIFESTO.md, one sample task file), Jina Reader for the rendered GitHub page, and `registry.npmjs.org/backlog.md` for version and dates. GitHub REST API: HTTP 403. Exa not used. Verbatim text in `raw/20261004-backlog-md-markdown-kanban-for-agents.md`.

## Related

- [[../../skills/tracking-tasks-with-backlog-md/SKILL|skill: tracking-tasks-with-backlog-md]]
- [[../../skills/keeping-handoff-docs/SKILL|skill: keeping-handoff-docs]]
- [[../pages/20260918-obsidian-skills|obsidian-skills: Agent Skills for Obsidian]]
- [[../../skills/using-obsidian-skills/SKILL|skill: using-obsidian-skills]]
- [[../stars/Fission-AI--OpenSpec|stars/Fission-AI--OpenSpec]]
- [[../../skills/scanning-agent-skills/SKILL|skill: scanning-agent-skills]]
