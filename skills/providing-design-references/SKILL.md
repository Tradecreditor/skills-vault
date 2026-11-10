---
name: providing-design-references
description: Gives Claude visual references (screenshots, optional third-party transitions.dev skill) to match real UI decisions. Use when vibe-coding an app, improving generic UI output, matching spacing or type, or planning pitch decks.
metadata:
  source_url: "https://instagram.com/p/Ddqj0svm6yq/"
  source_platform: instagram
  author: "nocodealex"
  captured_at: "2026-09-27"
  engagement: ""
  origin_type: "post"
  vault_status: "draft"
  reviewed_at: "2026-10-04T15:35:29Z"
  reviewed_by: "claude-code-cloud:vault-skill-reviewer"
  review_hash: "bab69aaf73e46a980b3da6991cb169d0e631b9e8736d509fad4f0bb454fd5463"
  review_report: "outputs/skill-reviews/2026-10-04-providing-design-references.md"
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
| UI transitions (menus, modals, counters) | transitions.dev | Copy-paste the code, or optionally install its Claude Code skill (see below) |
| App launch video | animos.app | Upload your app screenshot, pick a template (the post says 25) |
| Pitch deck structure | deck.gallery | Browse real decks (the post says 200+, from brands like OpenAI and Perplexity), screenshot the structure |

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

## Optional: transitions.dev skill (third-party)

transitions.dev is a third-party project (GitHub `Jakubantalik/transitions.dev`, its own "Transitions.dev License"). Its README and https://transitions.dev/skill.html document this install command; the vault has not audited that code. Scan it first with the vault's `scanning-agent-skills` skill, then install, pinned to the commit that was the repo's HEAD when this skill was written (it has no release tags):

```
npx skills add Jakubantalik/transitions.dev@20d70c1262bf721c0300c2946cbe1fc7605a555c --skill transitions-dev
```

The `owner/repo@<tag-or-commit>` pin and `--skill` form come from the `skills` CLI reference (https://github.com/vercel-labs/skills/blob/main/docs/commands.md). Upstream's own unpinned form is `npx skills add Jakubantalik/transitions.dev`; the same repo also ships a `transitions-ui-generation` skill that the unpinned command installs too. Upstream says the skill includes a library of 27+ transitions and adds commands such as `transitions reveal`, `transitions review` and `transitions apply`. Do not run the `npx transitions-dev ...` commands on that page: they are a separate npm package, and the Pro ones sign in through a browser.

## Pitfalls

- Screenshotting a whole page and asking Claude to "make it like this" produces a copy, not an adaptation — always say "match the decisions"
- godly.design is curated; if you paste a random production site, quality varies
- animos.app is browser-only; works best for simple looping demos, not complex interactive flows

## Source

- https://instagram.com/p/Ddqj0svm6yq/ — @nocodealex, 2026-09-24 (the four sites; it names no install command)
- https://transitions.dev/skill.html and https://raw.githubusercontent.com/Jakubantalik/transitions.dev/main/README.md — install command, read 2026-11-10
