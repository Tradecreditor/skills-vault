---
title: "Scrapegraph-ai"
slug: ScrapeGraphAI--Scrapegraph-ai
type: repo
status: draft
source_url: "https://github.com/ScrapeGraphAI/Scrapegraph-ai"
source_platform: github
author: "ScrapeGraphAI"
published: "2024-01-27"
captured_at: "2026-09-19T11:09:28.035576Z"
captured_by: "routine:github-stars-sync"
canonical_id: "github:ScrapeGraphAI/Scrapegraph-ai"
engagement: "stars=31107 forks=3137"
tags: ["ai-crawler", "ai-scraping", "ai-search", "crawler", "data-extraction", "firecrawl-alternative", "large-language-model", "llm", "markdown", "rag", "scraping", "scraping-python", "web-crawler", "web-crawlers", "web-data", "web-data-extraction", "web-scraper", "web-scraping", "web-search", "webscraping"]
related: []
needs_manual_text: false
---
## 摘要

ScrapeGraphAI 係一個用 LLM 加圖(graph)邏輯做網頁/本機文件擷取嘅 Python library,只需要講清楚想攞邊啲資訊,library 就自動幫你設計爬蟲流程,唔使自己逐個網站寫 selector。核心係 `SmartScraperGraph` 呢類 pipeline,俾一個 prompt 同一個來源(URL 或者 XML/HTML/JSON/Markdown 檔案),就輸出結構化 JSON;另外仲有 `SearchGraph`(跨多個搜尋結果頁擷取)、`SpeechGraph`(生成語音)、`ScriptCreatorGraph`(生成擷取用嘅 Python script)等變體,全部都有平行處理多頁嘅 Multi 版本。可以接 OpenAI、Groq、Azure、Gemini 或者用 Ollama 跑本機模型。

## Key facts

- **Repo**: [ScrapeGraphAI/Scrapegraph-ai](https://github.com/ScrapeGraphAI/Scrapegraph-ai)
- **Stars**: 31,107 | **Forks**: 3,137
- **Language**: Python
- **License**: MIT License
- **Install**: `pip install scrapegraphai` + `playwright install`
- **也有 MCP server**:[smithery.ai/server/@ScrapeGraphAI/scrapegraph-mcp](https://smithery.ai/server/@ScrapeGraphAI/scrapegraph-mcp)
- **Topics**: ai-crawler, ai-scraping, ai-search, crawler, data-extraction, firecrawl-alternative, large-language-model, llm, markdown, rag, scraping, scraping-python, web-crawler, web-crawlers, web-data, web-data-extraction, web-scraper, web-scraping, web-search, webscraping

## 點解值得留意

開源版本俾晒你完全控制(自己揀 LLM、自己管理 proxy 同瀏覽器),仲有一個對應嘅 managed cloud API(`scrapegraph-py`/`scrapegraph-js` SDK)俾唔想自己維運嘅人直接用 credit 叫用,兩條路線清楚分開,對想快速評估「自己起 vs 用現成服務」嘅人幾有參考價值。同 vault 入面其他 scraping/agent-reach 類工具（例如 Agent-Reach、OpenCLI)可以擺埋一齊比較唔同嘅擷取策略。

## Source

- URL: https://github.com/ScrapeGraphAI/Scrapegraph-ai
- Created: 2024-01-27
- Reader: routine:github-stars-sync

## Related
