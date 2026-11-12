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
  vault_status: "reviewer-approved"
  reviewed_at: "2026-11-12T07:51:49Z"
  reviewed_by: "routine:skill-review"
  review_hash: "78b15525add465fd5f974fc100f2c8c4c43ae8526381ddf28719a7e7916c7f87"
  review_report: "outputs/skill-reviews/2026-11-12-providing-design-references.md"
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

transitions.dev is a third-party project (GitHub `Jakubantalik/transitions.dev`, its own "Transitions.dev License"). Its README and https://transitions.dev/skill.html document the install as `npx skills add Jakubantalik/transitions.dev`; the vault has not audited that code. That command is unpinned and installs every skill the repo ships (`transitions-dev`, `transitions-polish`, `transitions-ui-generation`). To install only `transitions-dev`, from a commit you have scanned, clone the repo at the commit that was its HEAD when this skill was written (2026-11-08; it has no release tags), scan the clone with the vault's `scanning-agent-skills` skill, then install from the clone:

```
git clone https://github.com/Jakubantalik/transitions.dev
git -C transitions.dev checkout 20d70c1262bf721c0300c2946cbe1fc7605a555c
npx skills@1.7.6 add ./transitions.dev --skill transitions-dev
```

Do not pin with `owner/repo@<commit>`: `skills` 1.7.6 accepts that form but installs the default branch whatever follows the `@` (tested 2026-11-10: a ref that does not exist installs without an error), so it gives no pin. The local-path and `--skill` forms are in the `skills` CLI reference (https://github.com/vercel-labs/skills/blob/main/docs/commands.md); the `skills@1.7.6` version is this skill's addition. Upstream says the skill includes a library of 27+ transitions and adds commands such as `transitions reveal`, `transitions review` and `transitions apply`. Do not run the `npx transitions-dev ...` commands on that page: they are a separate npm package, and the Pro ones sign in through a browser.

## Pitfalls

- Screenshotting a whole page and asking Claude to "make it like this" produces a copy, not an adaptation — always say "match the decisions"
- godly.design is curated; if you paste a random production site, quality varies
- animos.app is browser-only; works best for simple looping demos, not complex interactive flows

## Source

- https://instagram.com/p/Ddqj0svm6yq/ — @nocodealex, 2026-09-24 (the four sites; it names no install command)
- https://transitions.dev/skill.html and https://raw.githubusercontent.com/Jakubantalik/transitions.dev/main/README.md — install command, read 2026-11-10
