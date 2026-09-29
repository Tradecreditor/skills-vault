---
title: "Claude Code: Fable 5.1 Advisor + Jev Routing Tree"
slug: 20260928-claude-code-fable-advisor-jev-tree
type: skill
status: draft
source_url: "https://x.com/thedelost/status/2104677530825634273"
source_platform: x
author: "thedelost"
published: "2026-09-28"
captured_at: "2026-09-29T19:02:40Z"
captured_by: "routine:capture-link"
canonical_id: "x:tweet:2104677530825634273"
engagement: "likes=1902 retweets=151 views=446089 bookmarks=3708"
tags: [claude-code, fable-5-1, advisor, jev, multi-agent, opus-5-5, subagent, routing, effort-level]
related: []
needs_manual_text: false
---

## 摘要

這篇推文提供了 Claude Code 的進階多模型架構設定技巧。核心概念是：以 Opus 5.5 作為主要程式碼撰寫模型，同時將 Fable 5.1 配置為 `/advisor`，讓它在三個關鍵時機介入審查：制定計劃前、錯誤重複出現時、以及宣告完成前。Jev engineering 則在更底層發揮作用，將不需要「思考」的路由決策（選擇工具、重試與否）交給 Jev 模型處理，節省大模型 token 開銷。作者提供了一個可直接貼入 Claude Code 的完整設定提示，自動建立 explorer/worker/researcher 子代理樹。

## Key facts

- **Enable**: run `/advisor fable` in Claude Code to assign Fable 5.1 as reviewer
- **Advisor checkpoints** (three only):
  - Before a plan: "is this the right approach?"
  - When the same error recurs: "am I digging in the wrong place?"
  - Before marking done: "what did I miss?"
- **Agent tree**:
  - Opus 5.5 on `high` → main session
  - `explorer`, `worker`, `researcher` → each `model: opus, effort: medium`
  - Fable 5.1 → advisor (reads full session + every tool call)
- **Settings**: `effortLevel: "high"` + `advisorModel: "fable"` in `~/.claude/settings.json`
- **Env vars to audit** (silently disable advisor or override effort):
  - `CLAUDE_CODE_DISABLE_ADVISOR_TOOL`
  - `DISABLE_TELEMETRY`
  - `CLAUDE_CODE_EFFORT_LEVEL` (overrides subagent effort)
- **Docs**: https://code.claude.com/docs/en/advisor
- **Setup prompt**: paste into Claude Code; it diffs all changes first, edits nothing until you approve

## 點解值得留意

- Fable 5.1 的完整 session 上下文閱讀能力使它成為理想審查者，只在三個最重要節點介入，避免打斷 Opus 5.5 的主工作流。
- Jev routing 模式與 skills-vault 的 Jev cost-reduction 研究（20260925-jev-seo-geo-audit-cost-down-90）直接對應，可在 Josep 的代理專案中降低路由成本。
- 提供的完整設定提示可即用，方便快速在任何 Claude Code 專案中重現這個三層代理架構。
- 與 `stacking-coding-agent-plugins` 技能互補，進一步強化 Claude Code 的多代理配置。

## Source

- URL: https://x.com/thedelost/status/2104677530825634273
- Author: @thedelost (delost) — "cooking at finance & ai"
- Published: 2026-09-28
- Engagement: likes=1902 retweets=151 views=446089 bookmarks=3708
- Reader: fxtwitter-via-curl

## Related

- [[../../skills/configuring-fable-advisor-jev-tree/SKILL|skill: configuring-fable-advisor-jev-tree]]
- [[20260925-jev-seo-geo-audit-cost-down-90|Jev cuts agent SEO/GEO audit-and-fix cost by 90%]]
- [[20260920-fast-jev-compaction|fast-jev-compaction]]
