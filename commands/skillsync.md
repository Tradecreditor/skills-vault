---
description: Record this project's installed skills and plugins in Jeff's Skill Installs database in Notion (run after installing or removing a skill)
argument-hint: "[--global] [notes]"
---
Record which agent skills and Claude Code plugins are installed in this project in my Notion database "Skill Installs"
(page "Skills HQ"). Follow the vault skill
https://raw.githubusercontent.com/Tradecreditor/skills-vault/main/skills/tracking-skill-installs-in-notion/SKILL.md.
My name is Jeff.

Steps:
1. Review check, on a fresh clone made outside this repository (never run vault code before it passes): the skill's
   `vault_status` must be `reviewer-approved` or `verified`, and
   `python3 -I <clone>/skills/auditing-agent-skills/scripts/static_scan.py --hash <clone>/skills/tracking-skill-installs-in-notion`
   must equal its `review_hash` (hash `auditing-agent-skills` first and compare it too, as
   skills/tracking-projects-in-notion/references/joining-projects-hq.md step 0 does). If either fails, stop and tell me.
2. If this project has no `scripts/skills-inventory.py`, copy it from that clone's
   `skills/tracking-skill-installs-in-notion/scripts/skills-inventory.py`, and add one line to this project's `handoff.md`
   "Environment facts": `skills-inventory.py copied from skills-vault <clone commit> (reviewed)`. Commit it with the inventory
   run below (in a PR-only repository, open the PR).
3. Run `python3 scripts/skills-inventory.py --dry-run`, then `python3 scripts/skills-inventory.py`. If my notes below say
   `--global`, also run `python3 scripts/skills-inventory.py --global --project "global:<a short name for this computer>"`.
   `NOTION_TOKEN` must be set in this environment; never print, echo or export it. Exit 2 means the run is off for a setup
   reason (the line names it): report it and stop, do not retry more than once.
4. Report the summary line(s) verbatim, and which skills were created, updated or marked Removed.

Notes from Jeff for this run (may be empty): $ARGUMENTS
