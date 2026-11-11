# Skill review: tracking-skill-installs-in-notion (2026-11-11)

**Verdict: PASS** (routine:skill-review, 2026-11-11T07:50:23Z)

Re-review: the content changed after the 2026-11-10 approval (review_hash 6cce53cc… → 06f74a6e…), so the skill went back to draft and through review again.

## Static scan
- floor: NEEDS_REVIEW; block findings: 0; review findings: 40
- review_rules: R2 (4), R4 (2), R5 (8), R6 (14), R8 (11), R11 (1)
- SkillSpector: not installed

## Reviewer verdict
```json
{
  "skill": "tracking-skill-installs-in-notion",
  "verdict": "PASS",
  "content_hash": "06f74a6ecdedb522676af1d0f01650d9b97381677695482638a975a04b8d2b34",
  "static": {"block": 0, "review_rules": ["R2", "R4", "R5", "R6", "R8", "R11"]},
  "skillspector": "not installed",
  "rules": {
    "R2": "acceptable: these are prose mentions of the user's own `npx skills add/remove` and `/plugin install` commands as the events that trigger an inventory run; the skill installs nothing itself",
    "R4": "acceptable: the only subprocess is the fixed argument list `git config --get remote.origin.url` (no shell, 10 s timeout), used to label the project",
    "R5": "acceptable: urllib calls go only to https://api.notion.com, the declared purpose; NOTION_API_BASE may only point at 127.0.0.1/localhost, and redirects are refused so the Authorization header never leaves Notion",
    "R6": "acceptable: NOTION_TOKEN is read from the environment, sent only as a Bearer header to the API base, removed from every message, never written to disk, and no traceback is ever printed",
    "R8": "acceptable: the flagged lines only read agent configuration (settings.json enabledPlugins, installed_plugins.json, known_marketplaces.json, skill folders) to list installs; nothing in agent config is written",
    "R11": "acceptable: the script was read in full (1054 lines, stdlib only) and does what SKILL.md describes: collect installs, plan, then create/patch Notion rows, enrich and audit; it never deletes or archives; it is byte-identical to the vault's scripts/skills-inventory.py (sha256 f764985a...)"
  },
  "checklist": {
    "S1": "ok",
    "S2": "ok",
    "S3": "acceptable: skill names, project labels, hostname-derived global labels and plugin ids are sent only to the user's private Notion database, which is the declared purpose",
    "S4": "ok",
    "S5": "ok",
    "S6": "ok",
    "S7": "acceptable: the plugin hooks (hooks/hooks.json, SessionStart/PostToolUse) are documented as existing vault plugin machinery outside this folder; the skill does not tell the agent to add hooks or change permissions",
    "S8": "acceptable: nothing is deleted (stale rows become Removed). The script writes only fingerprint and lock files under ~/.cache/skills-inventory (or SKILLS_INVENTORY_STATE), and the optional shell-profile env var is a user step tied to the declared purpose",
    "S9": "ok",
    "S10": "acceptable: SKILL.md line 75 and the script docstring say 'nothing on disk is ever written', but every non-dry-run sync creates a lock file and --if-changed writes a fingerprint under ~/.cache/skills-inventory. Lines 165-177 of the same file disclose both, so this is an inaccuracy, not concealment"
  },
  "quality": "Needs Improvement",
  "critical": [],
  "upstream": "Notion REST API (api.notion.com), not audited. The plugin files the skill describes (hooks/hooks.json, hooks/skill-install-sync.sh/.ps1, commands/skillsync.md) are outside this folder and were not audited. All of them exist on disk.",
  "summary": "The static floor is NEEDS_REVIEW with no block findings, and the script and SKILL.md were read in full: it reads local install records and writes only to the user's Notion database through NOTION_TOKEN, which is handled carefully (Notion host only, redirects refused, token scrubbed). Every referenced file exists, the description is 297 characters and contains 'Use when', and the body is 238 lines. Advisory fixes: correct the 'nothing on disk is ever written' claim (SKILL.md line 75 and the script docstring) to mention the ~/.cache lock and fingerprint files, and consider moving the long flag, exit-code and hook tables into references/."
}
```

## 說明
今次係重審：上次批准之後內容有改（script 加咗 OS 檔案鎖等），所以先退返 draft 再審。靜態掃描冇封鎖級發現；審查者讀晒 SKILL.md 同 1054 行 Python script，確認佢只讀本機嘅 skill／plugin 安裝紀錄、只連 api.notion.com、拒絕轉址、NOTION_TOKEN 只由環境變數讀而且唔會印出或寫入磁碟，亦唔會刪除任何嘢，所以判定通過。質素評級係「Needs Improvement」（非嚴重）：文件話「唔會寫磁碟」，但其實會喺 ~/.cache/skills-inventory 寫鎖檔同指紋檔（同一份文件其他段落有講明）。未審核部分（upstream）：Notion REST API，以及資料夾以外嘅 vault plugin 檔案（hooks/hooks.json、hooks/skill-install-sync.sh/.ps1、commands/skillsync.md）。
