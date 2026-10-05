---
slug: 20260928-agent-patterns-andrew-ng-4-anthropic-5-workflows
source_url: "https://www.threads.com/@mini_littlechanges/post/Dd1Qo5hE6JY"
canonical_id: "threads:Dd1Qo5hE6JY"
fetched_at: "2026-10-04T21:00:04Z"
reader: "jina"
---
{"author": "@mini_littlechanges", "author_name": "艾米莉 Mini 醬", "platform": "threads", "published": "2026-09-28", "published_from": "6d at fetch time 2026-10-04", "topic_tag": "agentic-patterns", "engagement": {"likes": 423, "replies": 10, "reposts": 41, "shares": 488, "views": "45.5K"}, "engagement_order": "likes, replies, reposts, shares inferred from Threads UI; the views line is shown separately", "post_url": "https://www.threads.com/@mini_littlechanges/post/Dd1Qo5hE6JY", "share_url": "https://www.threads.com/share/_xIBQNZnn/", "attached_media": "6-image carousel (images not read)"}

Post 1 — @mini_littlechanges (https://www.threads.com/@mini_littlechanges/post/Dd1Qo5hE6JY):

知名 AI 大師 Andrew Ng 之前做過一個超驚人嘅實驗：佢用一隻舊款 GPT，完全冇改過 model 本身，淨係幫佢改咗做嘢嘅流程，分數竟然由 48 分暴升到 95 分！直接跑贏當時最新、最強嘅 一model！佢歸納咗 4 個最核心嘅 Agent 模式：

1️⃣ Reflection（叫佢自己 Check 返自己寫嘅嘢） 2️⃣ Tool use（俾工具佢真係去操作） 3️⃣ Planning（先拆解步驟，再一步步做） 4️⃣ Multi-agent（分不同角色一齊協作）

加上 Anthropic 喺《Building Effective Agents》又整理咗 5 個超實用 Workflow：Prompt chaining、Routing、Parallelization、Orchestrator-workers 同埋 Evaluator-optimizer。

🛠️ 基本上，而家市面上大部分真正行得通嘅 AI Agent，底層其實就係呢 9 招！

[attached media: 6 images (carousel), not read]

423

10

41

488

45.5K views

The login-shell page also lists replies by other accounts. No reply could be identified as written by the post author. Replies as rendered by Jina, handle = the name shown in the reply header (not the post author):

Reply — @tszho_astrophotography:

Exactly 👍

Reply — @hackertale:

👏🏻👏🏻

Reply — @hk1989:

但佢都有講咁樣會燒token, 要計好數先得

Reply — @nikiforovviktor:

這其實就是後訓

Reply — @lok_uni:

其實近期做workflow都有試用反思流（Refelection)，佢唔係叫LLM自己check返自己做嘅野，其實係3個LLM

1) LLM 生成首個「初稿」結果 2）一個獨立嘅critic用某些標準去評核初稿，可以用同一個LLM, 可以用較平較快嘅LLM 3）最後再由LLM利用「Critic」嘅觀點，去決定修唔修正「初稿」，只能用「Critic」嘅觀點去修改

3個LLM各有分工，當中有好多設置同微調，依家落UAT每日玩自己同LLM玩改code/改prompt

Reply — @bubumomo12:

所以, model 其實沒進步過?

Reply — @brandon0513:

這篇整理得太強了 身為工程師對這 9 招很有感 最近也在研究怎麼把這些 Workflow 導入開發流程 感謝分享這麼紮實的內容

Reply — @hugo_on99.pv:

Bro discovered CoT all over again.....

Reply — @marukomurin:

AGI一句搞掂
