---
name: tracking-tasks-with-backlog-md
description: "Tracks agent and human work as Markdown task files with Backlog.md: init a backlog in a repo, create and move tasks on a CLI or local web Kanban, and let Claude Code, Codex or Gemini CLI work the board via CLI or MCP. Use when asked for a kanban, task board, backlog or to-do tracking for agents."
metadata:
  source_url: "https://github.com/MrLesk/Backlog.md"
  source_platform: "github"
  author: "MrLesk"
  captured_at: "2026-10-04T21:22:27Z"
  engagement: "stars=6.9k forks=441"
  origin_type: "repo"
  vault_status: "reviewer-approved"
  reviewed_at: "2026-10-05T07:49:32Z"
  reviewed_by: "routine:skill-review"
  review_hash: "a98f330fffff99307a3f4662875a8cec2b2ba19f3e41a3b817c9196810ebf3b9"
  review_report: "outputs/skill-reviews/2026-10-05-tracking-tasks-with-backlog-md.md"
---

# tracking-tasks-with-backlog-md

Backlog.md turns a Git repo (or any folder) into a project board where every task is a plain `.md` file, edited through a `backlog` CLI, a terminal Kanban, a local web Kanban, or an MCP server. Commands below are copied from the project README and CLI reference (github.com/MrLesk/Backlog.md) and were not run when this skill was drafted. Verbatim sources: `raw/20261004-backlog-md-markdown-kanban-for-agents.md`.

## When to use

- A person asks for a kanban, task board, backlog, or to-do tracking that Claude Code, Codex, Gemini CLI or Kiro can also read and update.
- Work should follow a reviewable loop: spec (tasks with acceptance criteria), then plan, then code, one task per PR.
- Task state should live in the repo as Markdown (diffable, Obsidian-friendly), with no server, account or telemetry.
- Not for a hosted team tracker (Linear, Jira): Backlog.md is local-first and file-based.

## Prerequisites

- Node.js with npm (or Bun, Homebrew or Nix, see step 1). The README states no minimum Node version, so check `backlog --version` after install.
- Permission to add a backlog folder (`backlog/` by default) to the target repo, and to let `backlog init` write an instruction block into `AGENTS.md`.
- In the skills vault: do not adopt it inside the vault itself yet. `backlog/` is not in `CLAUDE.md`'s folder-role table, so adopting it needs a `docs:` edit first, and `AGENTS.md` is a protected identical copy of `CLAUDE.md`. Try it in a separate project repo.
- Scan before installing (`skills/scanning-agent-skills`) and confirm the npm package `backlog.md` links to github.com/MrLesk/Backlog.md. Never run commands from a draft skill in another project unprompted.

## Steps

### 1. Install

```bash
npm i -g backlog.md
```

Global install from npm. README alternatives: `bun add -g backlog.md`, `brew install backlog-md`, `nix run github:MrLesk/Backlog.md`.

```bash
npx backlog.md init "My Project"
```

One-off run without installing. Use the full name `backlog.md`: plain `npx backlog` resolves to an unrelated third-party package.

### 2. Initialise a backlog

```bash
backlog init "My Awesome Project"
```

Creates the backlog structure in a Git repo through a short wizard (project name, backlog folder `backlog/` or `.backlog/` or a custom path, config location, AI integration).

```bash
backlog init "Personal Planning" --no-git
```

Filesystem-only project for non-code work; the saved config sets `checkActiveBranches=false`, `remoteOperations=false`, `autoCommit=false`.

Wizard choice for AI tools (README):

- CLI instructions (recommended): writes a short instruction file that tells agents to run `backlog instructions overview`. Scriptable with `--agent-instructions` (`--agent-instructions cursor` also targets AGENTS.md).
- MCP connector: auto-configures Claude Code, Codex, Gemini CLI, Kiro or Cursor.
- Skip: use it purely as a task manager.

Other documented init flags: `--task-prefix` (default IDs look like `TASK-1`), `--defaults`, `--backlog-dir <path>` with `--config-location <folder|root>`. Re-running `backlog init` or `backlog config` keeps current values.

### 3. Optional: connect an MCP client by hand

```bash
claude mcp add backlog --scope user -- backlog mcp start
codex mcp add backlog -- backlog mcp start
gemini mcp add backlog -s user backlog mcp start
```

Registers one user-scope server named `backlog` that follows the client's workspace. When adding MCP manually, add a line to CLAUDE.md or AGENTS.md telling agents to read `backlog://workflow/overview`. To pin one project, set `BACKLOG_CWD` in the server env or pass `"args": ["mcp", "start", "--cwd", "/absolute/path/to/your/project"]`. Check with `/mcp` in the AI tool.

### 4. Create and refine tasks

```bash
backlog task create "Render markdown as kanban"
backlog task edit BACK-1 -d "Detailed context" --ac "Clear acceptance criteria"
```

README examples (`BACK-1` is the README's example ID; your prefix is `TASK` unless set).

```bash
backlog task create "Feature" -d "Description" -a @sara -s "To Do" -l auth --priority high --ac "Must work" --dep task-1 -p 14
```

CLI reference: description, assignee, status, labels, priority, acceptance criteria, dependency and parent (`-p`, makes a sub-task). Also `--plan`, `--notes`, `--dod`, `--due-date 2026-08-10`, `--ref`, `--doc`, `--draft`.

Let an agent do the splitting (README prompt): "I want to add a search feature to the web view that searches tasks, docs, and decisions. Please decompose this into small Backlog.md tasks." Review checkpoint 1: read the descriptions and acceptance criteria.

### 5. The task file format

Tasks are Markdown files with YAML frontmatter in the backlog folder (this project's own repo: `backlog/tasks/back-697 - Keep-the-Nix-AVX2-check-independent-of-the-selected-Bun-package.md`). Observed in one real file, not a documented spec:

```markdown
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
modified_files:
  - flake.nix
type: bug
ordinal: 327000
---

## Description
<!-- SECTION:DESCRIPTION:BEGIN -->
...
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 ...
<!-- AC:END -->
```

Further sections in the same file: Definition of Done (`<!-- DOD:BEGIN -->`), Implementation Plan (`SECTION:PLAN`), Implementation Notes (`SECTION:NOTES`), Final Summary (`SECTION:FINAL_SUMMARY`). Default status columns are To Do, In Progress, Done. Read the real shape with `backlog task 7 --plain` instead of guessing.

### 6. See the board

```bash
backlog board
```

Live Kanban in the terminal (press `E` to edit a task in your editor). `backlog board export [file]` writes a shareable markdown snapshot.

```bash
backlog browser
```

Local web Kanban with drag-and-drop on `127.0.0.1:6420`, opens the browser. Add `--port 8080` to change the port and `--no-open` to stay headless.

### 7. Let an agent pick up and finish a task

1. Agent starts with `backlog instructions overview`, then reads the matching guide before acting: `backlog instructions task-creation`, `backlog instructions task-execution`, `backlog instructions task-finalization` (over MCP: `backlog://workflow/overview` and the same three names).
2. One task per agent session and one PR per task. README prompt: "Work on BACK-10 only. Research the codebase and write an implementation plan in the task. Wait for my approval before coding."
3. Find work: `backlog task list -s "To Do"`; read it with `backlog task 7 --plain`; machine-readable: `backlog task list --json` (also on `task view` and `search`).
4. Take it and record the plan: `backlog task edit 7 -a @your-agent-name -s "In Progress"` (the status flag is shown on `task create` in the CLI reference and on `task edit` in a project PR; confirm with `backlog task edit --help`), then `backlog task edit 7 --plan "Implementation approach"`. Review checkpoint 2: the human approves the plan.
5. Implement, then log and tick: `backlog task edit 7 --append-notes "New findings"`, `backlog task edit 7 --check-ac 1`, `backlog task edit 7 --final-summary "Completion summary"`. Review checkpoint 3: human reviews code and tests.
6. Mark verified work Done (or the configured final status). During cleanup `backlog task complete 7` moves finished work off the board and keeps its record; `backlog task archive 7` is for canceled, duplicate or invalid work.
7. Project convention for PRs (the Backlog.md repo's own AGENTS.md): branch `tasks/back-123-feature-name`, commit `BACK-123 - Title of the task`, PR title `{taskId} - {taskTitle}`.

Without an agent, the same files work from the CLI or browser: `backlog task list -s "To Do"`, `backlog search "kanban"`, `backlog board`, `backlog browser`.

### 8. Configure when needed

`backlog config` opens the wizard; `backlog config list`, `backlog config get defaultEditor`, `backlog config set autoCommit true`. Defaults: `statuses` To Do / In Progress / Done, `defaultPort` 6420, `autoCommit` false, `remoteOperations` true, `checkActiveBranches` true. Full list: ADVANCED-CONFIG.md in the repo.

## Pitfalls

- Prefer the CLI, MCP or web UI over hand-editing task files (README); never pick or reserve task IDs yourself. The repo's own guidelines block says not to edit task, draft, document, decision or milestone files directly.
- Multi-line text: `\n` is not converted. Repeat `--append-notes` per line or use real newlines inside double quotes. Text with literal backticks needs single-quoted arguments or the shell runs them as command substitution.
- Vault placement: `backlog init` writes to `AGENTS.md` (and `backlog agents --update-instructions` touches CLAUDE.md, AGENTS.md, GEMINI.md, copilot-instructions). Those are protected, identical-copy files here. Do not run init in the Obsidian vault folder until Josep has approved the `docs:` change.
- The web UI binds `127.0.0.1` only, so it is not reachable from other devices; in a cloud or remote session you would need port forwarding (an inference, not in the README).
- `onStatusChange` in config runs a shell command on every status change (the ADVANCED-CONFIG.md example launches `claude`). Never set it from untrusted text.
- MCP is optional: the project MANIFESTO calls it a "legacy, optional adapter" and the CLI canonical. Prefer CLI instructions unless the person wants MCP.
- Cross-branch checks (`checkActiveBranches`) can slow big repos; `remoteOperations: false` works offline. On Apple Silicon a Rosetta Node can install the wrong binary (README Troubleshooting).
- Unverified: exact star count and maintenance. 6.9k stars and 441 forks are the rounded figures from the GitHub page via Jina on 2026-10-04 (REST API returned 403); npm `1.53.0` was published 2026-09-24. The README says nearly all of the project's own code is written by AI agents.
- The frontmatter above comes from a single sample file and may change between versions; trust `backlog task <id> --plain` and `backlog <command> --help`.

## Source

- Repo and README: https://github.com/MrLesk/Backlog.md (MIT; npm package `backlog.md`, latest 1.53.0, 2026-09-24)
- Docs used: CLI-INSTRUCTIONS.md, ADVANCED-CONFIG.md, AGENTS.md and MANIFESTO.md in the repo
- Vault note: wiki/pages/20261004-backlog-md-markdown-kanban-for-agents.md and raw/20261004-backlog-md-markdown-kanban-for-agents.md
