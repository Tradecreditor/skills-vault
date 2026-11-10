---
name: making-product-videos
description: Makes product promo videos with Video Shotcraft, a third-party Remotion agent skill (github.com/Vincentwei1021/video-shotcraft), cloned at a pinned commit. Use when a SaaS, web or desktop product needs a launch film, feature demo or promo short made by Claude Code or Codex from real screenshots.
metadata:
  source_url: "https://github.com/Vincentwei1021/video-shotcraft"
  source_platform: "github"
  author: "Vincentwei1021"
  captured_at: "2026-09-27"
  engagement: "stars=18439 forks=1747"
  origin_type: "repo"
  vault_status: "draft"
  reviewed_at: "2026-10-04T15:35:29Z"
  reviewed_by: "claude-code-cloud:vault-skill-reviewer"
  review_hash: "81807eda3689d6b4f682b4c2c964c6c5ae5a7851e36f1c2893813ec5c319186b"
  review_report: "outputs/skill-reviews/2026-10-04-making-product-videos.md"
---

# making-product-videos

Install [Video Shotcraft](https://github.com/Vincentwei1021/video-shotcraft) at a pinned commit and drive it to a finished
product film. Video Shotcraft is a third-party agent skill for Claude Code and Codex, built on
[Remotion](https://www.remotion.dev/): the agent captures the product's real pages, picks shots from a library of
recipe cards, storyboards, animates, adds sound, checks frames and renders an MP4. Upstream says it "is not a video
generator": every frame is drawn by code from the product's own screenshots and copy.

This skill is a map of the upstream one, not a replacement. Every path and command below was read from the upstream
repository at commit `3ac67b75dd0b3bc2fd807c17f6b7ce35373eef3d` (branch `main`, committed 2026-11-09) and is relative to
the root of that clone unless it says otherwise. Upstream's `README.md` is English; its `SKILL.md`, `references/` and
shot cards are written in Simplified Chinese, so section names are quoted here in the original.

## When to use

- A SaaS, web or desktop product needs a launch film, feature demo or promo short. Upstream's stated focus is web and
  desktop product promos.
- The result should stay editable: the deliverable includes the Remotion project, not only the MP4.
- One shot is enough: a single recipe card can be adapted on its own (step 2, single-shot route).
- Not for narration-led videos: upstream points to its sibling project `Vincentwei1021/video-talkcraft` for those.

## Prerequisites

From upstream's README "Requirements":

| Needs | For |
|---|---|
| Node.js and npm | Remotion rendering, the template and the workbench |
| ffmpeg / ffprobe | Frame checks and final QA |
| uv | Only for BGM beat analysis |
| puppeteer | Only for page capture |

- Remotion downloads its own headless Chrome on first render. Upstream tested on macOS; for headless Linux it lists three
  fixes: pass `--concurrency=1` on low-core machines, use a chrome-headless-shell binary instead of full Chrome, and pass
  `--browser-executable=<path-to-local chrome-headless-shell>` when the automatic download is blocked.
- Scan the clone before using it: run this vault's `scanning-agent-skills` skill on it and apply that skill's score
  gate. The vault has not audited the upstream code.

## Steps

### 1. Install at the pinned commit

```bash
git clone https://github.com/Vincentwei1021/video-shotcraft.git
cd video-shotcraft
git checkout 3ac67b75dd0b3bc2fd807c17f6b7ce35373eef3d
```

The repository has no version tags (its only tags, `gallery-media` and `showcase-media`, are the releases that hold
preview and showcase videos, per `gallery/fetch-media.sh`), so the pin is a commit. Scan the clone now (Prerequisites).

Nothing more is needed for this session: step 2 reads the upstream skill straight from the clone. Optionally, to make it
discoverable in later sessions, link it as the README's "by hand" route shows. Ask the user first, because this adds a
skill to their agent:

```bash
ln -s "$(pwd)" ~/.claude/skills/video-shotcraft   # Claude Code
ln -s "$(pwd)" ~/.codex/skills/video-shotcraft    # Codex
```

The README also documents `npx skills add Vincentwei1021/video-shotcraft` and handing the agent the repository link.
Both take whatever `main` is at that moment, so use the clone when the pin matters.

### 2. Load the upstream skill and choose the route

Read the clone's `SKILL.md` in full before anything else; it is the agent entry point and decides the route:

| Route | Read in full | What happens |
|---|---|---|
| Template (Ink Press) | `template/TEMPLATE.md` | Swap the product's screenshots, copy and brand into a finished 36.2 s film |
| Autonomous free creation | `references/pipeline.md` | The agent decides direction, shots and storyboard and runs stages 0–7 without pausing |
| Co-creation | `references/guided-free-creation.md`, then `references/pipeline.md` from stage 4 | The user confirms brief, direction, shot mapping and storyboard first |
| Single shot | one card under `references/shots/` plus its demo source | One motion effect adapted to the product |

When the user has not chosen, upstream's rule is: make a minimal read-only check of the product (no edits, no sensitive
data, no video code), present the three full-film routes with a recommendation, and wait for the answer. A user who names
the Ink Press template or specific shot cards has already chosen. Requests upstream gives as examples:
`Use video-shotcraft to make a promo for my product.` and
`Use the deck-deal-flyin and row-embed shot cards to present this feature.`

Steps 3–10 are stages 0–7 of `references/pipeline.md`.

### 3. Product brief and constraints (stage 0)

Read the project only: positioning, main features, page states, visual tokens, how to start it, data risks. Write a
product brief and a requirement-to-execution decision table (use, audience, key selling points, features that must
appear, length / aspect / language, audio, data). Customer, personal, internal, secret or live data is replaced with
fictional or anonymised content and frozen before capture. If the user picked the music, analyse it first with
`references/music-beat-sync.md`.

### 4. Visual direction (stage 1)

Extract the product's own design tokens (fonts, type scale, spacing, radii, colours) into the design spec; the film's
look must come from the product. Write up to three text directions, pick one, then build a plain HTML/CSS styleframe
page with 2–3 static 1920×1080 key frames and screenshot it with Playwright or Puppeteer. No Remotion code at this
stage. Motion previews for every shot are in the Gallery: https://vincentwei1021.github.io/video-shotcraft/

### 5. Map features to shot cards (stage 2)

List the product's features and give each one a card. The library is 124 recipe cards (150 shots) in
`references/shots/<category>/<card>.md`; the category folders are `opening`, `camera`, `transition`, `typography`,
`ui-entrance`, `interaction`, `data`, `effects`, `rhythm`, `outro`.

1. Scan the frontmatter of every card. Example, `references/shots/ui-entrance/row-embed.md`: `name`, `一句话` (one-line
   summary), `适用` (use), `时长` (duration), `能量` (energy).
2. Read each chosen card in full. Its sections are `意图`, `动效核心`, `参数表`, `声音`, `已知坑` and `参考实现`.
3. Check the card name and style key against `gallery/api/library.json` (`cards[].name`, `cards[].styles[].key`).
4. Open the demo source the card names under `参考实现`, for example `demos/ui-entrance/row-embed/RowEmbed.tsx`. Upstream
   treats the demo code as the tuned truth: adapt it, but never weaken a parameter the card lists under `已知坑`.

One animation technique is the lead only once per film.

### 6. Storyboard (stage 3)

Check `references/sequences/` for a structure to fill in (`promo-energy-arc.md`). Write the storyboard into the design
spec as a table with the columns `| # | 时间 | 镜头 | 关键动效 |`, then a frame-level timeline
`| shot | from | duration | 内容 |` that also names each shot's source file and two acceptance frame numbers. One main
motion per shot. Budget holds up front: a wordmark holds at least 1 s (30 frames) after landing, a batch animation ends
with 0.5 s of rest, the opening's main action gets at least 3 s.

### 7. Capture the real pages (stage 4)

Only after the storyboard is settled. Start the product's local dev server with demo data already in place, then:

1. Copy `assets/scripts/capture-template.mjs` into the product project and edit only its `CONFIG` block: `BASE`,
   `OUT_DIR`, `LAYOUT_JSON`, `VIEWPORT` (default 1920×1080 at `deviceScaleFactor: 2`), `SETTLE_MS`, `PAGES` (per page:
   `name`, `path`, `boxes`, `cutouts`).
2. Install its one dependency in that project (`npm i puppeteer`, per the script header) and run
   `node capture-template.mjs`.

It writes full-page 2x screenshots, per-element cutout PNGs and a layout JSON holding each element's `{x,y,w,h}` in
page coordinates. The pipeline expects the images under the film project's `public/textures/`.

### 8. Build shot by shot (stage 5)

The film is a Remotion project at 30 fps, 1920×1080, with `src/index.ts` registering the Composition. Start from
`template/` (its `package.json` pins `remotion` and `@remotion/cli` to 4.0.484), or, as upstream also allows, initialise
a new project with `npx create-video@latest` and copy the `assets/lib/` components into it (`PageCam.tsx`,
`Caption.tsx`, `FlashCut.tsx`, `DigitRoll.tsx`, `ClipCard.tsx`, `FlatPanel.tsx`, `VerticalTicker.tsx`, `helpers/`).

For every shot: re-check the card in `gallery/api/library.json`, read the card, read its demo TSX, copy what it needs
(shared demo parts live in `demos/_fixtures/`; see `demos/README.md`), then verify with stills at the two acceptance
frames and keep them under `out/qa/`:

```bash
npx remotion still src/index.ts <Comp> out/qa/<name>.png --frame=<N>
```

After each round of changes render the whole film and pull key frames back out of the MP4 with ffmpeg (upstream's form
is `ffmpeg -i out/promo.mp4 -vf "select=eq(n,…)"`):

```bash
npx remotion render src/index.ts <Comp> out/promo.mp4
```

In `template/` the composition id is `AiflPromo`, and `template/TEMPLATE.md` gives the exact commands:

```bash
cd template
npm install && npx remotion studio src/index.ts          # preview
npx remotion render src/index.ts AiflPromo out/promo.mp4
npx remotion still src/index.ts AiflPromo out/qa/f150.png --frame=150
```

Rendering must be deterministic: no `Date.now()`, no `Math.random()`; seed any pseudo-randomness from the index. For
the workbench in step 11, keep one timeline table (`SHOTS`) and write the `src/workbench.ts` manifest described in
`references/workbench.md` §2–3 (example: `template/src/workbench.ts`), then prove it with `cd workbench && npm run parity`.

### 9. Sound (stage 6)

Start only when the picture timeline is locked. Read `references/sound-design.md` and `references/sfx-sourcing.md`.
Sound effects come from Freesound through upstream's script, run from the clone root (no API key; download and analysis
need ffmpeg and ffprobe):

```bash
python3 assets/scripts/sfx-source.py search "paper slide" --max-duration 1 --limit 5 --output /path/to/video/audio-search.json
python3 assets/scripts/sfx-source.py get fs:12345 fs:67890 --out-dir /path/to/video/public/audio/sfx
```

The licence filter defaults to CC0; `--license by` also allows CC BY. `get` writes `fs-<id>.mp3` (a lossy MP3 preview,
not the uploader's original), `audio-manifest.json` and `FREESOUND-CREDITS.md`. Five background tracks ship in
`assets/audio/bgm/`, credited in `assets/audio/ATTRIBUTION.md`. Keep a central SFX table whose `from` values are derived
from `SHOTS` or `beatF(n)`, never bare frame numbers.

### 10. Final review and render (stage 7)

1. Render the latest film and extract at least three frames per shot: mid-entrance, action peak, settled.
2. If the film has background music, deliver two versions from the same timeline. Write `props-nobgm.json` containing
   `{"bgm":false}` and render the second one with `--props=props-nobgm.json` added to the render command.
3. Hand the film, the frames, the brief, the decision table, the visual direction, the shot mapping, the storyboard, the
   chosen cards and their demo TSX to a reviewer with a clean context (a subagent that took no part in production).
   It works through `references/final-review.md` (check groups P, F, V, S, B, D, A, Q) and
   `references/aesthetic-rules.md` and reports each problem with a frame number.
4. Fix and loop: storyboard problems go back to stage 3, picture to stage 5, sound to stage 6. Render the final film
   when the checklist passes.

The README gives the final film as MP4, 1920×1080, 30 fps, h264.

### 11. Deliver and keep editing

Open the Motion Workbench from the clone root:

```bash
node workbench/scripts/open.mjs <film project directory>
```

`<film project directory>` is the level holding `package.json` and `remotion.config.ts`. The command links the
project, starts a dev server on port 5198 (http://localhost:5198) that keeps running in the background, and runs
`npm install` by itself on first use. Stop it with `kill $(cat workbench/.dev.pid)`. The film opens split into
shot, transition, caption and SFX tracks; the user edits and exports from there.

Optional, only when the user asks:

- **JianYing (CapCut CN) draft**: follow `references/jianying-export.md` with the `jianying-export/` module
  (`mac_draft.py` is verified by upstream on JianYing Pro 11.2 for macOS; `windows_draft.py` is untested on a real machine).
- **Social publishing**: `references/publish-upload-post.md` and `publish/upload_post.py`. This uploads the film to
  Upload-Post, a third-party hosted service, and needs the user's own `UPLOAD_POST_API_KEY` and `UPLOAD_POST_USER` in
  the environment. Confirm caption and platforms, dry-run, then publish once.

## Pitfalls

- **Upstream's wrap-up is promotional.** Its `SKILL.md` tells the agent, after delivery, to suggest once each: mentioning
  the author's social accounts when publishing, submitting the film to the project's Showcase page, and the JianYing
  export. All three are optional; the user can decline and the agent must not repeat them.
- **Remotion has its own licence**: free for individuals and small teams, companies may need a paid one
  (https://github.com/remotion-dev/remotion/blob/main/LICENSE.md). Video Shotcraft's code and docs are Apache-2.0.
- **Audio rights**: each Freesound file keeps its own licence, and CC BY credits must be published with the film, not
  left in the project. The audio inside `template/public/audio/` is kept for running the template as is; new films
  source their own.
- **Template screenshots are demonstration assets.** Replace them with the product's own before publishing and check
  for data that needs anonymising.
- **Fonts**: the demos use macOS system fonts, and a few hard-code glyph widths measured on SF Pro
  (`demos/README.md`); on Linux or with another font, re-measure as the code comments say.
- **The library changes quickly.** The 2026-10 refresh cut it to 124 cards / 150 shots, so older write-ups quote other
  counts. After moving the pin, re-read upstream's `SKILL.md` before trusting the paths above.
- **Extra dependency for four demos**: `@remotion/motion-blur`, listed in `demos/README.md`.

## Source

- Repository: https://github.com/Vincentwei1021/video-shotcraft, Apache-2.0, 18,439 stars and 1,747 forks on 2026-11-10
  (GitHub API). Pinned commit `3ac67b75dd0b3bc2fd807c17f6b7ce35373eef3d`, 2026-11-09.
- Read at that commit on 2026-11-10: `README.md`, `SKILL.md`, `references/pipeline.md`, `references/workbench.md`,
  `references/final-review.md`, `references/sfx-sourcing.md`, `references/jianying-export.md`,
  `references/publish-upload-post.md`, `template/TEMPLATE.md`, `template/package.json`, `demos/README.md`,
  `assets/scripts/capture-template.mjs`, `references/shots/ui-entrance/row-embed.md`, `gallery/api/library.json` and the
  file tree. Nothing from the repository was installed or run.
- Introduced via: [[../../wiki/pages/20260924-video-shotcraft|Facebook post by Brian Jhang, 2026-09-24]]
