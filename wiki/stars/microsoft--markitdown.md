---
title: "markitdown"
slug: microsoft--markitdown
type: repo
status: draft
source_url: "https://github.com/microsoft/markitdown"
source_platform: github
author: "Microsoft"
published: "2024-11-13"
captured_at: "2026-09-20T23:06:50Z"
captured_by: "routine:github-stars-sync"
canonical_id: "github:microsoft/markitdown"
engagement: "stars=185929 forks=13689"
tags: [autogen, autogen-extension, langchain, markdown, microsoft-office, openai, pdf]
related: []
needs_manual_text: false
---

## 摘要
MarkItDown 係微軟出嘅一個輕量級 Python 工具,專門將各種檔案格式(PDF、PowerPoint、Word、Excel、圖片、音訊、HTML、CSV/JSON/XML、ZIP、YouTube 連結、EPub 等)轉換做 Markdown,方便畀 LLM 同文字分析流程使用。之所以揀 Markdown 做輸出格式,係因為佢夠貼近純文字、又保留到標題、清單、表格、連結呢啲重要結構,而且好多主流 LLM(例如 GPT-4o)本身就「識講」Markdown,訓練數據入面亦有大量呢種格式,轉換出嚟嘅結果 token 效率亦高。工具支援第三方 plugin 擴充格式(包括加 OCR 嘅 markitdown-ocr plugin),亦可以駁埋 Azure Document Intelligence 或 Azure Content Understanding 做雲端高質轉換同結構化欄位擷取。

## Key facts
- Language: Python
- License: MIT
- Created: 2024-11-13
- Last pushed: 2026-09-16
- Stars: 185,929
- Forks: 13,689
- Install: `pip install 'markitdown[all]'`
- CLI: `markitdown path-to-file.pdf -o document.md`

## 點解值得留意
呢個係將檔案轉做 LLM 友善格式嘅事實標準工具之一,對於 vault-capture 呢類要處理 PDF/Office 文件嘅 skill 嚟講,可以直接攞嚟做轉換管道嘅底層依賴,唔使自己重新發明輪子。項目結構清晰咁分開核心 converter 同 plugin 生態,亦係一個睇「點樣設計一個 CLI + plugin 架構嘅工具」嘅好例子。

## Source
GitHub repository: https://github.com/microsoft/markitdown
Author: Microsoft
Published: 2024-11-13
Reader used: raw README via Exa (web_fetch_exa)

## Related
