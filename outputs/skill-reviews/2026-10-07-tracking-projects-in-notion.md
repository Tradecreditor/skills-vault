# Skill review: tracking-projects-in-notion — PASS

- Reviewed: 2026-10-07T17:52:41Z by the `vault-skill-reviewer` subagent, one skill per subagent, from a Claude Code cloud session following `routines/skill-review.md` (first review; the skill gained `references/joining-projects-hq.md` and a copy of `notion-sync.py`)
- Status set: `reviewer-approved`
- Content hash: `ae26b8c4da7095986a74feeef74a0f66b33959a48212bc908b695761e328c627`
- Static scan (`static_scan.py 4`): 0 block, 49 review findings; review rules R2, R4, R5, R6, R11
- SkillSpector: not installed
- Gate (routine step 4): all ok/acceptable; reviewer verdict PASS
- Not audited (upstream): Not audited: the Notion REST API (api.notion.com, Notion-Version 2026-03-11) and how the Notion MCP connector handles the CREATE TABLE / ALTER COLUMN statements. The join guide clones this vault's own repo (github.com/Tradecreditor/skills-vault) and runs its auditing-agent-skills static_scan.py, which was not re-audited here
- Before this review the joining guide went through nine rounds of independent walk-throughs and regression checks (session `01JCZqXBeWf7rDXGKbkNoWUB`); earlier PASS verdicts on intermediate versions were superseded by later edits.

## 摘要
過關。靜態掃描冇 block；`notion-sync.py` 全文讀過，只用標準庫，token 只會送去 api.notion.com，唔會刪卡，只改自己 Source 嘅卡，同 vault 嗰份逐字相同（有 test 保證）。新加嘅入門指引（`references/joining-projects-hq.md`）要 Jeff 確認先寫任何檔，私人卡名唔會入公開 repo，加 Notion option 前會重新攞清單再核對。品質建議：SKILL.md 太長（約 4,700 字），可以將 script 細節搬去 references。冇審：Notion REST API 本身，同 Notion connector 點樣處理 ALTER COLUMN。

## Reviewer verdict
```json
{
  "skill": "tracking-projects-in-notion",
  "verdict": "PASS",
  "content_hash": "ae26b8c4da7095986a74feeef74a0f66b33959a48212bc908b695761e328c627",
  "static": {
    "block": 0,
    "review_rules": [
      "R2",
      "R4",
      "R5",
      "R6",
      "R11"
    ]
  },
  "skillspector": "not installed",
  "rules": {
    "R2": "acceptable: nothing is installed from a package manager. The only flagged lines are a depth-1 git clone of this vault's own public repo (github.com/Tradecreditor/skills-vault) into a temp folder in the join guide, followed by read-only status and hash checks before anything is copied. The script uses only the standard library",
    "R4": "acceptable: there is one subprocess.run with a fixed argument list ['git','config','--get','remote.origin.url'], no shell and a 10 s timeout, and its output is only parsed for owner and repo. There is no eval or exec anywhere",
    "R5": "acceptable: urllib and http.client go only to https://api.notion.com. NOTION_API_BASE is refused unless it is http://127.0.0.1:<port> or http://localhost:<port>, and a NoRedirect handler refuses every redirect. Requests carry only the handoff In flight fields the description says it mirrors",
    "R6": "acceptable: NOTION_TOKEN is read only from the environment and sent only as the Bearer header to the API base. It is checked to be printable ASCII, scrubbed from every error and log line, and never printed. The docs forbid echoing it, give set/missing checks that do not reveal it, and never ask for it in chat",
    "R11": "acceptable: scripts/notion-sync.py (939 lines, standard library only) was read in full. It does what SKILL.md documents: parse handoff.md, create and patch only pages with its own Source, run a read-only --audit, no delete or archive, no local file writes. It is byte-identical to the vault's scripts/notion-sync.py (sha256 c04e554e...), and scripts/test_notion_sync.py asserts that"
  },
  "checklist": {
    "S1": "acceptable: references/joining-projects-hq.md is addressed to 'an agent working in one of Jeff's projects', and the exit table in SKILL.md says what 'a Routine' does with each code. Both are the declared purpose (SKILL.md links the guide as the onboarding runbook; the Routines run the scheduled sync and audit). Neither targets the reviewer or asks for anything to be hidden. There are no HTML comments, hidden Unicode or override phrases",
    "S2": "ok",
    "S3": "ok",
    "S4": "ok",
    "S5": "acceptable: there are no package installs. The join clones main of this vault's own repo (depth 1, not pinned) but copies the script only after both skills' review_hash values match, and it records the commit id. The only vault code it runs before that check is the reviewer-approved static_scan.py --hash under python3 -I. That scanner checks its own hash, so the check rests on push restrictions to main, which the guide says openly",
    "S6": "ok",
    "S7": "acceptable: onboarding adds a Projects HQ block to the joining project's CLAUDE.md, AGENTS.md or GEMINI.md, which is the declared onboarding purpose (SKILL.md 'Onboarding another project'). The block is drafted in chat (step 5) and written only after Jeff confirms the files (step 6). It never rewrites existing text, and for a repo that is not Jeff's it goes only into an untracked local file. Routine setup adds only api.notion.com to the cloud environment's allowed domains. No permission modes, hooks or MCP servers are touched",
    "S8": "acceptable: nothing is deleted: the script has no DELETE or archive calls, and cards are only set to Done or Dropped, for its own Source only. The riskiest step is restating a Notion select option list, where any option left out disappears from every card. It is needed to add an Area and is guarded: fetch a fresh list, restate all of it, verify afterwards, and stop and tell Jeff if anything is lost. Jeff adds the NOTION_TOKEN line to his shell profile by hand, with a warning about dotfiles repos. The skill creates no cron or startup entries",
    "S9": "ok",
    "S10": "ok"
  },
  "quality": "Needs Improvement",
  "critical": [],
  "upstream": "Not audited: the Notion REST API (api.notion.com, Notion-Version 2026-03-11) and how the Notion MCP connector handles the CREATE TABLE / ALTER COLUMN statements. The join guide clones this vault's own repo (github.com/Tradecreditor/skills-vault) and runs its auditing-agent-skills static_scan.py, which was not re-audited here",
  "summary": "PASS: no block findings (static floor NEEDS_REVIEW), SkillSpector is not installed, and a full read of all four files found the token confined to api.notion.com, no deletes, and every CLAUDE.md or AGENTS.md write waiting for Jeff's confirmation. Quality (advisory) is Needs Improvement: SKILL.md is about 4,700 words and repeats the policy and WIP rules from board-policy.md and CLAUDE.md, so the script details (parsing rules, flags, exit codes, retry behaviour) could move to a references file."
}
```
