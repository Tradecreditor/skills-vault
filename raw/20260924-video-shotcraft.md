---
slug: 20260924-video-shotcraft
source_url: "https://facebook.com/share/p/19YgQuaaCb"
canonical_id: "url:e14ea4c61b6c92d7ea867765b3445de350d9d62f"
fetched_at: "2026-09-27T00:00:00Z"
reader: "jina"
---
{"author": "Brian Jhang", "group": "AI 生活運用｜Brian Jhang's Edge 社群", "published": "2026-09-24", "engagement": "likes=34 comments=2 shares=27", "github_project": "https://github.com/Vincentwei1021/video-shotcraft", "github_stars": 9308, "github_forks": 847}

很多 AI 產品影片看起來像「會動的簡報」，不是模型不夠強，而是它根本沒有學過鏡頭語言。

AI Agent 影片工具分享 Day 5，我想介紹 Video Shotcraft。

它不是新的影片生成模型，也不是輸入一句話就自動成片的網站。它是一套建立在 Remotion 上的 Agent Skill，讓 Claude Code、Codex 不只會寫動畫程式碼，也知道應該選什麼鏡頭、停多久、在哪一幀加入聲音，以及完成後要怎麼驗收。

官方目前整理了 157 張鏡頭配方卡、214 種樣式與 214 段動態預覽。真正有價值的不是數量，而是每張卡片都包含用途、節奏、建議時長、參數、常見問題，以及已經調校過的 TSX 實作。

它的流程也不是叫 Agent 直接開始加特效，而是先理解產品與受眾，再決定視覺方向，把每項功能對應到適合的鏡頭，完成分鏡後才擷取真實產品畫面、逐鏡頭製作、設計聲音並進行終檢。

例如它會要求一個鏡頭只表達一個主要動作、重要資訊要留下閱讀時間、既有介面優先使用真實截圖，而不是讓 AI 隨手重畫；每個鏡頭還要輸出指定影格檢查，修改後重新渲染整片。

這也是我覺得這個專案最值得研究的地方：

AI 會做動畫，只解決了「能不能做」；把鏡頭語言、節奏和驗收標準變成 Agent 可以執行的規則，才開始解決「做得像不像專業作品」。

成片之後，還能在瀏覽器工作台調整鏡頭順序、長度、速度和部分樣式，或匯出到剪映繼續處理。但它不是 CapCut 或 Premiere 的完整替代品，也不適合直接拿來剪口播、紀錄片或長篇敘事影片。它最適合的是 SaaS、網頁與桌面產品的功能展示、發布影片和宣傳短片。

另外有三點要注意：專案本身採 Apache-2.0，但底層 Remotion 有獨立授權；內附部分音樂、音效的來源需要在商用前重新確認；官方所說的八輪逐幀審查是作者自己的製作流程，不是適用所有模型與專案的獨立 Benchmark。

截至 2026 年 9 月 24 日，專案在 GitHub 已有 9,308 Stars、847 Forks，而且今天仍有更新。

如果你正在用 Claude Code、Codex 或自己的 AI Agent 製作產品影片，這個專案值得收藏。不要只讓 Agent 學會產生畫面，也要讓它學會怎麼選擇、取捨與驗收。

Comments:
- Neil Hung: 謝謝分享
- Brian Jhang (Admin): Video Shotcraft：https://github.com/Vincentwei1021/video-shotcraft
