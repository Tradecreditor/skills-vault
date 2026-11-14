# skills/
Installable Agent-Skills folders (agentskills.io). Install anywhere:

    npx skills add Tradecreditor/skills-vault --list
    npx skills add Tradecreditor/skills-vault --skill <name> -a claude-code -a codex -a gemini-cli -a openclaw -a cursor -g -y

Claude Code: `/plugin marketplace add Tradecreditor/skills-vault` then `/plugin install skills-vault@tradecreditor-vault`.
After installing or removing a skill in a project, record it in Notion: `python3 scripts/skills-inventory.py` (or
`/skills-vault:skillsync` where the plugin is installed); see `tracking-skill-installs-in-notion`.
`vault-capture`, `vault-search`, `model-tiering`, `judging-with-jev`, `keeping-handoff-docs`, `tracking-projects-in-notion`, `tracking-skill-installs-in-notion` and `auditing-agent-skills` are the vault's own operating skills; everything else was captured from the web.

**Install into other projects only skills marked `reviewer-approved` or `verified`.** The plugin and `npx skills add` can still
reach every folder, so the status column is the gate: `draft` = not approved yet (never reviewed, or rejected; the report link
says which), `reviewer-approved` = passed the `skill-review` routine's audit, `verified` = Jeff's own mark, `deprecated` = retired.

## Skills in this vault
| name | vault_status | origin_type | what it does |
|---|---|---|---|
| auditing-agent-skills | reviewer-approved | vault-operations | Audits a skill folder for safety and quality and returns a PASS/FAIL verdict |
| auditing-seo-with-crawlie | reviewer-approved | post | Runs crawlie, an open-source local SEO + GEO crawler with CLI and MCP server |
| automating-browsers-with-playwright | reviewer-approved | repo | Connects an agent to a real browser via the Playwright MCP server |
| configuring-fable-advisor-jev-tree | reviewer-approved | post | Configures one Claude Code tree: Opus main session at high effort, Fable as /advisor, three Opus subagents, optional Jev judgment leaf through judging-with-jev |
| delegating-to-codex | reviewer-approved | repo | Calls OpenAI Codex from inside Claude Code for a code review or a delegated task |
| evaluating-llms-with-promptfoo | reviewer-approved | repo | Evaluates LLM prompts, agents and RAG pipelines with promptfoo, including red teaming |
| judging-with-jev | reviewer-approved | vault-operations | Asks TypeSafe's Jev typed yes/no, choice or score questions to classify, gate or dedupe |
| keeping-handoff-docs | reviewer-approved | vault-operations | Keeps one handoff.md per project: read it first, update it before a session that changed state ends |
| making-product-videos | reviewer-approved | repo | Creates cinematic product demo videos using Video Shotcraft (Remotion + Agent Skill) |
| modernizing-web-code-with-guidance | reviewer-approved | repo | Steers coding agents toward modern web platform APIs with the Modern Web Guidance CLI (search, retrieve, legacy-scan) |
| model-tiering | reviewer-approved | vault-operations | Picks the model tier and effort level: expensive models advise and review, Sonnet executes |
| providing-design-references | reviewer-approved | post | Provides Claude with visual design references so it can match real layouts and UI decisions |
| researching-competitor-landing-pages | reviewer-approved | post | Compares competitor landing pages on five fields with a ready agent prompt |
| saving-tokens-with-caveman | reviewer-approved | repo | Installs and uses caveman to cut agent token use (short replies, compressed tool output) |
| scanning-agent-skills | reviewer-approved | post | Scans third-party agent skills, plugins and MCP servers with NVIDIA SkillSpector before install |
| stacking-coding-agent-plugins | reviewer-approved | post | Scans, then installs pinned Graphify and chosen Agent Skills skills when the scan gate allows; describes Ponytail and OmniRoute without installing them |
| targeting-purchase-intent-keywords | reviewer-approved | post | Finds purchase-intent keywords, adds content + internal links, optimises conversion pages for e-com SEO |
| tracking-projects-in-notion | draft | vault-operations | Runs Jeff's cross-project kanban in Notion under one board policy; mirrors handoff.md In flight rows and audits the board weekly |
| tracking-skill-installs-in-notion | reviewer-approved | vault-operations | Records which skills and plugins are installed in which project or computer in Jeff's Notion database Skill Installs (`scripts/skills-inventory.py`) |
| tracking-tasks-with-backlog-md | reviewer-approved | repo | Tracks agent and human work as Markdown task files with Backlog.md |
| using-obsidian-skills | reviewer-approved | repo | Installs kepano/obsidian-skills into a project or Obsidian vault and helps choose its skills |
| using-ui-ux-pro-max | reviewer-approved | repo | Installs and applies the UI UX Pro Max skill for AI design system generation (192 rules, 79 styles) |
| vault-capture | verified | vault-operations | Captures a pasted link (X, Threads, Instagram, YouTube, GitHub, any page) into the vault |
| vault-search | verified | vault-operations | Searches the vault (index, skill descriptions, pages) for tools, skills and notes |

New skills start `draft`. The daily `skill-review` routine audits each one with an independent reviewer agent
(`.claude/agents/vault-skill-reviewer.md`, procedure `skills/auditing-agent-skills`) and sets `reviewer-approved` on a pass; Jeff no
longer reviews skills himself (2026-10-04). Reports live in `outputs/skill-reviews/`. An edit to an approved skill changes its
`review_hash` and sends it back through review. The capture routine adds a row when it drafts a skill; the weekly lint checks that
every skill folder has a row whose `vault_status` and `origin_type` match its frontmatter, and that approved skills still match their hash.
