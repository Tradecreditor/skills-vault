---
title: "ZCode — Z.ai open-source coding agent harness (desktop + web + CLI)"
slug: 20261002-zcode-zai-harness
type: repo
status: draft
source_url: "https://github.com/zai-org/ZCode"
source_platform: github
author: "zai-org"
published: "2026-09-20"
captured_at: "2026-10-02T16:20:00Z"
captured_by: "routine:weekly-hot-list"
canonical_id: "github:zai-org/ZCode"
engagement: "stars=7325 forks=2232 x_likes=2862 x_reposts=266 x_views=644039 (@zcode_ai)"
tags: [hot-list, 2026-W39, coding-agent, harness, z-ai, glm, security, typescript]
related: [hot-list/2026-W39]
needs_manual_text: false
---

## 摘要

ZCode 係 Z.ai（智譜）嘅 AI 編程工作台，提供桌面 app、瀏覽器介面同終端 Agent，專為 GLM-5.3 調校。2026-09-18 開發者 ferstar 揭發佢背景加密上傳成個 workspace（連 .git 歷史）去阿里雲 OSS，Z.ai 道歉、修復（v3.14.0），並喺 2026-09-21 以 Apache-2.0 開源。倉庫 2026-09-20 建立，開源後幾日已超過 7,000 stars；官方 @zcode_ai 道歉兼開源貼文 2,862 likes、644k views。注意：公開倉庫只有 2–3 個 commit，歷史同上傳代碼已清走，server 端保留情況只能靠官方說法。

## Key facts

- **What**: Electron desktop app, browser UI, terminal Agent CLI and runtime in one TypeScript monorepo (Apache-2.0); official harness for GLM-5.3.
- **Build**: Node.js 24.14.0 + pnpm 10.33.2; `pnpm bootstrap`, `pnpm dev:desktop`; Agent CLI source in `apps/zcode-cli/`.
- **Incident**: 2026-09-18 ferstar showed the client packaging the whole workspace incl. `.git`, encrypting it with a server-held key and uploading to Aliyun OSS; Z.ai disabled the Repo Wiki / snapshot workflow (v3.14.0), had CAICT and NSFOCUS confirm the bucket empty, open-sourced on 2026-09-21.
- **Caveat**: repo has only 2–3 commits (history erased); NOTICE.md says there is no default OS sandbox and `--prompt` without `--mode` runs in yolo; full security report still pending.
- **Numbers (2026-10-02)**: 7,325 stars, 2,232 forks (GitHub search API). X: @zcode_ai 2,862 likes / 266 reposts / 644,039 views; @zRdianjiao 1,391 likes; @ZixuanLi_ 975 likes (fxtwitter, Sep 21).

## 點解值得留意

Hot list 2026-W39 入選項目，詳見 [[hot-list/2026-W39|hot-list/2026-W39]]。注意本次 run 喺 2026-10-02 執行，stars 為當日數字（建立至今累計），唔係窗口結束（09-27）嗰刻。

## Source

- https://github.com/zai-org/ZCode — zai-org — 2026-09-20
- Reader: raw.githubusercontent.com README + GitHub search API (connector); raw text in `raw/20261002-zcode-zai-harness.md`.

## Related

- [[hot-list/2026-W39]]
- [[pages/20260920-fast-jev-compaction]]
