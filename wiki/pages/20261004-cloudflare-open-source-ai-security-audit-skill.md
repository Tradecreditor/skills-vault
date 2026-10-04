---
title: "Cloudflare 開源 AI security audit skill（vibe-coded app 安全審查）"
slug: 20261004-cloudflare-open-source-ai-security-audit-skill
type: post
status: draft
source_url: "https://www.instagram.com/reel/DeE57zWP038/"
source_platform: instagram
author: "nick_saraev"
published: "2026-10-04"
captured_at: "2026-10-04T15:53:27Z"
captured_by: "routine:capture-link"
canonical_id: "instagram:DeE57zWP038"
engagement: "likes=388 comments=401"
tags: [topic/agent-tooling, cloudflare, ai-security, vibe-coding, claude-code, security-audit, multi-agent]
related: []
needs_manual_text: false
---

## 摘要
Nick Saraev 介紹 Cloudflare 開源嘅一個 AI skill，用嚟搵 vibe-coded app 嘅安全漏洞。Cloudflare 原本係自用，據稱喺自家 codebase 搵到過 7,000 多個安全問題，GitHub 已超過 22k stars。Skill 可以安裝入 Claude Code：先 map 晒成個 app，再派一隊 AI agents 搜查登入、database、API，甚至 prompt injection。每個發現嘅 bug 會交畀另一個 agent 負責反駁，只有通過驗證嘅先會入報告，最後附上修復方法。帖文係 "Comment AUDIT" 引流，影片冇提供 repo 名稱。

## Key facts
- Claimed: open-sourced by Cloudflare, free, 22k+ GitHub stars, found 7,000+ security issues in Cloudflare's own codebase.
- Install into Claude Code (exact repo / command not given in the caption).
- Pipeline: map the app -> parallel agents hunt (auth, database, APIs, prompt injection for AI apps) -> separate agent tries to disprove each finding -> report with verified issues and fixes.
- Design idea: adversarial verification to cut false positives ("only shows what it can prove").
- Not verified against the Cloudflare source; repo name still to be found.

## 點解值得留意
- Hunt-then-disprove 係可以抄嘅 multi-agent 模式，同 vault 嘅 skill 安全掃描思路相近。
- 做 vibe-coded 項目（Iron Log 等）上線前可以試用。
- 需要搵出實際 repo，確認後再決定要唔要 draft skill。

## Source
- https://www.instagram.com/reel/DeE57zWP038/ — nick_saraev, 2026-10-04, likes=388 comments=401. Reader: Jina (caption) + Supadata metadata (counts); no audio transcript, the caption carries the substance.

## Related
- [[../pages/20260828-nvidia-skillspector-skill-security-scanner|NVIDIA SkillSpector]]
- [[../pages/20260930-cloudflare-cf-agentic-cli-replaces-wrangler|Cloudflare cf CLI]]
