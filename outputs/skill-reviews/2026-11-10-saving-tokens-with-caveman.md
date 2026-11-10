# Skill review: saving-tokens-with-caveman (2026-11-10)

**Verdict: PASS** (routine:skill-review, 2026-11-10T07:49:51Z)

## Static scan
- floor: NEEDS_REVIEW; block findings: 0; review findings: 2
- review_rules: R2 (2)
- SkillSpector: not installed

## Reviewer verdict
```json
{
  "skill": "saving-tokens-with-caveman",
  "verdict": "PASS",
  "content_hash": "585524b3ec96ab55999b9684c79f67a05b7870715e339141bb039e1ff207eae3",
  "static": {"block": 0, "review_rules": ["R2"]},
  "skillspector": "not installed",
  "rules": {"R2": "acceptable: `npx skills add JuliusBrussee/caveman -g` and `/plugin marketplace add JuliusBrussee/caveman` + `/plugin install caveman@caveman` name the project's own repository (matches metadata.source_url). The user's agent runs them with normal permission prompts, and the heading tells the reader to review first because the install edits agent configs"},
  "checklist": {
    "S1": "ok",
    "S2": "ok",
    "S3": "acceptable: the only data leaving the machine is caveman's optional Auto feature. It is opt-in (`caveman login`), and the skill says plainly that it sends data to the service and to check the README privacy section first",
    "S4": "ok",
    "S5": "acceptable: install sources are the upstream repo JuliusBrussee/caveman and the npm package `@caveman-ai/cli`, which the README documents as the installer (per /home/user/skills-vault/wiki/stars/JuliusBrussee--caveman.md). The package uses unpinned `@latest`, and the skill-only install uses `-g` (global). Both are stated openly and the user runs them by hand",
    "S6": "ok",
    "S7": "acceptable: the skill warns that the upstream installer edits agent configs, and `/caveman-compress` rewrites memory files such as CLAUDE.md with a backup. Compressing CLAUDE.md is one of the description's stated purposes, and the user starts it explicitly",
    "S8": "ok",
    "S9": "ok",
    "S10": "ok"
  },
  "quality": "Pass",
  "critical": [],
  "upstream": "caveman (github.com/JuliusBrussee/caveman, npm package @caveman-ai/cli, Claude Code plugin caveman@caveman, Auto hosted service): not audited",
  "summary": "The skill is a single short SKILL.md: no scripts, no block findings, and no text aimed at the agent or reviewer. Its installs point at the project's own repo and npm package, and it is open about config edits, CLAUDE.md compression and Auto's data sharing. Minor issues only: the CLI install is unpinned (@latest) and the skill-only install is global."
}
```

## 說明
呢個 skill 只有一個簡短嘅 SKILL.md，冇 script，靜態掃描冇任何封鎖級發現，亦冇任何針對 AI 或審查者嘅指令。佢教人點樣安裝同使用 caveman，安裝指令全部指向項目本身嘅 GitHub repo 同 npm 套件，並清楚講明安裝會改 agent 設定、壓縮 CLAUDE.md 會先備份、Auto 功能要登入先會傳送資料，所以判定通過。小問題：CLI 用 @latest 冇鎖版本，skill 安裝用 -g 全域安裝。未審核部分（upstream）：caveman 本身嘅程式碼（GitHub repo、npm 套件 @caveman-ai/cli、Claude Code plugin caveman@caveman）同 Auto 托管服務。
