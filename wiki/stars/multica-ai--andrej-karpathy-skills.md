---
title: "andrej-karpathy-skills"
slug: multica-ai--andrej-karpathy-skills
type: repo
status: draft
source_url: "https://github.com/multica-ai/andrej-karpathy-skills"
source_platform: github
author: "multica-ai"
published: "2026-01-27"
captured_at: "2026-10-16T06:10:15Z"
captured_by: "routine:github-stars-sync"
canonical_id: "github:multica-ai/andrej-karpathy-skills"
engagement: "stars=220137 forks=22129"
tags: ["claude-code", "claude-md", "guidelines", "karpathy", "prompt-engineering"]
related: [DietrichGebert--ponytail]
needs_manual_text: false
---
## 摘要

呢個 repo 其實就係一個 `CLAUDE.md` 檔案，目的係改善 Claude Code 嘅行為，內容源自 Andrej Karpathy 對 LLM 寫代碼常見毛病嘅觀察：靜靜雞作出錯誤假設、過度複雜化代碼、順手改動自己唔理解嘅部分。檔案濃縮成四條原則：先諗後寫（Think Before Coding）、簡單優先（Simplicity First）、精準改動（Surgical Changes）、以目標驅動執行（Goal-Driven Execution）。最後一條教你將「修 bug」變成「先寫會重現問題嘅測試，再令佢通過」，令 LLM 可以自己循環直至達標。README 亦提供 Claude Code plugin 安裝、直接 curl 落 CLAUDE.md，以及 Cursor rule 三種用法，並提醒呢套準則偏向謹慎多於速度。

## Key facts

- **Repo**: [multica-ai/andrej-karpathy-skills](https://github.com/multica-ai/andrej-karpathy-skills)
- **Stars**: 220,137 | **Forks**: 22,129
- **Language**: none (Markdown only)
- **License**: MIT (per README; GitHub API reports none)
- **Last push**: 2026-04-20
- **Install (plugin)**: `/plugin marketplace add forrestchang/andrej-karpathy-skills` then `/plugin install andrej-karpathy-skills@karpathy-skills`
- **Install (per project)**: `curl -o CLAUDE.md https://raw.githubusercontent.com/forrestchang/andrej-karpathy-skills/main/CLAUDE.md`
- **Also**: committed Cursor rule at `.cursor/rules/karpathy-guidelines.mdc`

## 點解值得留意

同 ponytail 一樣針對 agent「過度建構」嘅通病，但範圍更闊，連「亂作假設」同「順手改無關代碼」都管到，而且只需要一個檔案，零依賴。Star 數過 22 萬，反映呢套 CLAUDE.md 寫法已成社群共識。對本 vault 嚟講，可以拎嚟同 CLAUDE.md 現有規則對照，睇下有冇值得借用嘅原則；「每行改動都要追溯到用戶需求」呢個測試尤其實用。

## Source

- URL: https://github.com/multica-ai/andrej-karpathy-skills
- Created: 2026-01-27
- Reader: routine:github-stars-sync (Exa, raw README)
