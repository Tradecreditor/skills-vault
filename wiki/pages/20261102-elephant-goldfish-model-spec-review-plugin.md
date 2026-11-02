---
title: "google/elephant-goldfish-model — EGM: draft specs with a deep-context agent, review them with zero-context subagents"
slug: 20261102-elephant-goldfish-model-spec-review-plugin
type: repo
status: draft
source_url: "https://github.com/google/elephant-goldfish-model"
source_platform: github
author: "google"
published: "2026-09-13"
captured_at: "2026-11-02T08:50:00Z"
captured_by: "routine:weekly-hot-list"
canonical_id: "github:google/elephant-goldfish-model"
engagement: "stars=9544 forks=623 (+8316 stars from 1209 in the 2026-10-26 snapshot to 9525 at the W44 sweep)"
tags: [hot-list, 2026-W44, agent-skills, claude-code-plugin, codex-plugin, spec-driven-development, design-review, subagents, google]
related: [hot-list/2026-W44]
needs_manual_text: false
---

## 摘要

Elephant-Goldfish Model（EGM）係 Google 開源嘅 coding agent 插件，口號係「用大象做設計，用金魚做 review」。「大象」agent 記住成個項目嘅 context，同你一齊寫 spec；「金魚」reviewer 係全新、冇對話記憶嘅 subagent，只睇份草稿同引用嘅源碼，專門揾出冇講明嘅假設同盲點；最後由你拍板架構取捨先至寫 code。佢有 brainstorm、draft、review、resolve、bootstrap、review-loop、drift-report 七個 skill，Claude Code、Codex 同 Antigravity 都裝得到。README 話已經有幾千個 Google 工程師用緊。一星期由 1,209 星升到 9,525 星（+8,316），係 2026-W44 hot list 第二名。

## Key facts

- **Install (Claude Code)**: `claude plugin marketplace add google/elephant-goldfish-model` then `claude plugin install egm@egm`. **Codex**: `codex plugin marketplace add google/elephant-goldfish-model`, `codex plugin add egm@egm`. **Antigravity CLI**: `agy plugin install https://github.com/google/elephant-goldfish-model`. Start a new session after installing.
- **Workflow**: `/egm:egm-brainstorm <feature>` → `concepts_brief.md`; `/egm:egm-draft` → `design_draft.md`, section by section; `/egm:egm-review design_draft.md` → fresh reviewers check design, clarity, fit with the code and the implementation plan (five stages). Other skills: `egm-resolve`, `egm-bootstrap` (docs for an existing codebase), `egm-review-loop`, `egm-drift-report` (docs vs current source).
- **Requirement**: goldfish reviews need fresh subagent contexts; if the agent cannot create them, EGM stops the review. Use it for features that need design decisions, not small bug fixes.
- **Numbers**: 9,525 stars at the W44 sweep (2026-11-02 ~08:10 UTC) against 1,209 in the 2026-10-26 snapshot: **+8,316 in 7 days**; 9,544 / 623 forks shortly after. Created 2026-09-13. Topics include `agent-skills`, `claude-code-plugin`, `codex-plugin`, `spec-driven-development`. Apache-2.0; "not an officially supported Google product".
- **Registries**: SkillsMP lists `eg-brainstorm` from vshvedov/elephant-goldfish (a Codex port), no install counts. No in-window X post about it was found.

## 點解值得留意

- 2026-W44 hot list 第二名（heat 0.80，GitHub 單平台），詳見 [[hot-list/2026-W44|hot-list/2026-W44]]。
- 「零 context reviewer」正正係呢個 vault `skill-review` routine 嘅做法（獨立 reviewer subagent 審 draft skill）；EGM 將佢做成通用、可安裝嘅設計流程，值得對照。
- 同 Jeff 嘅 handoff / spec 習慣夾：大改動之前先出 spec、俾冇偏見嘅 reviewer 挑骨頭，再落手。

## Source

- https://github.com/google/elephant-goldfish-model — google — created 2026-09-13
- Reader: raw.githubusercontent.com README (curl), GitHub search API (`gh api`) for counts. Raw text in `raw/20261102-elephant-goldfish-model-spec-review-plugin.md`.

## Related

- [[hot-list/2026-W44]]
- [[pages/20261003-matt-pocock-skills-repo-agent-skills]]: Matt Pocock's skills (grill-me, to-spec) cover the same spec-before-code ground
- [[pages/20261005-cloudflare-security-audit-skill]]: another multi-phase skill with independently verified findings
