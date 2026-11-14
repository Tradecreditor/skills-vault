---
name: modernizing-web-code-with-guidance
description: Steers coding agents toward modern web platform APIs using the Modern Web Guidance CLI (search guides, retrieve one, scan for legacy patterns). Use when writing or reviewing frontend CSS, HTML or JS that may rely on legacy patterns or heavy polyfills.
metadata:
  source_url: "https://github.com/GoogleChrome/modern-web-guidance"
  source_platform: "github"
  author: "GoogleChrome"
  origin_type: "repo"
  vault_status: "draft"
---

# modernizing-web-code-with-guidance

Draft, from the repo README. Verify commands against the upstream docs before relying on them.

1. Search for a relevant guide: `npx modern-web-guidance@latest search "<what you are building>"`.
2. Read one guide by ID: `npx modern-web-guidance@latest retrieve "<guide-id>"`.
3. Prefer the platform feature the guide recommends (View Transitions, container queries, Anchor Positioning, Popover API, `scheduler.yield`) over a library or polyfill; keep fallbacks lightweight.
4. To audit an existing project: `npx modern-web-guidance@latest legacy-scan .` and review each finding before changing code.
5. Optional persistent install: `npx modern-web-guidance@latest install` (interactive; run only with the user's consent).

Source: https://github.com/GoogleChrome/modern-web-guidance
