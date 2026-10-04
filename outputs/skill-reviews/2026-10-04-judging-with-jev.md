# Skill review: judging-with-jev — PASS

- Reviewed: 2026-10-04T15:35:29Z by the `vault-skill-reviewer` subagent (Opus), one skill per subagent; first run, from a Claude Code cloud session following `routines/skill-review.md` before the Routine existed
- Status set: `reviewer-approved`
- Content hash: `639d4e71371d8110f280ccbe29561ade3e4f306be071500f85bfca89a1e338fa`
- Static scan (`static_scan.py 2`): 0 block, 19 review findings; review rules R5, R6, R8, R11
- SkillSpector: not installed
- Gate (routine step 4): all checks passed
- Not audited (upstream): TypeSafe Jev System One API (api.typesafe.ai; gateways ai-gateway.vercel.sh/typesafe and openrouter.ai/api): remote service, not audited; API reference taken from the third-party mirror jevwiki.ai

## 摘要
過關。自帶嘅 209 行 Python client 只會將資料同 `TYPESAFE_API_KEY` 送去設定好嘅 TypeSafe 主機，唔會印出金鑰，見到疑似機密嘅內容仲會拒絕送出。建議限制 `--base-url` 只准用三個官方主機。冇審查到嘅部分：TypeSafe 遠端服務本身。

## Reviewer verdict
```json
{
  "skill": "judging-with-jev",
  "verdict": "PASS",
  "content_hash": "639d4e71371d8110f280ccbe29561ade3e4f306be071500f85bfca89a1e338fa",
  "static": {
    "block": 0,
    "review_rules": [
      "R5",
      "R6",
      "R8",
      "R11"
    ]
  },
  "skillspector": "not installed",
  "rules": {
    "R5": "acceptable: the only network call is urllib POST to <base_url>/v1/systemone, default https://api.typesafe.ai (the vendor's own host, corroborated by the independent raw/20260920-fast-jev-compaction.md capture), with Vercel AI Gateway and OpenRouter named as alternative gateways for the same model",
    "R6": "acceptable: TYPESAFE_API_KEY is read only from the environment, sent only as a Bearer header to the configured base_url, and never printed, logged or written; SECRET_PATTERNS is a local filter that refuses secret-looking state and reports only the pattern name; SKILL.md lines are warnings against putting keys in state, on Bash lines or in the repo",
    "R8": "acceptable: false positive; line 30 only notes that a project .claude/settings.json allow rule does not bypass the auto-mode classifier, and nothing in the skill writes settings, hooks, MCP config or memory files",
    "R11": "acceptable: scripts/jev_ask.py is 209 lines of stdlib Python, read in full; no subprocess, eval or shell, fixed request shape, and it does what SKILL.md describes (probe/ask, band rule, exit codes 0/2/3/4, JEV_FAKE canned answers)"
  },
  "checklist": {
    "S1": "ok",
    "S2": "ok",
    "S3": "acceptable: state is trimmed item metadata (titles, snippets, README heads, summaries from a public vault) sent to the vendor or two named gateways, with a local secret filter; --base-url / JEV_BASE_URL accept any host, so an allowlist of the three documented hosts would harden it",
    "S4": "ok",
    "S5": "ok",
    "S6": "ok",
    "S7": "acceptable: no permission mode, hook, MCP server or memory file is changed. The user is asked to add the single host api.typesafe.ai to the cloud environment's allowlist. After an auto-mode 'Data Exfiltration' denial the key was moved off the Bash line into the script. That is defensible because the destination is the key's own issuer and the skill says a denial means Jev is off for the run, not that the agent should retry around it. The 'visibly sends' wording on line 121 still reads as classifier avoidance and should be reworded as plain secret hygiene",
    "S8": "ok",
    "S9": "acceptable: 'a routine step is a judgment' is broad, but naming the external TypeSafe Jev API and the vault-specific examples (type/topic tags, hot-list prefilter, near-duplicates) narrow it; it claims no built-in command or other skill's triggers",
    "S10": "acceptable: the calibration claim ('a 0.8 is right about 80% of the time') is the vendor's, stated as fact, and the API details come from a third-party mirror (jevwiki.ai) and from jevmodel.org, which the skill itself lists as a look-alike reseller. Both sources are labelled third-party, the endpoint is corroborated by recorded real runs and an independent upstream README, and vault_status is honestly draft"
  },
  "quality": "Needs Improvement",
  "critical": [],
  "upstream": "TypeSafe Jev System One API (api.typesafe.ai; gateways ai-gateway.vercel.sh/typesafe and openrouter.ai/api): remote service, not audited; API reference taken from the third-party mirror jevwiki.ai",
  "summary": "No block findings. The 209-line stdlib client sends the state and TYPESAFE_API_KEY only to the configured base_url (default api.typesafe.ai), refuses secret-looking state and never prints the key; keeping the key off the Bash line after an auto-mode denial is acceptable because any denial still means Jev is off. Advisory fixes: restrict --base-url to the three documented hosts and reword 'visibly sends'; also fix JEV_FAKE=references/jev-fake.example.json, which is relative to the skill folder rather than the repo root where the commands run, and lines 26-27, which contradict line 113 on proxy-injected credentials."
}
```
