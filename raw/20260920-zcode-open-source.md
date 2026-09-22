---
slug: 20260920-zcode-open-source
source_url: "https://github.com/zai-org/ZCode"
canonical_id: "github:zai-org/ZCode"
fetched_at: "2026-09-22T01:15:53Z"
reader: "github-connector+exa"
---

## Repo metadata (mcp__github__search_repositories, fetched 2026-09-22T01:15:53Z)

```json
{
  "full_name": "zai-org/ZCode",
  "description": "Z.ai's coding agent harness. Powerful, intelligent, extensible.",
  "homepage": "https://zcode.z.ai/",
  "created_at": "2026-09-20T12:01:16Z",
  "pushed_at": "2026-09-21T00:02:36Z",
  "language": "TypeScript",
  "license": "Apache-2.0",
  "stargazers_count": 5633,
  "forks_count": 1609,
  "open_issues_count": 11,
  "html_url": "https://github.com/zai-org/ZCode"
}
```

## README.md (raw.githubusercontent.com, main branch)

# ZCode

ZCode 是 AI 编程工作台，提供桌面应用、浏览器界面和终端 Agent。本仓库包含客户端、后端服务、共享 UI，以及 Agent CLI 与运行时源码。

| 入口 | 用途 | 开发命令 |
| -------------------- | -------------------------------------------------------------- | ------------------------------ |
| Desktop | Electron 桌面应用 | `pnpm dev:desktop` |
| Web / ZCode 命令行版 | 终端与浏览器工作台；将 TUI、Web、后端和 Agent 组装为独立运行包 | `pnpm dev:web` |
| Agent CLI | 在终端中使用 `zcode`，也为 Desktop 和 Web 提供 Agent 运行时 | `pnpm --filter @zcode/cli dev` |

安装命令行版（发行包）：
```bash
zcode          # 默认进入终端交互界面
zcode --web    # 启动 Web 界面
```

开发环境需要 Git、Node.js 24.14.0、pnpm 10.33.2；`pnpm bootstrap` 安装依赖并准备桌面本地运行资源。

仓库结构：packages/desktop（Electron）、packages/web、packages/server（HTTP/WebSocket）、packages/zcode-server-cli、packages/ui、packages/services、packages/shared|rpc|client、packages/provider(-node)、apps/zcode-cli（Agent CLI/TUI/运行时）。

功能与优惠范围、维护规则、执行与数据风险、许可与第三方版权说明见 NOTICE.md。

## NOTICE.md excerpt (the candid disclosure document referenced by press coverage)

> 共享运行配置默认采用 `build` 权限模式；独立 CLI 通过 `--prompt` 执行非交互任务时，未指定 `--mode` 会采用 `yolo`。... 当前共享 Agent 执行适配器不提供默认的操作系统沙箱。
>
> Computer Use：本仓库随附的 Computer Use 包为不可用占位实现，调用会返回不可用错误，不提供系统截图或操作能力。
>
> 官方 Coding Plan 模型网关转发：当前对代码列出的两个官方 Anthropic 兼容模型端点按协议、主机、有效端口和路径匹配；命中时自动改发 ZCode 网关，保留请求方法、正文、查询参数及除 Host 外的请求头，包括请求中的认证信息。

(Full NOTICE.md runs to many more sections on MCP/OAuth, session sharing, local data paths, updates. Fetched via raw.githubusercontent.com/zai-org/ZCode/main/NOTICE.md, truncated at 8000 chars for this capture.)

## Press context (for the 摘要, not verbatim source — see wiki page ## Source for links)

- Z.ai's ZCode was found on 2026-09-18 (developer "ferstar") silently uploading full local workspaces, including `.git` history (86.6% of a reported 345MB/42,411-file archive), to Alibaba Cloud OSS.
- Z.ai apologized 2026-09-18 (17:44 China time), attributing it to a codebase-indexing feature (session recovery / version rollback / auto Repo Wiki generation) and said it had fixed the behaviour.
- Z.ai open-sourced the entire ZCode workbench (desktop + web + terminal agent + backend/runtime) under Apache-2.0 on 2026-09-20/21, three days after the apology.
- First-day metrics reported by multiple outlets: ~5,368-5,633 stars, ~1,539-1,609 forks (~28-29% fork ratio, unusually high).
- Context: Anthropic cut Claude Code weekly limits 17% on 2026-09-14; Z.ai ran a GLM Coding Plan unlimited-usage promo through 2026-09-20, with the open-source commit landing on the promo's last day.
