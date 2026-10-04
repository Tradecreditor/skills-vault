# Skill review: providing-design-references — FAIL

- Reviewed: 2026-10-04T15:35:29Z by the `vault-skill-reviewer` subagent (Opus), one skill per subagent; first run, from a Claude Code cloud session following `routines/skill-review.md` before the Routine existed
- Status set: `draft`
- Content hash: `bab69aaf73e46a980b3da6991cb169d0e631b9e8736d509fad4f0bb454fd5463`
- Static scan (`static_scan.py 2`): 0 block, 1 review findings; review rules R2
- SkillSpector: not installed
- Gate (routine step 4): not ok/acceptable: R2, S5, S10; reviewer verdict FAIL
- Not audited (upstream): transitions.dev Claude Code skill (real install source unknown; `transitions-dev` is not an owner/repo and is not in the source post): not audited. npm `skills` CLI: not audited

## 摘要
唔過關。安裝指令 `npx skills add transitions-dev` 唔係出自原文，亦對唔上 transitions.dev 官方 repo，有機會裝錯第三方套件（S5、S10）。改用官方 owner/repo（鎖定版本），或者刪走安裝嗰段，就可以再審。

## Reviewer verdict
```json
{
  "skill": "providing-design-references",
  "verdict": "FAIL",
  "content_hash": "bab69aaf73e46a980b3da6991cb169d0e631b9e8736d509fad4f0bb454fd5463",
  "static": {
    "block": 0,
    "review_rules": [
      "R2"
    ]
  },
  "skillspector": "not installed",
  "rules": {
    "R2": "fail: SKILL.md line 56 `npx skills add transitions-dev` installs third-party agent-skill code from an unpinned bare name, not an owner/repo or URL. The name is not in the cited Instagram post (raw/20260924-4-free-design-sites-for-vibe-coders.md says only that it 'ships as a skill for Claude Code'), and nothing ties it to the transitions.dev project's own repository. The npm `skills` installer itself is the one the vault already uses; the argument is the problem."
  },
  "checklist": {
    "S1": "ok",
    "S2": "acceptable: the optional transitions.dev skill install is design-related and run by the user, but the description never mentions that the body installs a third-party skill",
    "S3": "acceptable: the only destinations are four named reference sites the user opens in a browser (godly.design, transitions.dev, animos.app, deck.gallery). The user chooses to upload an app screenshot to animos.app, which is that site's stated purpose; unreleased-app screenshots go to a third party",
    "S4": "ok",
    "S5": "fail: the one install names no checkable official source (bare `transitions-dev`, unpinned, not owner/repo), so it could resolve to a look-alike or to nothing",
    "S6": "ok",
    "S7": "acceptable: no permission, sandbox, hook, MCP or memory-file changes; the only agent-config effect is the optional skill install already failed under S5",
    "S8": "ok",
    "S9": "acceptable: 'vibe-coding an app' and 'improving UI output' are broad, but the other triggers are design-specific and nothing claims built-in commands or another skill's triggers",
    "S10": "fail: states 'transitions.dev ships as an Agent Skills package' and gives `npx skills add transitions-dev` as fact, but the cited source gives no package or repo name. The command was added by the drafter, is unverified, and is the basis for installing third-party agent code. Other figures (27+ transitions, 25 templates, 200+ decks) match the source"
  },
  "quality": "Needs Improvement",
  "critical": [],
  "upstream": "transitions.dev Claude Code skill (real install source unknown; `transitions-dev` is not an owner/repo and is not in the source post): not audited. npm `skills` CLI: not audited",
  "summary": "Static scan is clean (0 block findings, only R2), and the reference-site workflow in steps 1-3 is safe and usable. It fails because the install section gives `npx skills add transitions-dev` as fact: an unpinned bare name the cited post never gives, which cannot be tied to transitions.dev's official repo (S5, S10, R2). To fix, replace it with the project's verified owner/repo (pinned) and mention the install in the description, or remove the install section."
}
```
