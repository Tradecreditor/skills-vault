---
title: "cal.diy"
slug: calcom--cal.diy
type: repo
status: draft
source_url: "https://github.com/calcom/cal.diy"
source_platform: github
author: "calcom"
published: "2021-03-22"
captured_at: "2026-09-20T23:06:50Z"
captured_by: "routine:github-stars-sync"
canonical_id: "github:calcom/cal.diy"
engagement: "stars=48578 forks=15179"
tags: [next-auth, nextjs, open-source, postgresql, prisma, t3-stack, tailwindcss, trpc, turborepo, typescript, zod]
related: [greensock--gsap-skills, OWASP--secure-coding-practices-quick-reference-guide]
needs_manual_text: false
---

## 摘要
Cal.diy 係 Cal.com(排程/預約系統)嘅社群主導開源分支,將所有 enterprise 同商業限定功能(例如 Teams、Organizations、SSO/SAML)全部拆走,令成個 codebase 100% 用 MIT license,唔使 license key 就可以直接自架使用。項目用 Next.js、tRPC、React、Tailwind CSS、Prisma 同 Daily.co 起底,支援 Docker Compose 一鍵部署,亦有齊本地開發、資料庫遷移、E2E 測試等文件。官方提醒呢個版本只建議俾識自己管理伺服器、資料庫同資安嘅使用者做個人非正式用途,商業/企業場景應該用返正牌 Cal.com。

## Key facts
- Language: TypeScript
- License: MIT
- Created: 2021-03-22
- Last pushed: 2026-09-20
- Stars: 48,578
- Forks: 15,179
- Stack: Next.js, tRPC, React, Prisma, Tailwind CSS
- Quick start: `yarn dx` (Docker) or `docker compose up -d`

## 點解值得留意
對於想要完全自主掌控嘅排程/約會系統(例如幫客戶或者自己業務整 booking page),Cal.diy 提供一個冇商業限制嘅開源選擇,亦係一個研究 Next.js + tRPC + Prisma 大型 monorepo(turborepo)架構嘅好教材。留意呢個 fork 冇官方 hosted 版本,一定要自己部署管理。

## Source
GitHub repository: https://github.com/calcom/cal.diy
Author: calcom
Published: 2021-03-22
Reader used: raw README via Exa (web_fetch_exa)

## Related

- [[greensock--gsap-skills|gsap-skills]] — 都係商業產品開放出嚟嘅開源版本，但取向相反：GSAP 係全部 plugin 變免費，Cal.diy 係拆走商業功能淨返 MIT 部分。
- [[OWASP--secure-coding-practices-quick-reference-guide|secure-coding-practices-quick-reference-guide]] — 自架呢類處理用戶資料嘅系統，正正需要呢份安全編碼清單。
