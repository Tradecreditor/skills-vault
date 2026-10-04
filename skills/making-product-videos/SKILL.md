---
name: making-product-videos
description: Creates cinematic product demo videos using Video Shotcraft (Remotion + Agent Skill). Use when building SaaS/web/desktop product videos with Claude Code or Codex, Remotion, shot recipe cards, storyboard, and frame-by-frame QA.
metadata:
  source_url: "https://github.com/Vincentwei1021/video-shotcraft"
  source_platform: "github"
  author: "Vincentwei1021"
  captured_at: "2026-09-27"
  engagement: "stars=9308 forks=847"
  origin_type: "repo"
  vault_status: "draft"
  reviewed_at: "2026-10-04T15:35:29Z"
  reviewed_by: "claude-code-cloud:vault-skill-reviewer"
  review_hash: "81807eda3689d6b4f682b4c2c964c6c5ae5a7851e36f1c2893813ec5c319186b"
  review_report: "outputs/skill-reviews/2026-10-04-making-product-videos.md"
---

# making-product-videos

Turn a product into a cinematic demo video using [Video Shotcraft](https://github.com/Vincentwei1021/video-shotcraft) — an Agent Skill built on Remotion that encodes cinematography rules, shot recipes and QA checks so Claude Code / Codex can produce professional product videos, not just "animated slides".

## When to use

- You need to produce a product launch, feature demo or promo short for a SaaS, web or desktop app.
- You want Claude Code or Codex to generate Remotion animations that follow cinematography rules rather than free-form motion.
- You need a structured QA step: render, check specific frames, re-render until clean.

## Steps

### 1. Install

```bash
git clone https://github.com/Vincentwei1021/video-shotcraft
cd video-shotcraft
npm install
```

### 2. Understand product & audience

Tell the agent the product name, the one-line value prop, the target viewer, and the video goal (awareness, conversion, tutorial). This becomes the creative brief.

### 3. Visual direction

The agent picks a visual style from the 214 style library. Provide brand colors and reference screenshots if available.

### 4. Map features → shots

Each product feature maps to one shot from the 157 recipe cards. Each card includes:
- Purpose and use case
- Rhythm and timing
- Recommended duration
- TSX parameters
- Common pitfalls and fixes

### 5. Storyboard

Output a shot list: `[shot_index] [recipe_card_name] [duration_s] [content]`. One primary action per shot. Leave reading time for text-heavy frames.

### 6. Capture real UI

Before coding, capture actual product screenshots / screen recordings. The skill enforces: **use real UI, not AI-redrawn interfaces**.

### 7. Build shot by shot

For each shot, the agent:
1. Selects the matching TSX recipe
2. Fills in product-specific content and screenshots
3. Renders the shot
4. Outputs designated frames (specified in the recipe card) for review
5. Fixes issues and re-renders the full video

### 8. Audio design

Add background music, sound effects, and (optionally) voiceover. Check licenses before commercial use — bundled assets may have restrictions.

### 9. Final QA

Run the 8-round frame-by-frame check:
- Each shot plays correctly in isolation
- Transitions are smooth
- Text is readable with sufficient dwell time
- UI screenshots are crisp and not scaled awkwardly

### 10. Export

Use the browser workbench to reorder shots, adjust length/speed/styles. Export via Remotion CLI or hand off to CapJian (剪映) for further editing.

```bash
npx remotion render src/index.ts MyVideo out/video.mp4
```

## Pitfalls

- **Remotion license**: Remotion has its own commercial license separate from this skill's Apache-2.0. Check [remotion.dev/license](https://remotion.dev/license) before shipping.
- **Music/SFX rights**: Some bundled assets need re-verification for commercial use.
- **8-round QA is the author's workflow**: it is not an independent benchmark; adapt it to your production pace.
- **Not for**: talking-head / vlog content, documentaries, long narrative films — use a proper NLE for those.
- **yt-dlp / screen recording**: datacenter IPs are often blocked; capture screenshots on a local machine and pass them to the agent.

## Source

- Repo: https://github.com/Vincentwei1021/video-shotcraft (9,308 ⭐, Apache-2.0, active as of 2026-09-24)
- Introduced via: [[../../wiki/pages/20260924-video-shotcraft|Facebook post by Brian Jhang, 2026-09-24]]
