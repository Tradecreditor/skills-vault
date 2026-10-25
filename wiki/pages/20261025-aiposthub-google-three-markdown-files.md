---
title: "AI郵報：Google 分享 AGENTS.md / DESIGN.md / SKILL.md 三份 Markdown 分工"
slug: 20261025-aiposthub-google-three-markdown-files
type: post
status: draft
source_url: "https://www.threads.com/@aiposthub/post/De7IuM5gQlC"
source_platform: threads
author: "aiposthub"
published: "2026-10-25"
captured_at: "2026-10-25T00:00:00Z"
captured_by: "routine:capture-link"
canonical_id: "threads:De7IuM5gQlC"
engagement: "likes=21 replies=2 reposts=2 shares=25 views=2700"
tags: [topic/agent-tooling, threads, agents-md, design-md, skill-md, progressive-disclosure, google-cloud]
related: []
needs_manual_text: false
---

## 摘要
AI郵報引述 Google Cloud 分享嘅 AI Agent 工作方式：唔好將所有規則塞入同一段 Prompt，而係拆成三份 Markdown 文件。AGENTS.md 係 AI 嘅工作守則（專案背景、程式規範、開發流程、測試指令）；DESIGN.md 係設計指南（品牌顏色、字體、間距、元件樣式）；SKILL.md 係專業技能包（部署、內容編修等 SOP，用到先讀取）。重點係「逐步載入」：平時只讀最基本規則，需要設計或部署先載入對應文件，減少無關指令佔用上下文。文件要寫清楚具體指令同完成條件，而且工具要真係讀到。完整教學喺作者網站文章，呢個貼文只係摘要。

## Key facts
- Three-file split: `AGENTS.md` (project context, code conventions, dev workflow, test commands), `DESIGN.md` (brand colours, fonts, spacing, component styles), `SKILL.md` (task SOPs such as deployment or content editing, loaded on demand).
- Core idea: progressive loading. Baseline project rules always; `DESIGN.md` when doing design; matching `SKILL.md` when deploying.
- Caveat from the post: file names alone are not enough; files need concrete commands and completion criteria, and the AI tool must actually read them.
- Applies to Claude Code, Cursor and other coding agents.
- Full write-up linked: https://www.aiposthub.com/google-markdown-ai-news-20261025/ (not fetched; the claim about Google Cloud is the author's secondhand summary).

## 點解值得留意
- 同呢個 vault 嘅結構一致：CLAUDE.md/AGENTS.md 做基本規則，`skills/*/SKILL.md` 做按需載入。
- `DESIGN.md` 係新嘅一份分工，可考慮用喺有 UI 嘅專案。

## Source
- https://www.threads.com/@aiposthub/post/De7IuM5gQlC · aiposthub (AI郵報) · 2026-10-25
- Engagement: likes=21 replies=2 reposts=2 shares=25 views=2.7K (order inferred from Threads UI)
- Reader: Jina Reader (threads.com host)

## Related
- [[skills/vault-capture/SKILL|skill: vault-capture]]
