---
title: "career-ops"
slug: career-ops-hq--career-ops
type: repo
status: draft
source_url: "https://github.com/career-ops-hq/career-ops"
source_platform: github
author: "Santiago Fernández de Valderrama Aparicio (santifer)"
published: "2026-04-04"
captured_at: "2026-09-21T23:07:37Z"
captured_by: "routine:github-stars-sync"
canonical_id: "github:career-ops-hq/career-ops"
engagement: "stars=72352 forks=13619"
tags: [ai-agent, job-search, career, claude-code, cli]
related: []
needs_manual_text: false
---

## 摘要
career-ops 係一個開源、本機運行嘅 AI 求職系統,直接喺你已經用緊嘅 AI coding CLI(Claude Code、Codex、OpenCode 等)入面運作。佢會將每個職位評估做一份 A 到 H 嘅結構化報告,用五個維度嘅整體判斷得出 1-5 分嘅總分(唔係單純加減乘除公式),仲會自動生成 ATS 優化嘅 CV、掃描 Greenhouse/Ashby/Lever 等招聘平台、批量並行評估幾十個職位,同埋幫手搵返間公司入面啱傾嘅聯絡人。作者強調呢個系統「只評估、唔代交」:唔會自動幫你 submit 申請、唔會發 email、唔會 phone home 傳送你嘅資料,一切決定權都喺用家手上。作者自己用呢個系統評估咗 740 幾個職位、生成 100 幾份 CV,最後攞到一個 Head of Applied AI 嘅職位。

## Key facts
- Language: JavaScript
- License: MIT
- Created: 2026-04-04
- Last pushed: 2026-09-21
- Stars: 72,352
- Forks: 13,619
- Install: `npx @santifer/career-ops init`(或者 `git clone` + `npm install`)
- 支援 Claude Code、Codex、OpenCode、Antigravity CLI、Grok Build CLI 等多個 AI CLI,透過 `.agents/skills/career-ops/SKILL.md` 統一 skill 入口

## 點解值得留意
同呢個 vault 之前收錄過嘅 MadsLorentzen/ai-job-search 屬於同一個垂直領域(AI 求職自動化),但呢個項目社群規模大好多(7 萬幾星),而且特登用一個「Manifesto」同一份好詳細嘅「呢個系統唔會做咩」清單嚟建立信任(唔自動投遞、唔發送 email、唔傳送資料)。值得對比兩個項目喺 agent-skill 包裝、CLI 整合手法上嘅設計差異。

## Source
GitHub repository: https://github.com/career-ops-hq/career-ops
Author: Santiago Fernández de Valderrama Aparicio (santifer)
Published: 2026-04-04
Reader used: raw README via Exa (web_fetch_exa)

## Related
[[MadsLorentzen--ai-job-search]] (same vertical, different project)
