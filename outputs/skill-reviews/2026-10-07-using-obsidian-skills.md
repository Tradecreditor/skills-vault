# Skill review: using-obsidian-skills — FAIL

- Reviewed: 2026-10-07T16:04:28Z by the `vault-skill-reviewer` subagent, one skill per subagent, from a Claude Code cloud session following `routines/skill-review.md` (the skill's files changed: the owner's name was corrected to Jeff)
- Status set: `draft`
- Content hash: `c91c7b03fa42fe33d7a82e2c93fed9b26768883061ecada214083ed694554cd2`
- Static scan (`static_scan.py 4`): 0 block, 6 review findings; review rules R2, R8
- SkillSpector: not installed
- Gate (routine step 4): not ok/acceptable: S9; reviewer verdict FAIL
- Not audited (upstream): kepano/obsidian-skills (github.com/kepano/obsidian-skills; Claude Code plugin obsidian@obsidian-skills), the skills CLI (npm package skills), and the prerequisites Defuddle (github.com/kepano/defuddle) and Knap (github.com/obsidianmd/knap): not audited

## 摘要
唔過關，原因同 2026-10-04 一樣：描述觸發條件太闊（vault 入面編輯任何 .md 都觸發），而內文淨係教人裝一個未審查嘅第三方套件，仲同 `vault-capture` 重疊（S9）。今次只改咗擁有人名，冇修正呢個問題。收窄描述先可以再審。

## Reviewer verdict
```json
{
  "skill": "using-obsidian-skills",
  "verdict": "FAIL",
  "content_hash": "c91c7b03fa42fe33d7a82e2c93fed9b26768883061ecada214083ed694554cd2",
  "static": {
    "block": 0,
    "review_rules": [
      "R2",
      "R8"
    ]
  },
  "skillspector": "not installed",
  "rules": {
    "R2": "acceptable: lines 46, 47, 53, 55 and 63 install kepano/obsidian-skills from its own GitHub repo. They use /plugin commands the user types, npx skills or git clone, and they match the upstream README in raw/20260918-obsidian-skills.md. None is pinned to a tag or commit.",
    "R8": "acceptable: line 69 copies the upstream skills/ folder into Codex's skills directory, which is the install the description declares. It writes no settings, hooks, MCP servers or memory files. It may produce ~/.codex/skills/skills/ because the wording drops upstream's 'into your Codex skills path'."
  },
  "checklist": {
    "S1": "ok",
    "S2": "ok",
    "S3": "acceptable: the only destinations are github.com/kepano/obsidian-skills and the npm registry for npx skills. Nothing from the vault or the chat is sent.",
    "S4": "ok",
    "S5": "acceptable: every install names the official kepano/obsidian-skills repo, but none is pinned and npx skills has no version. The Defuddle and Knap prerequisites are only linked, with no install command.",
    "S6": "ok",
    "S7": "acceptable: files are written only into skill-discovery folders (the vault's .claude/, ~/.codex/skills, ~/.opencode/skills), which is the declared purpose. However, Option C's '/.claude' reads as the filesystem root, and .claude/ is a protected path in this vault.",
    "S8": "acceptable: it makes persistent installs into home-directory skill folders as declared. There are no deletes, schedules or shell-profile edits.",
    "S9": "fail: /home/user/skills-vault/skills/using-obsidian-skills/SKILL.md line 3 says 'Use when editing .md/.base/.canvas files, using Obsidian CLI, or scraping web pages inside a vault'. Inside an Obsidian vault (this repo is one) that matches nearly every task, while the body's only action is installing an unaudited third-party pack. 'Scraping web pages inside a vault' also overlaps the verified vault-capture skill, whose reader order CLAUDE.md fixes. This is unchanged from the 2026-10-04 FAIL.",
    "S10": "acceptable: line 74 says skills stay draft 'until Jeff reviews', which is out of date because the skill-review routine has done reviews since 2026-10-04. The other claims match the upstream README."
  },
  "quality": "Needs Improvement",
  "critical": [],
  "upstream": "kepano/obsidian-skills (github.com/kepano/obsidian-skills; Claude Code plugin obsidian@obsidian-skills), the skills CLI (npm package skills), and the prerequisites Defuddle (github.com/kepano/defuddle) and Knap (github.com/obsidianmd/knap): not audited",
  "summary": "No block findings, and every install points at kepano's official repo, but the description still triggers on any .md/.base/.canvas edit or web scraping inside a vault, which overlaps vault-capture while the body only installs an unaudited pack (S9 fail, same as the 2026-10-04 review). Fix: narrow the triggers to installing or setting up obsidian-skills when it is missing, add a check for an existing install, and drop the scraping trigger. Minor: '/.claude' should read '.claude/' at the vault root, the Codex copy may nest skills/skills, the installs are unpinned, the 'until Jeff reviews' line is out of date, and the body says little about applying the skills."
}
```
