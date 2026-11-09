---
description: Record this project's installed skills and plugins in Jeff's Skill Installs database in Notion (run after installing or removing a skill)
argument-hint: "[--global] [notes]"
---
Record which agent skills and Claude Code plugins are installed in this project in my Notion database "Skill Installs"
(page "Skills HQ"). The how-to is the vault skill
https://raw.githubusercontent.com/Tradecreditor/skills-vault/main/skills/tracking-skill-installs-in-notion/SKILL.md.
My name is Jeff.

The script to run is this plugin's own copy: `${CLAUDE_PLUGIN_ROOT}/scripts/skills-inventory.py` (the plugin is the
skills-vault repository itself, so no file is copied into this project). If that path did not expand or does not exist, use
the newest `~/.claude/plugins/cache/tradecreditor-vault/skills-vault/<version>/scripts/skills-inventory.py`; do not download
the script from anywhere else.

Steps:
1. `python3 <script> --root "<this project's root directory>" --dry-run` (Windows: `py -3`). Always pass `--root`: without it the
   script scans the plugin folder, not this project. Read the plan it prints (rows, created / updated / removed).
2. If it looks right, run it again without `--dry-run`. If my notes below say `--global`, also run
   `python3 <script> --global --project "global:<a short name for this computer>"` once.
3. `NOTION_TOKEN` must be set in this environment; never print, echo or export it. Exit 2 means the run is off for a setup
   reason (the line names it): report it and stop, do not retry more than once. Exit 3 means this project's `skills-lock.json`
   is unreadable: say so.
4. Report the summary line(s) verbatim, and which skills were created, updated or marked Removed. Nothing in this project is
   written or committed by this command.

Notes from Jeff for this run (may be empty): $ARGUMENTS
