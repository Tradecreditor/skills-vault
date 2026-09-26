---
title: "promptfoo: LLM Evals & Red Teaming"
slug: 20260923-promptfoo
type: tool
status: draft
source_url: "https://github.com/promptfoo/promptfoo"
source_platform: github
author: "promptfoo"
published: "2023-04-28"
captured_at: "2026-09-23T00:00:00Z"
captured_by: "routine:capture-link"
canonical_id: "github:promptfoo/promptfoo"
engagement: "stars=24793 forks=2258"
tags: [llm-eval, llm, red-teaming, pentesting, prompt-testing, evaluation-framework, ci-cd, rag, testing, ai-security]
related: ["skills/evaluating-llms-with-promptfoo", "stars/NousResearch--hermes-agent-self-evolution"]
needs_manual_text: false
---

## 摘要

promptfoo 是一個開源的 CLI 工具與函式庫，專門用於評估和紅隊測試 LLM 應用程式。它讓開發者能用宣告式設定檔自動測試提示詞、代理和 RAG 系統，無需手動試錯。工具支援跨模型比較（GPT、Claude、Gemini、DeepSeek 等），並可整合進 CI/CD 流程。評估完全在本地執行，提示詞不會離開本機，保障私密性。已在 OpenAI 和 Anthropic 內部使用，服務超過 1000 萬用戶的生產環境。

## Key facts

- **Install**: `npm install -g promptfoo` or `brew install promptfoo` or `pip install promptfoo`
- **Quick run**: `npx promptfoo@latest` (no install needed)
- **Init**: `promptfoo init --example getting-started`
- **Run eval**: `promptfoo eval`
- **View results**: `promptfoo view`
- Stars: 24,793 | Forks: 2,258 | Language: TypeScript | License: MIT
- Created: 2023-04-28 | Actively maintained (last push Sep 2026)
- Homepage: https://promptfoo.dev
- Supports: OpenAI, Anthropic, Azure, Bedrock, Ollama, and more
- Features: automated evals, red teaming/vulnerability scanning, model comparison, CI/CD integration, PR code scanning
- 100% local evaluation — prompts never leave your machine
- Battle-tested: powers LLM apps serving 10M+ users in production
- Used by OpenAI and Anthropic

## 點解值得留意

- **AI 安全必備工具**：提供 LLM 紅隊測試和漏洞掃描，對任何部署 AI 的專案都是關鍵防線。
- **CI/CD 整合**：可自動化 LLM 品質和安全測試，適合 Josep 的 Claude Code 和其他 AI 專案工作流程。
- **模型比較神器**：跨 GPT、Claude、Gemini 等模型對比評估，有助於選型和優化 prompt engineering。
- **本地執行隱私保障**：評估在本地跑，提示詞不外洩，適合包含敏感業務邏輯的專案。

## Source

- URL: https://github.com/promptfoo/promptfoo
- Author: promptfoo (organization)
- Published: 2023-04-28
- Engagement: stars=24793 forks=2258
- Reader used: exa (api.github.com + raw.githubusercontent.com)

## Related

- [[../../skills/evaluating-llms-with-promptfoo/SKILL|skill: evaluating-llms-with-promptfoo]] — 呢個 skill 就係由呢篇 promptfoo 頁面草擬出嚟，教點樣用佢做評估同紅隊測試。
- [[../stars/NousResearch--hermes-agent-self-evolution|hermes-agent-self-evolution]] — 兩者都圍繞「評分 → 改進」呢個 LLM 品質迴路：promptfoo 提供評估框架，hermes-agent-self-evolution 用評分結果自動演化 agent skill。
