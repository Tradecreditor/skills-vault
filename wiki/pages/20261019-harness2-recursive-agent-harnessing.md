---
title: "google-research/harness2 — Harness²: recursive, verifier-free harness improvement for agents"
slug: 20261019-harness2-recursive-agent-harnessing
type: repo
status: draft
source_url: "https://github.com/google-research/harness2"
source_platform: github
author: "Google Research (Ruiyao Xu, Yanfei Chen et al.)"
published: "2026-10-06"
captured_at: "2026-10-19T08:21:37Z"
captured_by: "routine:weekly-hot-list"
canonical_id: "github:google-research/harness2"
engagement: "stars=8540 forks=754; X @akshay_pachaar likes=5430 reposts=676 views=427642"
tags: [hot-list, 2026-W42, agent-harness, harness-engineering, self-improving-agents, opencode, codex, research]
related: [hot-list/2026-W42]
needs_manual_text: false
---

## 摘要

Harness² 係 Google Cloud AI Research 開源嘅框架（Apache-2.0，論文 arXiv:2610.14224），唔改模型權重，只改 agent 外面嗰層 harness：system prompt、guardrails、memory、tool guidance、subagents、skills、scripts 同 plugins。每個任務佢會先跑一次參考執行，再提出兩個候選修改，喺同一任務、同一條件下試跑，用行為對比（唔係標準答案）決定合併邊啲修改，即係 Propose–Probe–Compose。做完之後，有證據支持嘅修改同教訓會寫入一個持續更新嘅 improvement harness，畀下一個任務參考。README 報告單步改進喺 WorkBuddy-Bench 最多 +11.5 分、LAB 部分通過率 +11.8 個百分點；executor 可以用 OpenCode 或者 Codex。佢係 2026-W42 hot list 第三名，亦係今個星期唯一過到社交 gate 嘅項目（X 三個作者各 >= 300 likes）。

## Key facts

- **Install** (README; Linux, Python 3.12, uv): `uv venv --python 3.12 .venv && source .venv/bin/activate && uv pip install -e '.[render]'`, then `harness2-demo --output runs/demo --k 2` (deterministic editors, no model credentials). Benchmarks: `harness2-setup jb`, then `harness2 --bench jb --k 1 --mode parallel`.
- **Options**: `--k 1` one Propose–Probe–Compose step; `--k K --mode parallel` probes K general + K domain candidates; `--k K --mode sequential` refines through K steps; `--substrate cx` uses Codex instead of the default OpenCode executor.
- **Warning in the README**: executor network access is unrestricted and Codex runs with its sandbox disabled; restrict the network before evaluating so the agent cannot fetch benchmark answers. Not an officially supported Google product.
- **Results (README and arXiv abstract)**: across three professional benchmarks and four model–harness configurations, one step improves GLM-5 and Gemini 3.5 Flash over their base harnesses, by up to 11.5 points on WorkBuddy-Bench, 4.5 on JobBench and 11.8 pp on LAB's partial pass rate; a larger recursion budget adds more. The paper's default harness editor is Claude Opus 4.8 running under OpenCode. Secondary write-ups (for example @shao__meng's thread) also report cross-model transfer; those figures are not verified here.
- **Numbers (2026-10-19)**: 8,540 stars / 754 forks, created 2026-10-06. Not in the 2026-10-12 snapshot, so its 7-day star gain cannot be measured and no GitHub gate is claimed. X (fxtwitter, all 2026-10-18): @akshay_pachaar 2111753928031531232 5,430 likes / 676 reposts / 427,642 views; @Saboo_Shubham_ 2111691139011223640 768 / 78 / 55,191; @ai_for_success 2111782980574421497 658 / 50 / 37,341. Three authors >= 300 likes clears the X distinct-authors gate. Jev `topical` 0.90.

## 點解值得留意

- 2026-W42 hot list 第三名（X 單平台 heat 0.70）。按規則每星期至少一個入選項目要過 X 或 Threads gate，今個星期只有佢做到，詳見 [[hot-list/2026-W42|hot-list/2026-W42]]。
- 同 vault 本身好有關：vault 嘅 skills、CLAUDE.md、routines 其實就係 Jeff 嘅 harness。Harness² 嘅做法（同一任務 A/B 試修改、只保留有證據嘅教訓）可以借嚟改 `skill-review` 或者 routine prompt，唔一定要成套框架。
- 同 [[stars/NousResearch--hermes-agent-self-evolution|hermes-agent-self-evolution]]（用 DSPy + GEPA 優化 skills / prompts）係同一條「自我改進 harness」路線，可以對照睇。

## Source

- https://github.com/google-research/harness2 — Google Research — created 2026-10-06; paper https://arxiv.org/abs/2610.14224
- Reader: raw.githubusercontent.com README (curl) + GitHub search API (connector) for counts; X counts from fxtwitter. Raw text in `raw/20261019-harness2-recursive-agent-harnessing.md`.

## Related

- [[hot-list/2026-W42]]
- [[stars/NousResearch--hermes-agent-self-evolution]]: evolutionary self-improvement of an agent's skills and prompts
- [[stars/bytedance--deer-flow]]: a long-horizon agent harness of the kind Harness² edits
