---
title: "NVIDIA SkillSpector: Security Scanner for Agent Skills"
slug: 20260828-nvidia-skillspector-skill-security-scanner
type: tool
status: draft
source_url: "https://www.instagram.com/reel/DcllmSNv_Bk/"
source_platform: instagram
author: "nick_saraev"
published: "2026-08-28"
captured_at: "2026-09-27T15:01:27Z"
captured_by: "claude-code-cloud"
canonical_id: "instagram:DcllmSNv_Bk"
engagement: "likes=3.9K comments=3.3K"
tags: [agent-skills, ai-security, security-scanner, prompt-injection, supply-chain-security, claude-code, codex, mcp, nvidia]
related: [skills/scanning-agent-skills, 20260923-promptfoo, stars/vercel-labs--skills, 20260921-4-claude-code-plugins, stars/OWASP--secure-coding-practices-quick-reference-guide]
needs_manual_text: false
---

## 摘要
呢條 Instagram Reel 由 Nick Saraev（@nick_saraev）發佈，介紹 NVIDIA 開源嘅 SkillSpector：一個喺安裝 agent skill 之前先做安全掃描嘅工具，定位好似 Claude Code / Codex / Gemini CLI 同 skill 之間嘅「防毒軟件」。佢引用研究指出，喺 31,132 個被分析嘅 skill 入面，26.1% 有安全漏洞，5.2% 似乎帶有惡意意圖。SkillSpector 可以掃 Git repo、URL、zip、資料夾或者單一 SKILL.md，用 71 種 pattern（17 類，包括 prompt injection、資料外洩、權限提升、供應鏈、MCP tool poisoning 等）做靜態分析，再可選用 LLM 做語意判斷，最後俾一個 0–100 風險分數同 SAFE / CAUTION / DO NOT INSTALL 建議。佢亦可以作為 MCP server 掛入 Claude Code，令 agent 喺安裝 skill 前自己先 call 掃描。適合任何經常由第三方 repo 安裝 skill 或 plugin 嘅人。

## Key facts
- Repo: `github.com/NVIDIA/SkillSpector` — Python 3.12+, Apache-2.0, ~18.4k stars / ~1.6k forks (github.com page, 2026-09-27). Part of the NVIDIA Verified Skills pipeline (docs.nvidia.com/skills); passing skills go to the `NVIDIA/skills` catalog.
- Install (CLI only): `uv tool install git+https://github.com/NVIDIA/skillspector.git` (update: `uv tool update skillspector`).
- Install with MCP server: `uv tool install 'skillspector[mcp] @ git+https://github.com/NVIDIA/skillspector.git'`, then `claude mcp add skillspector -- skillspector mcp`. Exposes one tool `scan_skill(target, use_llm=true, output_format="json")` returning `risk_score`, `severity`, `recommendation`, `safe_to_install`, `findings`, plus `llm_used` / `scan_mode`.
- Docker (no Python): `docker build -t skillspector .` then `docker run --rm -v "$PWD:/scan" skillspector scan ./my-skill/ --no-llm`.
- Usage: `skillspector scan ./my-skill/` · `skillspector scan ./SKILL.md` · `skillspector scan https://github.com/user/my-skill` · `skillspector scan ./my-skill.zip`. Output: `--format terminal|json|markdown|sarif`, `--output <file>`; `--no-llm` = static only (file contents stay local).
- Coverage: 71 patterns / 17 categories — prompt injection, anti-refusal, data exfiltration, privilege escalation, supply chain (incl. live OSV.dev CVE lookup, typosquatting, `curl | bash`), excessive agency, output handling, system-prompt leakage, memory poisoning, tool misuse, rogue agent, trigger abuse (overly broad / shadowing skill triggers), Python AST (exec/eval/subprocess), taint tracking, YARA, MCP least privilege, MCP tool poisoning.
- Scoring: CRITICAL +50, HIGH +25, MEDIUM +10, LOW +5, x1.3 if the skill ships executable scripts. 0–20 LOW/SAFE · 21–50 MEDIUM/CAUTION · 51–80 HIGH and 81–100 CRITICAL = DO NOT INSTALL.
- Exit codes: `0` score ≤ 50, `1` score > 50 (or `--fail-on-findings` / `--fail-on-incomplete` fired), `2` error — usable as a CI/install gate. Suggested gate: SAFE allow · CAUTION warn · DO_NOT_INSTALL block.
- Baselines: `skillspector baseline ./my-skill/ -o .skillspector-baseline.yaml`, then `scan --baseline ...` reports only new findings.
- LLM stage providers via `SKILLSPECTOR_PROVIDER` (default `nv_build`): openai, anthropic, bedrock, ollama, azure_openai, openai_compatible, and key-less `claude_cli` / `codex_cli` / `gemini_cli` / `opencode_cli` that reuse the local CLI login. LLM stage raises precision to ~87%.
- Trust model: never executes the scanned skill; LLM mode sends file contents to the configured provider; SC4 sends dependency names to OSV.dev even with `--no-llm`; it is not a sandbox. Limits: weaker on non-English text, cannot read text in images or binaries.
- Research basis: "Agent Skills in the Wild" (Liu et al., 2026) — 42,447 skills collected, 31,132 analysed; skills with executable scripts are 2.12x more likely to be vulnerable.
- The reel itself is a "Comment SKILL" lead-magnet post; the caption does not give commands, the details above come from the repo README.

## 點解值得留意
- 呢個 vault 本身就係由第三方 repo 大量收 skill（github-stars-sync、`npx skills add`），入 `wiki/stars/` 或者真正安裝落 Claude Code 之前，用 `skillspector scan <repo> --no-llm` 做一次 gate 好合理；CLAUDE.md 已經講明 draft skill 唔好自動跑，SkillSpector 係第二重保險。
- 幫香港中小企做 AI 顧問時，客戶一定會問「裝人哋啲 skill / MCP 安唔安全」——呢個工具有具體分數同報告（SARIF / Markdown），可以直接放入顧問交付物或者 CI。
- `claude_cli` / `codex_cli` provider 唔使 API key，用返本機登入就可以做 LLM 語意分析，成本低。
- 條 Reel 本身係「留言 SKILL 攞資源」嘅 lead-magnet 格式（3.3K 留言），對 Jeff 做 AI 短片內容有參考價值。

## Source
- Link: https://www.instagram.com/reel/DcllmSNv_Bk/
- Author: Nick Saraev (@nick_saraev)
- Published: 2026-08-28
- Engagement: likes=3.9K comments=3.3K (as displayed on 2026-09-27)
- Reader: jina (r.jina.ai) for the caption; repo README via raw.githubusercontent.com; repo stats via github.com page (WebFetch). Exa was unavailable (credit limit).
- Referenced repo: https://github.com/NVIDIA/SkillSpector

## Related
- [[../../skills/scanning-agent-skills/SKILL|skill: scanning-agent-skills]] — 由呢篇整理出嚟嘅 draft skill：安裝第三方 skill / plugin / MCP 之前點樣用 SkillSpector 做 gate。
- [[20260923-promptfoo|promptfoo: LLM Evals & Red Teaming]] — 另一個 AI 安全工具：promptfoo 係對你自己嘅 LLM app 做 red teaming，SkillSpector 係對第三方 skill 做安裝前掃描，兩者互補。
- [[../stars/vercel-labs--skills|skills (vercel-labs)]] — `npx skills add` 一句就裝第三方 skill，正正係 SkillSpector 想擋喺前面嘅入口。
- [[20260921-4-claude-code-plugins|4 Claude Code Plugins That Fix the Real Bottlenecks]] — 同樣係 IG 上推薦裝一堆 plugin / skill 嘅內容；裝之前可以先用 SkillSpector 掃一次。
- [[../stars/OWASP--secure-coding-practices-quick-reference-guide|OWASP secure coding practices]] — 一般安全編碼清單，可以配合 SkillSpector 嘅供應鏈 / AST 類別一齊睇。
