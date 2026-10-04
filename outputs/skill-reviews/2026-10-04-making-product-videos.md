# Skill review: making-product-videos — FAIL

- Reviewed: 2026-10-04T15:35:29Z by the `vault-skill-reviewer` subagent (Opus), one skill per subagent; first run, from a Claude Code cloud session following `routines/skill-review.md` before the Routine existed
- Status set: `draft`
- Content hash: `81807eda3689d6b4f682b4c2c964c6c5ae5a7851e36f1c2893813ec5c319186b`
- Static scan (`static_scan.py 2`): 0 block, 2 review findings; review rules R2
- SkillSpector: not installed
- Gate (routine step 4): 2 critical quality issue(s); reviewer verdict FAIL
- Not audited (upstream): Video Shotcraft (github.com/Vincentwei1021/video-shotcraft, unpinned) and its npm dependencies, including Remotion (npm package remotion): not audited. No URL was fetched, so the repo's existence, license and star count are unverified.

## 摘要
唔過關。安全方面冇問題，但質素唔夠：核心步驟（風格庫、recipe card、逐個鏡頭 render、QA）冇路徑、冇指令，唯一一個 render 指令亦唔係出自上游 repo，agent 只能靠估（critical）。要根據上游 README 重寫先可以再審。

## Reviewer verdict
```json
{
  "skill": "making-product-videos",
  "verdict": "FAIL",
  "content_hash": "81807eda3689d6b4f682b4c2c964c6c5ae5a7851e36f1c2893813ec5c319186b",
  "static": {
    "block": 0,
    "review_rules": [
      "R2"
    ]
  },
  "skillspector": "not installed",
  "rules": {
    "R2": "acceptable: lines 29 and 31 git clone the tool's own repository (github.com/Vincentwei1021/video-shotcraft, which matches the description and metadata.source_url) and run npm install inside that clone. Nothing is installed globally, and the user's agent runs both steps with normal permission prompts. The clone is not pinned to a tag or commit, and npm install runs lifecycle scripts that were not audited."
  },
  "checklist": {
    "S1": "ok",
    "S2": "ok",
    "S3": "acceptable: the only network use is downloading from the tool's own GitHub repository and the npm registry (npm install, npx remotion). No repo contents, chat or environment data is sent anywhere.",
    "S4": "ok",
    "S5": "acceptable: the clone uses the project's own repository and npm install runs inside it, with no global install. It is not pinned, and the upstream dependency scripts were not audited.",
    "S6": "ok",
    "S7": "ok",
    "S8": "ok",
    "S9": "ok",
    "S10": "acceptable: the star and fork counts and the Apache-2.0 license come second-hand from a Facebook post (the Source section says so) and were not checked against the repo. 'CapJian (剪映)' gets CapCut/Jianying's name wrong. The skill does not claim to be official or audited."
  },
  "quality": "Needs Major Revision",
  "critical": [
    "SKILL.md steps 3, 4, 7, 9 and 10 depend on upstream assets and tooling: the 214-style library, the 157 recipe cards, per-shot rendering, designated-frame output, the '8-round' QA (only 4 checks are listed) and a browser workbench. None of these steps gives a file path or a command, and nothing tells the agent to load the upstream Video Shotcraft skill or README, so the agent has to guess the commands.",
    "SKILL.md line 85: the only render command, 'npx remotion render src/index.ts MyVideo out/video.mp4', uses an entry point and composition id that do not come from the source. The skill was compiled from a Facebook post summary (wiki/pages/20260924-video-shotcraft.md), which contains no commands, and the command has not been checked against the repo."
  ],
  "upstream": "Video Shotcraft (github.com/Vincentwei1021/video-shotcraft, unpinned) and its npm dependencies, including Remotion (npm package remotion): not audited. No URL was fetched, so the repo's existence, license and star count are unverified.",
  "summary": "The static scan found no block findings. The one flagged rule (R2: cloning the project's own repo, then npm install inside it) and every security checklist item are ok or acceptable. FAIL on quality: the core steps (style library, recipe cards, per-shot render, frame QA, workbench) give no paths or commands and never load the upstream skill, and the only render command was not taken from the repo. It needs a rewrite from the repo's own README or SKILL.md, pinned to a tag or commit."
}
```
