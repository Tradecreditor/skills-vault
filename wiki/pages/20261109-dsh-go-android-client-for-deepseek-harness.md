---
title: "ccch1mneyyy/dsh-Go — DSH Go: Android client that runs DeepSeek Harness on the phone or drives it remotely"
slug: 20261109-dsh-go-android-client-for-deepseek-harness
type: repo
status: draft
source_url: "https://github.com/ccch1mneyyy/dsh-Go"
source_platform: github
author: "ccch1mneyyy"
published: "2026-10-25"
captured_at: "2026-11-09T08:20:00Z"
captured_by: "routine:weekly-hot-list"
canonical_id: "github:ccch1mneyyy/dsh-Go"
engagement: "stars=16793 forks=723 (2026-11-09; 5203 in the 2026-11-02 snapshot, +11582 in 7 days)"
tags: [hot-list, 2026-W45, coding-agents, agent-harness, deepseek, dsh, android, mobile, phone-control, flutter]
related: [hot-list/2026-W45]
needs_manual_text: false
---

## 摘要

DSH Go 係社群開發、非官方嘅 DeepSeek Harness（dsh）Android 客戶端：可以喺手機本機跑 dsh（app 入面直接裝 Ubuntu、Node.js 同 DSH，唔使 root 或者另裝 Termux），亦可以透過 SSH 或 DSHarness Remote 遙控你電腦或伺服器上嘅 dsh。功能包括切換模型、傳圖、語音輸入、回應工具審批、plugin 原生卡片同表單，開咗無障礙權限仲可以讓本機引擎讀屏幕、撳掣同打字（手機控制）。README 對風險講得好清楚：AI 會錯、工具有真實後果、預設開咗匿名統計。一星期由 5,203 升到 16,793 stars，係 2026-W45 hot list 第二名，亦係 dsh 生態連續第三個星期入選。

## Key facts

- **What**: an Android app (Flutter/Dart) for DeepSeek Harness: on-device runtime (Ubuntu + Node.js + DSH installed from the app, PRoot startup, no root) or remote hosts over SSH / DSHarness Remote. Chat and web interfaces, model switching, images, voice, tool approvals, plugin UI (SDK and examples in the repo), optional phone control (read screen, tap, type) with Accessibility permissions.
- **Install**: Android 8.0+; download the arm64 APK from GitHub Releases or go.dshtui.com/download, choose an on-device runtime or a remote host, configure a model and credentials. Build from source: `bash tooling/setup-toolchain.sh`, `bash runtime/build-runtime.sh arm64-v8a`, `bash tooling/build-apk.sh -f arm64`.
- **Caveats** (README): unofficial, not affiliated with DeepSeek; anonymous usage statistics on by default (Settings → Privacy and sharing); phone-control tasks may send screen text or screenshots to the model. AGPL-3.0 (`sdk/` and `examples/` MIT).
- **Numbers**: 16,793 stars / 723 forks on 2026-11-09, created 2026-10-25; 5,203 in the 2026-11-02 snapshot, so **+11,582 in 7 days**. Clears the gain gate (3,000) and the new-repo gate (10,000).
- **X**: Chinese-language posts about the dsh "全家桶" mention it, but none was verified above the X gate (see the report's 方法 for the fxtwitter budget).

## 點解值得留意

- 2026-W45 hot list 第二名（heat 0.80，GitHub 單平台），詳見 [[hot-list/2026-W45|hot-list/2026-W45]]。
- 「coding agent 喺手機上跑、或者用手機遙控屋企部機」係 agent 用法嘅新方向；同 W44 嘅 Mika、今個星期 DIYgod/pinky 一樣係「agent 用手機」呢條線。
- 權限好大（無障礙 + 本機 shell），裝之前要讀佢嘅風險段落，唔好俾佢無人看管做不可逆嘅嘢。

## Source

- https://github.com/ccch1mneyyy/dsh-Go — ccch1mneyyy — created 2026-10-25
- Reader: raw.githubusercontent.com README.en.md (curl), GitHub search API (`gh api`) for counts. Raw text in `raw/20261109-dsh-go-android-client-for-deepseek-harness.md`.

## Related

- [[hot-list/2026-W45]]
- [[pages/20261026-deepseek-harness-everything-is-a-plugin]]: the harness it runs (W43 winner)
- [[pages/20261102-dsh-superagent-proactive-coding-agent]]: another dsh bundle (W44 winner)
