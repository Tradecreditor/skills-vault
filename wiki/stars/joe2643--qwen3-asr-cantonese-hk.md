---
title: "qwen3-asr-cantonese-hk"
slug: joe2643--qwen3-asr-cantonese-hk
type: repo
status: draft
source_url: "https://github.com/joe2643/qwen3-asr-cantonese-hk"
source_platform: github
author: "joe2643"
published: "2026-11-10"
captured_at: "2026-11-15T06:03:33Z"
captured_by: "routine:github-stars-sync"
canonical_id: "github:joe2643/qwen3-asr-cantonese-hk"
engagement: "stars=71 forks=4"
tags: ["asr", "cantonese", "speech-to-text", "qwen3-asr", "llama-cpp", "gguf"]
related: []
needs_manual_text: false
---
## 摘要

呢個 repo 提供 Qwen3-ASR 1.7B 同 0.6B 嘅香港廣東話微調模型，專門處理夾雜英文嘅香港口語，輸出會用「係、喺、嘅、咗、㗎」等日常口語字，英文詞保持英文，避免原版模型出簡體或內地風格嘅字。README 附有完整基準：1.7B v2.1 喺 FLEURS 嘅字元錯誤率係 3.89%（原版 4.20%，whisper-large-v3 20.97%），中英夾雜 MCE 測試由 11.74% 降到 5.52%。v2.1 另外支援「閂燈、開燈」等短語音指令同 hotword 上下文提示，唔會將 hotword 照抄出嚟。權重有 BF16、GGUF（Q4_K_M、Q6_K、Q8_0）、FP8 同 NVFP4 版本，可用 llama.cpp 嘅 llama-server、transformers、vLLM 或 ComfyUI 運行，亦已被 OraType 用作 macOS 語音輸入。

## Key facts

- **Repo**: [joe2643/qwen3-asr-cantonese-hk](https://github.com/joe2643/qwen3-asr-cantonese-hk)
- **Stars**: 71 | **Forks**: 4
- **Language**: Python
- **License**: Apache-2.0
- **Last push**: 2026-11-15
- **Install**: `hf download joe2643/Qwen3-ASR-1.7B-Cantonese-HK-GGUF <gguf> <mmproj> --local-dir models`, then `llama-server -m ... --mmproj ... --port 8180`; or `pip install qwen-asr` for transformers
- **Weights**: 1.7B GGUF Q4_K_M 1.1 GB; 0.6B Q4_K_M 397 MB; clips up to ~30 s tested

## 點解值得留意

Jeff 嘅工作環境以香港廣東話為主，呢個模型係少數針對香港口語同中英夾雜做過基準比較嘅開源 ASR，而且細到可以喺本機 CPU 跑。可以考慮用嚟做語音輸入、會議錄音轉寫或者影片字幕，同現有 capture 流程入面嘅 Instagram/Facebook 影片音訊轉寫（目前用 Supadata）互補。留意佢只評估過廣東話同廣東話夾英文，純普通話表現可能較差。

## Source

- URL: https://github.com/joe2643/qwen3-asr-cantonese-hk
- Created: 2026-11-10
- Reader: raw.githubusercontent.com README + Jina Reader (GitHub API JSON)
