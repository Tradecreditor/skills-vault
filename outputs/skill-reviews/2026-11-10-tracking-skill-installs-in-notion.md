# Skill review: tracking-skill-installs-in-notion (2026-11-10)

**Verdict: PASS** (routine:skill-review, 2026-11-10T07:49:51Z)

## Static scan
- floor: NEEDS_REVIEW; block findings: 0; review findings: 40
- review_rules: R2 (4), R4 (2), R5 (8), R6 (14), R8 (11), R11 (1)
- SkillSpector: not installed

## Reviewer verdict
```json
{
  "skill": "tracking-skill-installs-in-notion",
  "verdict": "PASS",
  "content_hash": "6cce53cc177a5a19c73698c5bbdae7445307117dfba2157a6dbd07e261671bc4",
  "static": {"block": 0, "review_rules": ["R2", "R4", "R5", "R6", "R8", "R11"]},
  "skillspector": "not installed",
  "rules": {
    "R2": "acceptable: these lines only mention `npx skills add` and `claude plugin install` as the events being recorded and the hook's match pattern. The skill installs nothing itself.",
    "R4": "acceptable: the only subprocess call is a fixed argument list, `git config --get remote.origin.url`, with no shell and a 10 s timeout. It is used to get the project label.",
    "R5": "acceptable: the script only contacts api.notion.com. NOTION_API_BASE accepts only 127.0.0.1 or localhost. Redirects are refused (NoRedirect), so the Authorization header cannot be forwarded to another host.",
    "R6": "acceptable: NOTION_TOKEN is read only from the environment and sent only as a Bearer header. It is scrubbed from every message, tracebacks are suppressed, and it is never written to disk.",
    "R8": "acceptable: every flagged line reads agent configuration (settings.json enabledPlugins, installed_plugins.json, known_marketplaces.json, skill folders). None of them writes it. This matches the stated purpose of inventorying installs.",
    "R11": "acceptable: I read all 979 lines of the Python file. It is standard library only and does what SKILL.md says: it collects data, plans, then creates or patches Notion rows. It never deletes or archives. It is byte-identical to the vault's scripts/skills-inventory.py (sha256 b187ed2a...)."
  },
  "checklist": {
    "S1": "ok",
    "S2": "ok",
    "S3": "acceptable: Notion receives skill names, project or repo names, lockfile sources and hashes, and by default a hostname-based global label. The skill states all of this, and Notion is the declared destination.",
    "S4": "ok",
    "S5": "ok",
    "S6": "ok",
    "S7": "acceptable: the skill documents the vault plugin's existing PostToolUse and SessionStart hooks (hooks/hooks.json, which is outside this folder). It does not add, change or install any hook or setting itself.",
    "S8": "acceptable: the only persistent things are --if-changed fingerprint files under ~/.cache/skills-inventory, which are disclosed. The other is an optional SKILLS_INVENTORY_GLOBAL_LABEL environment variable that the user sets on their own. Nothing is deleted, and Notion rows only become Removed.",
    "S9": "ok",
    "S10": "acceptable: SKILL.md line 71 and the script docstring say nothing is ever written to disk, but --if-changed writes fingerprint files. Both files disclose that elsewhere (SKILL.md line 161, docstring lines 20-22), so this is a wording inconsistency, not a hidden action."
  },
  "quality": "Pass",
  "critical": [],
  "upstream": "Notion REST API (api.notion.com); skills CLI (github.com/vercel-labs/skills) and Claude Code plugin records are only read, not installed: not audited. Vault files referenced but outside this folder (hooks/skill-install-sync.sh/.ps1, commands/skillsync.md, scripts/test_skills_inventory.py) exist but were not reviewed.",
  "summary": "No block findings. The script only reads local skill and plugin records, sends rows only to api.notion.com with an environment-only token that is scrubbed from all output, and never deletes anything. Minor issues (advisory): 'nothing on disk is ever written' ignores the disclosed ~/.cache fingerprint files, and the in-skill copy's default --root is the skill folder, so run it from the vault's scripts/ path or pass --root."
}
```

## 說明
靜態掃描冇封鎖級發現；審查者讀晒成個 979 行嘅 Python script，確認佢只係讀取本機嘅 skill 同 plugin 安裝紀錄，只會連去 api.notion.com，NOTION_TOKEN 只從環境變數讀、唔會印出或寫入磁碟，亦永遠唔會刪除任何嘢，同描述一致，所以判定通過。小問題：文件話「唔會寫入磁碟」，但 --if-changed 會喺 ~/.cache 寫指紋檔（其他段落有講明）；skill 內嘅 script 預設 --root 係 skill 資料夾，要由 vault 嘅 scripts/ 行或者加 --root。未審核部分（upstream）：Notion REST API、skills CLI（vercel-labs/skills），以及資料夾以外嘅 vault 檔案（hooks/skill-install-sync.*、commands/skillsync.md、scripts/test_skills_inventory.py）。
