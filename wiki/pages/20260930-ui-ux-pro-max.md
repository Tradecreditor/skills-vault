---
title: "UI UX Pro Max: AI Design Intelligence Skill for Coding Agents"
slug: 20260930-ui-ux-pro-max
type: repo
status: draft
source_url: "https://github.com/nextlevelbuilder/ui-ux-pro-max-skill"
source_platform: github
author: "nextlevelbuilder"
published: "2026"
captured_at: "2026-09-30T20:26:00Z"
captured_by: "routine:capture-link"
canonical_id: "github:nextlevelbuilder/ui-ux-pro-max-skill"
engagement: "stars=unknown (GitHub API proxy-blocked for non-attached repo)"
tags: [ui-ux, design-system, agent-skill, claude-code, vibe-coding, claude-plugin, npm, bm25, glassmorphism, tailwind, react, ai-design, multi-framework]
related: []
needs_manual_text: false
---

## 摘要

UI UX Pro Max 是一個開源的 Agent Skill，為 Claude Code、Cursor、Windsurf 等 AI 程式助手提供專業的 UI/UX 設計智慧。它內建 79 種可搜尋的 UI 樣式（如 Glassmorphism、Claymorphism、Brutalism）、192 種行業專屬色彩調色板、74 種字型搭配，以及針對 192 種行業類型的設計系統推理規則。透過 BM25 搜尋引擎，它能根據產品類型自動推薦最合適的設計系統，包括配色方案、排版選擇、Layout 模式及應避免的反模式。支援 22 種主流技術框架（React、Next.js、Tailwind、Vue、SwiftUI、Flutter 等），並可透過 Claude Marketplace 一鍵安裝或用 npm CLI 安裝到任何 AI 助手。v2.0 新增的設計系統生成器能在數秒內產出完整的訂製設計規範，是 vibe-coders 和需要快速生成專業 UI 的開發者的利器。

## Key facts

- **Install (Claude Code — Marketplace):**
  ```
  /plugin marketplace add nextlevelbuilder/ui-ux-pro-max-skill
  /plugin install ui-ux-pro-max@ui-ux-pro-max-skill
  ```
- **Install (CLI — recommended):**
  ```bash
  npm install -g ui-ux-pro-max-cli
  uipro init --ai claude   # or cursor / windsurf / gemini / codex / all
  ```
- **Install (npx, no global):** `npx ui-ux-pro-max-cli init --ai claude`
- 79 searchable UI styles (50 active, 29 supplemental, 9 deprecated); IDs are stable across versions
- 192 industry-specific reasoning rules → auto-generates Pattern + Style + Colors + Typography + Effects + Anti-patterns + Checklist
- 192 color palettes aligned 1:1 with product categories
- 74 Google Fonts pairings; 1,934 approved fonts in catalog
- 22 supported tech stacks (React, Next.js, Astro, Vue, Nuxt.js, Svelte, SwiftUI, React Native, Flutter, shadcn/ui, Angular, Laravel, Three.js, JavaFX, WPF, WinUI 3, UWP, Avalonia, Uno Platform, HTML+Tailwind, Jetpack Compose, CodeBuddy)
- 25 chart type recommendations for dashboards
- 119 UX guidelines including resilient text layout, reduced-motion, focus states, compact labels
- Search by industry: `python3 .claude/skills/ui-ux-pro-max/scripts/search.py "SaaS" --domain style --json`
- Uninstall: `uipro uninstall` (run from project root) or `uipro uninstall --global`
- Premium version adds Brand Identity, Logo Design, CIP, AI-image asset generation, Enterprise Design Tokens
- Website: https://uupm.cc · npm package: `ui-ux-pro-max-cli`
- MIT License; automated releases via semantic-release (Conventional Commits)

## 點解值得留意

- **Vibe coding 的設計副駕：** 直接給 Claude Code 或任何 AI 助手注入 UI/UX 設計智慧，無需手動翻查設計規範或自行撰寫 design system prompt——192 個行業規則即插即用。
- **BM25 推理引擎取代猜測：** 輸入產品類型，即可輸出 Pattern + Style + Colors + Typography + Anti-patterns + 交付前清單，大幅縮短 vibe-code 到可用 UI 的時間。
- **多平台 agent 統一安裝：** `uipro init --ai all` 一次為 Claude Code、Cursor、Windsurf、Codex CLI、Gemini CLI 等安裝，適合 Josep 同時用多個 AI 工具的工作流。
- **開源 + 可離線驗證：** 所有 catalog 數據提交在 repo 內，CI 離線執行，`npm --prefix cli run verify:data` 可本地驗證完整性，無需依賴雲端。

## Source

- **Repo:** https://github.com/nextlevelbuilder/ui-ux-pro-max-skill
- **Author:** nextlevelbuilder (viettranx)
- **Published:** 2026 (v2.0 released; exact date unavailable — GitHub API blocked by session proxy for non-attached repos)
- **Reader:** raw.githubusercontent.com (README.md, 37KB); GitHub REST API unavailable for this repo in this session

## Related

- [[../../skills/using-ui-ux-pro-max/SKILL|skill: using-ui-ux-pro-max]]
