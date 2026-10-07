# Skill review: tracking-tasks-with-backlog-md — PASS

- Reviewed: 2026-10-07T16:04:28Z by the `vault-skill-reviewer` subagent, one skill per subagent, from a Claude Code cloud session following `routines/skill-review.md` (the skill's files changed: the owner's name was corrected to Jeff)
- Status set: `reviewer-approved`
- Content hash: `f81d5480f85a39c64b205bccac267d6a6cf685476503f131d6b76306d8e93b0d`
- Static scan (`static_scan.py 4`): 0 block, 5 review findings; review rules R2
- SkillSpector: not installed
- Gate (routine step 4): all ok/acceptable; reviewer verdict PASS
- Not audited (upstream): Backlog.md (npm package backlog.md, Homebrew backlog-md, github.com/MrLesk/Backlog.md), including the AGENTS.md block `backlog init` writes and the MCP server: not audited

## 摘要
過關。只有一個 SKILL.md，安裝指令都指向 Backlog.md 官方來源，冇 block。今次只係將擁有人名改做 Jeff，令 hash 變咗，所以重審。冇審：Backlog.md 套件、`backlog init` 寫入嘅 AGENTS.md 區塊同 MCP server 本身。

## Reviewer verdict
```json
{
  "skill": "tracking-tasks-with-backlog-md",
  "verdict": "PASS",
  "content_hash": "f81d5480f85a39c64b205bccac267d6a6cf685476503f131d6b76306d8e93b0d",
  "static": {
    "block": 0,
    "review_rules": [
      "R2"
    ]
  },
  "skillspector": "not installed",
  "rules": {
    "R2": "acceptable: lines 41/44 install the official npm package backlog.md (github.com/MrLesk/Backlog.md) or the README's own bun/brew/nix alternatives, run by the user, with a step to check the package links to that repo and a warning about the look-alike `npx backlog`; lines 77-79 are optional, user-run MCP registrations of the locally installed `backlog mcp start`, which the description covers"
  },
  "checklist": {
    "S1": "ok",
    "S2": "acceptable: install, init, optional MCP registration and the AGENTS.md instruction block all serve the described goal of letting agents work the board, and the AGENTS.md write is listed as needing permission",
    "S3": "ok",
    "S4": "ok",
    "S5": "acceptable: official package and repo for the tool the skill is about; the global npm install is unpinned but user-run, an npx alternative is given, and a verify-before-install step is included",
    "S6": "ok",
    "S7": "acceptable: the user-scope MCP add and the one-line CLAUDE.md/AGENTS.md pointer to backlog://workflow/overview fall under the declared 'via CLI or MCP' purpose, are shown as explicit optional commands, need permission per Prerequisites, and are forbidden inside this vault",
    "S8": "ok",
    "S9": "acceptable: the generic 'kanban/task board/backlog' triggers overlap loosely with tracking-projects-in-notion, but they are qualified 'for agents', narrowed by a When-to-use section, and the body says not to adopt it in this vault",
    "S10": "ok"
  },
  "quality": "Pass",
  "critical": [],
  "upstream": "Backlog.md (npm package backlog.md, Homebrew backlog-md, github.com/MrLesk/Backlog.md), including the AGENTS.md block `backlog init` writes and the MCP server: not audited",
  "summary": "Single ASCII SKILL.md (183 lines, description 296 chars with 'Use when') that documents Backlog.md install, init, tasks, board and optional MCP setup with clear caveats; no block findings, and the R2 installs point at the project's official sources. Minor notes: stale review metadata (review_hash a98f... no longer matches), vault-specific lines in a portable skill, and the raw/ source path will not exist when the skill is installed outside the vault."
}
```
