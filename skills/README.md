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
| delegating-to-codex | draft | repo | Calls OpenAI Codex from inside Claude Code for a code review or a delegated task |
| evaluating-llms-with-promptfoo | draft | repo | Evaluates LLM prompts, agents and RAG pipelines with promptfoo, including red teaming |
| model-tiering | draft | vault-operations | Picks the model tier and effort level: expensive models advise and review, Sonnet executes |
| stacking-coding-agent-plugins | draft | post | Installs four coding-agent plugins (Graphify, Agent Skills, Ponytail, OmniRoute) |
| using-obsidian-skills | draft | repo | Installs and applies kepano/obsidian-skills for Obsidian markdown, bases and canvas |
| vault-capture | verified | vault-operations | Captures a pasted link (X, Threads, Instagram, YouTube, GitHub, any page) into the vault |
| vault-search | verified | vault-operations | Searches the vault (index, skill descriptions, pages) for tools, skills and notes |

New skills are `draft` until Josep reviews them. The capture routine adds a row when it drafts a skill; the weekly lint checks that every skill folder has a row whose `vault_status` and `origin_type` match its frontmatter.
