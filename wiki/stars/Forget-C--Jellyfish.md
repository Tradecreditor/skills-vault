---
title: "Jellyfish"
slug: Forget-C--Jellyfish
type: repo
status: draft
source_url: "https://github.com/Forget-C/Jellyfish"
source_platform: github
author: "Forget-C"
published: "2026-03-06"
captured_at: "2026-09-21T23:07:37Z"
captured_by: "routine:github-stars-sync"
canonical_id: "github:Forget-C/Jellyfish"
engagement: "stars=6466 forks=1121"
tags: [ai, short-drama, video-generation]
related: []
needs_manual_text: false
---

## 摘要
Jellyfish 係一個做 AI 短劇嘅端到端製作工作台,由劇本輸入、拆分鏡頭、角色/場景/道具/服裝一致性管理,一直做到生成圖片、影片同輸出。核心流程係「劇本拆解 → 鏡頭準備 → 候選確認 → 鏡頭就緒 → 生成工作區」,重有統一嘅異步任務中心追蹤所有文字、圖片、影片生成任務嘅狀態,支援取消同回復。佢將角色、場景、道具、服裝維護做一個共享嘅實體模型,俾唔同鏡頭可以重用同一批資產,減少 AI 生成畫面走樣嘅問題。

## Key facts
- Language: Python (backend) + frontend under `front/`
- License: Apache-2.0
- Created: 2026-03-06
- Last pushed: 2026-07-30
- Stars: 6,466
- Forks: 1,121
- Backend: `uv sync` + `uvicorn app.main:app`; Frontend: `pnpm install` + `pnpm dev`
- Docker Compose setup under `deploy/compose/` (frontend :7788, backend :8000, MySQL, Redis, RustFS)

## 點解值得留意
針對短劇/微劇呢個垂直場景,將「AI 生成」由一次性小工具做成有完整生產流程嘅工作台,強調一致性管理(角色/場景/道具跨鏡頭唔走樣)同任務可追蹤,呢個對想用 AI 做批量影片內容嘅創作者或者工作室幾有參考價值,亦都係一個管理長時間運行 AI 生成任務嘅基建設計案例。

## Source
GitHub repository: https://github.com/Forget-C/Jellyfish
Author: Forget-C
Published: 2026-03-06
Reader used: raw README via Exa (web_fetch_exa)

## Related
