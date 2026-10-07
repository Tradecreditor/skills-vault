# Skill review: judging-with-jev — PASS

- Reviewed: 2026-10-07T16:04:28Z by the `vault-skill-reviewer` subagent, one skill per subagent, from a Claude Code cloud session following `routines/skill-review.md` (the skill's files changed: the owner's name was corrected to Jeff)
- Status set: `reviewer-approved`
- Content hash: `6992a8e98995ef7f71cd1bff7563a1f6713095b4dc7975df10a093617ddb61c9`
- Static scan (`static_scan.py 4`): 0 block, 19 review findings; review rules R5, R6, R8, R11
- SkillSpector: not installed
- Gate (routine step 4): all ok/acceptable; reviewer verdict PASS
- Not audited (upstream): TypeSafe Jev System One API (api.typesafe.ai/v1/systemone; gateways ai-gateway.vercel.sh/typesafe and openrouter.ai/api): not audited. Its API details come from third-party mirrors (jevwiki.ai, and jevmodel.org, which SKILL.md also lists as a look-alike reseller), not from an official TypeSafe document.

## 摘要
過關。靜態掃描冇 block；附帶嘅 `jev_ask.py` 只用標準庫，只從環境變數讀 `TYPESAFE_API_KEY`，只將精簡內容送去 TypeSafe 或列明嘅 gateway。今次只係將擁有人名改做 Jeff，令 hash 變咗，所以重審。品質方面有幾處小矛盾（proxy credential 兩處講法唔同、報告門檻 3.5 對 2.5、`JEV_FAKE` 路徑）未改。冇審：TypeSafe Jev API 本身。

## Reviewer verdict
```json
{
  "skill": "judging-with-jev",
  "verdict": "PASS",
  "content_hash": "6992a8e98995ef7f71cd1bff7563a1f6713095b4dc7975df10a093617ddb61c9",
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
    "R5": "acceptable: scripts/jev_ask.py makes one urllib POST to <base_url>/v1/systemone. The default is api.typesafe.ai, which matches the endpoint in the independent raw/20260920-fast-jev-compaction.md. The only other hosts are the named Vercel AI Gateway and OpenRouter gateways. It sends trimmed state only.",
    "R6": "acceptable: TYPESAFE_API_KEY is read only from the environment (jev_ask.py:97) and sent as a Bearer header to the configured base_url host. It is never printed, logged or written. SKILL.md mentions the variable by name only, and jev_ask.py:39-43 are regexes that block secret-looking state before any request.",
    "R8": "acceptable: SKILL.md:34 only notes that a project .claude/settings.json allow rule does not get past the auto-mode classifier. Nothing in the skill writes settings, hooks, MCP servers or memory files.",
    "R11": "acceptable: scripts/jev_ask.py (209 lines, standard library only) was read in full. It does what SKILL.md describes: secret and size check, one POST, band thresholds, exit codes 0/2/3/4, and canned answers from JEV_FAKE. It has no eval, subprocess or shell."
  },
  "checklist": {
    "S1": "ok",
    "S2": "ok",
    "S3": "acceptable: trimmed state (README heads, post snippets, summaries from the public vault) goes to TypeSafe or the two named gateways, which is the skill's purpose. --base-url and JEV_BASE_URL accept any host, but nothing in the skill points them elsewhere, and it warns against look-alike resellers.",
    "S4": "acceptable: the key comes from the environment only and is never echoed. The curl example names $TYPESAFE_API_KEY but does not contain its value, and the body tells the agent to call the script instead.",
    "S5": "ok",
    "S6": "ok",
    "S7": "acceptable: the skill changes no permission mode, hook, MCP server or memory file. After an auto-mode classifier denial it moves the key off the command line into the script. The script call still goes through normal classification and prompts, and a denial is treated as Jev being off for that run, with no retry or workaround.",
    "S8": "acceptable: there are no deletes, scheduled jobs or startup entries. It only suggests the user keep TYPESAFE_API_KEY in their own shell profile.",
    "S9": "ok",
    "S10": "acceptable: calibration and price claims are credited to dated sources. API details come from third-party mirrors (jevwiki.ai, jevmodel.org) and the skill says so. The old review record on a draft does not claim approval."
  },
  "quality": "Needs Improvement",
  "critical": [],
  "upstream": "TypeSafe Jev System One API (api.typesafe.ai/v1/systemone; gateways ai-gateway.vercel.sh/typesafe and openrouter.ai/api): not audited. Its API details come from third-party mirrors (jevwiki.ai, and jevmodel.org, which SKILL.md also lists as a look-alike reseller), not from an official TypeSafe document.",
  "summary": "Static scan found no block findings; the bundled standard-library client jev_ask.py does what SKILL.md says, reads TYPESAFE_API_KEY only from the environment and sends trimmed state only to TypeSafe or the named gateways. Every referenced file exists and there are no critical issues. Quality fixes: SKILL.md:30 and :117 contradict each other on proxy-injected credentials, the report line in references/vault-routine-questions.md:88 says >=3.5 where the act threshold is 2.5, and JEV_FAKE=references/jev-fake.example.json does not resolve from the vault root."
}
```
