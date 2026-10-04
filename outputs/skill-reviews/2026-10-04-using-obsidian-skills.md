# Skill review: using-obsidian-skills — FAIL

- Reviewed: 2026-10-04T15:35:29Z by the `vault-skill-reviewer` subagent (Opus), one skill per subagent; first run, from a Claude Code cloud session following `routines/skill-review.md` before the Routine existed
- Status set: `draft`
- Content hash: `d4a8bb800c9398cb95a4f8ea4af61a1ff809c2e8096fee4b40d950957f5c42ce`
- Static scan (`static_scan.py 2`): 0 block, 6 review findings; review rules R2, R8
- SkillSpector: not installed
- Gate (routine step 4): not ok/acceptable: S9; reviewer verdict FAIL
- Not audited (upstream): kepano/obsidian-skills (github.com/kepano/obsidian-skills; Claude Code plugin obsidian@obsidian-skills), the skills CLI (npm package skills), and the prerequisites Defuddle (github.com/kepano/defuddle) and Knap (github.com/obsidianmd/knap): not audited

## 摘要
唔過關。觸發條件太闊：喺 Obsidian vault 入面編輯任何 .md 都會觸發，但內文淨係教人裝一個未審查嘅第三方套件，仲同 `vault-capture` 重疊（S9）。收窄描述就可以再審。

## Reviewer verdict
```json
{
  "skill": "using-obsidian-skills",
  "verdict": "FAIL",
  "content_hash": "d4a8bb800c9398cb95a4f8ea4af61a1ff809c2e8096fee4b40d950957f5c42ce",
  "static": {
    "block": 0,
    "review_rules": [
      "R2",
      "R8"
    ]
  },
  "skillspector": "not installed",
  "rules": {
    "R2": "acceptable: all five lines (SKILL.md 42, 43, 49, 51, 59) install kepano/obsidian-skills from its own GitHub repo, which is the skill's source_url and matches raw/20260918-obsidian-skills.md. They use user-typed /plugin commands, the skills CLI (npx skills) or git clone. None is pinned to a tag or commit.",
    "R8": "acceptable: line 65 copies the upstream skills/ folder into Codex's skills directory, which is the install the description declares. It writes no settings, hooks, MCP servers or memory files."
  },
  "checklist": {
    "S1": "ok",
    "S2": "ok",
    "S3": "acceptable: the only network destinations are github.com/kepano/obsidian-skills and the npm registry (for npx skills), and nothing from the vault or the chat is sent",
    "S4": "ok",
    "S5": "acceptable: every install names the official kepano/obsidian-skills repo, but none is pinned to a tag or commit, and npx skills has no version",
    "S6": "ok",
    "S7": "acceptable: files are written only into skill discovery folders (.claude/ in the vault root, ~/.codex/skills, ~/.opencode/skills), which is the declared purpose. Two caveats: Option C writes '/.claude', which reads as the filesystem root, and .claude/ is a protected path in this vault.",
    "S8": "acceptable: the skill makes persistent installs into home-directory skill folders, which is its declared purpose. It has no deletes, cron jobs or shell-profile edits.",
    "S9": "fail: the description says 'Use when editing .md/.base/.canvas files, using Obsidian CLI, or scraping web pages inside a vault'. In an Obsidian vault (this repo is one), that covers nearly every task, so the skill would load on routine note edits and captures, and the only action its body gives is installing an unaudited third-party pack. 'Scraping web pages inside a vault' also overlaps vault-capture, whose reader order CLAUDE.md fixes, and defuddle is not in that order.",
    "S10": "ok"
  },
  "quality": "Needs Improvement",
  "critical": [],
  "upstream": "kepano/obsidian-skills (github.com/kepano/obsidian-skills; Claude Code plugin obsidian@obsidian-skills), the skills CLI (npm package skills), and the prerequisites Defuddle (github.com/kepano/defuddle) and Knap (github.com/obsidianmd/knap): not audited",
  "summary": "There are no block findings, and every install points at kepano's official repo, but the triggers cover any .md/.base/.canvas edit or web scraping inside a vault, which here means nearly every task, while the body only installs an unaudited third-party pack (S9 fail). Fix: narrow the description to installing obsidian-skills or setting up an agent for an Obsidian vault when the pack is missing, add a step that checks whether it is already installed, and drop the scraping trigger that overlaps vault-capture. Minor: Option C's '/.claude' should read '.claude/' at the vault root, Option E may end up as skills/skills, the installs are unpinned, and the body says little about how to apply the skills once installed."
}
```
