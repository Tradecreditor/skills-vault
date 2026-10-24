---
title: "peach"
slug: peach-mitao--peach
type: repo
status: draft
source_url: "https://github.com/peach-mitao/peach"
source_platform: github
author: "peach-mitao"
published: "2026-08-19"
captured_at: "2026-10-24T06:04:00Z"
captured_by: "routine:github-stars-sync"
canonical_id: "github:peach-mitao/peach"
engagement: "stars=9198 forks=1100"
tags: ["local-first", "media-library", "self-hosted", "python", "react", "video-player"]
related: []
needs_manual_text: false
---
## 摘要

Peach（蜜桃）係一個單用戶、本地優先嘅個人影片館藏系統，README 以中文為主（另有英文版）。佢可以將本地硬碟同已掛載嘅網盤（115、PikPak、OneDrive 等）合併成一個館藏，用全螢幕封面牆挑片並原位播放，同一作品嘅不同版本、分卷集中切換。功能包括載入或在線搜尋字幕、讀取現有 NFO 同海報並由多個來源補齊資料、跨站追蹤創作者更新、按口味推薦，以及透過 115 或 PikPak 雲下載後自動整理入庫。觀看紀錄同設定全部存喺本機，掃描唔會改動原檔案，手動整理會先預覽並可撤回。專案標明 18+，只供成年人管理自己嘅收藏，倉庫本身不含媒體內容；預設勾選嘅遠程診斷可以取消。

## Key facts

- **Repo**: [peach-mitao/peach](https://github.com/peach-mitao/peach)
- **Stars**: 9,198 | **Forks**: 1,100
- **Language**: Python (backend) + React (UI)
- **License**: AGPL-3.0-or-later
- **Last push**: 2026-10-23
- **Install**: Windows installer/portable zip from Releases; macOS DMG built locally; from source needs Git, uv, Python 3.14+; Docker for VPS/NAS (`docs/DOCKER.md`)
- **Notes**: 18+ adult-content library manager; optional Sentry diagnostics on by default (can be turned off); demo at demo.peach.video

## 點解值得留意

呢個專案係「單用戶、本地優先、自架」軟件嘅一個完整例子：Python + React、跨平台安裝包同 Docker 部署齊全，而且有斷點續跑、預覽後才改檔、可撤回等穩健嘅設計取向，值得參考。對 vault 嚟講佢同 agent 技能關係唔大，主要係作為自架媒體管理同本地優先架構嘅參考。內容屬成人向，另外要留意預設開啟嘅遙測選項同 AGPL 授權。

## Source

- URL: https://github.com/peach-mitao/peach
- Created: 2026-08-19
- Reader: raw.githubusercontent.com README + Jina Reader (GitHub API JSON)
