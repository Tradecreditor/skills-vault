---
name: using-obsidian-skills
description: Installs kepano/obsidian-skills (obsidian-markdown, obsidian-bases, json-canvas, obsidian-cli, defuddle, knap) into a project or Obsidian vault. Use when asked to install or set up obsidian-skills, or to choose which of its skills a vault needs.
metadata:
  source_url: "https://github.com/kepano/obsidian-skills"
  source_platform: "github"
  author: "kepano"
  captured_at: "2026-09-18"
  engagement: "commits=46"
  origin_type: "repo"
  vault_status: "draft"
  reviewed_at: "2026-10-07T16:04:28Z"
  reviewed_by: "claude-code-cloud:vault-skill-reviewer"
  review_hash: "c91c7b03fa42fe33d7a82e2c93fed9b26768883061ecada214083ed694554cd2"
  review_report: "outputs/skill-reviews/2026-10-07-using-obsidian-skills.md"
---

# using-obsidian-skills

Installs the `kepano/obsidian-skills` Agent Skills pack so a compatible agent (Claude Code, Codex, OpenCode) has Obsidian-format skills, and helps pick which of its six skills a vault needs. It is an install and setup skill only: once the pack is installed, its own skills handle editing; this skill does not trigger on note edits, link captures or page scraping (`vault-capture` owns captures).

## Steps

1. **Check whether it is already installed. Install only if it is not.** Upstream README (https://raw.githubusercontent.com/kepano/obsidian-skills/main/README.md) names these install locations; look in each that applies:
   ```bash
   # Marketplace install: plugin id is obsidian@obsidian-skills
   grep -s "obsidian@obsidian-skills" .claude/settings.json .claude/settings.local.json ~/.claude/settings.json
   # npx skills / manual Claude Code install: skill folders in the vault's .claude/ (or .agents/skills/)
   ls -d .claude/skills/obsidian-markdown .agents/skills/obsidian-markdown 2>/dev/null
   # Codex: ~/.codex/skills; OpenCode: ~/.opencode/skills/obsidian-skills/skills/
   ls -d ~/.codex/skills/obsidian-markdown ~/.opencode/skills/obsidian-skills/skills/obsidian-markdown 2>/dev/null
   ```
   Any hit means it is installed: report where, and stop. No hit means install (step 3).
2. **Choose the skills** the vault needs from the table below; the pack installs all six together, so this only decides what to tell the user about.
3. **Install** with the option matching the agent (all from the upstream README; none is pinned to a tag or commit).
4. **Verify** by repeating the step 1 check and reporting the path found. Restart the agent if it does not list the skills (the README says OpenCode needs a restart).

## Skills included

| Skill | Purpose |
|---|---|
| `obsidian-markdown` | Obsidian Flavored Markdown: wikilinks, embeds, callouts, frontmatter properties |
| `obsidian-bases` | Obsidian Bases (`.base`): views, filters, formulas, summaries |
| `json-canvas` | JSON Canvas (`.canvas`): nodes, edges, groups, connections |
| `obsidian-cli` | Obsidian CLI: vault interaction, plugin/theme development |
| `defuddle` | Web page to clean markdown, removing navigation/ads to save tokens |
| `knap` | Template rendering from JSON/CSV; batch `.md` file generation |

## Installation options

### Option A: Claude Code marketplace
```
/plugin marketplace add kepano/obsidian-skills
/plugin install obsidian@obsidian-skills
```

### Option B: npx skills
```bash
# SSH
npx skills add git@github.com:kepano/obsidian-skills.git
# HTTPS
npx skills add https://github.com/kepano/obsidian-skills
```

### Option C: Manual, Claude Code
Add the contents of the repo to a `.claude/` folder in the root of the Obsidian vault (or the folder used with Claude Code). The upstream README writes this as `/.claude`; it means a folder in the vault root, not the filesystem root. In this vault `.claude/` is a protected path, so a non-core agent must not edit it: use the marketplace option or install in a different project.

### Option D: Manual, OpenCode
```bash
git clone https://github.com/kepano/obsidian-skills.git ~/.opencode/skills/obsidian-skills
```
Clone the full repo; do not copy only the inner `skills/` folder. The result must be `~/.opencode/skills/obsidian-skills/skills/<skill-name>/SKILL.md`. OpenCode auto-discovers `SKILL.md` files there; no config change is needed.

### Option E: Manual, Codex
Copy the repo's `skills/` directory into the Codex skills path (typically `~/.codex/skills`), so the result is `~/.codex/skills/<skill-name>/SKILL.md`, not `~/.codex/skills/skills/`.

## Pitfalls

- This skill is `vault_status: draft` until reviewed; never auto-run its commands from another project. The upstream pack is third-party code and is not audited by this vault.
- `defuddle` requires the [Defuddle](https://github.com/kepano/defuddle) CLI installed separately; `knap` requires the [Knap](https://github.com/obsidianmd/knap) tool. This skill gives no install command for either.

## Source

https://github.com/kepano/obsidian-skills (kepano); README read 2026-11-10 via `scripts/read-url.sh` (reader: jina).
