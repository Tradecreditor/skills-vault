# Agents 點樣讀社交媒體連結：有登入 vs 冇登入（2026-10-01）

**決定**：唔用任何登入帳號、cookie 或雲端瀏覽器。X 同 YouTube 行 Agent-Reach 預設 reader；Instagram 同 Facebook 用 Jina 攞文字，再用 **Supadata**（唯一一個 key，免費層每月 100 credits）轉錄影片語音。Supadata 只會用喺 IG / FB，唔會用喺 X 或 YouTube。Reddit、B站、小紅書、LinkedIn、TikTok 唔喺需求內。

## 摘要

Josep 主要由 Telegram 貼 X、Instagram、Facebook、YouTube 連結入 vault，由雲端 `capture-link` Routine 處理。而家冇登入已經讀到 X 單帖（fxtwitter）、Threads、IG caption（Jina 或公開 embed endpoint）、FB 公開帖（Jina）。讀唔到嘅係影片語音：IG reel / carousel 影片、FB 影片、YouTube 字幕（雲端 IP 被 YouTube 封 yt-dlp）。Agent-Reach 嘅 FB / IG 路線要喺桌面 Chrome 裝 OpenCLI 借用登入狀態，雲端 Routine 用唔到。所有要登入嘅方法（匯出 cookie、Playwright storageState、OpenCLI、Browser Use / Browserbase profile、Claude in Chrome）都違反平台條款、有封號風險，所以唔採用。Supadata 唔使登入就轉錄到 IG / FB 影片，免費層夠用（約每月 30 分鐘 AI 轉錄），所以成為唯一加入嘅 key，而且限定 IG / FB 先用。YouTube 喺雲端會只有 metadata 加 `needs_manual_text: true`，本機 Claude Code 跑一次先有字幕，呢個係接受咗嘅取捨。

## Per-platform matrix (what the vault does now)

| Platform | Without login (cloud Routine) | Key used | Cookie / login | Cost | Gap left |
|---|---|---|---|---|---|
| X | twitter-cli locally; `api.fxtwitter.com` JSON in the cloud (text, counts, video URL; 1000 req/min per IP, no key) | none | none (burner cookie only for the weekly search) | $0 | video tweets are not transcribed |
| Threads | Jina (text + 4 unlabeled counts); share links resolved through Jina | none (`SC_API_KEY` optional for labeled counts) | none | $0 | count order is inferred |
| Instagram | Jina (caption + counts from the login shell); when Jina rate-limits instagram.com, `instagram.com/p/<code>/embed/captioned/` (caption, username, likes) | `SUPADATA_KEY` for reel / carousel video audio and counts | none | $0; Supadata ~3 credits per 90-second reel | on-screen text in videos; DM-gated links |
| Facebook | Jina (public posts, videos, `/share/` links); facebook.com itself is egress-blocked in the cloud | `SUPADATA_KEY` for video / reel audio | none | $0 (+ Supadata credits for video) | private groups |
| YouTube | locally yt-dlp + subtitles; in the cloud Exa + oEmbed metadata only, `needs_manual_text: true` | none (by decision) | none | $0 | cloud captures need a local re-run for the transcript |

Agent-Reach's own coverage (upstream README, read 2026-10-01): without an account it reads web pages (Jina), YouTube subtitles and search, RSS, V2EX, public GitHub, single X posts, Bilibili, public LinkedIn pages, and searches the web through Exa. With a login it adds X search / timelines / articles (Cookie-Editor export), Reddit, Facebook and Instagram (OpenCLI reusing a logged-in desktop Chrome), 小紅書 and LinkedIn profiles. The cloud Routine has no desktop Chrome, which is why Facebook and Instagram need another route there.

## No-login options evaluated

- **Jina Reader (r.jina.ai)** — ~20 req/min anonymous, 500 with a free key. It blocks a whole domain for all anonymous users when it detects abuse elsewhere (`AbuseAlleviationError`, HTTP 403, status 40305, "blocked until <time>"); seen today on instagram.com, x.com and linkedin.com; threads.com and facebook.com read fine. A key is reported, not verified, to bypass the blocks. Adopted as the first reader; `JINA_API_KEY` optional.
- **Instagram `/embed/captioned/`** — public, returns the caption HTML (`class="Caption"`), username and like count. Used for two captures today while Jina was blocked. Adopted as the IG fallback.
- **FxTwitter (FxEmbed)** — `api.fxtwitter.com`, API v2 at `/2/`, OpenAPI at `/2/openapi.json`, open source, no key. Verified working from the cloud. Already the X reader.
- **Meta tokenless oEmbed** (since 2026-06-15, no app or token: `graph.facebook.com/v25.0/instagram_oembed`, `graph.threads.net/v1.0/oembed`, Facebook post/video oEmbed) — verified reachable for Threads, but the returned `html` is an empty embed shell with **no post text**. Not adopted (only useful as an existence check).
- **Supadata** (`api.supadata.ai`, docs.supadata.ai) — `GET /v1/transcript?url=<url>&text=true&mode=auto` for YouTube, TikTok, Instagram reels, X video, Facebook video / reel; `mode=native` returns existing captions, `generate` / `auto` runs AI transcription (videos over 20 min become an async job). `/v1/metadata?url=` for video details. Pricing (supadata.ai/pricing): 1 credit per existing transcript, 2 credits per AI-generated minute, 1 credit per URL fetch; free 100 credits/month, paid plans from $5/month, credits do not roll over. **Adopted for Instagram and Facebook only.**
- **ScrapeCreators** (`api.scrapecreators.com`) — IG post/reel info and AI transcript, Threads post with labeled counts, Facebook post / transcript, YouTube transcript, X tweet transcript, LinkedIn; 1 credit per request, 100 free (+ up to 7,000 bonus), $47 for 25k, credits never expire, cached results free. Not adopted now; the natural add-on if labeled IG / FB counts are ever wanted.
- **Apify / Bright Data / EnsembleData / RapidAPI** — per-result pricing ($1.50–2.70 per 1k records, or $100/month plans); overkill for 30–60 links a month. Not adopted.
- **Firecrawl** — refuses Instagram, YouTube and TikTok ("no longer supported"). Not adopted for social links.
- **YouTube official Data API** — cannot download captions of other people's videos; `youtube-transcript-api` is blocked from cloud IPs. Hence the cloud trade-off.

## With-login options evaluated (not adopted)

All of these breach Meta's Automated Data Collection Terms and X's terms, and the realistic cost is the account being checkpointed or banned. If ever used, only with a throwaway account.

- **Playwright with `storageState` / `--user-data-dir`** — log in once on a laptop, replay the session headless in the cloud. Meta checkpoints when the IP or fingerprint changes (home Hong Kong cookie replayed from a datacenter), sessions expire, and a leaked session file is full account access.
- **OpenCLI (jackwener)** — Chrome extension + local bridge; reuses your logged-in Chrome, so it needs your computer on. A remote browser can be attached with `OPENCLI_CDP_ENDPOINT`. This is Agent-Reach's Facebook / Instagram path.
- **Agent-Reach twitter-cli cookies** — `TWITTER_AUTH_TOKEN` + `TWITTER_CT0` from a burner account; the vault already allows this for X search only, never from a cloud routine.
- **Browser Use Cloud** ($0.02 per browser-hour, Profile Sync uploads cookies) · **Browserbase** (free 1 h, $20/month) · **Browserless** (free 1k units, $25/month) · **Steel.dev** ($0.10/h) · **Hyperbrowser**, **Kernel** — all keep persistent logged-in profiles; same ToS and ban exposure, plus $5–30/month.
- **Claude in Chrome / Claude Desktop built-in browser** — drive your own browser with your logins; only when your Mac is on and linked; a scheduled Routine cannot use them.
- **yt-dlp `--cookies-from-browser`, Instaloader `--sessionfile`, gallery-dl** — headless-capable but checkpoint-prone; the exported cookies.txt carries cookies for every site.

Hybrid idea kept for later: a "reader relay" — an always-on Mac (or a VPS with Camoufox) holding a burner profile behind Cloudflare Tunnel, exposing `POST /read {url}` with a bearer token that the Routine calls. Lowest checkpoint risk from a Hong Kong home IP, zero cash cost, but the same ToS exposure, so only if the no-login route proves insufficient.

## Verified from the cloud container (2026-10-01)

| Host | Reachable from the cloud session | Note |
|---|---|---|
| r.jina.ai | yes | domain blocks on instagram.com / x.com during the session |
| api.fxtwitter.com | yes | full JSON |
| api.supadata.ai | yes (401 without key) | |
| graph.threads.net | yes | tokenless oEmbed returns no text |
| www.instagram.com | yes (direct) | embed endpoint works |
| www.threads.com, www.aiposthub.com, www.facebook.com, graph.facebook.com, tiktok.com, linkedin.com, xiaohongshu.com, api.apify.com | no (egress 403) | Jina reads threads/facebook/aiposthub server-side |

## Unverified

- Whether a Jina API key bypasses the anonymous domain blocks.
- Supadata `/v1/metadata` fields for Facebook posts (documented for videos).
- vxtwitter / fixupx, Zyte, ScrapingBee social endpoints (not needed).

## Sources (read 2026-10-01)

- Agent-Reach README — github.com/Panniantong/Agent-Reach; twitter-cli — github.com/public-clis/twitter-cli
- Jina Reader — jina.ai/reader; rate-limit guide — agentscamp.com/guides/advanced/jina-reader-api
- Meta, "Introducing Tokenless Access to Meta oEmbed APIs" (2026-06-15) — developers.facebook.com/blog/post/2026/06/15/tokenless-access-to-meta-oembed-apis/
- FxEmbed API docs — docs.fxembed.com/api/introduction
- Supadata — docs.supadata.ai/get-transcript, supadata.ai/pricing
- ScrapeCreators — scrapecreators.com, docs.scrapecreators.com/llms.txt
- Apify Instagram scraper — apify.com/apify/instagram-scraper; Bright Data — brightdata.com/products/web-scraper/instagram; EnsembleData — ensembledata.com/pricing
- Browser Use pricing and auth — browser-use.com/pricing.md, browser-use.com/posts/web-agent-authentication; Browserless — browserless.io/pricing; Steel — docs.steel.dev/overview/pricinglimits
- OpenCLI — github.com/jackwener/OpenCLI; Claude in Chrome — code.claude.com/docs/en/chrome
- Meta Automated Data Collection Terms — facebook.com/legal/automated_data_collection_terms
- yt-dlp FAQ (cookies) — github.com/yt-dlp/yt-dlp/wiki/FAQ; Instaloader checkpoint issue — github.com/instaloader/instaloader/issues/2590
