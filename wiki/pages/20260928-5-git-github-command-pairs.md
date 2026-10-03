---
title: "5 Git & GitHub Command Pairs Explained (Merge vs Rebase, Fetch vs Pull, etc.)"
slug: 20260928-5-git-github-command-pairs
type: video
status: draft
source_url: "https://www.instagram.com/reel/Dd1QUCrirJg/"
source_platform: instagram
author: "@greatfrontend"
published: "2026-09-28"
captured_at: "2026-10-02T00:54:39Z"
captured_by: "routine:capture-link"
canonical_id: "instagram:Dd1QUCrirJg"
engagement: "likes=2520 comments=6"
tags: [topic/infra-devops, git, github, merge-vs-rebase, fetch-vs-pull, reset-vs-revert, fork-vs-clone, squash-merge, frontenddeveloper]
related: [20260930-hostinger-vps-cloudflare-tunnel-setup, 20260930-cloudflare-cf-agentic-cli-replaces-wrangler]
needs_manual_text: false
---

## 摘要

這是 GreatFrontEnd（@greatfrontend）製作的短影片，用視覺動畫解釋 5 組 Git 和 GitHub 命令，這些命令聽起來相似但作用不同。影片涵蓋 Merge 對 Rebase、Fetch 對 Pull、Reset 對 Revert、Fork 對 Clone，以及 Merge commit 對 Squash merge。每一對都有語音說明和動態圖示，非常適合初學者或需要複習基礎的開發者。影片獲得 2,520 個讚，是 GreatFrontEnd 系列中一個清晰易懂的 Git 入門教學。

## Key facts

**Merge vs Rebase**
- `git merge <branch>` — combines your branch with another; creates a new merge commit joining both histories; preserves full branch history.
- `git rebase <branch>` — replays your commits on top of a new base; produces a straight, linear history; rewrites commit SHAs.

**Fetch vs Pull**
- `git fetch origin` — downloads newest commits from the remote; does NOT change your working branch.
- `git pull origin <branch>` — fetch + automatic integration (merge or rebase) into your current branch.

**Reset vs Revert**
- `git reset <commit>` — moves branch pointer back to another commit; changes which commits the branch includes (can lose history).
- `git revert <commit>` — keeps all existing history; adds a new commit that undoes an earlier one (safe for shared branches).

**Fork vs Clone**
- **Fork** — creates your own copy of a repository on GitHub, separate from the original; done on github.com.
- **Clone** (`git clone <url>`) — downloads a repository onto your computer to work with locally.

**Merge commit vs Squash merge**
- **Merge commit** — keeps each PR commit; joins the two branch histories with a merge commit.
- **Squash merge** — combines all PR commits into one single commit on the target branch; cleaner log, loses granular history.

## 點解值得留意

- 這 5 組命令是新手最常搞混的 Git 概念，視覺化對比讓人一目了然，可直接用作入職培訓或 code review checklist 的參考材料。
- 對於使用 Claude Code 進行 git 操作的代理人來說，Reset vs Revert 和 Merge vs Rebase 的區別直接影響到在共用分支上的安全操作準則。
- Squash merge 策略與此 vault 的 `vault-capture` skill 提交規範相關（每個 URL 一個 commit），值得在 CLAUDE.md commit 指引中參考。

## Source

- **Link**: https://www.instagram.com/reel/Dd1QUCrirJg/
- **Author**: GreatFrontEnd (@greatfrontend)
- **Published**: 2026-09-28
- **Engagement**: likes=2520, comments=6
- **Reader**: supadata (transcript + metadata)

## Related

- [[20260930-hostinger-vps-cloudflare-tunnel-setup|Hostinger KVM 2 VPS + Cloudflare free tier]] — 同屬 topic/infra-devops；部署到 VPS 之前先搞清楚 fetch/pull 同 merge/rebase。
- [[20260930-cloudflare-cf-agentic-cli-replaces-wrangler|Cloudflare cf: agentic CLI replacing Wrangler]] — 同屬 topic/infra-devops，由 git 基礎去到 agent 操作雲端平台嘅 CLI。
