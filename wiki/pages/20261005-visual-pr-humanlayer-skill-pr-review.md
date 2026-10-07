---
title: "visual-pr (HumanLayer skill): visual outline in every PR to speed up review (Romi Patel)"
slug: 20261005-visual-pr-humanlayer-skill-pr-review
type: video
status: draft
source_url: "https://www.instagram.com/reel/DeHKRM2hLNn/"
source_platform: instagram
author: "romippatel"
published: "2026-10-05"
captured_at: "2026-10-07T00:00:00Z"
captured_by: "routine:capture-link"
canonical_id: "instagram:DeHKRM2hLNn"
engagement: "likes=59 comments=2"
tags: [topic/agent-tooling, claude-code, code-review, humanlayer, visual-pr, show-me]
related: []
needs_manual_text: false
---
## 摘要
Romi Patel 指 AI agent 寫 code 只需幾分鐘，但 code review 仍要幾個鐘，瓶頸已經由寫碼轉到審查。HumanLayer 嘅 Claude Code skill「visual-pr」會令 agent 開 PR 時附上視覺化大綱，交代點解要改、各部分點樣配合，等 reviewer 先理解再睇 diff。同一個 repo 另有「show-me」，喺 agent 仲在運行時用簡單圖表解釋進度。作者強調呢啲唔會取代閱讀 diff，只係令 review 更易。

## Key facts
- Skill `visual-pr`: agent adds a visual outline (why the change exists, how the pieces fit) when it opens a PR.
- Skill `show-me`: explains the agent's work with quick diagrams while it is still running.
- Both live in the repo github.com/humanlayer/skills (the reel does not give install commands; not verified against the repo).
- Caption-only capture: Jina returned the full caption; the reel's spoken audio was not transcribed (caption carries the substance).

## 點解值得留意
- 直接針對 agent 輸出 code 量大、人手 review 成為瓶頸嘅問題。
- 可試用喺 Jeff 用 Claude Code 開 PR 嘅項目（配合 vault PR 流程）。
- 可考慮日後單獨 capture humanlayer/skills repo 驗證內容。

## Source
- https://www.instagram.com/reel/DeHKRM2hLNn/ — romippatel (Romi Patel), 2026-10-05, likes=59 comments=2 (order inferred), reader: jina.

## Related
- [[pages/20261005-cloudflare-security-audit-skill|cloudflare/security-audit-skill]]
