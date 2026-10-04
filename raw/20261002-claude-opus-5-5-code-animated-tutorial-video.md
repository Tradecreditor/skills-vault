---
slug: 20261002-claude-opus-5-5-code-animated-tutorial-video
source_url: "https://www.facebook.com/share/v/19JqXuVvpu/"
canonical_id: "url:02aa64ff45ac1d2e3affc4b08ddbee5335137894"
fetched_at: "2026-10-04T21:20:08Z"
reader: "jina+supadata"
---
```json
{"author": "數位敘事力期刊（Journal of Digital Narrative）", "page_id": "61567617167509", "date": "not shown", "reactions": 299, "comments": 12, "shares": 134, "counts_note": "299/12/134 are three unlabeled numbers on the Jina page; order inferred as reactions/comments/shares from the Facebook UI. Title line says \"41K views · 299 reactions\".", "views": "41K (title); 41596 (Supadata metadata)", "supadata_metadata": {"video_id": "1060838723457433", "resolved_url": "https://www.facebook.com/Journal.of.Digital.Narrative/videos/1060838723457433/", "duration_seconds": 468, "views": 41596, "likes": 300, "comments": 12, "shares": null}, "supadata_transcript": "obtained on a single retry by the main session on 2026-10-04 (lang zh, mode=auto); verbatim in the transcript section at the end of this file", "share_url": "https://www.facebook.com/share/v/19JqXuVvpu/"}
```

Caption (as shown in the page title line):

【我請 Claude Opus 5.5 做了程式動畫的教學影片🙀】 by #數位敘事力期刊

網路上不少人製作了各類Opus 5.5做出來的程式代碼動畫，但主編覺得沒能讓大家理解底層邏輯，蠻可惜的，所以我乾脆請Opus 5.5自己做了動畫呈現這個概念......結果超級棒的🤣，這邊摘要這部影片的重點：

1️⃣ #模型選擇 對於動畫生成結果的影響
2️⃣ #程式代碼 畫出高品質動畫的邏輯
3️⃣ #資產資源 對畫出影片的影響（可以直接請Claude去抓）
4️⃣ #提示技巧 什麼樣的提示詞才能產出最佳效果
5️⃣ #影片產出 Loop涵蓋哪些細節流程

簡單來說，這類影片從某方面來說，就是Agent階段成果體現，從多模態模型，Coding底層邏輯，將剪輯邏輯跟提示詞指令結合，到最後如何讓AI完成產出結果的自動核檢驗，我相信很多人好奇的兩個問題：免費能不能做？需要使用哪些資源？

1️⃣ 基本上做不出來（這一部影片直接消耗掉我一週4%的用量😅）
2️⃣ 除了Claude token，還加上了Hyperframes的skill、Eleven Labs的語音
（Eleven Labs 生完這一部影片，一個月的免費用量就消耗掉一半了🤣）

以上詳細歷程，如果需要我的指令，我的鷹架在留言區，如果覺得這個實在很棒的話，幫我按讚、大力分享出去唷❤️

## Transcript (supadata)

lang zh, mode=auto, fetched 2026-10-04 by the main session on a single retry; text kept exactly as returned, including the ASR's character spacing and Simplified script.

你 现在 看到 的 这 支 影片 没有 打 开 任 何 一 套 剪 辑 软 体 每 一个 画 面 每 一 行 字 幕 甚 至 你 正 在 听 的 这个 声 音 全部 都是 用 程 式 码 产 生 的 今天 我们 就 把 这 条 产 线 从 头 到 尾 拆 开 来 看 第一 个 问题 要 用 哪 个 模 型? 如果 你要 从 零 做 一 整 支 教 学 动 画, 需要 规 划 分 镜 同 时 管 很多 个 场 景, 还 要 自己 检 查 画 面 有 没有 出 错 主 力 选 O pus 5. 5。 它 擅 长 长 时间 多 步 骤 的 复 杂 任 务。 如果 只是 日 常 微 调 例 如 改 颜 色, 调 一 段 转 场 S on et 5 又 快 又 省 至 于 批 次 修 改 字 幕, 替 换 100 个 单 名 这 种 小 事 交 给 Ha iku 4. 5 就 够 了 简 单 记, 动 画 越 复 杂 要 迭 代 的 步 骤 越 多 就 往 越 大的 模 型 靠 但是 等一下, 语 言 模 型 又 不会 画 画 它 怎么 做 得 出 动 画 关 键 在 于 刻 的 不 画 图, 它 写 的是 描 述 关 键 在 于 刻 的 不 画 图 一 支 影片, 其实 就是 很多 张 图 快 速 播 放 每 秒 30 张 每 一 张 长 什么 样 子, 只 取 决 于 一 件 事 现在 是 第 几 秒 所以, 我们 可以 把 影片 写 成 一个 函 数 给 它 时间 踢 它 就 回 传 这 一 格 的 画 面 这 种 写 法 叫 做 宣 告 式 动 画 你 用 H T ML、 C SS 和 GS AP 或 是 Re act 的 Rem otion 数 学 动 画 用 的 Man ning 去 描 述 在 第 几 秒 哪 个 东 西 移 动 到 哪 里 接 下 来 浏 览 器 负 责 把 每 一 格 画 出来 程 式 逐 格 截 图 最 后 交 给 FF M MP G 扎 成 影片 而 写 文 字 描 述 这 件 事 正 好 是 语 言 模 型 最 擅 长 的 很多 人 一 开始 就 叫 Cloud 帮 我 做 一 支 动 画 结 果 每 次 出来 的 都 不 一 样 比 较 稳 定 的 做 法 是 先 让 他 产 出 一 份 分 镜 表 而且 用 Jason 这 种 结 构 画 格 式 而且 用 Jason 这 种 结 构 化 格 式 每 一 幕 只 要 写 清楚 四 件 事 念 什么 旁 白 画 面 想 表 达 什么 要 演 几 秒 以及 跟 上 一 幕 怎么 接 有 了 这 份 蓝 图 后 面 的 画 面、 配 音、 字 幕 全部 都 照 着 同 一 份 资 料 走 不会 各 做 各 得 那 提 示 词 到底 要 怎么 写 我们 直接 比 较 左 边 只 写 一 句 帮 我 做 一 支 介 绍 AI 的 动 画 右 边 用 完 整 框 架 差 别 一 眼 就 看 得 出来 这个 框 架 有 八 个 参 数 第一, 角 色 与 观 众 影片 给 谁 看 决 定 语 气 和 声 显 第二, 成 品 规 格 每 秒 几 格, 总 长 几 秒 写 死 它 才 不会 出 现 奇怪 的 尺 寸 第三, 设 计 系 统 色 票, 字 形, 兼 具 风 格 才 会 前 后 一 致 第 四, 分 镜 Jason 就是 刚 刚 那 份 蓝 图 第 五 动 画 与 绘 用 什么 缓 动 曲 线 怎么 转 场, 节 奏 快 还是 慢 这 决 定 质 感 怎么 转 转 第 六, 技 术 约 束 指 定 用 哪 个 引 擎 并 且 禁 止 随 机 数 和 及 时 时间 确 保 每 次 渲 染 结 果 都 一 样 第 七 素 材 规 则 素 材 从 哪 里 来 授 权 是 什么, 截 图 要 多 大 第 八 验 收 标 准 要 求 他 自己 截 图 检 查 有 没有 字 跑 出 框 有 没有 对 齐 中 文 有 没有 变 成 方 块 最 后 记 住 一 句 话 形 容 词 不 如 数 字 与 其 说 动 画 要 流 畅 一点 不 如 直接 说 0. 6 秒 E ase out 有 了 提 示 词 C ode 开始 写 画 面 有 了 提 示 词 但 真 正 让 品 质 拉 开 差 距 的是 这个 回 圈 写 完 程 式 渲 染 出 预 览, 截 图 再 让 C ode 自己 看 这 张 图 他 会 发 现, 这里 的 字 超 出 框 了 这 两 个 元 素 没有 对 齐 然后 自己 修 正 再 跑 一次 这 就是 为什么 我们 在 提 示 词 里 要 写 验 收 标 准 你 给 它 看 得 见 的 标 准 它 才 收 得 到 位 接 下 来 是 声 音 你有 没有 想 过 为什么 有 些 AI 配 音 一 听 就是 机 器 语 音 合 成 其实 分 成 三 步 文 字 转 成 音 律 再 转 成 声 音 机 械 感 多 半 不是 音 色 的 问题 而 是 应 律 太 平。 而 是 音 律 台 没有 高 低 起 伏, 也 没有 该 有 的 停 顿 和 呼 吸。 所以, 要 让 声 音 自 然 有 三 个 方 法。 第一, 选 择 能 理 解 语 气 的 模 型, 像 这 支 影片 用 的 E le ven L apse。 第二, 用 标 点 点 和 停 顿 标 秋 控 制 断 句。 第三, 加 上 情 绪 提 示, 告诉 他, 第三, 加 上 情 绪 提 示 告诉 他 这 句 是 疑 问 是 强 调, 还是 轻 声 带 过 你 现在 听 到 的, 就是 这样 调 出来 的 声 音 很多 人 以 为 Wh is per 是 用 来 配 音 的 其实 刚 好 相 反 它 是 把 声 音 转 回 文 字 的 听 写 员 在 这 条 产 线 里 我们 用 它 做 一 件 很 精 准 的 事 找 出 每 一个 字 是 在 第 几 毫 秒 念 出来 的 有 了 这 些 时间 戳 字 幕 就 能 一个 字 一个 字 跟 着 声 音 走 画 面 上 的 动 画 也 能 刚 好 在 念 到 关 键 字 的 那 一 刻 出 现 这 就是 音 画 同 步 的 秘 密 最 后 把 整 条 线 串 起 来 选 对 模 型, 用 八 个 参 数 写 提 示 词 先 铲 出 分 镜, 再 生 成 画 面 并 自 我 修 正, 接 着 配 音, 对 齐 字 幕, 最 后 渲 染 成 影片。 选 对 模 型 用 八 个 参 数 写 工 具 会 一直 换 但 这 套 逻 辑 不会 变。 提 示 词 模 板 放 在 说 明 栏 换 你 动 手 试 试 看。 优 优 独 播 剧 场 —— Yo Yo Tele vision Series Exc lusive
