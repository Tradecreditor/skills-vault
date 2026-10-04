# Skill review: model-tiering — FAIL

- Reviewed: 2026-10-04T15:35:29Z by the `vault-skill-reviewer` subagent (Opus), one skill per subagent; first run, from a Claude Code cloud session following `routines/skill-review.md` before the Routine existed
- Status set: `draft`
- Content hash: `83e5bb68182b63012b777f0ed9af13a35fb49398313b02190443bc19bf905b7d`
- Static scan (`static_scan.py 2`): 0 block, 0 review findings; review rules none
- SkillSpector: not installed
- Gate (routine step 4): not ok/acceptable: S2; reviewer verdict FAIL
- Not audited (upstream): Anthropic Claude API advisor tool (beta header advisor-tool-2026-03-01, tool type advisor_20260301, documented at platform.claude.com; the reference was fetched 2026-07-11): not checked against the live doc. TypeSafe Jev, reached through skills/judging-with-jev (draft): not audited.

## 摘要
唔過關。描述話用嚟揀 Claude 模型，但內文會叫 agent 將大量判斷送去第三方嘅 TypeSafe Jev API，描述完全冇提（S2）。喺其他 project 用，資料會送去用家冇同意過嘅外部服務。要喺描述講明 Jev，或者將嗰部分搬去 `judging-with-jev`。

## Reviewer verdict
```json
{
  "skill": "model-tiering",
  "verdict": "FAIL",
  "content_hash": "83e5bb68182b63012b777f0ed9af13a35fb49398313b02190443bc19bf905b7d",
  "static": {
    "block": 0,
    "review_rules": []
  },
  "skillspector": "not installed",
  "rules": {},
  "checklist": {
    "S1": "acceptable: references/advisor-tool.md contains fenced system-prompt blocks and an '(Advisor: ...)' line addressed to the executor/advisor models. They are labelled templates to embed in API requests, not text aimed at the agent reading the skill. There are no HTML comments or hidden text, and all non-ASCII characters are visible punctuation.",
    "S2": "fail: the Part A table row (line 30) and Part C (lines 70-74) tell the agent to 'ask Jev first', which routes bulk yes/no/choice/score judgments over item contents to TypeSafe's Jev, a third-party non-Claude API. The description only promises to pick 'the Claude model tier' (Fable/Opus vs Sonnet) and never mentions Jev, so in another project this would send data to an outside provider the user did not opt into.",
    "S3": "acceptable: this folder makes no network call and names no host. Its only outbound path is the hand-off to Jev through the separate judging-with-jev skill (itself vault_status draft), which defines the endpoint and payload and must be reviewed there (see S2).",
    "S4": "ok",
    "S5": "ok",
    "S6": "ok",
    "S7": "ok",
    "S8": "ok",
    "S9": "acceptable: the triggers 'spawning subagents' and 'writing code that calls the Claude API' are broad and overlap the built-in claude-api skill. They are tied to choosing a model and effort level, and the skill claims no slash command and no other skill's name.",
    "S10": "acceptable: the skill makes no claim to be official, verified or audited. The description leaving out Jev is counted under S2. The body's internal contradictions are accuracy errors, reported under quality, not misrepresentation."
  },
  "quality": "Needs Improvement",
  "critical": [],
  "upstream": "Anthropic Claude API advisor tool (beta header advisor-tool-2026-03-01, tool type advisor_20260301, documented at platform.claude.com; the reference was fetched 2026-07-11): not checked against the live doc. TypeSafe Jev, reached through skills/judging-with-jev (draft): not audited.",
  "summary": "The static scan is clean (no block findings, no review rules) and the folder ships no scripts, installs or credentials. It fails S2 because Part A and Part C send bulk judgments to TypeSafe's third-party Jev API, which the 'Claude model tier' description never mentions. Also fix the Haiku/Sonnet swaps that contradict the reference (SKILL.md lines 68 and 85) and the 'Opus 5' / 'Fable 5.1' advisor pairings (lines 63-65), which are missing from the reference's valid-pair table; then name Jev in the description or move Part C into judging-with-jev, and re-review."
}
```
