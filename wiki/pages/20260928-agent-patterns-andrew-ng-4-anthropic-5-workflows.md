---
title: "9 agent patterns: Andrew Ng's 4 + Anthropic's 5 workflows"
slug: 20260928-agent-patterns-andrew-ng-4-anthropic-5-workflows
type: post
status: draft
source_url: "https://www.threads.com/@mini_littlechanges/post/Dd1Qo5hE6JY"
source_platform: threads
author: "@mini_littlechanges"
published: "2026-09-28"
captured_at: "2026-10-04T21:08:08Z"
captured_by: "claude-code-cloud"
canonical_id: "threads:Dd1Qo5hE6JY"
engagement: "likes=423 replies=10 reposts=41 shares=488 views=45.5K"
tags: [topic/agent-tooling, agent-patterns, andrew-ng, anthropic, building-effective-agents, agentic-workflow]
related: [20260928-claude-code-fable-advisor-jev-tree, langchain-ai--open_deep_research, bytedance--deer-flow]
needs_manual_text: false
---

## 摘要

艾米莉 Mini 醬（@mini_littlechanges）用廣東話整理「9 招 Agent 設計模式」。佢轉述 Andrew Ng 嘅實驗：用舊款 GPT、完全唔改 model，淨係改工作流程，分數由 48 分升到 95 分，並話連當時最新最強嘅 model 都跑贏；Ng 歸納出 4 個核心 Agent 模式：Reflection、Tool use、Planning、Multi-agent。再加上 Anthropic《Building Effective Agents》整理嘅 5 個 workflow：Prompt chaining、Routing、Parallelization、Orchestrator-workers、Evaluator-optimizer。作者結論係市面上大部分真正行得通嘅 AI Agent，底層就係呢 9 招。帖文附 6 張圖嘅 carousel（未讀取），文字部分只列名稱同一句話解釋 Ng 嘅 4 招，冇附原始來源連結。

## Key facts

- Author: 艾米莉 Mini 醬 (@mini_littlechanges), Cantonese post of 2026-09-28 under the Threads tag `agentic-patterns`; 6-image carousel attached (images not read).
- Claim (second-hand, no source link or benchmark name given): Andrew Ng ran an experiment where an older GPT, with the model itself unchanged and only the workflow changed, went from a score of **48 to 95**, beating the then-newest and strongest model.
- Andrew Ng's 4 core agent patterns as listed in the post:
  1. **Reflection** (have it check its own output)
  2. **Tool use** (give it tools to actually operate)
  3. **Planning** (break the task into steps first, then do them one by one)
  4. **Multi-agent** (different roles collaborate)
- Anthropic's "Building Effective Agents" 5 workflows as listed in the post: **Prompt chaining**, **Routing**, **Parallelization**, **Orchestrator-workers**, **Evaluator-optimizer** (the post gives names only, no definitions).
- Author's conclusion (author claims): most AI agents that really work in the market today are built on these 9 patterns.
- Replies by other accounts (not the author, as rendered): one says this approach burns tokens, so costs must be calculated; one describes running Reflection as 3 LLM roles (a draft, an independent critic that may be the same or a cheaper/faster LLM, then a final pass that revises the draft using only the critic's view) and says it is now in UAT; one jokes "Bro discovered CoT all over again"; others ask whether models have then not improved at all.
- Not captured: the 6-image carousel content (may contain definitions or diagrams), the original Andrew Ng material, the Anthropic article itself.
- Engagement: 423 likes, 10 replies, 41 reposts, 488 shares, 45.5K views (order inferred from Threads UI).

## 點解值得留意

- **客戶講解用 checklist**：「9 招」係一個易記嘅框架，Jeff 向香港中小企解釋 agent 唔係神秘黑盒、重點係工作流程設計（作者論點：改流程可以勝過換 model）時可以用；45.5K views 亦反映呢類整理帖受眾好大，可以做短影音題材。
- **對應 Claude Code 日常做法**：Planning、Orchestrator-workers、Evaluator-optimizer 對應 plan mode、subagent 同獨立 reviewer（vault 嘅 skill-review routine 用獨立 reviewer subagent 審核 draft skill，精神上接近 Evaluator-optimizer）；留言提到 Reflection 要拆成 draft、critic、reviser 三個角色，值得參考。
- **數字要核實先好引用**：「48 分升到 95 分」係轉述，冇列出 benchmark 同來源；用喺客戶簡報前，應直接睇 Andrew Ng 原講法同 Anthropic 嘅《Building Effective Agents》原文（可另行 capture）。

## Source

- Post: https://www.threads.com/@mini_littlechanges/post/Dd1Qo5hE6JY
- Author: @mini_littlechanges (艾米莉 Mini 醬) · Published: 2026-09-28
- Engagement: likes=423 replies=10 reposts=41 shares=488 views=45.5K (order inferred from Threads UI)
- Reader: jina (share link resolved via r.jina.ai; counts order inferred from Threads UI)
- Share URL: https://www.threads.com/share/_xIBQNZnn/
- Not read: the 6-image carousel attached to the post; "Related threads" by other accounts not captured.

## Related

- [[../pages/20260928-claude-code-fable-advisor-jev-tree|Claude Code: Fable 5.1 Advisor + Jev Routing Tree]] — advisor 審查加 routing 嘅 Claude Code 多模型設定，對應 Reflection 同 Routing
- [[../stars/langchain-ai--open_deep_research|open_deep_research]] — 分階段（搜尋、壓縮、寫報告）嘅 research agent，Planning／Orchestrator 式流程嘅實例
- [[../stars/bytedance--deer-flow|deer-flow]] — multi-agent 開源框架，對應 Multi-agent 模式
