---
slug: 20261002-claude-mods-overview-hooks-state
source_url: "https://www.facebook.com/638368594/posts/10163494558868595"
canonical_id: "facebook:10163494558868595"
fetched_at: "2026-10-02T09:10:00Z"
reader: "exa"
---
{"author": "Sean Liu", "published": "2026-10-02T08:06:00Z", "platform": "facebook", "page_id": "638368594", "post_id": "10163494558868595", "note": "final paragraph truncated by Exa — ends mid-sentence at 'Claude 的工具禁止規則，'"}

## Post by Sean Liu — 2026-10-02 08:06 UTC

稍稍的玩了一下 Claude Mods，以下略懂的說一些。

Claude Mods 是 Claude Code 的程式擴充功能。開發者可以用 JavaScript 或 TypeScript 改變 Claude Code 的執行流程與操作介面。Mod 可以處理提示詞、工具呼叫、模型請求與回傳結果。Anthropic 已於 2026 年 10 月 1 日發布這項功能。

Mod、Skill 與 MCP 各有不同用途。Skill 提供任務指引。MCP 提供外部工具與資料存取。Mod 直接參與 Claude Code 的事件處理，也可以繪製操作介面。Plugin 是安裝與分發單位，可以同時包含這些元件。

Mod 透過 function hooks 處理事件。Claude Code 發出事件後，會呼叫已註冊的函式。函式可以觀察事件、修改事件，或直接回傳結果。函式也可以透過 `next`，把事件交給下一個處理器。事件資料經過凍結，因此修改時需要建立副本。

多個 Mods 可以處理同一個事件。它們形成一條處理鏈。外層 Mod 先取得輸入，並在內層完成後取得結果。外層 Mod 也可以阻止後續處理。因此，政策檢查、個資處理與日誌記錄的順序，會影響系統行為。

Mods API 使用 `$` 作為介面。Mod 透過這個介面讀寫檔案、啟動程序、發出網路請求或呼叫模型。每次 API 呼叫本身也是事件。更外層的 Mod 可以觀察、修改或拒絕這些呼叫。這讓企業可以用程式限制其他 Mods 的操作。

Mods 可以協助管理模型的上下文。例如，Mod 可以在適當事件取得專案資料，或處理工具回傳的內容。它也可以記錄每次模型請求的用量。這些能力適合用於資料檢索、來源標示與執行紀錄。實際效果仍需要透過任務評測確認。

Mod 的狀態有不同保存期限。模組變數會在重新載入後重設。`$.state` 可以保留 Session 狀態，並支援介面自動更新。`$.store` 可以跨 Session 保存 Plugin 的 JSON 資料。開發者需要依資料用途選擇保存方式。

Mods 的權限需要另外檢查。Mod 可以使用執行者的權限操作檔案與程序。Claude 的工具禁止規則，[truncated — Exa did not return the remainder of the post]
