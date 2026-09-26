# Routine: vault-lint
Trigger: Schedule, weekly. Cron is evaluated in **UTC**. `0 2 * * 1` = Monday 10:00 HKT; `0 9 * * 1` = Monday 10:00 CET. The last field is the day of week (1 = Monday); leaving it `*` makes this run every day, which has happened.
A web-form preset is read in your BROWSER's timezone instead. Confirm against the next-run time shown after saving. Model: Sonnet. Repo: Tradecreditor/skills-vault. Pushes the report to main; opens a PR only when it proposes merges or renames.

## Prompt (paste verbatim)
You are the weekly lint routine for Josep's skills vault. The repository Tradecreditor/skills-vault is checked out. Let WEEK be this ISO week (e.g. 2026-W38).

Check, without modifying any content pages:
1. Catalogue integrity: every wiki/pages/*.md and wiki/stars/*.md has a row in wiki/index.md and vice versa; every row resolves to a file (a slug of the form <owner>--<repo> -> wiki/stars/<slug>.md; a date-prefixed slug <yyyymmdd>-... -> wiki/pages/<slug>.md; type is NOT the discriminator - a repo captured by pasting its link is type: repo and still lives in wiki/pages/, see the folder table in CLAUDE.md); canonical_id column present and unique; frontmatter has all required keys from CLAUDE.md; captured_at parses; status is draft|verified|deprecated.
2. Raw coverage: every page's slug has a raw/<slug>*.md unless needs_manual_text is true.
3. Skills: for each skills/*/SKILL.md, name == folder, description present, under 300 chars, contains "Use when"; body under 500 lines; metadata values are strings; vault_status present. (You may run bash scripts/vault-guard-check.sh HEAD~1 HEAD Tradecreditor for the mechanical part.)
4. Links: broken [[wikilinks]] and relative links; orphan pages (no inbound links and not in hot.md); pages with an empty ## Related.
5. Duplicates: two pages with the same canonical_id or the same source_url; near-duplicate titles.
6. Staleness: draft entries older than 30 days (list them for Josep to review); needs_manual_text pages older than 14 days.
7. Hygiene: files outside the allowed folders; anything that looks like a secret (tokens, cookies) anywhere in the repo; wiki/hot.md 最近 20 項 longer than 20 lines.

Write outputs/health/WEEK.md with a summary table (check, count, status), then one section per check listing the offending files, then a ## Suggested fixes section.
Apply only safe mechanical fixes yourself: add missing index rows, trim hot.md to 20 lines, add a missing ## Related heading. Do not merge, rename, delete or rewrite pages.
If you believe two entries should be merged or a file renamed, describe it in ## Suggested fixes and open a PR titled "lint: WEEK proposals" with the proposed edits on branch lint/WEEK instead of applying them.
Commit: git add -A; git commit -m "lint: WEEK"; git pull --rebase origin main; git push origin HEAD:main.
Append "## [date] lint | WEEK | outputs/health/WEEK" to wiki/log.md as part of that commit.
Final message: counts per check and the three most important items for Josep to look at.

NEVER delete or rename files. NEVER touch raw/.
