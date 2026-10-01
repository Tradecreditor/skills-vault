---
slug: 20260930-hostinger-vps-cloudflare-tunnel-setup
source_url: "https://www.threads.com/@systems_thinker_852/post/Dd59aV9meXX"
canonical_id: "threads:Dd59aV9meXX"
fetched_at: "2026-10-01T12:42:10Z"
reader: "jina"
---
{"author": "@systems_thinker_852", "author_name": "進擊地思考", "platform": "threads", "published": "2026-09-30", "published_from": "1d at 2026-10-01T12:42Z", "engagement": {"likes": 27, "replies": 9, "reposts": 2, "shares": 30, "views": "4.9K"}, "engagement_order": "likes, replies, reposts, shares inferred from Threads UI", "post_url": "https://www.threads.com/@systems_thinker_852/post/Dd59aV9meXX", "share_url": "https://www.threads.com/share/BBaR3zXHpW/", "topic_tag_on_post": "AI Threads", "contains_referral_link": true}

Post 1 — @systems_thinker_852 (https://www.threads.com/@systems_thinker_852/post/Dd59aV9meXX):

用咗 Hostinger + Cloudflare 幾個月，我個系統就係咁行，慳咗好多心機：

Hostinger VPS（KVM 2）= 約 US$6.5/月起就有 2 核 / 8GB / 100GB NVMe。Ubuntu 24.04 + Docker template 預裝好，開機即用， Asis都有。

Cloudflare 免費版做前置：DNS + SSL + WAF 都 $0。最正係 Tunnel ── VPS 一條對外 port 都唔使開，真實 IP 完全隱藏，DDoS 打到你都無嘢打。

兩樣夾埋最抵：唔使捱夜搞 cert/防火牆，reboot 自動起返晒，仲用 R2 每日自動做 DB 備份 + 做過真 restore 演練。細 SaaS / 個人站 $6.5 一個月搞掂，抵到笑。

想試就用我個 referral 註冊有折 👉 [hostinger.com…]

[link card: "Your exclusive Hostinger discount" — hostinger.com; referral link not followed, code not recorded]

27

9

2

30

4.9K views
