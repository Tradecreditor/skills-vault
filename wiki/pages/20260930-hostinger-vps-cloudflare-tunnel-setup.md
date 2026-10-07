---
title: "Hostinger KVM 2 VPS + Cloudflare free tier for a ~US$6.5/mo small SaaS"
slug: 20260930-hostinger-vps-cloudflare-tunnel-setup
type: post
status: draft
source_url: "https://www.threads.com/@systems_thinker_852/post/Dd59aV9meXX"
source_platform: threads
author: "@systems_thinker_852"
published: "2026-09-30"
captured_at: "2026-10-01T12:42:10Z"
captured_by: "claude-code-cloud"
canonical_id: "threads:Dd59aV9meXX"
engagement: "likes=27 replies=9 reposts=2 shares=30 views=4.9K"
tags: [topic/infra-devops, vps, hostinger, cloudflare, cloudflare-tunnel, r2-backup, small-saas, self-hosting]
related: [20260930-cloudflare-cf-agentic-cli-replaces-wrangler, 20260928-5-git-github-command-pairs]
needs_manual_text: false
---

## 摘要

「進擊地思考」（@systems_thinker_852）分享佢用咗幾個月嘅低成本部署組合：Hostinger KVM 2 VPS 加 Cloudflare 免費版。VPS 約 US$6.5／月起，Cloudflare 免費層負責 DNS、SSL、WAF，再用 Tunnel 令 VPS 唔使開任何對外 port、隱藏真實 IP。數據庫每日自動備份去 R2，作者話有做過真實 restore 演練。呢個方案幫細型 SaaS 同個人網站慳時間同成本，適合預算有限、想自己控制伺服器嘅開發者。要留意帖文末尾有 Hostinger referral 連結，屬推廣性質。

## Key facts

- Hostinger VPS **KVM 2**: from about **US$6.5/month**, **2 cores / 8GB / 100GB NVMe**
- Template: **Ubuntu 24.04 + Docker** preinstalled, usable straight after boot
- Cloudflare free tier in front: **DNS + SSL + WAF at $0**
- **Cloudflare Tunnel**: the VPS needs no open inbound port, real IP stays hidden (author's claim: DDoS has nothing to hit)
- Operations claims: no late-night cert/firewall work, services restart automatically after reboot
- **R2** used for **daily automatic DB backups**, and a real restore drill was done
- Author's framing: a small SaaS or personal site for $6.5/month
- The post ends with a Hostinger referral link (a referral link exists; not followed, code not recorded)

## 點解值得留意

- **Iron Log / English Overload 部署參考**：每月約 US$6.5 就有 2 核 8GB，Cloudflare 免費層做前置，適合 Jeff 個人 app 做低成本後端或測試環境。
- **客戶 SME 方案**：香港中小企想自架 n8n、內部工具或小型網站，可以用「VPS + Tunnel + R2 備份」做標準化報價，唔使開 port 亦減低安全風險。
- **備份加 restore 演練係重點**：好多教學只講備份，呢帖講明做過 restore，可以抽出做 checklist。
- **留意推廣成分**：內容混有 referral，屬作者自述經驗，上線前要自己實測。

## Source

- Post: https://www.threads.com/@systems_thinker_852/post/Dd59aV9meXX
- Author: @systems_thinker_852 (進擊地思考) · Published: 2026-09-30 (derived from "1d" at fetch time 2026-10-01T12:42Z)
- Engagement: likes=27 replies=9 reposts=2 shares=30 views=4.9K (order inferred from Threads UI)
- Reader: Jina Reader (r.jina.ai)
- Share URL: https://www.threads.com/share/BBaR3zXHpW/
- Not captured: the Hostinger referral link target (never followed), replies by other accounts, and the "Related threads" by other accounts

## Related

- [[pages/20260930-cloudflare-cf-agentic-cli-replaces-wrangler|Cloudflare cf: agentic CLI replacing Wrangler (3000+ APIs)]] — Cloudflare tooling captured in the same batch; no earlier infra pages exist in the vault
- [[pages/20260928-5-git-github-command-pairs|5 Git & GitHub Command Pairs Explained]] — same topic/infra-devops; the git basics behind deploying to this VPS
