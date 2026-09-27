---
name: providing-design-references
description: Provides Claude with visual design references so it can match real layouts and UI decisions instead of inventing generic styles. Use when vibe-coding an app, improving UI output, matching spacing or typography, or building pitch decks with Claude.
metadata:
  source_url: "https://instagram.com/p/Ddqj0svm6yq/"
  source_platform: instagram
  author: "nocodealex"
  captured_at: "2026-09-27"
  engagement: ""
  origin_type: "post"
  vault_status: "draft"
---

# providing-design-references

Give Claude something to see before asking it to design. Claude matches visual decisions accurately when shown a reference — it cannot invent taste from a text description alone.

## When to use

- Starting a new UI or redesigning a screen
- Claude keeps producing the same generic purple-gradient look
- You want a specific transition, spacing rhythm, or type scale
- Building a pitch deck or launch video

## Steps

### 1. Find a reference

| Goal | Site | How |
|---|---|---|
| Website layout / spacing / type | godly.design | Browse curated sites, screenshot the one you like |
| UI transitions (menus, modals, counters) | transitions.dev | Copy-paste the code, or install the Claude Code skill for 27+ transitions |
| App launch video | animos.app | Upload your app screenshot, pick one of 25 templates |
| Pitch deck structure | deck.gallery | Browse 200+ real decks (OpenAI, Perplexity, etc.), screenshot the structure |

### 2. Give Claude the screenshot

Paste the screenshot directly into Claude and prompt:

```
Match the layout, spacing and type decisions from this reference.
Not the brand — the decisions: spacing rhythm, type sizes, one accent color.
```

### 3. Iterate on decisions, not content

- Copy the *structure*: column widths, type hierarchy, padding ratios
- Do not copy brand colors, logos, or actual text
- Ask Claude to apply those decisions to your own content

## Install transitions.dev as a Claude Code skill

transitions.dev ships as an Agent Skills package. To install:

```
npx skills add transitions-dev
```

Once installed, Claude Code knows 27+ transitions by name — no pasting code or explaining the pattern.

## Pitfalls

- Screenshotting a whole page and asking Claude to "make it like this" produces a copy, not an adaptation — always say "match the decisions"
- godly.design is curated; if you paste a random production site, quality varies
- animos.app is browser-only; works best for simple looping demos, not complex interactive flows

## Source

- https://instagram.com/p/Ddqj0svm6yq/ — @nocodealex, 2026-09-24
