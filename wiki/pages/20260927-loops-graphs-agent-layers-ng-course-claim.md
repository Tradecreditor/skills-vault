---
title: "Loops and Graphs for Agents: X Post Claims an Andrew Ng Course (Unverified)"
slug: 20260927-loops-graphs-agent-layers-ng-course-claim
type: post
status: draft
source_url: "https://x.com/res1dualedge/status/2104300857928098075"
source_platform: x
author: "@res1dualedge"
published: "2026-09-27"
captured_at: "2026-10-04T21:18:05Z"
captured_by: "claude-code-cloud"
canonical_id: "x:tweet:2104300857928098075"
engagement: "likes=4049 reposts=567 replies=40 quotes=13 bookmarks=11517 views=1664798"
tags: [topic/agent-tooling, agent-loops, graph-orchestration, x, engagement-bait, course]
related: [20260928-agent-patterns-andrew-ng-4-anthropic-5-workflows, 20260928-claude-code-fable-advisor-jev-tree]
needs_manual_text: true
---

## 摘要

@res1dualedge（Residual）喺 2026-09-27 發帖，聲稱「Andrew Ng 剛發佈最好嘅 2 小時 Graph Engineering 課程」，附一段 1 小時 52 分鐘長片同分段時間戳（第一個 agent 9:14、loop engineering 33:11、graph engineering 1:02:46、自我改寫 agent 1:30:15、完整 graph 系統 1:49:05），並用「Prompts → Agents → Loops → Graphs」作框架。帖文冇附任何來源連結；佢引用嘅 @hanakoxbt 長文（2026-08-23，836 萬瀏覽）全文冇提過 Andrew Ng，結尾反而係推銷作者自己嘅課程，所以 Ng 嘅歸屬未能核實，成條帖應視為 engagement-bait（吸互動）。影片內容未轉錄，亦未能確認影片真係出自 Ng。真正有用嘅係被引用文章嘅方法：loop 係「產出 → 檢查 → 修正 → 重複」，關鍵係程式可判定嘅 check；graph 由 splitter、worker、code node、gate 四種節點組成，loop 住喺節點內、graph 喺節點之間；人手批准則按「出錯後有幾難還原」（blast radius）分級，而唔係睇模型信心。

## Key facts

- The post (2026-09-27, @res1dualedge "Residual") claims: "Andrew Ng just dropped the best 2-hour course on Graph Engineering: from single agent to full automation". Attached video: 1:52:26, 1923x1080, not transcribed.
- Chapter list in the tweet: 9:14 your first agent · 33:11 loop engineering · 1:02:46 graph engineering · 1:30:15 agents that rewrite themselves · 1:49:05 full graph system.
- Framing in the tweet: "Prompts → Agents → Loops → Graphs"; "same model, same tokens, completely different week"; "the step-by-step guide is below, save it while it is still early". The "guide" is a quote-tweet of an X Article by @hanakoxbt.
- **Verification status: UNVERIFIED.** The tweet gives no link, course title or platform for the Andrew Ng claim; the quoted article (full text captured in raw/) never mentions Andrew Ng; the video's provenance was not checked and its audio was not transcribed. Vault assessment: engagement-bait (celebrity name + timestamps + "save it"). Account context from fxtwitter: joined 2026-07-20, 1,428 followers.
- Quoted X Article: "Loops and Graphs: how to stop babysitting agents and only approve the last step (full course)" by @hanakoxbt (Hanako, 19,305 followers), 2026-08-23; views=8,369,798 likes=1,978 reposts=297 replies=64 quotes=51 bookmarks=7,551.
- That article ends by promoting the author's own 20-lesson course ("templates, the configs and the order to build them in", agent-layers.vercel.app), a DM-keyword offer ("Graph") and a Telegram channel. The site was not fetched; price not shown in the captured text. The article says "all five layers" while the tweet's ladder names four rungs; the captured text does not itemise the five.
- Method in the quoted article (as stated by its author):
  - Loop = four parts: produce → check → correct → repeat until green. "The check is the whole thing" and must be evaluable by a program, e.g. "the test suite exits 0", "every claim carries a source line", "the diff touches only files listed in the plan". Not checks: "the output looks good", "the model says it is confident", "no errors were raised".
  - A loop makes one unit of work correct; a graph decides which units exist, their order and what can run at the same time. "The loop lives inside a node. The graph lives between them."
  - Node = one bounded job (one input in, one output out); edge = a real data dependency. Test every arrow: does the next step read the previous step's output? If you cannot name the variable that crosses, there is no edge and the wait is waste.
  - Four node types: splitter (cuts the work; split by blast radius, not by folder), worker (one unit, one lens, own context; a shared window makes parallel auditors converge on the same finding), code node (merge, rank, dedupe, compare; "if you can describe the transformation without using the words judge, decide, assess or summarize, it is code"), gate.
  - Two return paths: a short correction edge (gate sends one rejected unit back to its producer; fixes this run) and a long learning edge (an accepted result becomes a derived constraint that lands in the splitter's brief; fixes later runs).
  - Return the unit, not the batch. A return carries UNIT, VERDICT, REASON, EVIDENCE and SCOPE ("fix this file only"). Cap at three attempts; three failed corrections means the fault is in the plan.
  - Gate on blast radius, not confidence. Lane 1 reversible and contained (copy change, test, covered isolated function) opens first; lane 2 reversible but wide (shared utility, schema addition) needs deterministic checks plus a clean trajectory; lane 3 hard to reverse (migrations, deletions, production data, money) never opens regardless of score. Inside an open lane the gate reads evidence in order: deterministic results, this run's trajectory, the node's past rollback rate, and the model's own assessment last.
  - Build order: gate first, then lanes, then the learning edge last. Put the human on one step of highest consequence and lowest reversibility (approve the merge, choose which fixes ship); a human mid-graph becomes the slowest node.
- Not captured: the video content, the article's cover and four diagram images, the course site, the Telegram channel.

## 點解值得留意

- 呢條帖係標準 engagement-bait 例子：166 萬瀏覽、11,517 bookmarks，但冇來源連結，被引用文章亦冇提 Ng。拆解短影音/社交內容，或者教香港中小企客戶點查證 AI 資訊，可以當案例。
- 被引用文章嘅方法唔算新，但夠實用：先寫程式可判定嘅 check、按 blast radius 開 gate、退回單位而唔係整批、最多重試 3 次、人手批准只放喺最高風險一步。Josep 用 Claude Code 為客戶搭 agent 時，可以直接當設計 checklist。
- 「冇需要判斷就用 code node，有判斷先用模型」同 vault routines 用 Jev 做低成本 gate 嘅做法一致；同 vault 已有嘅 agent-patterns 頁並排睇，但要分清楚：Ng 嘅歸屬喺呢條帖係未核實嘅，唔好當成 Ng 嘅教材引用。

## Source

- URL: https://x.com/res1dualedge/status/2104300857928098075
- Author: @res1dualedge (Residual) · Published: 2026-09-27 (2026-09-27T20:03:15Z)
- Engagement: likes=4049 reposts=567 replies=40 quotes=13 bookmarks=11517 views=1664798
- Quoted article: https://x.com/hanakoxbt/status/2091515787366306154 (X Article, 2026-08-23)
- Reader: fxtwitter JSON (api.fxtwitter.com), which includes the quoted X Article's text blocks; the video audio is not transcribed (no Supadata for X).

## Related

- [[../pages/20260928-agent-patterns-andrew-ng-4-anthropic-5-workflows|9 agent patterns: Andrew Ng's 4 + Anthropic's 5 workflows]] - the vault's existing agent-patterns note; a comparison point for the loop and graph layers described here.
- [[../pages/20260928-claude-code-fable-advisor-jev-tree|Claude Code: Fable 5.1 Advisor + Jev Routing Tree]] - a Claude Code multi-agent tree where cheap Jev gates decide which forks need the big model.
