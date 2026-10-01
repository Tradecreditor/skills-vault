---
title: "OpenAI Agents API: Computer Use to Multi-Agent Guide"
slug: 20260929-openai-agents-api-computer-use-guide
type: article
status: draft
source_url: "https://www.aiposthub.com/openai-agents-api-computer-use-guide/"
source_platform: web
author: "aiposthub.com"
published: "2026-09-29"
captured_at: "2026-10-01T12:40:08Z"
captured_by: "claude-code-cloud"
canonical_id: "url:400cf7debe5ba276ecc375fda29d11389b006346"
engagement: "none"
tags: [topic/agent-platforms, openai, agents-api, computer-use, multi-agent, sandbox, mcp, devday-2026]
related: [20260928-claude-code-fable-advisor-jev-tree, openai--codex-plugin-cc, microsoft--playwright-mcp]
needs_manual_text: false
---

## 摘要

呢篇文章用白話拆解 OpenAI 喺 DevDay 2026 公開嘅 Agents API：佢將 Codex 內部使用嘅代理執行框架開放畀所有開發者，包括受管工作階段、工具、沙箱、上下文壓縮、失敗恢復、Computer use 同多代理編排。文章解釋點解自己砌代理要處理嘅「膠水工程」可以交畀平台，亦提醒 Computer use 較脆弱、有提示注入風險，而多代理唔一定比單一代理好。文末提供一套七步由原型到正式環境嘅導入法同需要監控嘅指標。啱晒想評估 OpenAI 代理平台、又唔想盲目追熱門「代理」概念嘅開發者同顧問。

## Key facts

- Announced at OpenAI DevDay 2026: the Agents API exposes the agent execution framework used inside Codex to all developers.
- Core pieces: managed sessions, orchestration, managed context compaction, failure recovery, tools, sandboxes, MCP support, Computer use, multi-agent orchestration.
- Pricing (as stated in the article): OpenAI says there is no extra API platform fee during the public beta; model tokens, tools and sandbox usage are still billed.
- Computer use: the agent operates GUIs via screen understanding plus mouse/keyboard. Treat it as a fragile tool; prefer a stable API where one exists; restrict sites and actions, add human approval for irreversible actions, keep screenshots/structured logs, set timeouts and max attempts; guard against prompt injection from web pages.
- Multi-agent only pays off when work can be split clearly, run in parallel, or needs independent review; otherwise a single agent with clear tools is cheaper and easier to debug.
- Seven-step rollout: (1) pick a task with a clear done-criterion and recoverable errors; (2) build 20-50 real cases labelled success / partial / failure; (3) expose only necessary tools with narrow params, auth, input checks and logs; (4) set budgets (max tokens, tool calls, run time, retries); (5) add human approval points for external-state changes; (6) return evidence (source URLs, file diffs, test results); (7) launch in shadow mode or small traffic before opening write access.
- Metrics to track: first-pass completion rate vs after-retry completion rate; per-successful-task tokens, tool fees, sandbox time and human-intervention minutes (use percentiles and max, not just average); latency split into model wait / tool wait / human approval; blocked over-permission actions, prompt-injection events, sensitive-data access, irreversible actions.
- FAQ answer: Responses API focuses on model responses and tool calls; Agents API adds persistent sessions, orchestration, compaction, recovery, sandbox and multi-agent. Confirm the interface against the latest official docs.
- Author's take: the platform provides the execution skeleton; domain rules (matching, refund approval, data residency) still have to be written into tools and evals.
- References listed in the article: OpenAI "Introducing the Agents API", OpenAI Developers "Agents API overview", OpenAI Developers "Computer use tool", OpenAI "DevDay 2026 recap".

## 點解值得留意

- 幫香港中小企做 AI 顧問時，客人成日問「OpenAI 嘅 agent 平台值唔值得用」；呢篇有現成嘅評估框架（七步導入、預算上限、人手批准點）可以直接搬入提案。
- 「Computer use 要限站點、不可逆操作要人批准、防提示注入」同 Josep 自己用 Claude Code / 瀏覽器自動化時嘅安全習慣一致，可以當 checklist 同客戶講。
- 多代理「唔一定好」嘅判斷三問，適合放入短影音內容拆解「點解唔好一開始就砌多代理」。
- Iron Log / English Overload 如果日後加入長流程代理功能，可以參考其指標清單（首次完成率、每成功任務成本）。

## Source

- URL: https://www.aiposthub.com/openai-agents-api-computer-use-guide/
- Author: aiposthub.com (no byline shown) · Published: 2026-09-29 (Jina Published Time)
- Engagement: none shown
- Reader: Jina Reader (r.jina.ai)
- Not captured: article images (dropped from raw); the tag/navigation chrome. The four reference links are listed in raw but were not fetched.

## Related

- [[pages/20260928-claude-code-fable-advisor-jev-tree|Claude Code: Fable 5.1 Advisor + Jev Routing Tree]] - Claude-side multi-agent routing, a comparison point for Agents API orchestration.
- [[stars/openai--codex-plugin-cc|openai--codex-plugin-cc]] - Codex tooling, the harness the Agents API is said to expose.
- [[stars/microsoft--playwright-mcp|microsoft--playwright-mcp]] - a structured browser-control alternative to screenshot-based Computer use.
