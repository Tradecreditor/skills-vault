---
title: "agent-skills"
slug: addyosmani--agent-skills
type: repo
status: draft
source_url: "https://github.com/addyosmani/agent-skills"
source_platform: github
author: "addyosmani"
published: "2026-02-15"
captured_at: "2026-11-11T06:02:51Z"
captured_by: "routine:github-stars-sync"
canonical_id: "github:addyosmani/agent-skills"
engagement: "stars=115331 forks=12108"
tags: ["agent-skills", "claude-code", "codex", "cursor", "antigravity", "skills"]
related: []
needs_manual_text: false
---
## 摘要

Agent Skills 係 Addy Osmani 整理嘅一套「生產級工程技能」，目標係令 AI coding agent 好似資深工程師咁，每個開發階段都跟足流程同品質關卡。成個包有 25 個 skill（24 個生命週期 skill 加一個 `using-agent-skills` 元 skill），按 Define、Plan、Build、Verify、Review、Ship 六個階段分類，例如 spec-driven-development、test-driven-development、code-review-and-quality、security-and-hardening、shipping-and-launch。另有 9 個 slash command（`/spec`、`/plan`、`/build`、`/test`、`/review`、`/ship` 等）同四個 agent persona（code-reviewer、test-engineer、security-auditor、web-performance-auditor）。`/build auto` 可以一次過批准計劃後自動逐個 task 實作，每個 task 仍然測試同獨立 commit。支援 Claude Code、Cursor、Codex、Gemini CLI、Copilot、Windsurf、Kiro 等多個 agent。

## Key facts

- **Repo**: [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills)
- **Stars**: 115,331 | **Forks**: 12,108
- **Language**: JavaScript
- **License**: MIT
- **Last push**: 2026-11-01
- **Install (any agent)**: `npx skills add addyosmani/agent-skills` (all 25) or `--skill <name>` for one; `--list` to browse
- **Claude Code**: `/plugin marketplace add addyosmani/agent-skills` then `/plugin install agent-skills@addy-agent-skills`
- **Caveat**: installing a single skill via npx omits the repo-level `references/` checklists (issue #361).

## 點解值得留意

呢個係一套有完整生命週期嘅工程流程 skill 包，同 vault 嘅 skill 庫可以互相對照，尤其係 spec-driven、doubt-driven 同 constraint-driven development 呢類「防 agent 偷懶」嘅設計。Star 數過十一萬，社群驗證度高，但 skill 數量多，全裝會增加 context 負擔，建議揀要用嘅先裝。安裝前應先用 scanning-agent-skills 掃描，並留意佢未有喺 vault 內草擬 skill，因為佢本身係一個 skill 集合而唔係單一 skill。

## Source

- URL: https://github.com/addyosmani/agent-skills
- Created: 2026-02-15
- Reader: Jina Reader (GitHub API JSON) + raw.githubusercontent.com README
