---
title: "小礦工挖挖礦：Moli，專為 AI 代理而設的 Rust 瀏覽器"
slug: 20261028-moli-rust-browser-for-ai-agents
type: post
status: draft
source_url: "https://www.instagram.com/reel/De9t1wcD01v/"
source_platform: instagram
author: "yt_tiny_miner"
published: "2026-10-27"
captured_at: "2026-10-28T00:00:00Z"
captured_by: "routine:capture-link"
canonical_id: "instagram:De9t1wcD01v"
engagement: "not shown by reader"
tags: [topic/agent-tooling, instagram, moli, rust, headless-browser, playwright, open-source]
related: [20261012-moli-headless-browser-for-ai-agents]
needs_manual_text: false
---

## 摘要
有人用 Rust 寫了一個專為 AI 代理設計的無頭瀏覽器，名叫 Moli，開源，GitHub 據稱有兩萬多顆星。佢嘅設計係先處理頁面結構，要點座標先排版、要截圖先繪畫，所以代理讀網頁唔使先渲染畫面。官方測試 192 個真實網站，Moli 抓到有用內容嘅有 103 個，Chrome 係 101 個；中位記憶體 73MB 對 773MB，約係 Chrome 十分之一。官方亦寫明唔追求同 Chrome 畫面完全一致。輸出可揀 Markdown、JSON 或語意樹，Playwright 亦可直接連接。

## Key facts
- Name: Moli; open source; written in Rust; "20k+" GitHub stars (per the post, not verified).
- Design: structure first; layout only when coordinates are requested; screenshot rendered only on demand.
- Official benchmark (as quoted): 192 real sites; useful content captured on 103 (Moli) vs 101 (Chrome); median memory 73MB vs 773MB.
- Does not aim for pixel parity with Chrome.
- Outputs: Markdown, JSON, or semantic tree; Playwright can connect to it.
- Repo URL not given in the caption; reel audio not transcribed (caption carries the substance).

## 點解值得留意
- 對 agent 讀網頁嘅記憶體同成本有參考價值，可同 Agent-Reach / OpenCLI 等讀取工具比較。
- 數字係官方自測，經二手轉述，採用前應到 repo 核實。

## Source
- https://www.instagram.com/reel/De9t1wcD01v/ — yt_tiny_miner, ~2026-10-27. Reader: Jina (caption in body; counts not available).

## Related
- [[Panniantong--Agent-Reach|Agent-Reach]]
- [[jackwener--OpenCLI|OpenCLI]]
- [[20261012-moli-headless-browser-for-ai-agents|lexmount/moli（先前已入庫嘅 repo 頁）]]
