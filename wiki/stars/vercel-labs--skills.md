---
title: "skills"
slug: vercel-labs--skills
type: repo
status: draft
source_url: "https://github.com/vercel-labs/skills"
source_platform: github
author: "Vercel Labs"
published: "2026-01-14"
captured_at: "2026-09-20T00:00:00Z"
captured_by: "routine:github-stars-sync"
canonical_id: "github:vercel-labs/skills"
engagement: "stars=32090 forks=2737"
tags: [agent-skills, agents, tools]
related: [LottieFiles--motion-design-skill, Leonxlnx--taste-skill, greensock--gsap-skills, cathrynlavery--diagram-design, upstash--context7]
needs_manual_text: false
---

## 摘要
開放 agent skills 生態嘅 CLI 工具，一句 `npx skills add <來源>` 就裝到 skill。支援 79 種 agent，包括 OpenCode、Claude Code、Codex、Cursor 等等，會自動偵測你裝咗邊個。來源格式好闊：GitHub 簡寫（owner/repo）、完整 URL、指向 repo 入面某一個 skill 嘅路徑、GitLab、Azure Repos、任何 git URL，甚至本地資料夾。私有 repo 用返你本身嘅 git 憑證，唔使另外設定。另有 `skills use`，唔安裝都可以即場產生 prompt 或者直接開一個 agent 嚟跑。
## Key facts
- Language: TypeScript
- License: MIT
- Created: 2026-01-14
- Last pushed: 2026-09-18
- Stars: 32,090
- Forks: 2,737
- Homepage: https://skills.sh
- CLI-based: npx skills

## 點解值得留意
你個 vault 就係靠呢個 CLI 對外開放——`npx skills add Tradecreditor/skills-vault` 用嘅正正係佢。佢事實上已經成為 skill 分發嘅共同標準，所以佢支援咩來源格式，直接決定你啲 skill 可以點樣俾人攞去用。
## Source
GitHub repository: https://github.com/vercel-labs/skills
Author: Vercel Labs
Captured: 2026-09-20

## Related

- [[LottieFiles--motion-design-skill|motion-design-skill]] — 嗰篇筆記寫明用 `npx skills add` 裝，係呢個 CLI 嘅實際用例。
- [[Leonxlnx--taste-skill|taste-skill]] — 兩者都覆蓋 Claude Code / Codex 等多個平台嘅 skill 分發。
- [[greensock--gsap-skills|gsap-skills]] — GSAP skills 明言配呢個 CLI 就可以裝落 40 幾種 agent。
- [[cathrynlavery--diagram-design|diagram-design]] — 都係將 skill 分發到多個 agent client 嘅方式：一個用 plugin marketplace，一個用 CLI。
- [[upstash--context7|context7]] — 兩者都支援「CLI + Skills」模式，唔一定要用 MCP。
