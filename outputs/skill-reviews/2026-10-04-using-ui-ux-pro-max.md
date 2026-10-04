# Skill review: using-ui-ux-pro-max — PASS

- Reviewed: 2026-10-04T15:35:29Z by the `vault-skill-reviewer` subagent (Opus), one skill per subagent; first run, from a Claude Code cloud session following `routines/skill-review.md` before the Routine existed
- Status set: `reviewer-approved`
- Content hash: `109de2680a9877a779a01971e273020007b6d2a686098fdde4ac858f067f54bd`
- Static scan (`static_scan.py 2`): 0 block, 4 review findings; review rules R2, R10
- SkillSpector: not installed
- Gate (routine step 4): all checks passed
- Not audited (upstream): UI UX Pro Max plugin/skill (github.com/nextlevelbuilder/ui-ux-pro-max-skill, Claude Code marketplace) and npm package ui-ux-pro-max-cli (the uipro CLI, plus the scripts/search.py it installs): not audited

## 摘要
過關。只會從官方 GitHub marketplace 同 npm 套件安裝，唯一一個刪除指令只會刪佢自己裝落嘅資料夾。冇審查到嘅部分：上游 plugin 同 CLI。

## Reviewer verdict
```json
{
  "skill": "using-ui-ux-pro-max",
  "verdict": "PASS",
  "content_hash": "109de2680a9877a779a01971e273020007b6d2a686098fdde4ac858f067f54bd",
  "static": {
    "block": 0,
    "review_rules": [
      "R2",
      "R10"
    ]
  },
  "skillspector": "not installed",
  "rules": {
    "R2": "acceptable: installs only from the tool's own sources. These are the Claude Code marketplace at github.com/nextlevelbuilder/ui-ux-pro-max-skill (same as source_url) and the npm package ui-ux-pro-max-cli, which that repo's README documents. Neither is pinned and the npm install is global (-g), but an npx route with no global install is also given, and the user's agent runs every step with normal permission prompts",
    "R10": "acceptable: `rm -rf .claude/skills/ui-ux-pro-max` is a manual uninstall fallback. It only removes the project-relative folder that the skill's own install creates"
  },
  "checklist": {
    "S1": "ok",
    "S2": "ok",
    "S3": "acceptable: the only network use is fetching the tool from its own GitHub marketplace repo and from the npm registry. The skill text sends no user data anywhere",
    "S4": "ok",
    "S5": "acceptable: both install routes name the project's official repo and its README-documented npm package. Neither is pinned and the npm install is global, but the description says the skill installs the tool, and a no-global npx alternative is offered",
    "S6": "acceptable: the skill ships no scripts. It points the agent at upstream's installed .claude/skills/ui-ux-pro-max/scripts/search.py, which is upstream code and not audited here",
    "S7": "acceptable: installing the skill or plugin into agent folders (/plugin install, uipro init --ai <agent|all>) is the stated purpose, and every command is shown. The skill text changes no permissions, sandbox, hooks or memory files. However, --ai all writes into every supported agent's folder, and the unaudited plugin could bring its own hooks",
    "S8": "acceptable: the only deletion is the uninstall of the folder the install created. Nothing is scheduled or added to startup",
    "S9": "acceptable: the triggers stay within UI and design-system work, the description names the specific tool it installs, and it does not claim built-in commands or other skills' triggers. The bare keywords react and tailwind are broad, though, and should be narrowed to explicit UI UX Pro Max or design-system requests",
    "S10": "acceptable: the description matches the body, and the core counts (192 rules, 79 styles, BM25) match raw/20260930-ui-ux-pro-max.md. Some details are not in that raw file and are unverified: 34 landing patterns, the 21-agent list, the uipro-cli rename and the 200-file limit. None of them is used to justify a risky step"
  },
  "quality": "Needs Improvement",
  "critical": [],
  "upstream": "UI UX Pro Max plugin/skill (github.com/nextlevelbuilder/ui-ux-pro-max-skill, Claude Code marketplace) and npm package ui-ux-pro-max-cli (the uipro CLI, plus the scripts/search.py it installs): not audited",
  "summary": "The static scan found no block-level findings. The single SKILL.md only wraps installing UI UX Pro Max from its official GitHub marketplace repo and npm package ui-ux-pro-max-cli (not pinned, global npm install), plus an uninstall limited to the project folder, and it has no injection, no data sent out and no credential handling. Quality needs work: the 'Use when' keyword list (react, tailwind) is broad, the two install methods read as steps to run in sequence, and the search.py path only works after a project install with uipro init, not after a marketplace plugin install."
}
```
