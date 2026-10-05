---
slug: 20260928-claude-opus-5-5-tutorial-animation-prompt
source_url: "https://www.threads.com/@pin._.wen/post/Dd0VbUxDRZv"
canonical_id: "threads:Dd0VbUxDRZv"
fetched_at: "2026-10-04T20:59:47Z"
reader: "jina"
---
{"author": "@pin._.wen", "author_name": "張品妏", "platform": "threads", "published": "2026-09-28", "engagement": {"likes": "1.5K", "replies": 59, "reposts": 277, "shares": "2K"}, "engagement_order": "likes, replies, reposts, shares inferred from Threads UI", "post_url": "https://www.threads.com/@pin._.wen/post/Dd0VbUxDRZv", "share_url": "https://www.threads.com/share/BAdRbSMGiN/", "attached_media": "1 video (cover frame only; video not watched)", "replies_source": "author replies read from the embedded JSON of the share-page HTML (fetched 2026-10-04T20:58:52Z); the post text and counts are from the Jina markdown of the canonical post URL"}

Post 1 — @pin._.wen (https://www.threads.com/@pin._.wen/post/Dd0VbUxDRZv):

沒時間研究，所以直接請claude生成一個教學影片給我，對懶得看文章的人好有幫助，太厲害了！ Prompt 放留言~~

[attached media: video cover frame]

1.5K

59

277

2K

Post 2 — @pin._.wen reply (https://www.threads.com/@pin._.wen/post/Dd0WbNdGV6q):

請幫我上網研究大家怎麼用 Claude Opus 5.5 製作動畫，整理成一套清楚的操作流程，再用這套流程親手做一部「如何用 Opus 5.5 做動畫」的教學動畫。
第一階段：資料收集

1. 搜尋範圍：YouTube 教學影片（可讀字幕或說明欄）、X/Twitter、Reddit（r/ClaudeAI 等）、個人部落格、Medium、GitHub 範例專案，以及 Anthropic 官方文件。
2. 關鍵字用中英文都搜，例如：「Claude Opus 5.5 animation」「Claude 做動畫」「Claude Remotion」「Claude Manim」「Claude SVG animation」「Claude HTML animation prompt」「Claude artifact animation」。
3. 以最近三月內的資料為主，至少參考 【10】 個以上不同來源。
4. 每個來源記下：作者、網址、用的工具或技術、他們的提示詞寫法、遇到的問題和解法。

Post 3 — @pin._.wen reply (https://www.threads.com/@pin._.wen/post/Dd0WedGmfxO):

第二階段：整理分析

1. 先分類大家的做法。我不確定是用動畫工具還是寫程式碼，請幫我釐清，可能包括：
 * 程式碼類：HTML/CSS/JS、SVG、Canvas、GSAP、Three.js、Remotion（React 影片）、Manim（Python 數學動畫）、Motion Canvas 等
 * 工具搭配類：Claude 寫腳本或分鏡，再交給其他動畫或影片工具
2. 比較各做法的難易度、適合對象、成品效果和優缺點，做成表格。
3. 歸納出一套「新手也能照做」的標準流程，例如：構想 → 寫腳本/分鏡 → 下提示詞 → 生成程式碼 → 預覽修改 → 匯出影片。每一步都附上實際可用的提示詞範例。
4. 列出大神們共同提到的技巧，以及常見的錯誤。

Post 4 — @pin._.wen reply (https://www.threads.com/@pin._.wen/post/Dd0Wm94GWU0):

第三階段：製作教學動畫

1. 內容：用動畫呈現第二階段整理出的流程，讓沒有經驗的人看完就知道怎麼開始。
2. 長度：約 【2-4】 分鐘，分成 【5–7】 個段落（開場 → 各步驟 → 小技巧 → 結尾總結）。
3. 風格由你決定，以清楚易懂為最高原則。可以是扁平插畫、資訊圖表或簡約動態文字，配色統一、畫面不要太雜。
4. 語言：畫面文字用繁體中文，專有名詞保留英文。
5. 製作方式：請採用你研究後認為最適合的方法，最好就是教學裡介紹的方法，讓這部動畫本身也是示範。
6. 動畫要能自動播放，也要有暫停、上一段、下一段的控制。

第四階段：交付內容

1. 一份研究報告，包含來源列表（附連結）、做法比較表和標準流程。
2. 分鏡腳本：每一段的畫面描述、文字、秒數。
3. 成品動畫：可直接播放的網頁版。如果做得到，也請附上 MP4 或匯出影片的方法。
4. 完整原始碼和使用說明，讓我之後能自己修改。

注意事項

* 如果某些資訊查不到或不確定，請直接說明，不要編造。
* 開始製作動畫前，先把第二階段的流程和分鏡給我確認。

Reply — @lojomate (not the post author; https://www.threads.com/@lojomate/post/Dd1O0slDL7T), shown in the thread:

Claude Code 是原生可以生成影片嗎？？
還是接駁其他影片MCP生成？

Post 5 — @pin._.wen reply (https://www.threads.com/@pin._.wen/post/Dd1PBjJGRBm), answering the question above:

沒有串mcp喔～

Reply — @lojomate (not the post author; https://www.threads.com/@lojomate/post/Dd1UMOtDBoJ), shown in the thread:

所以直接原生可以生成影片嗎？
還是用Claude Code 操作剪片軟件？

Post 6 — @pin._.wen reply (https://www.threads.com/@pin._.wen/post/Dd1VxFMmZbY), answering the question above:

可以直接生成喔，我就是直接貼這些prompt給Claude code生成的，沒有用到其他的軟體

其實這些prompt也是Claude幫我生成的，我實際只有跟他說：

我想要這樣詢問ai
你幫我上網收集大家使用 opus 5.5 製作動畫的教學，也可以看youtube，然後整理出一份他們的使用流程方法，我不確定他們是用動畫還是用寫程式碼的方式，總之參考網路大神的方法，幫我做出一部如何做的教學動畫，風格你自訂清楚表達就好
你幫我整理出更完整的提示詞
