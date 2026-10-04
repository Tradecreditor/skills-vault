---
slug: 20261004-backlog-md-markdown-kanban-for-agents
source_url: "https://github.com/MrLesk/Backlog.md"
canonical_id: "github:MrLesk/Backlog.md"
fetched_at: "2026-10-04T21:22:27Z"
reader: "github-raw+jina+npm-registry (GitHub REST API answered 403 for this session; Exa not used)"
---
{"repo": "MrLesk/Backlog.md", "description": "Backlog.md - A tool for managing project collaboration between humans and AI Agents in a git ecosystem", "description_source": "Title line of the Jina render of https://github.com/MrLesk/Backlog.md", "stars": "6.9k", "stars_note": "rounded display ('Star 6.9k') in the page header of https://github.com/MrLesk/Backlog.md/tree/main/backlog/tasks rendered via Jina on 2026-10-04; the repo root page rendered via Jina shows only a badge image, no number", "forks": 441, "open_issues_display": 61, "open_pull_requests_display": 15, "license": "MIT (README; npm registry license field MIT)", "latest_commit_seen": "BACK-706 - Remove redundant tests while preserving shipped behavior (2026-09-28), the latest commit touching backlog/tasks per the tree page; not necessarily the repo's latest commit", "created_at": "not visible (GitHub REST API 403); the npm package backlog.md was first published 2025-06-13 (version 0.1.0)", "npm_latest": "1.53.0", "npm_latest_published": "2026-09-24T17:28:54Z", "github_rest_api": "HTTP 403 (repo not attached to this session) -> numbers above come from the rendered page via Jina, per GitHub page via Jina on 2026-10-04", "verified": ["README text", "npm latest version and dates", "stars/forks display (rounded)"], "unverified": ["exact star count", "repo creation date", "primary language from the API (AGENTS.md says Bun with TypeScript 5)", "npm weekly downloads"]}

# ===== README.md (verbatim, https://raw.githubusercontent.com/MrLesk/Backlog.md/HEAD/README.md, 392 lines, 18013 bytes) =====
<!-- BEGIN README.md -->
<p align="center">
  <img src="./.github/backlog-logo.png" alt="Backlog.md logo" width="120">
</p>

<h1 align="center">Backlog.md</h1>
<p align="center"><strong>Markdown‑native Task Manager &amp; Kanban visualizer for any Git repository</strong></p>
<p align="center">AI agents write the code. You review the tasks: before, during, and after.</p>

<p align="center">
  <a href="https://www.npmjs.com/package/backlog.md"><img src="https://img.shields.io/npm/v/backlog.md?color=brightgreen" alt="npm version"></a>
  <a href="https://www.npmjs.com/package/backlog.md"><img src="https://img.shields.io/npm/dm/backlog.md" alt="npm downloads"></a>
  <a href="https://github.com/MrLesk/Backlog.md/blob/main/LICENSE"><img src="https://img.shields.io/github/license/MrLesk/Backlog.md" alt="MIT license"></a>
  <a href="https://github.com/MrLesk/Backlog.md"><img src="https://img.shields.io/github/stars/MrLesk/Backlog.md?style=social" alt="GitHub stars"></a>
</p>

<p align="center">
<code>npm i -g backlog.md</code>
</p>

![Backlog demo GIF using: backlog board](./.github/backlog-v1.40.gif)


---

> **Backlog.md** turns any folder into a **self‑contained project board**
> powered by plain Markdown files and a zero‑config CLI.

## Why Backlog.md in the AI era

AI agents can now produce more plausible code in an hour than you can carefully read in a day.
The bottleneck is no longer writing code. It's your attention. You can't meaningfully review
15,000 generated lines in one sitting, but you can read a screenful of task specs with acceptance
criteria before any code exists, and push back while a misunderstanding is still one sentence,
not a rebuilt feature.

Backlog.md structures agent work around **three review checkpoints**:

1. **Review the spec:** the agent decomposes your idea into tasks with descriptions, acceptance
   criteria, and milestones before implementation starts.
2. **Review the plan:** the agent researches your codebase and writes its implementation plan
   into the task. Approve it or steer before any code is written.
3. **Review the code:** one task = one context window = one PR. Diffs stay a size a human can
   actually read.

Afterwards, the completed tasks remain in Git as a permanent record of what was attempted and why,
legible to you, your team, and the next agent.

**Dogfooded:** nearly all of Backlog.md's own code is written by AI agents working through
Backlog.md itself. The full task ledger lives in this repo's [backlog folder](backlog/tasks).

📺 **See it in action:** [Devoxx Belgium 2025](https://www.youtube.com/watch?v=LSoDQU_9MMA) · [AI Engineer Code Summit 2025](https://www.youtube.com/watch?v=zMXKhhwiCIc)

## Features

* 🤖 **AI-ready** -- works with Claude Code, Gemini CLI, Codex, Kiro & any other MCP or CLI compatible AI assistant

* 📝 **Markdown-native tasks** -- every task is a plain `.md` file in your repo

* ✅ **Acceptance criteria & Definition of Done** -- verifiable scope per task, plus a reusable DoD checklist for every new task

* 🎯 **Milestones & dependencies** -- structure bigger efforts and make execution order reviewable, with task detail showing what a task waits on and what waits on it

* 📊 **Terminal Kanban** -- `backlog board` paints a live board in your shell; `backlog board export` creates shareable markdown reports

* 🌐 **Web UI** -- `backlog browser` serves a local Kanban board with drag-and-drop and task editing forms

* 🔍 **Search** -- fuzzy search across tasks, docs & decisions with `backlog search`

* 🔒 **Local-first** -- no server, no account, no telemetry; tasks are plain files in your repo, and remote Git operations are optional

* 💻 Cross-platform (macOS, Linux, Windows) · 🆓 MIT-licensed & open-source


---

## <img src="./.github/5-minute-tour-256.png" alt="Getting started" width="28" height="28" align="center"> Getting started

```bash
# Install
npm i -g backlog.md
# or: bun add -g backlog.md
# or: brew install backlog-md
# or: nix run github:MrLesk/Backlog.md

# Initialize in any Git repo
backlog init "My Awesome Project"

# Or initialize without Git for local/non-code projects
backlog init "Personal Planning" --no-git
```

> [!TIP]
> **Running one-off with `npx`?** This tool's npm package is named `backlog.md`, so use the full name: `npx backlog.md init "My Project"`, `npx backlog.md board`.
> Without an install, `npx backlog` resolves to an unrelated third-party npm package — not this tool.
> (With `backlog.md` installed as a project dependency, `npx backlog` runs the local binary as usual.)

### Run with Nix

Run Backlog.md directly from the repository flake:

```bash
nix run github:MrLesk/Backlog.md -- --version
```

Or install the named package into your Nix profile:

```bash
nix profile install github:MrLesk/Backlog.md#backlog-md
```

The Nix flake supports `x86_64-linux`, `aarch64-linux`, and
`aarch64-darwin`. The x86_64 Linux package uses Bun's baseline runtime so it
also works on pre-AVX2 processors with AVX support. Intel macOS users can use
the npm, Bun, or Homebrew installation instead.

The init wizard will ask how you want to connect AI tools:
- **CLI instructions** (recommended): creates a short instruction file that tells agents to run `backlog instructions overview`.
- **MCP connector**: optionally auto-configures Claude Code, Codex, Gemini CLI, Kiro or Cursor for teams that prefer MCP.
- **Skip**: no AI setup; use Backlog.md purely as a task manager.

For Cursor with CLI instructions, select AGENTS.md or pass `--agent-instructions cursor`; both use the same AGENTS.md target. Backlog.md preserves existing AGENTS.md content and does not migrate or remove unrelated user-managed `.cursor/rules` files.

Everything is stored as human-readable Markdown in a project-local backlog folder such as `backlog/`, `.backlog/`, or a custom project-relative path configured through `backlog.config.yml` (e.g. `backlog_directory: my-backlog`). Task IDs use a configurable prefix (`backlog init --task-prefix`): the default produces `TASK-1`-style IDs, while this repository uses `back`, so examples below show `BACK-1`-style IDs. Git is optional: `backlog init --no-git` creates a filesystem-only project.

---

## Working with AI agents

This is the recommended flow for Claude Code, Codex, Gemini CLI, Kiro and similar tools, following the **spec‑driven AI development** approach.
After running `backlog init`, agents should start by running `backlog instructions overview`. Work in this loop:

**Step 1: Describe your idea.** Tell the agent what you want to build and ask it to split the work into small tasks with clear descriptions and acceptance criteria.

**🤖 Ask your AI Agent:**
> I want to add a search feature to the web view that searches tasks, docs, and decisions. Please decompose this into small Backlog.md tasks.

> [!NOTE]
> **Review checkpoint #1:** read the task descriptions and acceptance criteria.

**Step 2: One task at a time.** Work on a single task per agent session, one PR per task. Good task splitting means each session can work independently without conflicts. Make sure each task is small enough to complete in a single conversation. You want to avoid running out of context window.

**Step 3: Plan before coding.** Ask the agent to research and write an implementation plan in the task. Do this right before implementation so the plan reflects the current state of the codebase.

**🤖 Ask your AI Agent:**
> Work on BACK-10 only. Research the codebase and write an implementation plan in the task. Wait for my approval before coding.

> [!NOTE]
> **Review checkpoint #2:** read the plan. Does the approach make sense? Approve it or ask the agent to revise.

**Step 4: Implement and verify.** Let the agent implement the task.

> [!NOTE]
> **Review checkpoint #3:** review the code, run tests, check linting, and verify the results match your expectations.

Mark verified work Done (or the configured final status). During periodic cleanup, use `backlog task complete` to move it off the board while preserving its record and dependency links. Use `backlog task archive` for canceled, duplicate, or invalid work; it removes incoming dependencies and task references.

If the output is not good enough: clear the plan/notes/final summary, refine the task description and acceptance criteria, and run the task again in a fresh session.

---

## Working without AI agents

Use Backlog.md as a standalone task manager from the terminal or browser.

```bash
# Create and refine tasks
backlog task create "Render markdown as kanban"
backlog task edit BACK-1 -d "Detailed context" --ac "Clear acceptance criteria"

# Track work
backlog task list -s "To Do"
backlog task list --json | jq '.tasks[] | .id'
backlog task edit BACK-1 --comment "Can we split the UI work into a separate PR?" --comment-author @sara
backlog search "kanban"
backlog board

# Work visually in the browser
backlog browser
```

You can switch between AI-assisted and manual workflows at any time; both operate on the same Markdown task files. Just prefer Backlog.md commands (CLI/MCP/Web) over hand-editing task files, so field types and metadata stay consistent.

Read commands support stable, versioned JSON for scripts and integrations. Use `--json` with `task list`, `task view`, the `task <id>` shorthand, and `search`. JSON mode is noninteractive and keeps successful stdout machine-readable. Add `--watch` to `task list --json` for an initial full list followed by changed full replacements, using the exact same JSON format. Read successive complete JSON values; each response replaces the previous list.

**Learn more:** [CLI reference](CLI-INSTRUCTIONS.md) | [Advanced configuration](ADVANCED-CONFIG.md)

---

## <img src="./.github/web-interface-256.png" alt="Web Interface" width="28" height="28" align="center"> Web Interface

Launch a web interface for visual task management on the local machine. The server listens on `127.0.0.1` and is not
reachable from other devices on the LAN or VPN:

```bash
# Start the web server (opens browser automatically)
backlog browser

# Custom port
backlog browser --port 8080

# Don't open browser automatically
backlog browser --no-open
```

**Features:**
- Interactive Kanban board with drag-and-drop
- Multi-select cards to move several tasks to one column
- Task creation and editing with forms
- Interactive acceptance criteria editor with checklists
- Real-time updates across all views
- Responsive design for desktop and mobile
- Task archiving with confirmation dialogs
- Seamless CLI integration - all changes sync with markdown files

![Web Interface Screenshot](./.github/web.jpeg)

To keep the Web UI running as an auto-starting local service, see [Running Backlog.md as a Service](backlog/docs/doc-003%20-%20Running-Backlog-Browser-as-a-Service.md).

---

## 🔧 MCP Integration (Model Context Protocol)

CLI instructions are the default AI setup. MCP remains supported for AI coding assistants like Claude Code, Codex, Gemini CLI and Kiro when you explicitly prefer an MCP connector.
You can run `backlog init` (even if you already initialized Backlog.md) and choose MCP integration, or follow the manual steps below.

### Client guides

<details>
  <summary><strong>Claude Code</strong></summary>

  ```bash
  claude mcp add backlog --scope user -- backlog mcp start
  ```

</details>

<details>
  <summary><strong>Codex</strong></summary>

  ```bash
  codex mcp add backlog -- backlog mcp start
  ```

</details>

<details>
  <summary><strong>Gemini CLI</strong></summary>

  ```bash
  gemini mcp add backlog -s user backlog mcp start
  ```

</details>

<details>
  <summary><strong>Kiro</strong></summary>

  ```bash
  kiro-cli mcp add --scope global --name backlog --command backlog --args mcp,start
  ```

</details>

<details>
  <summary><strong>Cursor / other MCP clients</strong></summary>

  Use the manual JSON config below in your client's MCP settings.

</details>

Use the shared `backlog` server name everywhere. The server finds the active project from your client's MCP roots, and re-resolves when you switch workspace or worktree. A single user-scope server covers every repo.

<details>
  <summary><strong>Manual config</strong></summary>

```json
{
  "mcpServers": {
    "backlog": {
      "command": "backlog",
      "args": ["mcp", "start"],
      "env": {
        "BACKLOG_CWD": "/absolute/path/to/your/project"
      }
    }
  }
}
```

Set `BACKLOG_CWD` to pin the server to one project and stop workspace following. Use it to always target the same backlog, or when your client can't report MCP roots.
If your IDE supports custom args but not env vars, you can also use `["mcp", "start", "--cwd", "/absolute/path/to/your/project"]`.
Until the server finds an initialized project, it serves `backlog://init-required`.

</details>

> [!IMPORTANT]
> When adding the MCP server manually, add a short instruction to your CLAUDE.md/AGENTS.md files telling agents to read `backlog://workflow/overview`.
> This step is not required when using `backlog init` as it adds these instructions automatically.
> For CLI-based setups, use `backlog instructions overview` to fetch the current workflow guidance.


Once connected, agents can read the Backlog.md workflow instructions via `backlog://workflow/overview`, with detailed guides at `backlog://workflow/task-creation`, `backlog://workflow/task-execution`, and `backlog://workflow/task-finalization`.
Use `/mcp` command in your AI tool (Claude Code, Codex, Kiro) to verify if the connection is working.

---

## <img src="./.github/cli-reference-256.png" alt="CLI Reference" width="28" height="28" align="center"> CLI reference

Full command reference covering task management, search, board, docs, decisions, and more: **[CLI-INSTRUCTIONS.md](CLI-INSTRUCTIONS.md)**

Quick examples: `backlog`, `backlog instructions`, `backlog task create`, `backlog task list`, `backlog task edit`, `backlog milestone add`, `backlog milestone rename`, `backlog milestone remove`, `backlog search`, `backlog board`, `backlog browser`.

Full help: `backlog --help`

---

## <img src="./.github/configuration-256.png" alt="Configuration" width="28" height="28" align="center"> Configuration

Backlog.md works with zero configuration. Settings merge from CLI flags, then the project config file (`backlog.config.yml` when present, otherwise `backlog/config.yml` or `.backlog/config.yml`), then built‑in defaults.

Run `backlog config` with no arguments to launch the interactive wizard (the same experience triggered from `backlog init` advanced setup). It walks through cross-branch accuracy (`checkActiveBranches`, `remoteOperations`, `activeBranchDays`), Git workflow (`autoCommit`, `bypassGitHooks`), ID formatting (`zeroPaddedIds`), editor integration (`defaultEditor`), Definition of Done defaults, and Web UI defaults (`defaultPort`, `autoOpenBrowser`). Skipping the wizard applies the safe built-in defaults, and rerunning `backlog init` or `backlog config` pre-populates prompts with your current values.

For filesystem-only projects (`backlog init --no-git`), the saved config forces `checkActiveBranches=false`, `remoteOperations=false`, and `autoCommit=false` so CLI, Web, and MCP local-file workflows do not depend on a Git repository.

### Definition of Done defaults

Set project-wide DoD items with `backlog config` (or during `backlog init` advanced setup), in the Web UI (Settings → Definition of Done Defaults), or by editing the project config file directly:

```yaml
definition_of_done:
  - Tests pass
  - Documentation updated
  - No regressions introduced
```

When a project uses root config discovery, edit `backlog.config.yml` instead of `backlog/config.yml`.

These items are added to every new task by default. You can add more on create with `--dod`, or disable defaults per task with `--no-dod-defaults`.

For the full configuration reference (all options, default values, commands, and detailed notes), see **[ADVANCED-CONFIG.md](ADVANCED-CONFIG.md)**.

---

## Troubleshooting

### Apple Silicon (macOS)

On M-series Macs, `backlog` can fail with `illegal hardware instruction` or `Binary package not installed for darwin-...` when Node, Bun, or Homebrew run under Rosetta (x64 emulation) and install the Intel binary instead of the arm64 one — or the other way around. The launcher runs whichever darwin variant (arm64 or x64) is actually installed, but a clean native-arch install is the reliable fix.

Check what your tools report:

```bash
uname -m                            # arm64 = Apple Silicon hardware; x86_64 = Intel or a Rosetta shell
node -p process.arch                # architecture of your Node/Bun runtime
sysctl -in sysctl.proc_translated   # 1 = current shell runs under Rosetta
which brew                          # /opt/homebrew = arm64 brew, /usr/local = Intel brew
```

If the architectures disagree, reinstall with the native one:

```bash
# Homebrew: make sure `which brew` prints /opt/homebrew, then
brew reinstall backlog-md

# npm
arch -arm64 npm i -g backlog.md

# Bun
arch -arm64 bun add -g backlog.md
```

Running an x64 Node under Rosetta on purpose also works: `backlog` falls back to whichever `backlog.md-darwin-*` package is present.

---

## 📺 Talks & Community

Watch Backlog.md in action:

- **Devoxx Belgium 2025**: [the spec-driven agent workflow behind Backlog.md, live on stage](https://www.youtube.com/watch?v=LSoDQU_9MMA)
- **AI Engineer Code Summit 2025**: [Backlog.md: task management for AI agents](https://www.youtube.com/watch?v=zMXKhhwiCIc)
- Slides from these and more talks: [mrlesk.com/talks](https://mrlesk.com/talks)

### Community tools

- **[vscode-backlog-md](https://marketplace.visualstudio.com/items?itemName=ysamlan.vscode-backlog-md)** - VS Code extension with issues panel, kanban view, and editing. ([ysamlan/vscode-backlog-md](https://github.com/ysamlan/vscode-backlog-md))

---

## License

Backlog.md is released under the **MIT License**: do anything, just give credit. See [LICENSE](LICENSE).

<!-- END README.md -->

# ===== npm registry fields used (https://registry.npmjs.org/backlog.md, fetched 2026-10-04) =====
```json
{
  "name": "backlog.md",
  "dist-tags": {
    "latest": "1.53.0"
  },
  "license": "MIT",
  "homepage": "https://backlog.md",
  "repository": {
    "url": "git+https://github.com/MrLesk/Backlog.md.git",
    "type": "git"
  },
  "bin": {
    "backlog": "cli.js"
  },
  "author": {
    "url": "https://github.com/MrLesk",
    "name": "Alex Gavrilescu"
  },
  "keywords": [
    "cli",
    "markdown",
    "kanban",
    "task",
    "project-management",
    "backlog",
    "agents"
  ],
  "optionalDependencies (platform binaries)": {
    "backlog.md-linux-x64": "1.53.0",
    "backlog.md-darwin-x64": "1.53.0",
    "backlog.md-linux-arm64": "1.53.0",
    "backlog.md-windows-x64": "1.53.0",
    "backlog.md-darwin-arm64": "1.53.0",
    "backlog.md-windows-arm64": "1.53.0"
  },
  "time.created": "2025-06-13T17:21:08.707Z",
  "time.modified": "2026-09-24T17:28:54.860Z",
  "published_versions_count": 232,
  "first_version": [
    "0.1.0",
    "2025-06-13T17:21:09.521Z"
  ],
  "last_versions": {
    "1.49.3": "2026-08-03T21:30:58.182Z",
    "1.50.0": "2026-08-09T20:45:37.834Z",
    "1.50.1": "2026-08-10T07:49:39.860Z",
    "1.51.0": "2026-09-02T21:35:26.537Z",
    "1.52.0": "2026-09-12T12:09:45.984Z",
    "1.53.0": "2026-09-24T17:28:54.558Z"
  }
}
```

# ===== CLI-INSTRUCTIONS.md (verbatim, raw.githubusercontent.com HEAD, 421 lines) =====
<!-- BEGIN CLI-INSTRUCTIONS.md -->
# CLI Reference

Full command reference for Backlog.md. For getting started, see [README.md](README.md).

All examples use the `backlog` command, available after installing the `backlog.md` package globally (`npm i -g backlog.md`) or as a project dependency. For one-off runs without installing, use the full package name — `npx backlog.md <command>`, e.g. `npx backlog.md board`; without an install, `npx backlog` resolves to an unrelated third-party npm package, not this tool.

## Project Setup

| Action      | Example                                              |
|-------------|------------------------------------------------------|
| Initialize project | `backlog init [project-name]` (creates backlog structure with a minimal interactive flow) |
| Re-initialize | `backlog init` (preserves existing config, allows updates) |
| Advanced settings wizard | `backlog config` (no args) — launches the full interactive configuration flow |

`backlog init` keeps first-run setup focused on the essentials:
- **Project name** – identifier for your backlog (defaults to the current directory on re-run).
- **Backlog folder** – choose `backlog/`, `.backlog/`, or a custom project-relative path.
- **Config location** – for built-in folders, choose folder-local `config.yml` or root `backlog.config.yml`; custom paths use root `backlog.config.yml`.
- **Integration choice** – decide whether your AI tools use **CLI instructions** (recommended), the optional **MCP connector**, or no AI setup.
- **Instruction files (CLI path)** – the CLI setup writes a short nudge to AGENTS.md by default in non-interactive setup. `--agent-instructions cursor` also selects AGENTS.md, and the interactive CLI and Web setup identify Cursor under that shared target. Existing user-managed `.cursor/rules` files may coexist; Backlog.md does not migrate or remove them, and repeated initialization preserves non-Backlog content in AGENTS.md.
- **Advanced settings prompt** – default answer "No" finishes init immediately; choosing "Yes" jumps straight into the advanced wizard documented in [ADVANCED-CONFIG.md](ADVANCED-CONFIG.md).

The advanced wizard includes interactive Definition of Done defaults editing (add/remove/reorder/clear), so project checklist defaults can be managed without manual YAML edits.

You can rerun the wizard anytime with `backlog config`. All existing CLI flags (for example `--defaults`, `--agent-instructions`) continue to provide fully non-interactive setups, and init also supports `--backlog-dir <path>` plus `--config-location <folder|root>` for scripted configuration.

Humans and agents can run `backlog instructions` for workflow guides and `backlog instructions overview` for the overview.

## Documentation

- Document IDs are global across all subdirectories under `backlog/docs`. You can organize files in nested folders (e.g., `backlog/docs/guides/`), and `backlog doc list` and `backlog doc view <id>` work across the entire tree.
- Use `backlog doc create "New Guide" -p guides` to create a document in a docs subdirectory. The created output includes the persisted docs-relative file path, such as `backlog/docs/guides/doc-1 - New-Guide.md`.
- Use `backlog doc update doc-1 --content "Updated markdown"` to update document content. Add `--title`, `-t/--type`, `--tags`, or `-p/--path` to update metadata or move the document while preserving omitted fields.
- Use `backlog doc search "query"` for scoped document search with plain text output that includes document IDs and follow-up `backlog doc view <docId>` commands. Use `--limit <number>` to cap results.
- Document paths are always relative to the docs directory. Absolute paths and traversal segments such as `..` are rejected.

## Task Management

| Action      | Example                                              |
|-------------|------------------------------------------------------|
| Create task | `backlog task create "Add OAuth System"`                    |
| Create with description | `backlog task create "Feature" -d "Add authentication system"` |
| Create with assignee | `backlog task create "Feature" -a @sara`           |
| Create with status | `backlog task create "Feature" -s "In Progress"`    |
| Create with labels | `backlog task create "Feature" -l auth,backend`     |
| Create with priority | `backlog task create "Feature" --priority high`     |
| Create with due date | `backlog task create "Feature" --due-date 2026-08-10` |
| Create with plan | `backlog task create "Feature" --plan "1. Research\n2. Implement"`     |
| Create with AC | `backlog task create "Feature" --ac "Must work,Must be tested"` |
| Add DoD items on create | `backlog task create "Feature" --dod "Run tests"` |
| Create without DoD defaults | `backlog task create "Feature" --no-dod-defaults` |
| Create with notes | `backlog task create "Feature" --notes "Started initial research"` |
| Create with final summary | `backlog task create "Feature" --final-summary "Completion summary"` |
| Create with deps | `backlog task create "Feature" --dep task-1,task-2` |
| Create with refs | `backlog task create "Feature" --ref https://docs.example.com --ref src/api.ts` |
| Create with docs | `backlog task create "Feature" --doc https://design-docs.example.com --doc docs/spec.md` |
| Create sub task | `backlog task create -p 14 "Add Login with Google"`|
| Create (all options) | `backlog task create "Feature" -d "Description" -a @sara -s "To Do" -l auth --priority high --ac "Must work" --notes "Initial setup done" --dep task-1 --ref src/api.ts --doc docs/spec.md -p 14` |
| List tasks  | `backlog task list [-s <status>] [-a <assignee>] [-p <parent>] [--labels <labels>] [--search <query>] [--limit <n>]` |
| List filtered | `backlog task list --labels frontend,bug --search "login" --limit 10 --plain` |
| List in windows | `backlog task list --max-count 20 --skip 20 --plain` |
| Count tasks | `backlog task list --status "To Do" --count` |
| List as JSON | `backlog task list --status "To Do" --json` |
| Watch as JSON | `backlog task list --json --watch` |
| List by parent | `backlog task list --parent 42` or `backlog task list -p task-42` |
| View detail | `backlog task 7` (interactive UI, press 'E' to edit in editor) |
| View (AI mode) | `backlog task 7 --plain`                           |
| View as JSON | `backlog task 7 --json` |
| Edit        | `backlog task edit 7 -a @sara -l auth,backend`       |
| Add plan    | `backlog task edit 7 --plan "Implementation approach"`    |
| Add AC      | `backlog task edit 7 --ac "New criterion" --ac "Another one"` |
| Add DoD     | `backlog task edit 7 --dod "Ship notes"` |
| Remove AC   | `backlog task edit 7 --remove-ac 2` (removes AC #2)      |
| Remove multiple ACs | `backlog task edit 7 --remove-ac 2 --remove-ac 4` (removes AC #2 and #4) |
| Check AC    | `backlog task edit 7 --check-ac 1` (marks AC #1 as done) |
| Check DoD   | `backlog task edit 7 --check-dod 1` (marks DoD #1 as done) |
| Check multiple ACs | `backlog task edit 7 --check-ac 1 --check-ac 3` (marks AC #1 and #3 as done) |
| Uncheck AC  | `backlog task edit 7 --uncheck-ac 3` (marks AC #3 as not done) |
| Uncheck DoD | `backlog task edit 7 --uncheck-dod 3` (marks DoD #3 as not done) |
| Mixed AC operations | `backlog task edit 7 --check-ac 1 --uncheck-ac 2 --remove-ac 4` |
| Mixed DoD operations | `backlog task edit 7 --check-dod 1 --uncheck-dod 2 --remove-dod 4` |
| Add notes   | `backlog task edit 7 --notes "Completed X, working on Y"` (replaces existing) |
| Append notes | `backlog task edit 7 --append-notes "New findings"` |
| Add comment | `backlog task edit 7 --comment "Question for review" --comment-author @sara` |
| Add final summary | `backlog task edit 7 --final-summary "Completion summary"` |
| Append final summary | `backlog task edit 7 --append-final-summary "More details"` |
| Clear final summary | `backlog task edit 7 --clear-final-summary` |
| Add deps    | `backlog task edit 7 --dep task-1 --dep task-2`     |
| Set due date | `backlog task edit 7 --due-date 2026-08-10` |
| Clear due date | `backlog task edit 7 --clear-due-date` |
| Complete    | `backlog task complete 7` (move finished work to completed storage) |
| Archive     | `backlog task archive 7` (canceled, duplicate, or invalid work) |

Mark finished work Done (or the configured final status). During periodic cleanup, use Complete to move it off the board while preserving its record and dependency links. Archive removes incoming dependencies and task references.

### Paging long lists

`task list`, `search`, `draft list`, `milestone list`, `doc list`, `doc search`, and `decision list` print every match by default. `--max-count <n>` prints at most `n` items and `--skip <n>` leaves out the first `n`, as in `git log`. Both apply after filtering, sorting, and `--limit`, in the order the output prints: `task list` groups by status unless `--sort priority` prints one flat list, plain `search` prints tasks, then documents, then decisions, and `milestone list` prints active milestones before completed ones. Each list has a stable order: tasks, drafts, and decisions break ties by ID, documents sort by title and then path, search results by score and then corpus order, and milestones follow their files and then the tasks that name them. So consecutive windows of an unchanged backlog join into the complete output without overlapping or leaving items out. With `--json`, `task list` windows its flat `tasks` array in sort order without status groups and `search` windows its results in relevance order, so read all windows of a list in one output mode. The options print text instead of opening an interactive view.

Output cut by a window ends with the shown range, the total, and the command that prints the following items:

```text
Showing 21-40 of 57 items. Next: backlog task list --status 'To Do' --max-count 20 --skip 40
```

The last window has no `Next:` part, and a `--skip` past the end prints only `Showing 0 of 57 items.` Output that is not cut has no footer. `--count` prints only the number of items the same command would list, as `grep --count` does; it cannot be combined with `--json`. There are no short forms because `-m` already means `--milestone`. `--limit` keeps its behavior: it silently shortens the list before any window applies.

Task comments are append-only discussion entries with optional author labels. Use comments for review questions and collaboration notes; use implementation notes for execution progress and final summary for PR-ready completion notes. Comment bodies may contain Markdown, but standalone `---` lines are reserved as comment delimiters.

Task and milestone due dates are calendar days stored as `YYYY-MM-DD`. Use a plain date such as `2026-08-10`; a due date carries no time and no timezone.

### Stable JSON output

Use `--json` when a script or integration needs structured output:

```bash
backlog task list --status "To Do" --json | jq '.tasks[] | .id'
backlog task view BACK-7 --json | jq '.task.acceptanceCriteria'
backlog task BACK-7 --json
backlog search "authentication" --json | jq '.results[] | [.type, .data.id]'
```

Use `backlog task list --json --watch` to receive the full matching list immediately, then a full replacement whenever its JSON result changes. Every response uses exactly the same fields, envelope, indentation, and trailing newline as `task list --json`. Read successive complete JSON values, not individual lines or the whole stream as one document. For example:

```bash
backlog task list --json --watch | jq --unbuffered -c '.tasks'
```

Each response replaces the subscriber's previous list, including an empty `tasks` array. Filters, sorting, limits, and local editable task scope are unchanged; completed storage, archives, drafts, and other branches are not added to the list. Dependency and configuration changes can update derived fields or which tasks match. Unchanged results are suppressed, and rapid edits or slow consumers may coalesce intermediate states. The command reconciles periodically as well as on file notifications; this is a current-state subscription, not an edit history. Restart it to receive a fresh full list.

`--watch` requires `--json` and cannot be combined with `--plain`. Stop it with Ctrl+C or terminate the process; closing the output pipe also stops it. It also ends when the process that started it ends. A failure after earlier responses writes a diagnostic to stderr and exits nonzero without emitting a replacement for that failed read.

Each successful response is one pretty-printed JSON document followed by a newline. The top-level contract is versioned and identifies the command result:

| Command | Envelope |
|---------|----------|
| `task list --json` | `{ "schemaVersion": 1, "kind": "task-list", "tasks": [...] }` |
| `task view <id> --json` and `task <id> --json` | `{ "schemaVersion": 1, "kind": "task-view", "task": {...} }` |
| `search [query] --json` | `{ "schemaVersion": 1, "kind": "search", "results": [...] }` |

Task list and task search results use these compact fields: `id`, `title`, `status`, `type`, `priority`, `project`, `assignees`, `reporter`, `labels`, `milestone`, `parentTaskId`, `acceptanceCriteriaCompleted`, `acceptanceCriteriaCount`, `references`, `modifiedFiles`, `ordinal`, `createdAt`, `updatedAt`, `dueDate`, and `isReady`. `acceptanceCriteriaCompleted` is the number of checked acceptance criteria and `acceptanceCriteriaCount` is the total; both are `0` when the task has no acceptance criteria. `project` reports the task's `project:` frontmatter and is `null` when the task has none. Setting or filtering by it requires a `projects:` list in the project config. `isReady` is derived from the whole visible corpus at read time and never stored: it is `true` when the task is unfinished and every dependency it names resolved to a completed task, and `false` for a finished task or one whose dependencies are unfinished, unknown, or ambiguous. It is the same verdict `task list --ready` filters on.

Task view includes the same progress counts alongside the full checklist and adds `path`, `description`, `dependencies`, `dependencyGraph`, `readiness`, `references`, `documentation`, `modifiedFiles`, `subtasks`, `acceptanceCriteria`, `definitionOfDone`, `implementationPlan`, `implementationNotes`, `comments`, and `finalSummary`. `path` is relative to the project root. Checklist entries contain `index`, `text`, and `checked`. Comment entries contain `index`, `body`, `createdAt`, and `author`.

Task view also carries `dependencyGraph`, a property of the task detail that is derived from the whole visible corpus at read time and never stored in the Markdown file. `task.dependencies` stays the task's own list of direct dependency IDs, unchanged. `task.dependencyGraph` contains `root` (the selected task's ID), `nodes`, and `edges`. Each edge is `{ "from": ..., "to": ... }` and always points from the task that declares the dependency to the task it depends on, so `to` blocks `from`. Each node contains `id`, `title`, `status`, `state`, `completed`, `dependencyDepth`, and `dependentDepth`. The two depths are the shortest hop counts from the root: `0` is the root itself, `1` is a direct relationship, anything higher is transitive, and `null` means the node is not reachable in that direction. Nodes are listed root first and then by task ID, edges by `from` and then `to`. See "Dependency Management" for what the graph covers and how it reports identities it cannot resolve.

`readiness` explains the `isReady` field above it and comes from the same derivation. It contains `isReady`, `isBlocked`, `blockingDependencies` (dependencies that resolved to unfinished tasks), and `missingDependencies` (dependency IDs no single visible task claims). Both lists fail closed: an unknown or ambiguous dependency blocks instead of being treated as satisfied.

Search keeps relevance order and discriminates every result with `type` and `data`. Task data uses the compact task fields. Document data contains `id`, `title`, `type`, `path`, `tags`, `createdAt`, and `updatedAt`. Decision data contains `id`, `title`, `status`, and `date`. Search scores are not part of the version 1 public contract.

When `--max-count` or `--skip` cuts a `task list`, `search`, or `decision list` result, the envelope also contains `total`, the number of items before the window, and `nextSkip`, the `--skip` value for the following items or `null` when none follow. Output that is not cut has neither field.

Absent scalar fields are `null`, and absent collections are `[]`. Date-only values remain `YYYY-MM-DD`; UTC date-times use RFC 3339. Internal fields, absolute paths, raw Markdown source objects, branch metadata, and search implementation details are not exposed.

`--json` and `--plain` are mutually exclusive. Explicit JSON mode is always noninteractive, including in a terminal. Without `--json`, existing interactive, explicit plain, and automatic non-TTY plain behavior is unchanged. One-shot errors leave stdout empty, write a concise message to stderr, and exit nonzero. Version 1 may gain backward-compatible fields, but removing, renaming, retyping, or changing documented field semantics requires a new `schemaVersion`.

### Multi-line input (description/plan/notes/comments/final summary)

The CLI preserves input literally — `\n` sequences are not auto-converted. Use one of the following forms (recommended order for AI agents):

**1. Repeat `--append-*` for each line (works in every shell, including Claude Code / Codex / agent sandboxes):**

```bash
backlog task edit 7 --notes "First line"
backlog task edit 7 --append-notes "Second line"
backlog task edit 7 --append-notes "Third line"
```

**2. Real newlines inside double quotes (single command):**

```bash
backlog task create "Feature" --desc "Line1
Line2

Final paragraph"
```

The same shape works for `--plan`, `--notes`, `--comment`, `--final-summary`, and the `--append-*` variants.

**3. Shell-specific shorthand (interactive shells only — rejected by tree-sitter-based agent sandboxes, see [#595](https://github.com/MrLesk/Backlog.md/issues/595)):**

- **Bash/Zsh (ANSI-C quoting)**

  ```bash
  backlog task edit 7 --notes $'Line1\nLine2'
  ```

- **POSIX sh (printf substitution)**

  ```bash
  backlog task create "Feature" --desc "$(printf 'Line1\nLine2\n\nFinal paragraph')"
  ```

- **PowerShell (backtick-n)**

  ```powershell
  backlog task create "Feature" --desc "Line1`nLine2`n`nFinal paragraph"
  ```

### Literal backticks in task text

When task text includes Markdown code spans, quote it so the shell passes the backticks literally. Unescaped backticks in double-quoted or unquoted arguments are command substitution in many shells, and Backlog.md cannot recover the original text after the shell has already executed it.

Use single-quoted CLI arguments for values that contain literal backticks:

```bash
backlog task create 'Document `backlog init` setup' \
  --ac 'Instructions mention `backlog init --defaults` literally'
```

If single quotes are not practical in your shell, escape each literal backtick before running the command. Do not rely on Backlog.md to sanitize accidental command output after substitution.

## Milestone Management

Milestones are managed through milestone files. Use CLI commands instead of editing milestone markdown directly so IDs, filenames, task references, and archive state stay consistent.

| Action | Example |
|--------|---------|
| List milestones | `backlog milestone list --plain` |
| List completed milestones too | `backlog milestone list --show-completed --plain` |
| Add milestone | `backlog milestone add "Release 1.0"` |
| Add with description | `backlog milestone add "Beta" --description "Beta scope"` |
| Add with due date | `backlog milestone add "Beta" --due-date 2026-08-10` |
| Rename and update tasks | `backlog milestone rename "Release 1.0" "Release 2.0"` |
| Set due date without renaming | `backlog milestone rename "Release 1.0" "Release 1.0" --due-date 2026-08-10` |
| Clear due date | `backlog milestone rename "Release 1.0" "Release 1.0" --clear-due-date` |
| Rename without task updates | `backlog milestone rename m-1 "Release 2.0" --no-update-tasks` |
| Remove and clear task milestones | `backlog milestone remove "Release 1.0"` |
| Remove and keep task values | `backlog milestone remove "Release 1.0" --task-handling keep` |
| Remove and reassign tasks | `backlog milestone remove "Release 1.0" --task-handling reassign --reassign-to "Release 2.0"` |
| Archive milestone | `backlog milestone archive m-1` |

`milestone remove` task handling modes are `clear` (default), `keep`, and `reassign`. `--reassign-to` is required when using `--task-handling reassign`, and the target must be an active milestone file.

## Search

Find tasks, documents, and decisions across your entire backlog with fuzzy search:

| Action             | Example                                              |
|--------------------|------------------------------------------------------|
| Search tasks       | `backlog search "auth"`                        |
| Filter by status   | `backlog search "api" --status "In Progress"`   |
| Filter by priority | `backlog search "bug" --priority high`        |
| Combine filters    | `backlog search "web" --status "To Do" --priority medium` |
| Plain text output  | `backlog search "feature" --plain` (for scripts/AI) |
| JSON output        | `backlog search "feature" --json` (for structured integrations) |
| Find by modified file | `backlog search --modified-file src/path.ts --plain` |
| Page results       | `backlog search "api" --max-count 20 --skip 20 --plain` |

**Search features:**
- **Fuzzy matching** -- finds "authentication" when searching for "auth"
- **Modified-file lookup** -- tasks can record project-root-relative modified files; find them later with `--modified-file`
- **Interactive filters** -- refine your search in real-time with the TUI
- **Live filtering** -- see results update as you type (no Enter needed)

## Draft Workflow

| Action      | Example                                              |
|-------------|------------------------------------------------------|
| Create draft | `backlog task create "Feature" --draft`             |
| Draft flow  | `backlog draft create "Spike GraphQL"` → `backlog draft promote 3.1` |
| Demote to draft| `backlog task demote <id>` |

## Dependency Management

Manage task dependencies to express execution order:

| Action      | Example                                              |
|-------------|------------------------------------------------------|
| Add dependencies | `backlog task edit 7 --dep task-1 --dep task-2`     |
| Add multiple deps | `backlog task edit 7 --dep task-1,task-5,task-9`    |
| Create with deps | `backlog task create "Feature" --dep task-1,task-2` |
| View dependencies | `backlog task 7` (shows dependencies in task view)  |
| Validate dependencies | Use task commands to automatically validate dependencies |

**Dependency Features:**
- **Automatic validation**: verifies that referenced dependency tasks exist
- **Flexible formats**: Use `task-1`, `1`, or comma-separated lists like `1,2,3`
- **Completion tracking**: See which dependencies are blocking task progress

### Dependency graph in task detail

Task detail shows the whole dependency context around the selected task, under `Dependency Graph`, directly above the description. It is derived and read-only, and it replaces the raw `Dependencies:` ID list in plain output: the graph names the same direct dependencies and resolves their titles, status, and everything behind them.

Every plain task output uses this one layout, so `task create --plain`, `task edit --plain`, `task view --plain`, and the MCP task results all render identically. `--json` is unaffected: `task.dependencies` remains the editable direct list alongside `task.dependencyGraph`.

```text
Dependency Graph:
--------------------------------------------------
Depends on (1 direct, 2 total):
└─ BACK-2 - Parser rewrite [In Progress]
   └─ BACK-1 - Token schema [completed]

Dependents (2 direct, 2 total):
├─ BACK-8 - Migration guide [To Do]
└─ BACK-9 - Release checklist [To Do]
```

- **Edge direction.** A dependency edge points from the task that declares it to the task it depends on, so the task it points at blocks the task it comes from.
- **Direct versus transitive.** `Depends on` lists everything the selected task transitively depends on; `Dependents` lists everything that transitively depends on it. Nesting shows the distance: the outermost entries are direct relationships and everything indented below them is transitive. The heading counts both, as `N direct, M total`.
- **Dependents.** "Dependents" means the tasks this one blocks. It is the reverse of the task's own dependency list, and nothing on it is editable from here; change it on the task that declares it.
- **Visibility.** The graph resolves against exactly what task detail can already see: the current checkout plus completed tasks for the CLI, TUI, and MCP, and the configured cross-branch corpus in the browser. Archiving a task takes it out of every one of those, so an archived ID stops resolving instead of coming back.
- **Cycles and repeats.** Every task appears once. A relationship that points back into the branch above it is marked `(cycle)`, and a task already shown elsewhere in the same section is marked `(shown above)` rather than being expanded again.
- **Unresolved identities.** `unknown task ID` means no visible task claims that ID. `ambiguous task ID` means more than one record claims it, so nothing is chosen. Neither is ever treated as satisfied, and the graph never traverses past one, so anything behind it is left out rather than reported as resolved. Diagnose and repair duplicate IDs with `backlog doctor` before trusting a graph that reports one.

## Board Operations

| Action      | Example                                              |
|-------------|------------------------------------------------------|
| Kanban board      | `backlog board` (interactive UI, press 'E' to edit in editor) |
| Export board | `backlog board export [file]` (exports Kanban board to markdown) |
| Export with version | `backlog board export --export-version "v1.0.0"` (includes version in export) |

## Statistics & Overview

| Action      | Example                                              |
|-------------|------------------------------------------------------|
| Project overview | `backlog overview` (interactive TUI showing project statistics) |

## Web Interface

| Action      | Example                                              |
|-------------|------------------------------------------------------|
| Web interface | `backlog browser` (launches the local-machine-only web UI on `127.0.0.1:6420`) |
| Web custom port | `backlog browser --port 8080 --no-open` |

The Web UI listens only on `127.0.0.1`; it is not reachable from other devices on the LAN or VPN.

To keep the Web UI running in the background with auto-start on boot, see [Running Backlog.md as a Service](backlog/docs/doc-003%20-%20Running-Backlog-Browser-as-a-Service.md).

## Documentation

| Action      | Example                                              |
|-------------|------------------------------------------------------|
| Create doc | `backlog doc create "API Guidelines"` |
| Create with path | `backlog doc create "Setup Guide" -p guides/setup` |
| Create with type | `backlog doc create "Architecture" -t guide` |
| Update content | `backlog doc update doc-1 --content "Updated markdown"` |
| Update metadata/path | `backlog doc update doc-1 --title "Setup Handbook" -t guide --tags setup,runbook -p guides` |
| List docs | `backlog doc list` |
| Search docs | `backlog doc search "architecture" --limit 5` |
| View doc | `backlog doc view doc-1` |

## Decisions

| Action      | Example                                              |
|-------------|------------------------------------------------------|
| Create decision | `backlog decision create "Use PostgreSQL for primary database"` |
| Create with status | `backlog decision create "Migrate to TypeScript" -s proposed` |

## Agent Instructions

| Action                                          | Example                                              |
|-------------------------------------------------|------------------------------------------------------|
| Open the local CLI documentation entry point | `backlog` |
| List workflow guides | `backlog instructions` |
| Required first read for task workflow | `backlog instructions overview` |
| Read a detailed workflow guide | `backlog instructions task-execution` |
| Update CLI agent instruction files | `backlog agents --update-instructions` (updates CLAUDE.md, AGENTS.md, GEMINI.md, .github/copilot-instructions.md) |

## Maintenance

| Action      | Example                                                                                      |
|-------------|----------------------------------------------------------------------------------------------|
| Cleanup done tasks | `backlog cleanup` (move old completed tasks to completed folder to cleanup the kanban board) |

Full help: `backlog --help`

---

## Sharing & Export

### Board Export

Export your Kanban board to a clean, shareable markdown file:

```bash
# Export to default Backlog.md file
backlog board export

# Export to custom file
backlog board export project-status.md

# Force overwrite existing file
backlog board export --force

# Export to README.md with board markers
backlog board export --readme

# Include a custom version string in the export
backlog board export --export-version "v1.2.3"
backlog board export --readme --export-version "Release 2024.12.1-beta"
```

Perfect for sharing project status, creating reports, or storing snapshots in version control.

---

## Shell Tab Completion

Backlog.md can install tab completion for bash, zsh, fish, and PowerShell.

**Quick Installation:**
```bash
# Auto-detect and install for your current shell
backlog completion install

# Or specify shell explicitly
backlog completion install --shell bash
backlog completion install --shell zsh
backlog completion install --shell fish
backlog completion install --shell pwsh
```

**What you get:**
- Command completion: `backlog <TAB>` → shows all commands
- Dynamic task IDs: `backlog task edit <TAB>` → shows actual task IDs from your backlog
- Smart flags: `--status <TAB>` → shows configured status values
- Context-aware suggestions for priorities, labels, and assignees

Full documentation: See [completions/README.md](completions/README.md) for detailed installation instructions, troubleshooting, and examples.

<!-- END CLI-INSTRUCTIONS.md -->

# ===== ADVANCED-CONFIG.md (verbatim, raw.githubusercontent.com HEAD, 74 lines) =====
<!-- BEGIN ADVANCED-CONFIG.md -->
# Advanced Configuration

For getting started and the interactive wizard overview, see [README.md](README.md#-configuration).

## Configuration Commands

| Action      | Example                                              |
|-------------|------------------------------------------------------|
| View all configs | `backlog config list` |
| Get specific config | `backlog config get defaultEditor` |
| Set config value | `backlog config set defaultEditor "code --wait"` |
| Enable auto-commit | `backlog config set autoCommit true` |
| Bypass git hooks | `backlog config set bypassGitHooks true` |
| Enable cross-branch check | `backlog config set checkActiveBranches true` |
| Set active branch days | `backlog config set activeBranchDays 30` |
| Set default assignees | `backlog config set defaultAssignee "@alice,@bob"` |

Running `backlog config` with no arguments launches the interactive advanced wizard, including guided Definition of Done defaults editing (add/remove/reorder/clear).

## Available Configuration Options

| Key               | Purpose            | Default                       |
|-------------------|--------------------|-------------------------------|
| `defaultAssignee` | Assignees for new tasks created without `-a` | `[]`             |
| `defaultStatus`   | First column       | `To Do`                       |
| `definition_of_done` | Default DoD checklist items for new tasks | `(not set)` |
| `statuses`        | Board columns      | `[To Do, In Progress, Done]`  |
| `priorities`      | Ordered task priority labels | `[High, Medium, Low]` |
| `projects`        | Allowed project values for monorepo backlogs | `(not set)` |
| `dateFormat`      | Display-only date format | `yyyy-mm-dd`            |
| `includeDatetimeInDates` | Add time to new dates | `true`              |
| `defaultEditor`   | Editor for 'E' key | Platform default (nano/notepad) |
| `defaultPort`     | Web UI port        | `6420`                        |
| `autoOpenBrowser` | Open browser automatically | `true`            |
| `remoteOperations`| Enable remote git operations | `true`           |
| `autoCommit`      | Automatically commit task changes | `false`       |
| `bypassGitHooks`  | Skip git hooks when committing (uses --no-verify) | `false`       |
| `zeroPaddedIds`   | Pad all IDs (tasks, docs, etc.) with leading zeros | `(disabled)`  |
| `checkActiveBranches` | Check task states across active branches for accuracy | `true` |
| `activeBranchDays` | How many days a branch is considered active | `30` |
| `onStatusChange`  | Shell command to run on status change | `(disabled)` |
| `backlog_directory` | Project-relative backlog folder, chosen at `backlog init` and read from `backlog.config.yml` in the project root | `backlog` |

## Detailed Notes

> Editor setup guide: See [Configuring VIM and Neovim as Default Editor](backlog/docs/doc-002%20-%20Configuring-VIM-and-Neovim-as-Default-Editor.md) for configuration tips and troubleshooting interactive editors.

> **Note**: Set `remoteOperations: false` to work offline. This disables git fetch operations and loads tasks from local branches only, useful when working without network connectivity.

> **Git Control**: By default, `autoCommit` is set to `false`, giving you full control over your git history. Task operations will modify files but won't automatically commit changes. Set `autoCommit: true` if you prefer automatic commits for each task operation.

> **Git Hooks**: If you have pre-commit hooks (like conventional commits or linters) that interfere with backlog.md's automated commits, set `bypassGitHooks: true` to skip them using the `--no-verify` flag.

> **Performance**: Cross-branch checking ensures accurate task tracking across all active branches but may impact performance on large repositories. You can disable it by setting `checkActiveBranches: false` for maximum speed, or adjust `activeBranchDays` to control how far back to look for branch activity (lower values = better performance).

> **Status Change Callbacks**: Set `onStatusChange` to run a shell command whenever a task's status changes. Available variables: `$TASK_ID`, `$OLD_STATUS`, `$NEW_STATUS`, `$TASK_TITLE`. Per-task override via `onStatusChange` in task frontmatter. Example: `'if [ "$NEW_STATUS" = "In Progress" ]; then claude "Task $TASK_ID ($TASK_TITLE) has been assigned to you. Please implement it." & fi'`

> **Default Assignee**: `defaultAssignee` is a list, so `backlog config set defaultAssignee "@alice,@bob"` stores both names. Every create surface (CLI `task create` and `draft create`, the creation wizard, TUI, Web, MCP) applies it when no assignee is supplied. An explicit assignee replaces the default entirely instead of merging with it, and setting the value to an empty string clears the default so new tasks start unassigned. To keep a single task unassigned while the default stays configured, pass an explicit empty assignee: `backlog task create "Title" -a ""`. The same value clears existing assignees on edit: `backlog task edit BACK-1 -a ""` (MCP `task_create`/`task_edit` use an empty `assignee` array). When editing `config.yml` by hand, quote the names (`default_assignee: ["@alice"]`) because `@` starts a reserved YAML character; a value YAML cannot read is ignored rather than guessed at.

> **Priority Values**: Set `priorities` to an ordered list of labels such as `["Very High", "High", "Medium", "Low", "Very Low"]`. The first value sorts highest. CLI, MCP, and Web inputs accept configured values case-insensitively and store normalized lowercase values in task frontmatter.

> **Project Values**: `projects` tags each task with one project in a monorepo-style backlog. It has no default, so the field stays inert until you set it — until then no surface offers it, and `--project` fails with a message naming the config file. Set it by editing the project config file directly (like `statuses`, `labels`, `types`, and `priorities`, it cannot be changed with `backlog config set`):
>
> ```yaml
> projects: ["web", "api", "mobile"]
> ```
>
> Once configured, CLI, MCP, and Web inputs accept the values case-insensitively and store the configured spelling in task frontmatter. Filter with `backlog task list --project web`, `backlog search --project web`, or repeat/comma-separate values for OR semantics. Clear a task's project with `backlog task edit <id> --project ""`. Read current values with `backlog config get projects`.

> **Date/Time Support**: Backlog.md now supports datetime precision for all dates. New items automatically include time (YYYY-MM-DD HH:mm format in UTC), while existing date-only entries remain unchanged for backward compatibility. Use the migration script `bun src/scripts/migrate-dates.ts` to optionally add time to existing items.

> **Date Display Format**: `dateFormat` only changes how dates are *displayed* in the web UI and TUI; markdown files always store dates in the canonical `yyyy-mm-dd [hh:mm]` UTC format. The format string is split at the first whitespace into a date part and an optional time part. Date part tokens (case-insensitive, each exactly once): `yyyy`, `mm` (month), `dd`; any other characters are kept literally. Time part tokens: `hh` and `mm` (minutes) — `mm` means month in the date part and minutes in the time part. If a stored value includes a time it is always shown: through the format's time part when present, otherwise appended as ` hh:mm`. Date-only values never invent a time. Invalid formats fall back to the canonical display. Agent-facing output (`--plain` CLI output and MCP responses) always stays canonical regardless of this setting. Example: `dateFormat: dd/mm/yyyy` renders `2026-07-04 21:54` as `04/07/2026 21:54`.

> **Custom Backlog Folder**: `backlog_directory` is chosen when the project is initialized — select "Custom project-relative path" in the wizard or run `backlog init --backlog-dir my-backlog --config-location root` — and init refuses to move the folder afterwards. Unlike every other key here it is read only from `backlog.config.yml` in the project root: the same key inside `backlog/config.yml` is ignored, and `backlog config` cannot set, get, or list it. The path is only checked lexically: absolute values and paths that normalize to outside the project are ignored, while a relative path that symlinks outside the repository is accepted. When the value is ignored Backlog.md uses `backlog/` or `.backlog/` if one exists, and otherwise reports that no project was found.

<!-- END ADVANCED-CONFIG.md -->

# ===== AGENTS.md of the Backlog.md repo, the BACKLOG.MD GUIDELINES block only (verbatim; the rest is contributor guidance for that repo) =====
<!-- BEGIN AGENTS.md excerpt -->
<!-- BACKLOG.MD GUIDELINES START -->
<CRITICAL_INSTRUCTION>

## Backlog.md Workflow

This project uses Backlog.md for task and project management.

**At the beginning of each conversation in this project, run `backlog instructions overview` before answering or taking action. Re-read it only if you have not read it yet in the current conversation.**

Use the overview to decide whether to search, read, create, or update Backlog tasks.

Before task lifecycle actions, read the matching detailed guide:
- `backlog instructions task-creation` before creating or splitting tasks
- `backlog instructions task-execution` before planning, changing status or assignee, adding a plan or implementation notes, or implementing task work
- `backlog instructions task-finalization` before checking acceptance criteria, writing final summaries, or moving tasks to terminal statuses

Use `backlog <command> --help` before running unfamiliar commands. Help shows options, fields, and examples.

Do not edit Backlog task, draft, document, decision, or milestone markdown files directly. Use the `backlog` CLI so metadata, relationships, and history stay consistent.

</CRITICAL_INSTRUCTION>
<!-- BACKLOG.MD GUIDELINES END -->
<!-- END AGENTS.md excerpt -->

# ===== MANIFESTO.md section "Surface Hierarchy" (verbatim excerpt, raw.githubusercontent.com HEAD) =====
<!-- BEGIN MANIFESTO.md excerpt -->
## Surface Hierarchy

The product has several interfaces, but they must express one coherent model.

1. **The CLI is canonical.** It defines the complete, scriptable workflow for humans and agents.
2. **CLI instructions are the canonical agent workflow.** They are the default way to teach an agent how to use Backlog.md.
3. **The TUI and browser are human-facing views over the same semantics.** They should make common work clear and pleasant without inventing incompatible behavior.
4. **MCP is a legacy, optional adapter.** It may remain useful for clients that prefer it, but features must not be designed MCP-first or exist only through MCP.

New capabilities begin in the shared product model and canonical CLI workflow. Other
surfaces adopt them deliberately. A convenience surface must not silently weaken
validation, safety, or meaning.

<!-- END MANIFESTO.md excerpt -->

# ===== Sample task file (verbatim, backlog/tasks/back-697 - Keep-the-Nix-AVX2-check-independent-of-the-selected-Bun-package.md, raw.githubusercontent.com HEAD) =====
<!-- BEGIN sample task file -->
---
id: BACK-697
title: Keep the Nix AVX2 check independent of the selected Bun package
status: Done
assignee:
  - '@codex-nix-check'
created_date: '2026-09-27 22:27'
updated_date: '2026-09-27 22:33'
labels: []
dependencies: []
references:
  - 'https://github.com/MrLesk/Backlog.md/issues/1009'
  - 'https://github.com/MrLesk/Backlog.md/pull/802'
  - >-
    https://github.com/NixOS/nixpkgs/commit/e439af0fbc7197adb2c600a537511828d5c6adb7
  - 'https://github.com/oven-sh/bun/releases/tag/bun-v1.3.13'
modified_files:
  - flake.nix
  - DEVELOPMENT.md
type: bug
ordinal: 327000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
A newer nixpkgs revision selects Bun baseline, but the Nix install check treats that selected archive as a known AVX2-only negative control and invokes a path it does not contain. Use an explicit known control archive while preserving the existing packaged Backlog checks on the Ivy Bridge CPU model and native package smoke checks. Do not update the flake lock or change platform support.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 The negative CPU compatibility control uses a known AVX2 archive independent of nixpkgs Bun source selection.
- [x] #2 Existing positive Backlog checks under Ivy Bridge emulation and native installed-package smoke checks remain in place.
- [x] #3 Validation covers the locked nixpkgs input and the issue-reported Bun 1.3.13 baseline input as far as the available build environment allows, with any unrun build stated explicitly.
<!-- AC:END -->

## Definition of Done
<!-- DOD:BEGIN -->
- [x] #1 Not applicable: bunx tsc --noEmit; no TypeScript changed.
- [x] #2 Not applicable: bun run check .; only Nix and Markdown changed. Scoped git diff --check passed.
- [x] #3 Not applicable: bun test; this change affects Nix packaging. Official archive hash, integrity, and executable path checks passed.
<!-- DOD:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. Pin avx2BunArchive in flake.nix directly to the official Bun 1.3.13 bun-linux-x64.zip archive with SHA-256 SRI sha256-ecB3H6i5LDOq5B4VoODTB+qZ0OLwAxfHHGxTI3p44lo=. Keep fetching the archive so the normal Bun derivation is not realized for this control.
2. Keep runtime selection, supported systems, native installed-package smoke, QEMU Ivy Bridge exit-132 control, positive CLI version/help checks, and emulation-only JIT settings unchanged. Update the matching DEVELOPMENT.md sentence.
3. Verify the complete official archive bytes, hash, ZIP integrity, and bun-linux-x64/bun path. Compare the unchanged installCheckPhase and remaining flake against HEAD; check the owned diff and unchanged flake.lock.
4. Compare source selection in locked nixpkgs 61b7c44c4073f0b827768aff0049561b5110ea5a and issue override c043004d1c6985732bcc1cbc5a9c9aecbbb4e0f0. Record that local Nix evaluation and both builds are unavailable. Fresh existing CI can prove only the locked input; no override build is claimed.
5. Keep the direct fetch pin after subtraction and architecture review, then finalize the CLI task record and commit/push only flake.nix, DEVELOPMENT.md, and this record under coordinator authorization.
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
Research only, 2026-09-27: confirmed issue #1009 and PR #802. Both the current locked nixpkgs revision (61b7c44c4073f0b827768aff0049561b5110ea5a) and the issue's override (c043004d1c6985732bcc1cbc5a9c9aecbbb4e0f0) package Bun 1.3.13. Upstream commit e439af0fbc7197adb2c600a537511828d5c6adb7 changes only the x86 Linux source URL/hash from bun-linux-x64.zip to bun-linux-x64-baseline.zip. The existing flake still treats that selected source as AVX2-only and invokes bun-linux-x64/bun.
Pin provenance: the locked nixpkgs Bun package declares sha256-ecB3H6i5LDOq5B4VoODTB+qZ0OLwAxfHHGxTI3p44lo= for the normal x64 1.3.13 archive. Official oven-sh/bun release metadata independently reports SHA-256 79c0771fa8b92c33aae41e15a0e0d307ea99d0e2f00317c71c6c53237a78e25a; conversion to SRI matches exactly. Archive-byte verification and ZIP path inspection remain part of implementation validation.
Environment: Darwin arm64; nix, nix-instantiate, qemu-x86_64, limactl, colima, and orb are not on PATH. Docker CLI is installed, but both desktop-linux and default contexts report unavailable daemons. No Nix evaluation, Linux build, or QEMU runtime proof has been run. No tools, accounts, or builders were changed.
Scope: only flake.nix and the matching existing DEVELOPMENT.md wording need source changes. The native smoke script also covers MCP/browser behavior and must remain unchanged. Source-writer release is still pending; no source, test, documentation, ref, index, or commit changes made by this task.

Coordinator released the sole source-writer slot for BACK-697. Implementing only flake.nix and the matching DEVELOPMENT.md wording; preserve all existing runtime and compatibility checks. No finalization, commits, push, or other source changes until architecture review.

Implementation frozen for architecture review: flake.nix now fetches the fixed official Bun 1.3.13 AVX2 archive directly, and DEVELOPMENT.md describes that pinned control. Owned diff: 2 files, 7 insertions, 3 deletions. No lockfile, runtime selection, supported systems, CI, or other source changes.
Validation: downloaded all 39,125,828 bytes from the official GitHub release URL into memory; computed SHA-256 SRI equals sha256-ecB3H6i5LDOq5B4VoODTB+qZ0OLwAxfHHGxTI3p44lo=; ZIP integrity passes and members are bun-linux-x64/ and bun-linux-x64/bun. Static comparison against HEAD confirms the entire flake is unchanged except avx2BunArchive, including the complete native smoke and QEMU installCheckPhase. The full gate SHA-256 is 592cf74d80e6a5ffa1670201d45d95545eb2b075458e728485bafd0a80384fa4. git diff --check passes for both owned files; git diff --exit-code -- flake.lock passes.
Validation limit: nix, nix-instantiate, nixfmt, alejandra, and statix are unavailable. No Nix syntax evaluation, locked-input build, c043004 override build, or QEMU runtime check was run. Docker remains unavailable; no environment changes made. The source/hash comparison covers both selected Bun 1.3.13 inputs but does not prove either build. An unrelated full Bun suite was not run.
Subtraction review: one direct fetch binding and one matching documentation edit are sufficient. No new helper, layer, test file, or remaining task-scoped simplification identified. Frozen source SHA-256: flake.nix dc824a60f4d26fb33c2659ac4375849b1d171f3c47d544e54f210c3391d737b0; DEVELOPMENT.md 8da35a4376b76233cc693ce0d57205a49f16bb3ac6c517de486566bee359d049. No task finalization, commit, push, checkout, ref, or index changes.

Finalization authorized after architecture review recommended keeping the frozen diff unchanged, with no findings, and the coordinator presented that result to Alex. Rechecked reviewed source hashes and the empty Git index before finalization. All three acceptance criteria are supported by the archive/source evidence and preserved gate comparison above; criterion 3 explicitly permits validation within available tooling and records every unrun build. Default TypeScript/Biome/Bun checklist entries are restated as not applicable to avoid claiming commands that were not run.
<!-- SECTION:NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Pinned the AVX2 negative-control archive to official Bun 1.3.13 independently of nixpkgs Bun source selection, fixing the baseline archive/path mismatch. Updated DEVELOPMENT.md. Native package smoke, positive and negative Ivy Bridge checks, JIT settings, runtime selection, supported systems, and flake.lock remain unchanged.
Verified the official 39,125,828-byte archive against SHA-256 SRI sha256-ecB3H6i5LDOq5B4VoODTB+qZ0OLwAxfHHGxTI3p44lo=, ZIP integrity, and bun-linux-x64/bun. The full installCheckPhase is byte-for-byte unchanged; scoped diff checks pass. Architecture review recommended keeping the change unchanged with no findings.
Local Nix evaluation, locked-input build, issue-override build, and QEMU execution were unavailable and were not run. TypeScript, Biome project checks, and Bun tests are not applicable to this Nix/Markdown-only change and were not claimed. The coordinator will monitor fresh locked-input CI; that does not prove the issue override was built.
<!-- SECTION:FINAL_SUMMARY:END -->

<!-- END sample task file -->

# ===== Jina render of the repo page: fields recorded (per GitHub page via Jina on 2026-10-04) =====
- Title line: "GitHub - MrLesk/Backlog.md: Backlog.md - A tool for managing project collaboration between humans and AI Agents in a git ecosystem"
- Repo root page (https://github.com/MrLesk/Backlog.md): README text only; star and licence badges are images, so no star number appears.
- Tree page (https://github.com/MrLesk/Backlog.md/tree/main/backlog/tasks): header lines "Fork 441", "Star 6.9k", "Issues 61", "Pull requests 15"; "Latest commit" for the folder: "BACK-706 - Remove redundant tests while preserving shipped behavior c…" on Sep 28, 2026 (69e7b15).

# ===== AGENTS.md of the Backlog.md repo, section "Git Workflow" (verbatim excerpt; this is the Backlog.md project's own contributor convention) =====
<!-- BEGIN AGENTS.md Git Workflow excerpt -->
## Git Workflow

- **Branching**: Use feature branches when working on tasks (e.g. `tasks/back-123-feature-name`)
- **Committing**: Use the following format: `BACK-123 - Title of the task`
- **PR titles**: Use `{taskId} - {taskTitle}` (e.g. `BACK-123 - Title of the task`)
- **Github CLI**: Use `gh` whenever possible for PRs and issues

<!-- END AGENTS.md Git Workflow excerpt -->

# ===== Evidence for the status flag on task edit (verbatim phrase from the description of PR #1036 as shown on the Jina tree page) =====
- "`backlog task edit 1 -s \"In Progress\" --priority high` produced the updated list 0.07 s after the command returned" (BACK-689 / PR #1036, 2026-09-23)
