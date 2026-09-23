---
title: "whisperX"
slug: m-bain--whisperX
type: repo
status: draft
source_url: "https://github.com/m-bain/whisperX"
source_platform: github
published: "2022-12-09"
captured_at: "2026-09-19T11:09:28.035983Z"
captured_by: "routine:github-stars-sync"
canonical_id: "github:m-bain/whisperX"
engagement: "stars=24120 forks=2429"
tags: ["asr", "speech", "speech-recognition", "speech-to-text", "whisper"]
related: []
needs_manual_text: false
---
## 摘要

WhisperX 係喺 OpenAI Whisper 基礎上,加入強制音位對齊(phoneme alignment)同語音活動偵測(VAD)分批處理嘅語音識別工具,用 large-v2 模型都可以做到 70 倍實時速度嘅轉錄,仲有準確到單字級嘅時間戳。原生 Whisper 得返句子級時間戳,誤差可以去到幾秒;WhisperX 用 wav2vec2.0 呢類音位模型做強制對齊,將每隻字嘅開始/結束時間都對準返落去。佢仲整合咗 pyannote-audio 做多人講者分離(speaker diarization),可以直接標記邊句係邊個講嘅。安裝好簡單,`pip install whisperx` 就得,支援 GPU(CUDA 12.8)同 CPU/Mac 執行,亦有 Python API 可以逐步(transcribe → align → diarize)自己組裝流程。

## Key facts

- **Repo**: [m-bain/whisperX](https://github.com/m-bain/whisperX)
- **Install**: `pip install whisperx`
- **Stars**: 24,120 | **Forks**: 2,429
- **Language**: Python
- **License**: BSD 2-Clause "Simplified" License
- **Topics**: asr, speech, speech-recognition, speech-to-text, whisper

## 點解值得留意

呢個 project 喺 2023 年 INTERSPEECH 收錄咗論文,亦攞過 Ego4d transcription challenge 冠軍,長期維護、star 數高達二萬幾,對要處理會議記錄、Podcast 或者影片字幕自動化嘅場景好有用。用開 Whisper 但覺得時間戳唔準嘅人,可以直接用嚟取代。

## Source

- URL: https://github.com/m-bain/whisperX
- Created: 2022-12-09
- Reader: routine:github-stars-sync

## Related
