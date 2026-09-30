# skills/
Installable Agent-Skills folders (agentskills.io). Install anywhere:

    npx skills add Tradecreditor/skills-vault --list
    npx skills add Tradecreditor/skills-vault --skill <name> -a claude-code -a codex -a gemini-cli -a openclaw -a cursor -g -y

Claude Code: `/plugin marketplace add Tradecreditor/skills-vault` then `/plugin install skills-vault@tradecreditor-vault`.
`vault-capture`, `vault-search` and `model-tiering` are the vault's own operating skills; everything else was captured from the web.

## Skills in this vault
| name | vault_status | origin_type | what it does |
|---|---|---|---|
| automating-browsers-with-playwright | draft | repo | Connects an agent to a real browser via the Playwright MCP server |
| configuring-fable-advisor-jev-tree | draft | post | Configures Claude Code with Fable 5.1 as advisor and an Opus 5.5 + Jev-routed multi-agent tree |
| delegating-to-codex | draft | repo | Calls OpenAI Codex from inside Claude Code for a code review or a delegated task |
| evaluating-llms-with-promptfoo | draft | repo | Evaluates LLM prompts, agents and RAG pipelines with promptfoo, including red teaming |
| making-product-videos | draft | repo | Creates cinematic product demo videos using Video Shotcraft (Remotion + Agent Skill) |
| model-tiering | draft | vault-operations | Picks the model tier and effort level: expensive models advise and review, Sonnet executes |
| providing-design-references | draft | post | Provides Claude with visual design references so it can match real layouts and UI decisions |
| scanning-agent-skills | draft | post | Scans third-party agent skills, plugins and MCP servers with NVIDIA SkillSpector before install |
| stacking-coding-agent-plugins | draft | post | Installs four coding-agent plugins (Graphify, Agent Skills, Ponytail, OmniRoute) |
| targeting-purchase-intent-keywords | draft | post | Finds purchase-intent keywords, adds content + internal links, optimises conversion pages for e-com SEO |
| using-obsidian-skills | draft | repo | Installs and applies kepano/obsidian-skills for Obsidian markdown, bases and canvas |
| using-ui-ux-pro-max | draft | repo | Installs and applies the UI UX Pro Max skill for AI design system generation (192 rules, 79 styles) |
| vault-capture | verified | vault-operations | Captures a pasted link (X, Threads, Instagram, YouTube, GitHub, any page) into the vault |
| vault-search | verified | vault-operations | Searches the vault (index, skill descriptions, pages) for tools, skills and notes |

New skills are `draft` until Josep reviews them. The capture routine adds a row when it drafts a skill; the weekly lint checks that every skill folder has a row whose `vault_status` and `origin_type` match its frontmatter.
