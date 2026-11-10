---
title: "OpenSandbox"
slug: opensandbox-group--OpenSandbox
type: repo
status: draft
source_url: "https://github.com/opensandbox-group/OpenSandbox"
source_platform: github
author: "opensandbox-group"
published: "2025-12-17"
captured_at: "2026-11-10T06:06:37Z"
captured_by: "routine:github-stars-sync"
canonical_id: "github:opensandbox-group/OpenSandbox"
engagement: "stars=17004 forks=1605"
tags: ["sandbox", "ai-agent", "ai-infra", "kubernetes", "aaif"]
related: [20261006-cua-computer-use-agent-sandbox]
needs_manual_text: false
---
## 摘要

OpenSandbox 係一個俾 AI agent 用嘅沙盒執行環境，可以喺自己嘅基建上面跑，屬於 Agentic AI Foundation（AAIF）項目。佢提供隔離環境，等 AI 應用執行程式碼、跑指令、管理檔案，甚至操作瀏覽器或桌面。README 講明可以先用 Docker 喺本機開始，再透過統一嘅 sandbox API 部署到 Kubernetes；Fast Sandbox runtime 用 Firecracker，建立時間 P50 約 64 毫秒，並支援保留記憶體同磁碟狀態嘅暫停／恢復。另外有出口網絡策略、Credential Vault（令 agent 呼叫外部服務時唔會見到真實憑證）、多種語言 SDK、`osb` CLI 同 MCP 整合，範例涵蓋 Claude Code、Codex CLI、Playwright 同 agent 評測。

## Key facts

- **Repo**: [opensandbox-group/OpenSandbox](https://github.com/opensandbox-group/OpenSandbox)
- **Stars**: 17,004 | **Forks**: 1,605
- **Language**: Python (SDKs for Java/Kotlin, TypeScript, C#, Go too)
- **License**: Apache-2.0
- **Last push**: 2026-11-10
- **Install**: `uvx opensandbox-server init-config ~/.sandbox.toml --example docker` then `uvx opensandbox-server`; SDK `uv pip install opensandbox`. Needs Docker and Python 3.10+

## 點解值得留意

如果想俾 coding agent 或 browser agent 喺隔離環境跑未受信任嘅程式碼，呢個係一個可自架、由本機 Docker 一路擴展到 Kubernetes 嘅選擇。Credential Vault 同按沙盒設定嘅出口網絡限制，直接回應 agent 安全嘅兩個痛點。同 vault 內 delegating-to-codex 或瀏覽器自動化類 skill 配合，可以作為更安全嘅執行層參考。

## Source

- URL: https://github.com/opensandbox-group/OpenSandbox
- Created: 2025-12-17
- Reader: raw.githubusercontent.com README + Jina Reader (GitHub API JSON)

## Related
- [[../pages/20261006-cua-computer-use-agent-sandbox|Cua: give your AI agent its own computer]] — 同樣俾 agent 獨立環境，Cua 係針對桌面操作（Lume 虛擬 Mac）。
