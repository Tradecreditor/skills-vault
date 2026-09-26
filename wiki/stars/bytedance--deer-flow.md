---
title: "deer-flow"
slug: bytedance--deer-flow
type: repo
status: draft
source_url: "https://github.com/bytedance/deer-flow"
source_platform: github
author: "ByteDance"
published: "2025-05-07"
captured_at: "2026-09-20T00:00:00Z"
captured_by: "routine:github-stars-sync"
canonical_id: "github:bytedance/deer-flow"
engagement: "stars=82755 forks=11432"
tags: [agent, agentic, ai-agents, deep-research, superagent, multi-agent]
related: [assafelovic--gpt-researcher, langchain-ai--open_deep_research, THU-MAIC--OpenMAIC]
needs_manual_text: false
---

## 摘要
DeerFlow 係 ByteDance 開源嘅「超級 Agent Harness」,2.0 版由零重寫,唔再淨係一個 Deep Research 框架,而係一套識自己協調子 agent(sub-agents)、記憶(memory)同沙盒(sandbox)嘅通用執行引擎,靠可擴充嘅 skills 去完成幾乎任何任務。項目喺 2026 年 2 月 28 號 v2 推出之後攞咗 GitHub Trending 全球第一。安裝流程有一鍵設定精靈(`make setup`),兩分鐘內就可以揀 LLM provider、網絡搜尋、sandbox 模式、bash 權限等安全選項,推薦配合 Doubao-Seed-2.0-Code、DeepSeek v3.2 或者 Kimi 2.5 呢類模型使用。除咗 Docker 一鍵部署,佢仲支援 MCP server、IM channel 接入、LangSmith/Langfuse/Monocle 追蹤,同埋長期記憶、排程任務、終端機 TUI 等進階功能。

## Key facts
- Language: Python
- License: MIT
- Created: 2025-05-07
- Last pushed: 2026-09-20
- Stars: 82,755
- Forks: 11,432
- Homepage: https://deerflow.tech
- Supports: Python, Node.js, TypeScript

## 點解值得留意
呢個項目由 v1 嘅純 Deep Research 工具,進化成有 sub-agent 編排、context engineering 同長期記憶嘅通用 agent harness,對想自己起一個可以長時間運行、多步驟研究/寫程式任務嘅 agent 底座嘅人有參考價值。原有 1.x 分支仍然維護,亦可以對比睇到框架設計嘅演進。

## Source
GitHub repository: https://github.com/bytedance/deer-flow
Author: ByteDance
Captured: 2026-09-20

## Related

- [[assafelovic--gpt-researcher|gpt-researcher]] — 同屬開源 research/agent 框架，可以比較架構取捨。
- [[langchain-ai--open_deep_research|open_deep_research]] — 兩者都可拆件配置唔同模型做唔同工序。
- [[THU-MAIC--OpenMAIC|OpenMAIC]] — 都係多 agent 協作平台，deer-flow 係通用 harness，OpenMAIC 專攻教學。
