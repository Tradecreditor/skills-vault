---
slug: 20260928-claude-code-fable-advisor-jev-tree
source_url: "https://x.com/thedelost/status/2104677530825634273"
canonical_id: "x:tweet:2104677530825634273"
fetched_at: "2026-09-29T19:02:40Z"
reader: "fxtwitter-via-curl"
---
{"author":"thedelost","name":"delost","followers":2976,"likes":1902,"retweets":151,"views":446089,"bookmarks":3708,"created_at":"2026-09-28T21:00:01Z"}

Claude Code tip: once Opus 5.5 is your main model, stop leaving Fable 5.1 sitting idle

put it on call with /advisor

run /advisor fable

Opus 5.5 keeps writing the code
Fable 5.1 reads the full session, every tool call included, and only speaks up at three points:

→ before a plan: is this the right approach?
→ when the same error comes back: am I digging in the wrong place?
→ before "done": what did I miss?

Fable 5.1 reviews. Opus 5.5 ships

Jev engineering is the same move one layer down: the forks that need no thinker (which file, which tool, retry or stop) go to Jev in under half a second, and the big model only sees the ones that split

- the full tree
> Opus 5.5 on high runs the main session
> explorer reads the code
> worker edits and runs tests
> researcher pulls the docs
> all three on medium
> Fable 5.1 on call as the advisor

paste the tree and this prompt into Claude Code ↓

"Rebuild my Claude Code setup around this tree:

1. Check ~/.claude/agents and .claude/agents for subagents that already fit explorer, worker and researcher.

> Draft new ones only for missing roles
> Give each model: opus, effort: medium
> Skip any that pin a different model and list them

2. Set the main session to high via effortLevel in ~/.claude/settings.json, and set advisorModel to fable

3. Find anything that keeps the advisor off (CLAUDE_CODE_DISABLE_ADVISOR_TOOL, DISABLE_TELEMETRY, any variable that stops feature-flag fetching) plus CLAUDE_CODE_EFFORT_LEVEL, which overrides subagent effort. Report them, change nothing

4. Add one rule to ~/.claude/CLAUDE.md: consult the advisor before a large plan, when an error repeats, and before calling a long task done

Show me every change as a diff first. No edits until I say go."

↳ https://code.claude.com/docs/en/advisor
