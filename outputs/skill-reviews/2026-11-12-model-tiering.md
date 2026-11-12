# Skill review: model-tiering (2026-11-12)

**Verdict: PASS**

- Reviewed by: routine:skill-review (independent `vault-skill-reviewer` subagent, verdict checked by the routine)
- Content hash (H): `d49c630788a67befcfca6099f74554dafb7711098013ac1719026875eec48571`
- Static scan: floor `NEEDS_REVIEW`, block findings 0, review findings 0, review rules none (-)
- SkillSpector: not installed

## Verdict JSON
```json
{
  "skill": "model-tiering",
  "verdict": "PASS",
  "content_hash": "d49c630788a67befcfca6099f74554dafb7711098013ac1719026875eec48571",
  "static": {"block": 0, "review_rules": []},
  "skillspector": "not installed",
  "rules": {},
  "checklist": {
    "S1": "acceptable: the only text written to a model is in references/advisor-tool.md: two fenced example system-prompt blocks and a Haiku nudge, shown as templates for the user's own executor prompts in API code. They are referenced from SKILL.md and do not address the reader, reviewer or routine.",
    "S2": "ok",
    "S3": "ok",
    "S4": "ok",
    "S5": "ok",
    "S6": "ok",
    "S7": "ok",
    "S8": "ok",
    "S9": "ok",
    "S10": "ok"
  },
  "quality": "Pass",
  "critical": [],
  "upstream": "Claude API advisor tool (platform.claude.com advisor-tool doc, beta advisor-tool-2026-03-01), summarised from a 2026-07-11 fetch: not re-verified",
  "summary": "Text-only guidance (SKILL.md plus one reference, no scripts) on choosing Claude model tiers, effort levels and the advisor tool. It has no network, credential, install or configuration actions, and every linked file exists. The quality notes are minor: the name is not a gerund, some wording is personal ('my projects', Hermes), and the model IDs and beta details will go out of date."
}
```

## 說明
通過。純文字指引（SKILL.md 加一個 reference 檔），講點樣揀 Claude 模型等級、effort 同 advisor tool；冇網絡、憑證、安裝或者設定改動，靜態掃描冇任何發現。未審核部分：Claude API advisor tool 文件（2026-07-11 擷取嘅摘要，未再核實），模型 ID 同 beta 細節日後可能過時。
