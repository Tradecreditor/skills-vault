---
title: "google-analytics-mcp"
slug: googleanalytics--google-analytics-mcp
type: repo
status: draft
source_url: "https://github.com/googleanalytics/google-analytics-mcp"
source_platform: github
published: "2025-07-16"
captured_at: "2026-09-19T11:09:28.036193Z"
captured_by: "routine:github-stars-sync"
canonical_id: "github:googleanalytics/google-analytics-mcp"
engagement: "stars=3242 forks=693"
tags: []
related: []
needs_manual_text: false
---
## 摘要

呢個係 Google Analytics 官方出嘅本機 MCP server,俾 LLM 通過 Google Analytics Admin API 同 Data API 讀取你嘅網站數據。裝好之後會俾到幾組 tool:攞帳戶/資源(property)資訊、跑標準報表(`run_report`)同漏斗報表(`run_funnel_report`)、攞自訂維度同指標、仲有即時報表(`run_realtime_report`)。設定流程需要開通兩個 GA API、用 Application Default Credentials 授權(read-only scope),然後喺 Gemini CLI 或者 Claude Code(`claude mcp add analytics-mcp`)登記呢個 server。裝好之後就可以直接用自然語言問「呢排我個 GA property 邊個 event 最受歡迎」呢類問題。

## Key facts

- **Repo**: [googleanalytics/google-analytics-mcp](https://github.com/googleanalytics/google-analytics-mcp)
- **Stars**: 3,242 | **Forks**: 693
- **Language**: Python
- **License**: Apache License 2.0
- **Install**: `pipx run analytics-mcp`(要先開通 GA Admin API + Data API,同用 `gcloud auth application-default login` 設定憑證)
- **Claude Code**: `claude mcp add analytics-mcp --scope user -e GOOGLE_APPLICATION_CREDENTIALS=... -e GOOGLE_PROJECT_ID=... -- pipx run analytics-mcp`
- **Topics**: 冇(repo 未打 topic)

## 點解值得 star

Google 官方直接出嘅 GA MCP server(而唔係第三方包裝),對經常要問「網站流量點樣」嘅人嚟講幾直接,一個指令就可以喺 Claude Code / Gemini CLI 度直接查 Analytics 數據做分析,唔使開 GA 網頁介面篤嚟篤去。留意佢仲係 Experimental 階段,而且憑證授權步驟(OAuth client + ADC)幾多步,唔算即開即用。

## Source

- URL: https://github.com/googleanalytics/google-analytics-mcp
- Created: 2025-07-16
- Reader: routine:github-stars-sync

## Related
