# Skill review: keeping-handoff-docs — FAIL

- Reviewed: 2026-10-04T15:35:29Z by the `vault-skill-reviewer` subagent (Opus), one skill per subagent; first run, from a Claude Code cloud session following `routines/skill-review.md` before the Routine existed
- Status set: `draft`
- Content hash: `36d0139cf19663afaf5c0fbdff4e123d2ef9b3c337c16db41cd2b340c79f4fec`
- Static scan (`static_scan.py 2`): 0 block, 2 review findings; review rules R2, R6
- SkillSpector: not installed
- Gate (routine step 4): not ok/acceptable: S7; reviewer verdict FAIL
- Not audited (upstream): skills CLI (npm package `skills`, run via npx, unpinned): not audited

## 摘要
唔過關。「喺其他 project 安裝」嗰段叫 agent 喺人哋嘅 CLAUDE.md／AGENTS.md 加規則，但描述冇講，亦冇叫 agent 改之前先俾用家睇（S7）。要喺描述講明呢一步，再改成用家明確要求先做，跟住再審。

## Reviewer verdict
```json
{
  "skill": "keeping-handoff-docs",
  "verdict": "FAIL",
  "content_hash": "36d0139cf19663afaf5c0fbdff4e123d2ef9b3c337c16db41cd2b340c79f4fec",
  "static": {
    "block": 0,
    "review_rules": [
      "R2",
      "R6"
    ]
  },
  "skillspector": "not installed",
  "rules": {
    "R2": "acceptable: `npx skills add Tradecreditor/skills-vault --skill keeping-handoff-docs` installs this skill from its own source repository via the skills CLI, run by the user; unpinned",
    "R6": "acceptable: line 41 only forbids putting secrets, tokens, cookies or personal data in handoff.md and says to name where a credential lives; nothing reads, prints or writes a credential"
  },
  "checklist": {
    "S1": "ok",
    "S2": "acceptable: reading, updating and committing handoff.md serve the description; the rules-file edit in the install section is judged under S7",
    "S3": "ok",
    "S4": "ok",
    "S5": "acceptable: the only install is this skill from its own repo via the skills CLI from npm, user-run, though not version-pinned",
    "S6": "ok",
    "S7": "fail: 'Installing the SOP in another project' step 2 tells the agent to add rules to the project's CLAUDE.md / AGENTS.md so that 'the rule enforces itself'. The description never declares this. There is no step to show the change to the user or wait for their request, and the broad 'starting work in a repo' trigger lets it reach repos that never adopted the SOP",
    "S8": "ok",
    "S9": "acceptable: the triggers are broad by design for a start-of-session and end-of-session SOP, and the start action is read-only. No built-in command or other skill's triggers are claimed. It should still be narrowed to repos that already have handoff.md or to an explicit install request (see S7)",
    "S10": "acceptable: the claims match the content and the cited repo files exist (handoff.md, outputs/20261003-jev-pilots-handoff.md, routines/README.md); 'the rule enforces itself' mildly overstates what an instruction line can guarantee"
  },
  "quality": "Needs Improvement",
  "critical": [],
  "upstream": "skills CLI (npm package `skills`, run via npx, unpinned): not audited",
  "summary": "The skill has no block findings, no scripts, no network use and no hidden content, but its install section adds rules to other projects' CLAUDE.md/AGENTS.md without declaring this in the description or asking the user first (S7). To fix it, name the install in the description, gate step 2 on an explicit user request that shows the two lines first, and say what to do in a repo with no handoff.md. The quality issues are minor: the template's 'How to update' has 4 rules where SKILL.md says five, and it has no slot for the 'proven / not yet proven' lists."
}
```
