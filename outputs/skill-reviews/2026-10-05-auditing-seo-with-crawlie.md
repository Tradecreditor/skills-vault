# Skill review: auditing-seo-with-crawlie — PASS

- Reviewed: 2026-10-05T07:49:32Z by `routine:skill-review` (independent `vault-skill-reviewer` subagent, one skill per subagent)
- Status set: `reviewer-approved`
- Content hash: `805a8a9a19bf69e94903ca2b58631bc416cc9db7a2c4b67291fbf6b53e440be3`
- Static scan (`static_scan.py 4`): 0 block, 6 review findings; review rules R2, R8
- SkillSpector: not installed
- Gate (routine step 4): all checks passed
- Not audited (upstream): crawlie (npm package crawlie, Claude Code plugin crawlie@spronta, github.com/spronta/crawlie): not audited

## 摘要
過關。呢個 skill 教人安裝同使用開源 SEO／GEO 爬蟲 crawlie，並將佢嘅本機 MCP server 接入 agent。安裝來源（npm 套件 crawlie 同 spronta/crawlie plugin marketplace）都係項目官方來源，MCP 設定變更亦會先展示，符合描述用途；但版本冇鎖定。冇審查到嘅部分：上游 crawlie 套件、plugin 同佢嘅程式碼。

## Reviewer verdict
```json
{
  "skill": "auditing-seo-with-crawlie",
  "verdict": "PASS",
  "content_hash": "805a8a9a19bf69e94903ca2b58631bc416cc9db7a2c4b67291fbf6b53e440be3",
  "static": {
    "block": 0,
    "review_rules": [
      "R2",
      "R8"
    ]
  },
  "skillspector": "not installed",
  "rules": {
    "R2": "acceptable: installs only the tool the skill is about. That is `npm i -g crawlie` (the skill says to first check the package links back to github.com/spronta/crawlie) and the plugin from the project's own repo, `claude plugin marketplace add spronta/crawlie`. The user runs both. Neither is pinned to a version.",
    "R8": "acceptable: the description says the skill can 'wire an SEO crawler into an agent'. It shows the exact `claude mcp add` command and the claude_desktop_config.json snippet, and both only register a local stdio server named crawlie-mcp."
  },
  "checklist": {
    "S1": "ok",
    "S2": "ok",
    "S3": "acceptable: crawling sends requests only to the site the user names. The skill tells the agent to use local mode and keep away from the hosted Crawlie Cloud unless the client agrees.",
    "S4": "ok",
    "S5": "acceptable: the npm package and the plugin marketplace both match the project's own repo, spronta/crawlie. Neither is pinned, and the plugin starts its MCP server through npx. The global npm install is how the tool the description names gets installed.",
    "S6": "ok",
    "S7": "acceptable: registering the MCP server is a declared purpose, and the change is shown before it is made. Permissions, hooks and memory files are left alone.",
    "S8": "ok",
    "S9": "ok",
    "S10": "ok"
  },
  "quality": "Pass",
  "critical": [],
  "upstream": "crawlie (npm package crawlie, Claude Code plugin crawlie@spronta, github.com/spronta/crawlie): not audited",
  "summary": "This is a single-file skill for installing and running the crawlie SEO/GEO crawler and registering its MCP server. It has no block findings, and its installs and MCP config changes come from the project's own sources and match its stated purpose. Advisory: the npm and plugin installs are not pinned, and the commands were copied from the README without being run."
}
```
