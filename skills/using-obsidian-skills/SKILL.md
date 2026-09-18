---
name: using-obsidian-skills
description: Installs and applies kepano/obsidian-skills (obsidian-markdown, obsidian-bases, json-canvas, obsidian-cli, defuddle, knap) in any agent working inside an Obsidian vault. Use when editing .md/.base/.canvas files, using Obsidian CLI, or scraping web pages inside a vault.
metadata:
  source_url: "https://github.com/kepano/obsidian-skills"
  source_platform: "github"
  author: "kepano"
  captured_at: "2026-09-18"
  engagement: "commits=46"
  origin_type: "repo"
  vault_status: "draft"
---

# using-obsidian-skills

Install and use the `kepano/obsidian-skills` Agent Skills pack so any compatible agent (Claude Code, Codex, OpenCode) can correctly author Obsidian-native file formats and interact with the Obsidian CLI.

## When to use

- Working inside an Obsidian vault with Claude Code or another agent
- Editing `.md` files that use Obsidian-flavored syntax (wikilinks, embeds, callouts, properties)
- Creating or editing `.base` (Obsidian Bases) or `.canvas` (JSON Canvas) files
- Using the Obsidian CLI for plugin/theme development
- Extracting clean markdown from web pages before saving to a vault (defuddle)
- Batch-rendering Markdown templates from JSON/CSV data (knap)

## Skills included

| Skill | Purpose |
|---|---|
| `obsidian-markdown` | Obsidian Flavored Markdown: wikilinks, embeds, callouts, frontmatter properties |
| `obsidian-bases` | Obsidian Bases (`.base`): views, filters, formulas, summaries |
| `json-canvas` | JSON Canvas (`.canvas`): nodes, edges, groups, connections |
| `obsidian-cli` | Obsidian CLI: vault interaction, plugin/theme development |
| `defuddle` | Web page → clean markdown, removing navigation/ads to save tokens |
| `knap` | Template rendering from JSON/CSV; batch `.md` file generation |

## Installation

### Option A: Claude Code Marketplace (recommended)
```
/plugin marketplace add kepano/obsidian-skills
/plugin install obsidian@obsidian-skills
```

### Option B: npx
```bash
# SSH
npx skills add git@github.com:kepano/obsidian-skills.git
# HTTPS
npx skills add https://github.com/kepano/obsidian-skills
```

### Option C: Manual — Claude Code
Add the repo contents to `/.claude` in your Obsidian vault root (the folder you open with Claude Code).

### Option D: Manual — OpenCode
```bash
git clone https://github.com/kepano/obsidian-skills.git ~/.opencode/skills/obsidian-skills
# Clone the full repo; do NOT copy only the inner skills/ folder
# OpenCode auto-discovers SKILL.md files — no config changes needed
```

### Option E: Manual — Codex
Copy the `skills/` directory to `~/.codex/skills`.

## Pitfalls

- For OpenCode: clone the **full repo** into `~/.opencode/skills/obsidian-skills/`, not just the inner `skills/` subfolder — otherwise the path structure breaks auto-discovery.
- Skills are `vault_status: draft` until Josep reviews; do not auto-run skill commands from a draft in another project.
- `defuddle` requires the [Defuddle](https://github.com/kepano/defuddle) CLI to be installed separately.
- `knap` requires the [Knap](https://github.com/obsidianmd/knap) tool.

## Source

https://github.com/kepano/obsidian-skills — kepano — agentskills.io specification
