---
title: "Back up agent workflows as Skill-format zips (Grokbot / Claude)"
slug: 20261003-backup-agent-workflows-as-skill-zips
type: post
status: draft
source_url: "https://www.threads.com/@rico.ai.solo/post/DeBUAFsH310"
source_platform: threads
author: "@rico.ai.solo"
published: "2026-10-03"
captured_at: "2026-10-04T21:10:23Z"
captured_by: "claude-code-cloud"
canonical_id: "threads:DeBUAFsH310"
engagement: "likes=37 reposts=3 shares=49 views=4.5K"
tags: [topic/knowledge-mgmt, agent-skills, backup, workflow, skill-md, github]
related: [stars/vercel-labs--skills, 20260930-ui-ux-pro-max]
needs_manual_text: false
---

## 摘要

MC Chan（@rico.ai.solo）提醒用 Grokbot 或 Claude 嘅人，要備份自己已經建立好嘅 workflow，咁遇到突發情況就可以隨時抽身、轉用其他 agent。佢嘅做法分四步：先揀最常用同工作量最大嘅流程（簡單流程新 agent 好容易重做，唔使打包）；再叫 Agent 用 Skill 格式將流程打包成 Zip，用 Skill.md 寫清楚流程，並將 Python 等程式碼放入 script folder。之後可以將 zip 傳去 Google Drive，或者技術性啲就將更新全部推上 GitHub。作者自己會盡量將流程變成 Python script，令 AI 輸出穩定，打包備份亦更簡單，但佢話呢個方向比較適合技術型玩家。

## Key facts

- Advice (author): back up the workflows you built on Grokbot or Claude so you can leave quickly in an emergency (「隨時在突發情況抽身離開」). The post names no specific incident.
- **Step 1**: identify the most-used flows and the heaviest-workload flows. Simple flows are easy for a new agent to rebuild, so they need no special packaging.
- **Step 2**: ask your agent to package each flow as a Zip in Skill format. Use `Skill.md` (the author's spelling) to describe the whole flow clearly, and put the related code (e.g. Python scripts) into a script folder inside the package.
- **Step 3**: upload the zip to Google Drive, or, the more technical route, skip the zip and push all updates to GitHub.
- **Step 4**: the author converts as many flows as possible into Python scripts, for two reasons he gives: code lets you control the AI's output so results stay stable day to day, and packaging and backup become simpler and clearer. He says this direction suits technical users.
- No commands, tool names, repo links or template are given; the only layout detail is a Skill.md plus a script folder in a zip.
- The author's "Skill format" matches the Agent Skills layout this vault uses (`SKILL.md` plus `scripts/`); that match is this vault's reading, not stated in the post.
- Engagement: 37 likes, 3 reposts, 49 shares, 4.5K views. The reply count was not shown (blank in the page).

## 點解值得留意

- **同呢個 vault 做法一致**：流程寫成 SKILL.md 加 scripts/，再用 GitHub 備份，正正係 Josep 現時嘅玩法；可以用嚟向客戶解釋「點樣避免被單一 AI 平台綁死」。
- **SME 交付項目**：幫香港中小企建立 agent workflow 時，交付包可以連同 Skill 格式備份（Google Drive zip 或 GitHub repo），減低平台鎖定同賬戶被封嘅風險。
- **穩定性策略**：將重複流程轉成 Python script，令 AI 只做少數判斷，輸出更可預測；同 skills 內 `scripts/` 嘅用法一致。
- **安全提醒（帖中冇提）**：打包同上傳前要確認 zip 或 repo 入面冇夾帶 API key、cookie 或客戶資料。

## Source

- Post: https://www.threads.com/@rico.ai.solo/post/DeBUAFsH310
- Author: @rico.ai.solo (MC Chan) · Published: 2026-10-03
- Engagement: likes=37 reposts=3 shares=49 views=4.5K
- Counts: read from the labeled Like / Comment / Repost / Share row of the share-page HTML, because Jina's markdown carried no counts for this post; the Comment count was blank, so replies is omitted
- Reader: jina (share link resolved via r.jina.ai; counts order inferred from Threads UI)
- Share URL: https://www.threads.com/share/BBJKrxZo07/
- Not captured: a separate later post by the same author (DeBnCOvH8wb, shown under "Related threads") about asking Grokbot to back up a workflow to GitHub; other "Related threads"

## Related

- [[../stars/vercel-labs--skills|skills]] — `npx skills add` CLI for installing Agent Skills from GitHub; the install side of a GitHub-backed skill backup
- [[../pages/20260930-ui-ux-pro-max|UI UX Pro Max]] — an example of a Skill-format repo distributed through GitHub
