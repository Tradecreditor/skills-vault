---
name: saving-tokens-with-caveman
description: Explains how to install and use JuliusBrussee/caveman to cut agent token use (short replies, compressed tool output, model routing). Use when reducing coding-agent token cost, shortening replies, or compressing CLAUDE.md memory files.
metadata:
  source_url: "https://github.com/JuliusBrussee/caveman"
  source_platform: "github"
  author: "JuliusBrussee"
  captured_at: "2026-11-10T06:06:37Z"
  engagement: "stars=118720 forks=6906"
  origin_type: "repo"
  vault_status: "draft"
---
# Saving tokens with caveman

Caveman (Apache-2.0) shortens agent replies, shrinks what agents read, and routes models. Notes: `wiki/stars/JuliusBrussee--caveman.md`.

## Install (review before running; it edits agent configs)
- Skill only: `npx skills add JuliusBrussee/caveman -g`
- Claude Code plugin: `/plugin marketplace add JuliusBrussee/caveman` then `/plugin install caveman@caveman`
- Full CLI: `npx @caveman-ai/cli@latest` (Node.js 22.13+); `caveman status` shows what is on; `caveman off <part>` disables one.

## Use
- `/caveman` answers short, code and paths stay verbatim; `/ultracave` is terser. Say `stop caveman` to return to normal.
- `/caveman-compress <file>` shrinks memory files such as `CLAUDE.md` and keeps a backup.
- Auto (model/effort routing) needs a free account (`caveman login`) and sends data to the service; check the README privacy section first.

## Caveats
Figures (33.2% fewer input tokens, 54% cheaper Auto) are the project's own; the Auto run was interim. Do not install from a draft skill in other projects.
