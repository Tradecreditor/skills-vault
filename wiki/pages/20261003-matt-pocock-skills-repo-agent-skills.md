---
title: "Matt Pocock open-sources his agent skills (mattpocock/skills)"
slug: 20261003-matt-pocock-skills-repo-agent-skills
type: post
status: draft
source_url: "https://www.threads.com/@easyanythinghk/post/DeBeoDtgAo5"
source_platform: threads
author: "@easyanythinghk"
published: "2026-10-03"
captured_at: "2026-10-04T21:09:15Z"
captured_by: "claude-code-cloud"
canonical_id: "threads:DeBeoDtgAo5"
engagement: "likes=108 replies=3 reposts=12 shares=123"
tags: [topic/repo-picks, agent-skills, matt-pocock, github, coding-agents, skill-md]
related: [vercel-labs--skills, 20260921-4-claude-code-plugins, 20260918-obsidian-skills]
needs_manual_text: false
---

## 摘要

@easyanythinghk（帳號名「dev」）喺 Threads 推介 TypeScript 名人 Matt Pocock 將自己日常用嘅 agent skills 開源，repo 係 `mattpocock/skills`。帖文話內容有 Shell 腳本、AI 編程 workflow 同 debug 技巧，完全免費，並聲稱佢係 GitHub Trending 第 6 名、累積 27.4 萬星、單日 +955 星；repo 連結喺作者自己第一則回覆。根據 repo README，呢套嘢叫「Skills For Real Engineers」，以 SKILL.md 為主，分 Engineering 同 Productivity 兩大類共 27 個 skill（例如 grill-me、tdd、diagnosing-bugs），可用 Claude Code plugin 或 `npx skills@latest add mattpocock/skills` 安裝。因為 GitHub API 喺呢個環境回 403，星數同排名未能核實，只可當作帖文嘅說法。

## Key facts

- What it is: `github.com/mattpocock/skills`, titled "Skills For Real Engineers". README tagline: "My agent skills that I use every day to do real engineering - not vibe coding." Stance: small, composable skills that work with any model, as opposed to GSD, BMAD and Spec-Kit, which "own the process".
- Poster's claims (NOT verified): GitHub Trending #6, "27.4 萬" (274K) total stars, +955 stars in a day, the skill set was used privately for a long time before being open-sourced, and reviews say it should have been seen earlier.
- GitHub verification (2026-10-04): api.github.com answered HTTP 403 ("GitHub access to this repository is not enabled for this session"), so stars, license, pushed_at and topics were not retrieved. README fetched fine via raw.githubusercontent.com (233 lines) and is stored verbatim in the raw file.
- From the README (author's own statements): about 60,000 developers on his newsletter; listed on skills.sh (skills.sh/mattpocock/skills); in Claude Code's official marketplace.
- Install, copied verbatim from the README (NOT run). Pick one route; the README warns that installing both leaves every skill twice.
  - Claude Code: `claude plugins install mattpocock-skills`, or inside a session `/plugin install mattpocock-skills` (managed, read-only bundle that updates when he ships).
  - Codex and other agents: `npx skills@latest add mattpocock/skills` (choose the skills and the agents; make sure `setup-matt-pocock-skills` is one of them).
  - Editable copy for tinkerers: the same `npx skills@latest add mattpocock/skills`, then `npx skills update` to pull his latest changes.
  - After install, run `/setup-matt-pocock-skills` once per repo: it asks which issue tracker you use (GitHub, Linear or local files), your triage labels, and where docs are saved.
- The 27 skills listed in the README. Engineering, user-invoked: ask-matt, grill-with-docs, triage, improve-codebase-architecture, setup-matt-pocock-skills, to-spec, to-tickets, implement, implement-spec, wayfinder, retro. Engineering, model-invoked: prototype, diagnosing-bugs, research, tdd, domain-modeling, codebase-design, code-review, pr, wizard. Productivity, user-invoked: grill-me, handoff, teach, to-questionnaire, wait-what. Productivity, model-invoked: grilling, writing-for-agents.
- README split: user-invoked skills are typed by you (for example `/grill-me`) and orchestrate; model-invoked skills can also be reached for automatically by the agent. The README calls `/grill-me` and `/grill-with-docs` its most popular skills.
- Poster wording vs README: the post says ".agents skill set" with "Shell scripts, AI coding workflows, debug tips". The README presents SKILL.md skills under `skills/engineering/` and `skills/productivity/`; it links to a `.agents/adr/` folder (architecture decision records), and only the `wizard` skill is described as generating bash wizards. Treat the post's description as loose.
- Engagement: 108 likes, 3 replies, 12 reposts, 123 shares (order inferred from Threads UI; no view count shown).

## 點解值得留意

- **同 vault 直接對應**：Jeff 嘅 vault 本身就係可安裝 skills 嘅庫，呢個 repo 係一個大型、有 Claude Code 官方 marketplace 版本嘅參考，可以對照佢嘅 user-invoked / model-invoked 分法，同 vault 嘅 `keeping-handoff-docs`（對應 `handoff`）、`model-tiering` 等 skill 比較。
- **顧問流程可借用**：`grill-with-docs`、`to-spec`、`to-tickets` 係「先問到對齊需求，再拆單」嘅流程，適合用喺幫香港中小企做 AI 項目嘅需求訪談；`tdd`、`diagnosing-bugs` 可以直接放入 Claude Code 項目。
- **安裝前先掃描**：`npx skills@latest add` 同 plugin 都係第三方內容，裝落客戶項目前先用 vault 嘅 `scanning-agent-skills` 掃一次；27.4 萬星同 Trending 第 6 都未核實，等 GitHub API 可用先好引用。
- **短影音題材**：「大神私藏 skills 全公開」有噱頭，但 hook 要跟 README，唔好照抄帖文「Shell 腳本」呢個說法。

## Source

- Post: https://www.threads.com/@easyanythinghk/post/DeBeoDtgAo5
- Author: @easyanythinghk (display name "dev") · Published: 2026-10-03
- Engagement: likes=108 replies=3 reposts=12 shares=123 (order inferred from Threads UI)
- Reader: Jina Reader (r.jina.ai) for the post; the author's reply (id DeBetCTAFY0, posted about 40 seconds later, holds the repo link) read from the share-page HTML; GitHub README via raw.githubusercontent.com (api.github.com 403)
- Share URL: https://www.threads.com/share/BBK7rXuE7Y/
- Repo: https://github.com/mattpocock/skills
- Not captured: the post's image, "Related threads" by other accounts

## Related

- [[../stars/vercel-labs--skills|skills (vercel-labs)]] — the `npx skills` installer the README uses to deliver these skills
- [[../pages/20260921-4-claude-code-plugins|4 Claude Code Plugins That Fix the Real Bottlenecks]] — another bundle of skills and plugins for Claude Code
- [[../pages/20260918-obsidian-skills|obsidian-skills: Agent Skills for Obsidian]] — another Agent Skills repo already in the vault
