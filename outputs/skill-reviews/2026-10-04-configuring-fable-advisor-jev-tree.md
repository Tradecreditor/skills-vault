# Skill review: configuring-fable-advisor-jev-tree — FAIL

- Reviewed: 2026-10-04T15:35:29Z by the `vault-skill-reviewer` subagent (Opus), one skill per subagent; first run, from a Claude Code cloud session following `routines/skill-review.md` before the Routine existed
- Status set: `draft`
- Content hash: `5636bb9d2f04edcccada9855c9d38ef40bde74f258cea59987cbb5eda121c1a5`
- Static scan (`static_scan.py 2`): 0 block, 3 review findings; review rules R8
- SkillSpector: not installed
- Gate (routine step 4): not ok/acceptable: S9, S10; 1 critical quality issue(s); reviewer verdict FAIL
- Not audited (upstream): Claude Code advisor feature (code.claude.com/docs/en/advisor): the /advisor command, the advisorModel and effortLevel settings keys, the CLAUDE_CODE_DISABLE_ADVISOR_TOOL and CLAUDE_CODE_EFFORT_LEVEL env vars and the subagent 'effort' field were copied from the source post and not checked against the docs; not audited

## 摘要
唔過關。安全方面冇問題（改設定之前會先出 diff，等用家批准），但個名同描述都講有「Jev 路由」，內文完全冇教點樣設定 Jev，仲會搶走 `judging-with-jev` 嘅觸發（S9、S10、critical）。要補返 Jev 步驟，或者另開一個唔包 Jev 嘅 skill，先可以再審。

## Reviewer verdict
```json
{
  "skill": "configuring-fable-advisor-jev-tree",
  "verdict": "FAIL",
  "content_hash": "5636bb9d2f04edcccada9855c9d38ef40bde74f258cea59987cbb5eda121c1a5",
  "static": {
    "block": 0,
    "review_rules": [
      "R8"
    ]
  },
  "skillspector": "not installed",
  "rules": {
    "R8": "acceptable: the three flagged lines (36, 42, 46) are the pasted setup prompt reading/drafting ~/.claude/agents, setting effortLevel and advisorModel in ~/.claude/settings.json, and adding one advisor rule to ~/.claude/CLAUDE.md. Configuring Claude Code is the declared purpose, and the prompt requires a diff and an explicit 'go' before any edit"
  },
  "checklist": {
    "S1": "ok",
    "S2": "acceptable: the global ~/.claude/CLAUDE.md rule is not named in the description, but it serves the advisor setup and is gated behind a diff",
    "S3": "acceptable: the skill makes no network calls. It labels DISABLE_TELEMETRY and feature-flag blockers as advisor blockers but only reports them, so turning telemetry back on stays the user's choice",
    "S4": "ok",
    "S5": "ok",
    "S6": "ok",
    "S7": "acceptable: it writes user-global settings.json, agents and CLAUDE.md, which is its declared purpose, and it shows every change as a diff and waits for approval first",
    "S8": "ok",
    "S9": "fail: 'adding Jev routing to a Claude Code session' is a trigger that matches nothing in the body. It would pull Jev-routing requests away from judging-with-jev, the vault skill that actually covers Jev",
    "S10": "fail: the name, description and line 16 promise a 'Jev-routed multi-agent tree' with 'Jev handling routing decisions', but Jev is never defined, configured or listed in the agent tree table. The source post mentions Jev only as a conceptual aside"
  },
  "quality": "Needs Improvement",
  "critical": [
    "SKILL.md description and line 16: the skill promises Jev routing and lists 'adding Jev routing' as a trigger, but no step, table row or reference covers Jev. An agent triggered for that task would have to guess. Fix: add real Jev steps (for example by pointing to judging-with-jev), or deprecate this skill and draft a non-Jev skill under a new folder, since files cannot be renamed"
  ],
  "upstream": "Claude Code advisor feature (code.claude.com/docs/en/advisor): the /advisor command, the advisorModel and effortLevel settings keys, the CLAUDE_CODE_DISABLE_ADVISOR_TOOL and CLAUDE_CODE_EFFORT_LEVEL env vars and the subagent 'effort' field were copied from the source post and not checked against the docs; not audited",
  "summary": "The static floor is NEEDS_REVIEW, with no block findings and three acceptable R8 config writes gated behind a diff. The skill fails because its name and description advertise Jev routing that the body never defines or configures (S9, S10, critical). The advisor and subagent setup itself is faithful to the source and safe."
}
```
