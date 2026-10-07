---
title: "cloudflare/security-audit-skill — six-phase, adversarially verified security audit skill for coding agents"
slug: 20261005-cloudflare-security-audit-skill
type: repo
status: verified
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

## Review（2026-10-07，Jeff approved）

- **Verdict**: Jeff approved；已經全域安裝喺 `~/.claude/skills/security-audit`（直接由已掃描嘅 clone 複製，commit `c1c8a8c`，冇經 `npx skills add`）。
- **SkillSpector**（只跑 static；`claude_cli` LLM pass 失敗，因為 CLI 未登入）：score 86–100，CRITICAL / DO NOT INSTALL。逐條人手核對過，全部係 false positive：
  - MP3 / PE3 / PE1 / EA2 / TM3 嘅位置都係 skill 自己解釋攻擊類型嘅文字（例如問 repo 有冇 check-in `.env`）。
  - test 檔嘅 PE3 係用 `/etc/passwd` 做 path-traversal 測試輸入。
  - AE1 只係指 skill 會喺執行時先寫出 `findings.json`、`REPORT.md` 等檔案；scanner 自己都講明唔係 evasion 嘅證據。
  - RP1 係 README 入面冇 pin 版本嘅 `npx skills`。
- **Scripts**：`validate-findings.cjs` 同 `validate-coverage-ledger.cjs` 只 import `fs` / `path` / `util`，只讀檔：冇 network、冇 child process、冇寫檔。
- **Windows 限制**：喺 Node 22 / Windows 上，`validate-findings` 有 7 條 CLI test fail（"OS no-follow and nonblocking input protection is unavailable"），所以 phase 4 嘅 `findings.json` 檢查喺原生 Windows 會拒絕執行。改喺 WSL 或者 macOS / Linux 跑，或者接受報告未經 schema 驗證。`validate-coverage-ledger` 31 條 test 全部通過。

## Source

- https://github.com/cloudflare/security-audit-skill — Cloudflare — created 2026-06-18
- Reader: raw.githubusercontent.com README (curl) + GitHub search API (connector); raw text in `raw/20261005-cloudflare-security-audit-skill.md`.

## Related

- [[hot-list/2026-W40]]
- [[pages/20261004-cloudflare-open-source-ai-security-audit-skill]]
- [[pages/20260828-nvidia-skillspector-skill-security-scanner]]
- [[../../skills/scanning-agent-skills/SKILL|skill: scanning-agent-skills]]
