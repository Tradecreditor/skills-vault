# Skill review: stacking-coding-agent-plugins (2026-11-12)

**Verdict: PASS**

- Reviewed by: routine:skill-review (independent `vault-skill-reviewer` subagent, verdict checked by the routine)
- Content hash (H): `d9602d78986cfd5c182a67162aa24314c07a48e069d8d7a6d22c83a721daf024`
- Static scan: floor `NEEDS_REVIEW`, block findings 0, review findings 3, review rules R2, R8 (R2×2, R8×1)
- SkillSpector: not installed

## Verdict JSON
```json
{
  "skill": "stacking-coding-agent-plugins",
  "verdict": "PASS",
  "content_hash": "d9602d78986cfd5c182a67162aa24314c07a48e069d8d7a6d22c83a721daf024",
  "static": {"block": 0, "review_rules": ["R2", "R8"]},
  "skillspector": "not installed",
  "rules": {
    "R2": "acceptable: line 70 installs graphifyy==0.9.103 from PyPI, pinned. The skill says the Graphify-Labs README names this as the official package and that PyPI links back to the repo. Line 82 only describes what that install adds. The Agent Skills steps use the pinned official skills CLI (npm skills@1.7.6, vercel-labs/skills) at tag 0.6.15 and project scope only. Every install comes after a scan gate and runs through the user's permission prompts.",
    "R8": "acceptable: line 88 is the CLAUDE.md block that `graphify install` appends to the user's Claude Code config directory. The description declares it ('CLAUDE.md entry'), the body shows the exact block and waits for the user's yes before running the command, and it lists the hook-registering variants and declines to run them unless the user names them."
  },
  "checklist": {
    "S1": "ok",
    "S2": "ok",
    "S3": "acceptable: the pinned skills CLI sends anonymous usage telemetry, and the body discloses this and says how to turn it off (DISABLE_TELEMETRY=1 / DO_NOT_TRACK=1). Graphify parses code locally and the body says that `/graphify .` sends docs and images to the model. Other destinations are PyPI, npm and GitHub, which belong to the named tools.",
    "S4": "ok",
    "S5": "acceptable: every install is pinned to the project's own registry package or tag (graphifyy==0.9.103 on PyPI, skills@1.7.6 on npm, addyosmani/agent-skills tag 0.6.15). The body explains the double-y PyPI name and gives its source. For Ponytail and OmniRoute it gives no install commands.",
    "S6": "ok",
    "S7": "acceptable: the only agent-config change is Graphify's global CLAUDE.md block plus its skill folder. It is declared in the description, shown before running, and removable with `graphify uninstall`. The hook-installing variants are not run unless the user asks for them by name. OmniRoute's ANTHROPIC_BASE_URL change and Ponytail's hooks are described, not performed.",
    "S8": "ok",
    "S9": "ok",
    "S10": "ok"
  },
  "quality": "Pass",
  "critical": [],
  "upstream": "graphifyy 0.9.103 (PyPI; github.com/Graphify-Labs/graphify, including the install.py that writes CLAUDE.md), npm skills 1.7.6 (github.com/vercel-labs/skills), github.com/addyosmani/agent-skills tag 0.6.15: not audited. Ponytail and OmniRoute are described only and not installed.",
  "summary": "No block findings. Each install is pinned to its official source, sits behind a SkillSpector gate and the user's permission prompts, and every config change is shown first. Ponytail and OmniRoute are now described only, which fixes every failure from the 2026-11-07 review. Advisory: add `--only-binary=:all:` to `pip download` so no sdist build runs during the scan step, and put DISABLE_TELEMETRY=1 in the npx commands."
}
```

## 說明
通過。冇 block 級發現；每個安裝都鎖定官方來源版本（graphifyy==0.9.103、skills@1.7.6、addyosmani/agent-skills tag 0.6.15），安裝前有 SkillSpector 掃描關卡同用戶權限提示，改 CLAUDE.md 之前會先展示內容。Ponytail 同 OmniRoute 而家只作描述、唔安裝，修正咗 2026-11-07 嘅失敗原因。未審核部分：graphifyy、skills CLI、addyosmani/agent-skills 上游代碼。
