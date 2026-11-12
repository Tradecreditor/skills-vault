# Skill review: making-product-videos (2026-11-12)

**Verdict: PASS**

- Reviewed by: routine:skill-review (independent `vault-skill-reviewer` subagent, verdict checked by the routine)
- Content hash (H): `01ffb1ad140aca5776400443b92d2105d23db4d6edf91ee82bcf8ca55c778a32`
- Static scan: floor `NEEDS_REVIEW`, block findings 0, review findings 8, review rules R2, R6, R8 (R2×5, R6×1, R8×2)
- SkillSpector: not installed

## Verdict JSON
```json
{
  "skill": "making-product-videos",
  "verdict": "PASS",
  "content_hash": "01ffb1ad140aca5776400443b92d2105d23db4d6edf91ee82bcf8ca55c778a32",
  "static": {"block": 0, "review_rules": ["R2", "R6", "R8"]},
  "skillspector": "not installed",
  "rules": {
    "R2": "acceptable: the skill clones the official upstream repo (Vincentwei1021/video-shotcraft) at a pinned commit and says to scan it first. The other installs are standard ecosystem packages run by the user's agent: puppeteer, the template's own npm install (remotion pinned to 4.0.484) and Remotion's official create-video. The unpinned npx skills add route is mentioned, and the skill advises against it when the pin matters",
    "R6": "acceptable: UPLOAD_POST_API_KEY and UPLOAD_POST_USER are the user's own keys, read from the environment for an optional publish step done only on request. They are never printed or written",
    "R8": "acceptable: the symlink into ~/.claude/skills or ~/.codex/skills is optional and labelled so. It installs the skill this one is about, and the skill tells the agent to ask the user first. No settings, hooks, MCP or memory files are touched"
  },
  "checklist": {
    "S1": "ok",
    "S2": "acceptable: the Upload-Post upload, the JianYing export and the reviewer subagent are all disclosed, optional or part of the pipeline, and done only when the user asks. Upstream's promotional wrap-up is flagged, and the agent is told to make each suggestion only once",
    "S3": "acceptable: the network destinations are github.com (clone), the npm registry, Remotion's Chrome download, Freesound (SFX search, no key) and Upload-Post (optional, disclosed as a third-party hosted service). The local workbench runs on localhost:5198",
    "S4": "ok",
    "S5": "acceptable: the upstream clone is pinned to commit 3ac67b75dd0b3bc2fd807c17f6b7ce35373eef3d, and npm packages come from official names. npx create-video@latest is unpinned but is Remotion's official scaffolder",
    "S6": "acceptable: the folder ships no scripts. The upstream scripts the agent runs (capture-template.mjs, sfx-source.py, workbench/scripts/open.mjs, which starts a background server and runs npm install) are described accurately, run by the user's agent with normal prompts, and are preceded by a required scan of the clone",
    "S7": "ok",
    "S8": "acceptable: the only persistent process is the workbench dev server, which is disclosed along with how to stop it (kill $(cat workbench/.dev.pid)). There are no deletes outside files the pipeline creates and no scheduling",
    "S9": "ok",
    "S10": "ok"
  },
  "quality": "Pass",
  "critical": [],
  "upstream": "Video Shotcraft (github.com/Vincentwei1021/video-shotcraft @ 3ac67b75dd0b3bc2fd807c17f6b7ce35373eef3d, including its SKILL.md and references in Simplified Chinese, scripts, workbench, publish/upload_post.py), Remotion (npm remotion, @remotion/cli, create-video), puppeteer, Freesound, Upload-Post: not audited",
  "summary": "This is a single-file map of the third-party Video Shotcraft skill: it pins the upstream commit, tells the agent to scan the clone before use, and asks the user before linking it into the agent's skills folder. It ships no executable code, all referenced vault files exist, and the description is 296 characters and contains 'Use when'. Upstream code and its Chinese-language instructions were not audited, and the agent is told to follow them."
}
```

## 說明
通過。呢個係第三方 Video Shotcraft skill 嘅單檔指南：鎖定上游 commit、使用前要求掃描 clone、連結入 agent skills 資料夾之前會問用戶；本身冇可執行代碼。R2/R6/R8 都符合其用途（官方套件、用戶自己嘅 Upload-Post key、可選 symlink）。未審核部分：Video Shotcraft 上游（包括簡體中文指示、scripts、workbench）、Remotion、puppeteer、Freesound、Upload-Post。
