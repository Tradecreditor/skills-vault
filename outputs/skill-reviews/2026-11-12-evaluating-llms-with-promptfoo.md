# Skill review: evaluating-llms-with-promptfoo (2026-11-12)

**Verdict: PASS**

- Reviewed by: routine:skill-review (independent `vault-skill-reviewer` subagent, verdict checked by the routine)
- Content hash (H): `1a046af3d94ed935f161233ff3704243d1b4d0a2121809368e5399eee5119152`
- Static scan: floor `NEEDS_REVIEW`, block findings 0, review findings 5, review rules R2, R6 (R2×3, R6×2)
- SkillSpector: not installed

## Verdict JSON
```json
{
  "skill": "evaluating-llms-with-promptfoo",
  "verdict": "PASS",
  "content_hash": "1a046af3d94ed935f161233ff3704243d1b4d0a2121809368e5399eee5119152",
  "static": {"block": 0, "review_rules": ["R2", "R6"]},
  "skillspector": "not installed",
  "rules": {
    "R2": "acceptable: SKILL.md lines 34-40 install the official promptfoo package under its own name (npm promptfoo, brew promptfoo, pip promptfoo) or run npx promptfoo@latest. These are the tool's documented channels, run by the user's agent with normal prompts. The packages are not pinned, and npm -g is a global install that the description does not mention; npx is offered as a no-install alternative.",
    "R6": "acceptable: lines 53-54 are placeholder exports (sk-..., sk-ant-...) that set provider keys as environment variables. Nothing prints, logs, writes or commits the keys."
  },
  "checklist": {
    "S1": "ok",
    "S2": "ok",
    "S3": "acceptable: the skill sends prompts and test cases only to the model providers the user configures. It discloses share URLs, telemetry and hosted remote generation (PROMPTFOO_DISABLE_REMOTE_GENERATION) and tells the user to check them before using sensitive data.",
    "S4": "ok",
    "S5": "acceptable: every install names the official promptfoo package. None is pinned, and the global npm install is not mentioned in the description, but it is the tool's own documented install path.",
    "S6": "ok",
    "S7": "ok",
    "S8": "ok",
    "S9": "ok",
    "S10": "ok"
  },
  "quality": "Needs Improvement",
  "critical": [],
  "upstream": "promptfoo (npm/brew/PyPI package promptfoo, github.com/promptfoo/promptfoo): not audited",
  "summary": "The skill is a single SKILL.md with no scripts and no block findings. It installs promptfoo only from the official promptfoo packages, takes API keys from environment variables, and discloses where data goes. Quality is advisory: someone should check that the step 7 flag `promptfoo eval --fail-on-error` exists, because the text right after it says eval already exits 100 on failure. The 'When to use' section is written in second person, which the reviewer criteria advise against."
}
```

## 說明
通過。只有一個 SKILL.md，冇 script，冇 block 級發現；只會由 promptfoo 官方套件（npm / brew / PyPI）安裝，API key 只從環境變數讀取，亦有講明資料會傳去邊度。品質評為「Needs Improvement」（屬建議性質）：第 7 步嘅 --fail-on-error 參數值得核實。未審核部分：promptfoo 上游套件同 repo。
