# Skill review: tracking-projects-in-notion (2026-11-11)

**Verdict: FAIL** (routine:skill-review, 2026-11-11T07:50:23Z)

Re-review: the content changed since the 2026-10-07 review (review_hash ae26b8c4… → ab2c5085…).

## Static scan
- floor: NEEDS_REVIEW; block findings: 0; review findings: 50
- review_rules: R2 (2), R4 (2), R5 (8), R6 (36), R8 (1), R11 (1)
- SkillSpector: not installed

## Reviewer verdict
```json
{
  "skill": "tracking-projects-in-notion",
  "verdict": "FAIL",
  "content_hash": "ab2c50858db5f26f519638493c1642c68af94b38ac97fe5abfdbf6c1c81034a0",
  "static": {"block": 0, "review_rules": ["R2", "R4", "R5", "R6", "R8", "R11"]},
  "skillspector": "not installed",
  "rules": {
    "R2": "acceptable: joining-projects-hq.md step 0a shallow-clones the vault's own repo (github.com/Tradecreditor/skills-vault) into a temp dir only to read status lines and compare review hashes; nothing from it is installed",
    "R4": "acceptable: notion-sync.py line 775 runs a fixed argv `git config --get remote.origin.url` with no shell and no interpolated input",
    "R5": "acceptable: all requests go to https://api.notion.com (NOTION_API_BASE override limited to 127.0.0.1/localhost, redirects refused), which is the API the skill is about",
    "R6": "acceptable: NOTION_TOKEN is read from the environment, sent only as a Bearer header to the API base, scrubbed from every message, never printed; docs forbid echoing it and warn against dotfiles repos",
    "R8": "fail: references/board-policy.md section 1 (lines 19-28) and joining-projects-hq.md step 3.3 tell any session in a project whose CLAUDE.md/AGENTS.md/GEMINI.md lacks a Projects HQ block to write that block into the instruction file (creating the file if missing) before other work, explicitly 'No separate ask to Jeff is needed' / 'without asking', reporting only afterwards; the change is not shown first and the description does not declare it",
    "R11": "acceptable: scripts/notion-sync.py (939 lines, stdlib only) read in full; it does what SKILL.md says (one-way sync filtered by Source, read-only audit, no deletes/archives, no schema changes) and is byte-identical to the vault's scripts/notion-sync.py"
  },
  "checklist": {
    "S1": "ok",
    "S2": "acceptable: Notion writes, handoff edits and the vault clone are all part of the declared board/sync/onboarding purpose",
    "S3": "acceptable: only handoff In flight rows go to api.notion.com, the declared destination; audit output prints only this source's card titles",
    "S4": "acceptable: token only from NOTION_TOKEN; user sets it in OS env or a shell profile with a not-tracked-by-git warning; never asked in chat",
    "S5": "acceptable: no package installs; the script is copied from a vault clone only after a review_hash check",
    "S6": "ok",
    "S7": "fail: board-policy.md section 1 (Jeff 2026-11-10 rule) and joining-projects-hq.md step 3.3 have the agent append a Projects HQ rules block to the project's CLAUDE.md / AGENTS.md / GEMINI.md, creating the file if absent, without showing the change first or asking ('No separate ask to Jeff is needed'). It triggers in any new project session that loads the policy, not only during an explicit join. The repo join path (steps 5-7) does confirm with Jeff first and would be fine on its own",
    "S8": "acceptable: nothing is deleted or archived; the select-option restate (which can wipe options) is fenced by fetch-fresh / restate-all / re-verify / stop-and-tell-Jeff",
    "S9": "ok",
    "S10": "acceptable: claims match the code; but the description does not mention that the skill writes agent instruction files on its own initiative"
  },
  "quality": "Needs Improvement",
  "critical": [],
  "upstream": "Notion REST API (api.notion.com) and the Notion MCP connector: not audited",
  "summary": "Static floor NEEDS_REVIEW with no block findings, and the sync script is clean and stays within Notion. FAIL on S7/R8: the 2026-11-10 board-policy rule (board-policy.md section 1, echoed in joining-projects-hq.md step 3.3) has agents append a rules block to CLAUDE.md/AGENTS.md/GEMINI.md in any new project without asking or showing the change first. To fix it, require showing the block and getting confirmation before writing (as the repo join's step 6 already does), and declare the instruction-file write in the description."
}
```

## 說明
唔通過。靜態掃描冇封鎖級發現，notion-sync.py 亦乾淨，只連 api.notion.com。問題喺 2026-11-10 新加嘅規則：references/board-policy.md 第 1 節同 joining-projects-hq.md 第 3.3 步，叫任何新項目嘅 session 喺 CLAUDE.md／AGENTS.md／GEMINI.md 冇 Projects HQ 段落時，自行寫入（冇檔就新建），而且明寫「唔使問 Jeff」，事前唔顯示改動，description 亦冇講明會改 agent 指令檔（S7／R8 fail）。修正方法：寫入前先顯示段落並取得確認（好似 repo join 第 6 步咁），同埋喺 description 講明會寫指令檔。未審核部分（upstream）：Notion REST API 同 Notion MCP connector。
