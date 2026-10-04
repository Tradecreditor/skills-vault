# Skill review: automating-browsers-with-playwright — PASS

- Reviewed: 2026-10-04T15:35:29Z by the `vault-skill-reviewer` subagent (Opus), one skill per subagent; first run, from a Claude Code cloud session following `routines/skill-review.md` before the Routine existed
- Status set: `reviewer-approved`
- Content hash: `18133d1e406323cbde15765b6cffe52405ab41ae9fb9350b2edcf040e0649d22`
- Static scan (`static_scan.py 2`): 0 block, 1 review findings; review rules R2
- SkillSpector: not installed
- Gate (routine step 4): all checks passed
- Not audited (upstream): @playwright/mcp (npm package @playwright/mcp@latest, github.com/microsoft/playwright-mcp): not audited; unpinned

## 摘要
過關。只係教 agent 用 Microsoft 官方嘅 `@playwright/mcp` 接駁瀏覽器，冇隱藏指令，亦冇將資料送去其他地方。冇審查到嘅部分：上游 `@playwright/mcp` 套件本身，而且用 `@latest`，冇鎖定版本。

## Reviewer verdict
```json
{
  "skill": "automating-browsers-with-playwright",
  "verdict": "PASS",
  "content_hash": "18133d1e406323cbde15765b6cffe52405ab41ae9fb9350b2edcf040e0649d22",
  "static": {
    "block": 0,
    "review_rules": [
      "R2"
    ]
  },
  "skillspector": "not installed",
  "rules": {
    "R2": "acceptable: line 23 `claude mcp add playwright npx @playwright/mcp@latest` registers Microsoft's official npm package @playwright/mcp (repo microsoft/playwright-mcp), which is the tool the skill is about. The user's agent runs it with normal permission prompts. It matches the upstream install line recorded in wiki/stars/microsoft--playwright-mcp.md. It is unpinned (@latest)."
  },
  "checklist": {
    "S1": "ok",
    "S2": "ok",
    "S3": "acceptable: the only destinations are the npm registry (via npx) and the pages the user points the browser at; `--cdp-endpoint <url>` is an optional endpoint the user picks, and nothing is sent to any other host",
    "S4": "acceptable: no keys, passwords or cookies are handled; `--cdp-endpoint` can attach to an existing browser and its logged-in sessions, but it is listed only as an option, never as a default",
    "S5": "acceptable: the package is the official @playwright/mcp from Microsoft, but `@latest` means each launch fetches whatever version is newest; pinning a version would be safer",
    "S6": "ok",
    "S7": "acceptable: registering an MCP server is the declared purpose, and the exact `claude mcp add` command and JSON config are shown; `--allow-unrestricted-file-access` (lifts the workspace and file:// restriction) is listed without a risk warning but is not a default",
    "S8": "ok",
    "S9": "acceptable: the triggers are browser-automation verbs; 'browse' is broad and may overlap with built-in browser or web-fetch tools, but the skill claims no catch-all or slash-command triggers",
    "S10": "acceptable: it labels itself 'Draft, unreviewed' and the install command matches upstream; the flag details (--mobile, --idle-timeout, devtools cap, codegen languages) could not be checked offline because the review does not fetch URLs"
  },
  "quality": "Needs Improvement",
  "critical": [],
  "upstream": "@playwright/mcp (npm package @playwright/mcp@latest, github.com/microsoft/playwright-mcp): not audited; unpinned",
  "summary": "The static scan found no block-level issues and the one install (R2) is Microsoft's official @playwright/mcp package, though unpinned. Quality needs work: the body never shows the snapshot-then-act workflow or a step to confirm the server is connected, line 52 wrongly groups `--ignore-https-errors` (which weakens HTTPS checks) with the origin lists as 'not security boundaries', `--allow-unrestricted-file-access` has no risk warning, and the line 53 idle-timeout note reads backwards."
}
```
