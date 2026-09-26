---
title: "obsidian-skills: Agent Skills for Obsidian"
slug: 20260918-obsidian-skills
type: repo
status: draft
source_url: "https://github.com/kepano/obsidian-skills"
source_platform: github
author: "kepano"
published: "2026-01-02"
captured_at: "2026-09-18T00:00:00Z"
captured_by: "routine:capture-link"
canonical_id: "github:kepano/obsidian-skills"
engagement: "commits=46"
tags: [obsidian, agent-skills, llm-wiki, claude-code, knowledge-management]
related: []
needs_manual_text: false
---

## 摘要

這是由 Obsidian 核心開發者 kepano 創建的 Agent Skills 套件，專為在 Obsidian vault 中使用 AI 助理而設計。套件遵循 [agentskills.io](https://agentskills.io/specification) 規範，可與 Claude Code、Codex、OpenCode 等任何相容的 AI 助理配合使用。內含六個技能：obsidian-markdown（Obsidian 風格 Markdown）、obsidian-bases（Bases 資料庫）、json-canvas（JSON 畫布）、obsidian-cli（命令列操作）、defuddle（網頁內容淨化）和 knap（範本批量渲染）。安裝方式多樣，支援 Claude Code 插件市場、npx 一行指令或手動複製。此套件讓 AI 助理真正「懂」Obsidian 的原生格式與工具，大幅提升在 vault 內的操作效率。

## Key facts

- **Repo**: `kepano/obsidian-skills` — by kepano (creator of Obsidian's Minimal theme and core contributor)
- **Spec**: Follows [Agent Skills specification](https://agentskills.io/specification); compatible with Claude Code, Codex, OpenCode
- **Skills included** (6):
  - `obsidian-markdown` — create/edit Obsidian Flavored Markdown with wikilinks, embeds, callouts, properties
  - `obsidian-bases` — create/edit Obsidian Bases (`.base`) with views, filters, formulas, summaries
  - `json-canvas` — create/edit JSON Canvas (`.canvas`) with nodes, edges, groups, connections
  - `obsidian-cli` — interact with Obsidian vaults via the Obsidian CLI; plugin/theme dev
  - `defuddle` — extract clean markdown from web pages, removing clutter to save tokens
  - `knap` — render Markdown templates from JSON or CSV data; batch file generation
- **Install via Claude Code marketplace**:
  ```
  /plugin marketplace add kepano/obsidian-skills
  /plugin install obsidian@obsidian-skills
  ```
- **Install via npx**:
  ```
  npx skills add git@github.com:kepano/obsidian-skills.git
  # or HTTPS:
  npx skills add https://github.com/kepano/obsidian-skills
  ```
- **Install manually for Claude Code**: add repo contents to `/.claude` in your Obsidian vault root
- **Install for OpenCode**: `git clone https://github.com/kepano/obsidian-skills.git ~/.opencode/skills/obsidian-skills` (clone the full repo, not just `skills/`)
- **Install for Codex**: copy `skills/` directory to `~/.codex/skills`

## 點解值得留意

- Josep 的 skills-vault 本身就是一個 Obsidian vault，`obsidian-markdown` 和 `obsidian-cli` 技能可以直接套用，讓 AI 助理更正確地編輯 vault 內的 wiki 頁面格式
- `defuddle` 技能與 `vault-capture` 的 Jina Reader 步驟互補：可在抓取網頁後用 defuddle 進一步清理，節省 token
- `knap` 的 JSON/CSV 批量模板渲染功能，有潛力自動化 `wiki/pages/` 的生成流程
- kepano 是 Obsidian 生態的重要貢獻者，這套 skills 代表一種「官方認可」的 agent-Obsidian 互動範式，值得追蹤後續更新

## Source

- **URL**: https://github.com/kepano/obsidian-skills
- **Author**: kepano
- **Published**: 2025 (approx, repo has 46 commits)
- **Reader**: github-raw (README) + exa (repo page)

## Related

- [[../../skills/using-obsidian-skills/SKILL|skill: using-obsidian-skills]]
- [[20260904-jackywine-obsidian-2026|2026 我的 Obsidian 完整分享]]
