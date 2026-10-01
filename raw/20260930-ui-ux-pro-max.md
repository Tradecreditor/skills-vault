---
slug: 20260930-ui-ux-pro-max
source_url: "https://github.com/nextlevelbuilder/ui-ux-pro-max-skill"
canonical_id: "github:nextlevelbuilder/ui-ux-pro-max-skill"
fetched_at: "2026-09-30T20:26:00Z"
reader: "raw.githubusercontent.com (GitHub API blocked by session proxy; raw content fetched directly)"
---
{"repo": "nextlevelbuilder/ui-ux-pro-max-skill", "description": "An AI skill that provides design intelligence for building professional UI/UX across multiple platforms and frameworks", "stars": "unknown (GitHub REST API blocked by session proxy — non-attached repo)", "note": "Metadata fetched from README.md via raw.githubusercontent.com"}

# [UI UX Pro Max](https://uupm.cc)

An AI skill that provides design intelligence for building professional UI/UX across multiple platforms and frameworks.

## What's New in v2.0

### Intelligent Design System Generation

The flagship feature of v2.0 is the **Design System Generator** - an AI-powered reasoning engine that analyzes your project requirements and generates a complete, tailored design system in seconds.

### 192 Industry-Specific Reasoning Rules

The reasoning engine includes specialized rules for:

| Category | Examples |
|----------|----------|
| **Tech & SaaS** | SaaS, Micro SaaS, B2B Service, Developer Tool / IDE, AI/Chatbot Platform, Cybersecurity Platform |
| **Finance** | Fintech/Crypto, Banking, Insurance, Personal Finance Tracker, Invoice & Billing Tool |
| **Healthcare** | Medical Clinic, Pharmacy, Dental, Veterinary, Mental Health, Medication Reminder |
| **E-commerce** | General, Luxury, Marketplace (P2P), Subscription Box, Food Delivery |
| **Services** | Beauty/Spa, Restaurant, Hotel, Legal, Home Services, Booking & Appointment |
| **Creative** | Portfolio, Agency, Photography, Gaming, Music Streaming, Photo/Video Editor |
| **Lifestyle** | Habit Tracker, Recipe & Cooking, Meditation, Weather, Diary, Mood Tracker |
| **Emerging Tech** | Web3/NFT, Spatial Computing, Quantum Computing, Autonomous Drone Fleet |

## Features

- **79 Searchable UI Styles (50 active)** - Glassmorphism, Claymorphism, Minimalism, Brutalism, Neumorphism, Bento Grid, Dark Mode, AI-Native UI, and more
- **192 Color Palettes** - Industry-specific palettes aligned 1:1 with the 192 product types
- **74 Font Pairings** - Curated typography combinations with Google Fonts imports
- **25 Chart Types** - Recommendations for dashboards and analytics
- **22 Tech Stacks** - React, Next.js, Astro, Vue, Nuxt.js, Nuxt UI, Svelte, SwiftUI, React Native, Flutter, HTML+Tailwind, shadcn/ui, Jetpack Compose, Angular, Laravel, Three.js, JavaFX, WPF, WinUI 3, UWP, Avalonia, Uno Platform
- **119 UX Guidelines** - Best practices, anti-patterns, accessibility rules, resilient text layout, compact labels, and cancellable interactions
- **192 Reasoning Rules** - Industry-specific design system generation (NEW in v2.0)

## Installation

### Using Claude Marketplace (Claude Code)

```
/plugin marketplace add nextlevelbuilder/ui-ux-pro-max-skill
/plugin install ui-ux-pro-max@ui-ux-pro-max-skill
```

### Using CLI (Recommended)

```bash
# Install CLI globally
npm install -g ui-ux-pro-max-cli

# Go to your project
cd /path/to/your/project

# Install for your AI assistant
uipro init --ai claude      # Claude Code
uipro init --ai cursor      # Cursor
uipro init --ai windsurf    # Windsurf
uipro init --ai antigravity # Antigravity
uipro init --ai copilot     # GitHub Copilot
uipro init --ai kiro        # Kiro
uipro init --ai codex       # Codex CLI
uipro init --ai gemini      # Gemini CLI
uipro init --ai all         # All assistants
```

### Global Install (Available for All Projects)

```bash
npm install -g ui-ux-pro-max-cli
uipro init --ai claude --global
```

## Style Taxonomy

The catalog contains **79 searchable styles** backed by stable IDs and aliases:

| Status | Count | Search behavior |
|--------|------:|-----------------|
| Active | 50 | Included in normal recommendations and shown by default in the gallery |
| Supplemental | 29 | Returned for exact or explicit variant/system intent |
| Deprecated | 9 | Excluded from normal ranking |

## Premium vs Basic

**Basic (Open Source):** 79 UI styles, 192 product types, BM25 search, 22 frameworks, Design System Generation CLI.
**Premium:** Brand Identity, Logo Design, CIP, AI-image generation assets, Enterprise Design Tokens, Priority Support.

## License

MIT License
