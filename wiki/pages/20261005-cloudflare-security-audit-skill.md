---
title: "cloudflare/security-audit-skill — six-phase, adversarially verified security audit skill for coding agents"
slug: 20261005-cloudflare-security-audit-skill
type: repo
status: draft
source_url: "https://github.com/cloudflare/security-audit-skill"
source_platform: github
author: "Cloudflare"
published: "2026-06-18"
captured_at: "2026-10-05T08:19:24Z"
captured_by: "routine:weekly-hot-list"
canonical_id: "github:cloudflare/security-audit-skill"
engagement: "stars=24488 forks=1452 (+6554 stars since 2026-09-20 snapshot)"
tags: [hot-list, 2026-W40, agent-skills, security-audit, ai-security, multi-agent, claude-code, cloudflare]
related: [hot-list/2026-W40]
needs_manual_text: false
---

## 摘要

cloudflare/security-audit-skill 係 Cloudflare 開源（MIT）嘅 coding-agent skill，將 agent 變成安全審計員：分六個階段做 reconnaissance、按 coverage ledger 派多個獨立 hunter 搵漏洞、交畀另一個新 agent 嘗試推翻每個發現、輸出 `findings.json`（confirmed / needs_validation / rejected）、再獨立核實，最後出報告。佢係 Cloudflare 內部 vulnerability harness 嘅起點。冇 OS 級 sandbox 嘅話，佢唔會執行目標 code，只會將 lead 標做 `needs_validation`。Vault 之前已經收咗一條 Instagram 介紹（冇 repo 名），呢頁補返正式 repo。佢係 2026-W40 hot list 嘅 GitHub 單平台入選項目。

## Key facts

- **Install**: `npx skills add https://github.com/cloudflare/security-audit-skill --skill security-audit` (add `--global` for a user-level install).
- **Use**: start the agent in the target codebase and ask e.g. `security audit this codebase` or `do a security review, output to ~/audits/my-project`. Direct audit / pen-test requests use full audit mode; questions use guidance mode. Default output `~/security-audit-skill/<repo-name>/run-<N>`.
- **Phases**: reconnaissance → coverage-led hunting → candidate validation by a fresh verifier → structured output (`findings.json` validated against `report-schema.json`) → independent record verification → `REPORT.md`, `FINDINGS-DETAIL.md`, `NEEDS-VALIDATION.md`.
- **Requirements**: a model with tool use and parallel sub-agents; Node.js for the zero-dependency validators; an OS-enforced sandbox (no external network, sanitised env, resource limits, scratch-only writes) before it executes target code.
- **Design**: the agent that checks a finding is never the one that found it; severity needs impact; defence-in-depth gaps are hardening notes; one run finds roughly half of what repeated runs find.
- **Numbers**: 24,488 stars / 1,452 forks on 2026-10-05; 17,934 in the 2026-09-20 snapshot (+6,554 in 15 days, about 3,059 per 7 days pro-rated). No in-window X post found.

## 點解值得留意

- Hot list 2026-W40 第三名（heat 0.80，單平台 GitHub topical gate），同時係 2026-W38 Watch 第一位，詳見 [[hot-list/2026-W40|hot-list/2026-W40]]。
- Jeff 嘅 vibe-coded 項目（Iron Log 等）上線前可以用；hunt-then-disprove 模式亦適用於 vault 自己嘅 skill review。
- 係可安裝 skill，值得 draft 一個 vault skill（install + sandbox 要求 + 讀報告次序）；今次 routine 冇寫，因為 `skills/` 改動要同時更新 `handoff.md`，而 routine 唔可以改 handoff。

## Source

- https://github.com/cloudflare/security-audit-skill — Cloudflare — created 2026-06-18
- Reader: raw.githubusercontent.com README (curl) + GitHub search API (connector); raw text in `raw/20261005-cloudflare-security-audit-skill.md`.

## Related

- [[hot-list/2026-W40]]
- [[pages/20261004-cloudflare-open-source-ai-security-audit-skill]]
- [[pages/20260828-nvidia-skillspector-skill-security-scanner]]
- [[../../skills/scanning-agent-skills/SKILL|skill: scanning-agent-skills]]
