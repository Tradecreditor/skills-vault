# Skill review: tracking-tasks-with-backlog-md — PASS

- Reviewed: 2026-10-05T07:49:32Z by `routine:skill-review` (independent `vault-skill-reviewer` subagent, one skill per subagent)
- Status set: `reviewer-approved`
- Content hash: `a98f330fffff99307a3f4662875a8cec2b2ba19f3e41a3b817c9196810ebf3b9`
- Static scan (`static_scan.py 4`): 0 block, 5 review findings; review rules R2
- SkillSpector: not installed
- Gate (routine step 4): all checks passed
- Not audited (upstream): Backlog.md (npm package backlog.md, github.com/MrLesk/Backlog.md, Homebrew formula backlog-md): not audited

## 摘要
過關。呢個 skill 用 Backlog.md 將工作記錄做 Markdown 任務檔，透過 CLI 或 MCP 操作看板。安裝指令指向官方 npm 套件 backlog.md，MCP 註冊只係啟動工具自己嘅本機 server，屬可選步驟並清楚列出；版本冇鎖定。小提示：任務 frontmatter 嘅 onStatusChange 都可以執行 shell 指令，skill 未有提及。冇審查到嘅部分：上游 Backlog.md 套件同程式碼。

## Reviewer verdict
```json
{
  "skill": "tracking-tasks-with-backlog-md",
  "verdict": "PASS",
  "content_hash": "a98f330fffff99307a3f4662875a8cec2b2ba19f3e41a3b817c9196810ebf3b9",
  "static": {
    "block": 0,
    "review_rules": [
      "R2"
    ]
  },
  "skillspector": "not installed",
  "rules": {
    "R2": "acceptable: the install line is npm i -g backlog.md, the official package for github.com/MrLesk/Backlog.md, matching the README (raw/ lines 28, 91, 93). The bun, brew and nix alternatives point to the same project. The claude/codex/gemini 'mcp add' lines register the tool's own local 'backlog mcp start' server, which fits the description's 'work the board via CLI or MCP'. They are optional and shown as explicit commands for the user to run."
  },
  "checklist": {
    "S1": "ok",
    "S2": "ok",
    "S3": "ok",
    "S4": "ok",
    "S5": "acceptable: the global npm install of the official backlog.md package is unpinned. The skill says to check that the npm package links to the official repo, and it warns that plain 'npx backlog' runs an unrelated package.",
    "S6": "ok",
    "S7": "acceptable: the MCP registration at user scope and the AGENTS.md/CLAUDE.md instruction block from 'backlog init' are part of the stated purpose (agents working the board via MCP). They are optional, shown first and flagged in Prerequisites and Pitfalls as protected files in this vault.",
    "S8": "ok",
    "S9": "ok",
    "S10": "ok"
  },
  "quality": "Pass",
  "critical": [],
  "upstream": "Backlog.md (npm package backlog.md, github.com/MrLesk/Backlog.md, Homebrew formula backlog-md): not audited",
  "summary": "This is a single-file skill (skills/tracking-tasks-with-backlog-md/SKILL.md) with no block findings. Its R2 install and MCP-registration lines use the official Backlog.md package and the tool's own local MCP server, and they match the vendored README. Minor note: the onStatusChange warning covers config but not the per-task override in task frontmatter, which can also run a shell command."
}
```
