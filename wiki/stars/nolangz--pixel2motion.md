---
title: "pixel2motion"
slug: nolangz--pixel2motion
type: repo
status: draft
source_url: "https://github.com/nolangz/pixel2motion"
source_platform: github
author: "Nolan Z"
published: "2026-06-12"
captured_at: "2026-09-20T00:00:00Z"
captured_by: "routine:github-stars-sync"
canonical_id: "github:nolangz/pixel2motion"
engagement: "stars=2303 forks=192"
tags: [logo-animation, svg-animation, ai-design-tools, motion-design, claude-skill]
related: [motion-canvas--motion-canvas, greensock--gsap-skills, LottieFiles--motion-design-skill, Forget-C--Jellyfish]
needs_manual_text: false
---

## 摘要
將點陣 logo（PNG／JPG／WebP／截圖）轉成乾淨嘅 SVG，再喺上面編排動畫，最後輸出一個可互動嘅 HTML 展示頁。關鍵係佢分兩段：先擬合出一個經過 QA 驗證嘅靜態向量，用疊圖逐次對比原圖，檢查標誌比例、圓點位置、文字基線同筆畫粗幼，確認之後先至開始做動態。IoU 只當診斷指標，平滑度同結構先係硬門檻——一個 IoU 高但邊緣鋸齒嘅描繪會被否決，寧要複雜度低而平滑嘅版本。交付物包括 logo.svg、motion.css、獨立可跑嘅 logo_motion.html、動態說明 motion_spec.md，同一批 QA 截圖做憑證。
## Key facts
- Language: Python
- License: MIT
- Created: 2026-06-12
- Last pushed: 2026-08-21
- Stars: 2,303
- Forks: 192
- Homepage: https://nolangz.github.io/pixel2motion/
- Focus: Logo animation, SVG generation, motion design

## 點解值得留意
大部分向量化工具淨係追求貼近原圖，結果係一堆改唔郁嘅路徑。呢個輸出嘅 SVG 將標誌、圓點、文字拆成可個別定址嘅部件，所以動畫先至編排得到——呢個結構化嘅要求，正正係 AI 生成向量圖最容易失手嘅地方。
## Source
GitHub repository: https://github.com/nolangz/pixel2motion
Author: Nolan Z
Captured: 2026-09-20

## Related

- [[motion-canvas--motion-canvas|Motion Canvas]] — 兩者都用程式碼精確控制動畫時序。
- [[greensock--gsap-skills|gsap-skills]] — 都係將動畫設計知識包裝做 agent skill。
- [[LottieFiles--motion-design-skill|motion-design-skill]] — 都係俾 agent 用嘅動作設計原則同工具包。
- [[Forget-C--Jellyfish|Jellyfish]] — 都強調將生成資產拆做可獨立管理嘅部件，減少走樣。
