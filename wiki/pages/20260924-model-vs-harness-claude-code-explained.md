---
title: "Model vs harness：Claude 係 model，Claude Code 係 harness"
slug: 20260924-model-vs-harness-claude-code-explained
type: post
status: draft
source_url: "https://www.instagram.com/reel/Dds27dKtVo6/"
source_platform: instagram
author: "aiwithbuntyshah"
published: "2026-09-24"
captured_at: "2026-10-04T21:18:26Z"
captured_by: "claude-code-cloud"
canonical_id: "instagram:Dds27dKtVo6"
engagement: "likes=2.3K comments=40"
tags: [topic/agent-tooling, claude-code, harness, agent-loop, terminal-bench, explainer]
related: [20261002-zcode-zai-harness, 20261002-magpie-agent-model-switcher, 20260928-agent-patterns-andrew-ng-4-anthropic-5-workflows]
needs_manual_text: false
---

## 摘要
Bunty Shah（@aiwithbuntyshah）用一條 reel 解釋 AI 入面「model」同「harness」嘅分別。佢指 model 單獨只可以輸入文字、輸出文字，開唔到檔案、行唔到指令、跑唔到測試，包住 model 嘅軟件（harness）先令佢「有手」。以 Claude 為例：Claude 係 model，Claude Code 係 harness。Harness 提供嘅嘢包括工具、think → act → observe 循環、每回合重建 context、allow / ask / deny 權限，以及各有全新 context window 嘅 sub-agents。帖文引述一項 2026 年研究，話只改 harness、model 不變，Terminal-Bench 2.0 就升咗 13.7 分，但冇附連結或研究名稱，屬未核實。

## Key facts
- Claim: a model on its own only takes text in and sends text out; it cannot open a file, run a command or execute a test. The "harness" is the software wrapped around it and "is what gives it hands".
- Example given: "Claude is the model, Claude Code is the harness."
- What the harness adds, per the caption:
  - Tools: the model writes a tool request, the harness runs it and feeds the result back.
  - The loop: think -> act -> observe -> repeat (example in the caption: "1 failed -> fix -> 42 passed").
  - Context: the model is stateless, so every turn the harness rebuilds what it sees and decides what stays, gets summarized or gets reloaded.
  - Permissions: allow / ask / deny.
  - Sub-agents: each has its own fresh context window; only a summary comes back.
- Claim: this is why the same model feels brilliant in one app and clumsy in another.
- Statistic (unverified): "One 2026 study: model fixed, harness changed -> +13.7 points on Terminal-Bench 2.0." No study title, authors or link are given in the caption.
- Closing line: "A brilliant model with no harness is a brain in a jar." The post ends with a prompt asking which harness the viewer is using.
- Format: reel. The spoken audio was not transcribed (no Supadata call); the caption carries the whole argument, so `needs_manual_text` is false.

## 點解值得留意
- 「model 係腦、harness 係手腳」呢個框架好啱同香港中小企客解釋：點解同一個 model 喺唔同工具表現差咁遠，亦可以用嚟支持揀 Claude Code 呢類 harness 嘅理據。
- 五個組件（tools、loop、context、permissions、sub-agents）可以直接做成 Jeff 設計 agent workflow 或客戶培訓嘅檢查清單。
- 同 vault 已有嘅 ZCode（開源 coding agent harness）及 magpie（切換 model）互補：一個講 harness 本身，一個講 harness 下面換 model。
- +13.7 分嘅數字冇來源，引用畀客戶之前要先搵返原研究核實。

## Source
- https://www.instagram.com/reel/Dds27dKtVo6/ — Bunty Shah (@aiwithbuntyshah), 2026-09-24, likes=2.3K comments=40. Reader: jina (caption); counts order likes/comments inferred.

## Related
- [[../pages/20261002-zcode-zai-harness|ZCode — Z.ai open-source coding agent harness (desktop + web + CLI)]]
- [[../pages/20261002-magpie-agent-model-switcher|magpie — one menu-bar panel and local gateway for every coding agent's model]]
- [[../pages/20260928-agent-patterns-andrew-ng-4-anthropic-5-workflows|9 agent patterns: Andrew Ng's 4 + Anthropic's 5 workflows]]
