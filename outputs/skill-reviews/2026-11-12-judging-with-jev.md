# Skill review: judging-with-jev (2026-11-12)

**Verdict: PASS**

- Reviewed by: routine:skill-review (independent `vault-skill-reviewer` subagent, verdict checked by the routine)
- Content hash (H): `0b0c575189475a2edb81a7220caa2f66c6dd2e8a05729282ed1ce3882da845ce`
- Static scan: floor `NEEDS_REVIEW`, block findings 0, review findings 19, review rules R5, R6, R8, R11 (R5×5, R6×12, R8×1, R11×1)
- SkillSpector: not installed

## Verdict JSON
```json
{
  "skill": "judging-with-jev",
  "verdict": "PASS",
  "content_hash": "0b0c575189475a2edb81a7220caa2f66c6dd2e8a05729282ed1ce3882da845ce",
  "static": {"block": 0, "review_rules": ["R5", "R6", "R8", "R11"]},
  "skillspector": "not installed",
  "rules": {
    "R5": "acceptable: the only network call is jev_ask.py POSTing state+questions to <base_url>/v1/systemone, default https://api.typesafe.ai (the API this skill is about); the curl in SKILL.md is documentation of the same wire format; JEV_BASE_URL/--base-url can redirect it, and SKILL.md names the three legitimate hosts and warns against look-alike resellers",
    "R6": "acceptable: TYPESAFE_API_KEY is read only from the environment and sent only as the Bearer header on that request; it is never printed, logged or written to a file; the SECRET_PATTERNS lines are a local refusal filter that reports pattern names only, never matched text",
    "R8": "acceptable: line 34 only states that a project .claude/settings.json allow rule does not bypass the auto-mode classifier; the skill writes no agent configuration and tells the reader not to work around a denial (a denial means Jev is off for that run)",
    "R11": "acceptable: scripts/jev_ask.py (215 lines, stdlib only) was read in full and does what SKILL.md says: kill switch, input validation, secret/size refusal, one POST, response normalisation, banding, exit codes 0/2/3/4, and canned answers under JEV_FAKE; no eval, no subprocess, no shell, and it writes no files"
  },
  "checklist": {
    "S1": "ok",
    "S2": "ok",
    "S3": "acceptable: state data goes to the Jev API by design; the skill tells callers to send trimmed data fields only, never secrets or whole raw/ files, and the script refuses state that looks like it holds a secret",
    "S4": "ok",
    "S5": "ok",
    "S6": "ok",
    "S7": "acceptable: it discusses the auto-mode permission classifier only to explain why the key must stay off the command line; it changes no permission, hook, MCP or memory-file settings and does not tell the agent to get around a denial",
    "S8": "ok",
    "S9": "ok",
    "S10": "ok"
  },
  "quality": "Pass",
  "critical": [],
  "upstream": "TypeSafe Jev System One API (api.typesafe.ai; optionally via Vercel AI Gateway or OpenRouter): remote service, not audited",
  "summary": "The static floor is NEEDS_REVIEW with no block findings, and every R5/R6/R8/R11 flag fits a skill that calls one declared decision API through a short stdlib script that never exposes the key. All referenced files exist. One minor note: the key goes to whatever JEV_BASE_URL is set to, and the JEV_FAKE example path is relative to the skill folder, not the vault root."
}
```

## 說明
通過。冇 block 級發現；scripts/jev_ask.py（215 行，只用標準庫）已完整閱讀：只向 Jev API（預設 api.typesafe.ai）發一個 POST，API key 只從環境變數讀、只放喺 Bearer header，唔會印出或寫入檔案，並會拒絕似含秘密嘅輸入。R5/R6/R8/R11 都符合用途。未審核部分：TypeSafe Jev System One 遠端服務。注意 JEV_BASE_URL 可改變 key 送去嘅地址。
