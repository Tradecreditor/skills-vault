# Skill review: stacking-coding-agent-plugins (2026-11-07)

**Verdict: FAIL** (stays `draft`)

- Reviewer: `vault-skill-reviewer` subagent, run by `routine:skill-review`
- Content hash: `665efe4c655de4c0532073782826114b9b73a91012810a7598a7711b5e3d994b`
- Static scan (`static_scan.py 4`): floor `NEEDS_REVIEW`, 0 block findings, 5 review findings: R2 ×4 (SKILL.md lines 37, 53, 61, 70), R8 ×1 (line 46)
- SkillSpector: not installed
- Routine checks: verdict field FAIL; rules R2 starts with "fail"; checklist S2–S7 and S10 fail; `critical` not empty.

## Verdict JSON
```json
{
  "skill": "stacking-coding-agent-plugins",
  "verdict": "FAIL",
  "content_hash": "665efe4c655de4c0532073782826114b9b73a91012810a7598a7711b5e3d994b",
  "static": {"block": 0, "review_rules": ["R2", "R8"]},
  "skillspector": "not installed",
  "rules": {
    "R2": "fail: line 37 pins uv tool install graphifyy==0.9.103. That would be acceptable if the PyPI name really belongs to Graphify-Labs/graphify, but this review cannot confirm it. Lines 61 and 70 clone unpinned HEAD from personal GitHub accounts (DietrichGebert/ponytail, diegosouzapw/OmniRoute) and then run whatever their READMEs say. Line 53 (npx skills add addyosmani/agent-skills) is unpinned but comes from the named author's own repository.",
    "R8": "acceptable for line 46 only: it says up front that Graphify appends to ~/.claude/CLAUDE.md and adds ~/.claude/skills/graphify/. Not acceptable for the Ponytail session-start hook (see S7), which the scan did not flag because it is spelled out in a README the skill points to."
  },
  "checklist": {
    "S1": "ok",
    "S2": "fail: the description says the skill installs plugins. It never says it re-routes every model request through a third-party proxy (OmniRoute) or registers a session-start hook (Ponytail).",
    "S3": "fail: step 4 points ANTHROPIC_BASE_URL at an unaudited OmniRoute router, which 'silently switches' to any of 352 unnamed providers. Every prompt, the repo contents and the API credentials would pass through hosts the skill never names.",
    "S4": "fail: OmniRoute's config (omniroute.config.json) needs provider keys, and the step gives no rule that they come from environment variables. Re-pointing ANTHROPIC_BASE_URL also hands the user's Anthropic key to the proxy.",
    "S5": "fail: Ponytail and OmniRoute are cloned unpinned from personal accounts with no reason why they are the official source. The Graphify package name graphifyy (with an extra y) is a look-alike of the project name, and nothing in the folder shows that the Graphify-Labs project publishes it.",
    "S6": "fail: 'Follow repo README to register...' and 'or equivalent' tell the agent to carry out instructions from unaudited remote READMEs. The commands that would actually run are not in the skill.",
    "S7": "fail: Ponytail is installed as a Claude Code session-start hook from an unpinned, unaudited repository, without showing the hook. OmniRoute changes ANTHROPIC_BASE_URL. Graphify's CLAUDE.md append is disclosed, which is acceptable on its own.",
    "S8": "acceptable: no deletions. The persistent changes (a hook, a global CLAUDE.md block, global uv tools) only partly fit the declared purpose and are judged under S7.",
    "S9": "ok",
    "S10": "fail: unsourced figures ('~54% less code', 'up to 94%', '~20% cost saving', '352 providers', 'Work continues uninterrupted') justify the two riskiest steps, a hook and a traffic proxy. The only source is an Instagram reel."
  },
  "quality": "Needs Major Revision",
  "critical": [
    "Step 3 (Ponytail) and step 4 (OmniRoute) are too vague to follow without guessing at commands: 'Follow repo README to register as a Claude Code session-start hook', 'Point ANTHROPIC_BASE_URL (or equivalent) at the OmniRoute endpoint', and an omniroute.config.json whose format is never shown."
  ],
  "upstream": "graphifyy 0.9.103 on PyPI (claimed to be github.com/Graphify-Labs/graphify), github.com/addyosmani/agent-skills via npx skills, github.com/DietrichGebert/ponytail, github.com/diegosouzapw/OmniRoute: none audited",
  "summary": "No block findings, but step 4 sends all agent traffic and API credentials through an unaudited third-party router to unnamed providers. Step 3 installs a session-start hook from an unpinned personal repo by following its README. Both steps are too vague to run without guessing, and they are justified by unsourced figures from an Instagram reel, so the skill stays draft."
}
```

## 說明
今次重審係因為 Graphify 安裝步驟改咗（hash 變咗），但結果仍然唔合格。靜態掃描冇封鎖級問題，不過第 4 步要將 `ANTHROPIC_BASE_URL` 指去未經審核嘅 OmniRoute 代理，所有提示、程式碼同 API 金鑰都會經過佢轉發去唔具名嘅供應商；第 3 步叫 agent 跟住一個未鎖版本嘅個人 repo README 去裝 session-start hook，實際會執行乜指令 skill 入面根本冇寫。加上 `graphifyy` 套件名同項目名似係仿冒、數據只來自一條 Instagram reel，所以維持 draft。冇審核嘅上游：PyPI 套件 graphifyy 0.9.103、addyosmani/agent-skills、DietrichGebert/ponytail、diegosouzapw/OmniRoute 四者嘅實際程式碼。
