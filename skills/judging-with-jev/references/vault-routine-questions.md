# Jev question sets for the vault's four Routines

Copy-paste material for the pilots described in `outputs/20261002-jev-in-vault-routines.md`. Each block gives the state fields to send, the exact `questions` map, the thresholds, the fallback and the line of the routine prompt it attaches to. Label meanings in `choice` criteria are copied verbatim from `CLAUDE.md` / `skills/vault-capture/SKILL.md` so Jev and the lint share one definition; when those change, change them here too.

Shapes follow TypeSafe's API reference (OpenAPI spec mirrored on jevwiki.ai, read 2026-10-02): `noul` returns `answers.<id>.noul` (0–1); `choice` takes `criteria` as a map label → description and returns `choice` plus `probabilities`; `score` takes `criteria` as an **ordered array** of level descriptions and returns `score`, a float that counts from 0 (five levels → 0–4) plus `legend` and `probabilities`. The thresholds below are on that 0-based scale.

Common state header for every request:

```json
{"goal": "<one sentence: what the routine is deciding right now>", "vault_scope": "AI agents, agent skills, MCP servers, coding agents (Claude Code / Codex / Gemini CLI / OpenClaw / Cursor), LLM knowledge tools (Obsidian, LLM wiki), developer tooling around them"}
```

(`vault_scope` is the `scope:` string from `wiki/hot-list/_config.yaml`; read it from the file at run time rather than hard-coding it.)

---

## weekly-hot-list (Opus) — pilot 1

### H1 `in_scope` — which X / Threads hits deserve the 40 fxtwitter verifications and the Jina reads
Attaches to step 1b ("only then fxtwitter-verify the in-window hits (the fxtwitter cap is 40…)") and 1c ("read each post via Jina"). One request per search hit, after the zero-cost date filter and before any fetch.

State: header + `{"platform": "x|threads", "title": "...", "snippet": "...", "author": "...", "published": "YYYY-MM-DD", "url": "..."}` (≈ 300 tokens).

```json
{
  "in_scope": {
    "type": "score",
    "instructions": "How strongly is this post about a new or trending item inside vault_scope: an AI agent, agent skill, MCP server, coding-agent tool or plugin, LLM knowledge tool, or a repository of one of these? Rate on the five levels below.",
    "criteria": [
      "unrelated to vault_scope (general news, lifestyle, finance, unrelated software)",
      "mentions AI or developers but no specific tool, skill, server or repo",
      "about a specific tool in an adjacent area (general LLM app, no-code automation, generic SaaS)",
      "about a specific agent / skill / MCP / coding-agent item but as commentary or a list",
      "announces, reviews or benchmarks a specific agent / skill / MCP / coding-agent item, likely with a link or install command"
    ]
  }
}
```

Thresholds (0–4 scale): `≥ 2.5` → verification list, sorted by score, top 40 get fxtwitter; `1.5–2.5` → Opus looks at the snippet and decides; `< 1.5` → skipped, counted. Fallback: Opus reads every snippet as today. Cap: 600 decisions per run for this question.

### H2 `topical` — the `min_stars_gained_7d_if_topical` gate
Attaches to step 1a and `_config.yaml` → `gates.github.min_stars_gained_7d_if_topical` ("README/topics mention agent, skill, MCP, Claude Code, Codex, OpenClaw"). One request per GitHub candidate; batch H4 into the same request for winners.

State: header + `{"full_name": "owner/repo", "description": "...", "topics": ["..."], "readme_head": "<first 60 lines>", "stars": n, "created_at": "..."}` (≈ 1,500 tokens).

```json
{
  "topical": {
    "type": "noul",
    "instructions": "The repository is an AI agent, an agent skill, an MCP server, a Claude Code / Codex / OpenClaw / Cursor plugin or harness, or developer tooling built specifically for such agents. A general library that merely mentions AI does not count."
  }
}
```

Thresholds: `≥ 0.80` topical (use the 1,500 gate); `0.50–0.80` Opus reads the README and decides; `< 0.50` not topical (use the 3,000 gate). Fallback: Opus decides for every repo as today. Jev never changes the star numbers or the gate arithmetic.

### H3 `same_item` — group an X / Threads post with its GitHub repo
Attaches to "Group candidates by item (canonical GitHub repo when one exists, otherwise normalised product name)". Ask only for pairs where the post text contains the repo name, the owner handle, or a github.com link, so the pair count stays small (≈ 50 a week).

State: header + `{"post": {"text": "...", "author": "...", "links": ["..."]}, "repo": {"full_name": "...", "description": "...", "homepage": "..."}}` (≈ 600 tokens).

```json
{
  "same_item": {
    "type": "noul",
    "instructions": "The post is about this exact repository or the product it ships (same name, same maker, or it links to it), not about a competitor, a fork or a different project with a similar name."
  }
}
```

Thresholds: `≥ 0.80` merge into one item; `0.50–0.80` Opus decides; `< 0.50` keep separate. Fallback: Opus pairs by eye.

### H4 `installable_skill` — draft SKILL.md for a winner (later)
Attaches to step 3 ("draft skills/<name>/SKILL.md only if it is an installable skill or a repeatable procedure"). Batch with H2 for the 2–3 winners only.

```json
{
  "installable_skill": {
    "type": "noul",
    "instructions": "The source is either an installable agent skill / plugin / MCP server with install steps, or it teaches a repeatable procedure an agent could follow step by step. News, opinion, benchmarks and product announcements without steps do not count."
  }
}
```

Thresholds: `≥ 0.80` draft; otherwise do not draft and do not spend Opus tokens deliberating. Fallback: Opus decides.

Reporting: `## 方法` gets one line — `jev: in_scope N asked / K ≥3.5 / D deferred / S skipped; topical N asked / …; fallbacks F (<reason>)`.

---

## github-stars-sync (Sonnet) — pilot 2

### S2 `summary_from_readme` — pick backfill candidates
Attaches to step 5b. Run **after** the existing Python CJK filter (which stays), over every `wiki/stars/*.md` once a week (Monday run) or over the files the CJK filter did not flag; the lowest probabilities become the ≤ 3 backfill candidates.

State: header + `{"full_name": "...", "description": "<repo description>", "summary": "<## 摘要 body>", "readme_head": "<first 100 lines>"}` (≈ 1,200 tokens).

```json
{
  "summary_from_readme": {
    "type": "noul",
    "instructions": "The summary states at least two concrete facts that appear in the README but not in the one-line description (how it is installed or used, what problem it solves, a number, a component). A summary that only rewords the description, or is generic, does not count."
  }
}
```

Thresholds: `< 0.50` → backfill candidate (rewrite 摘要 and 點解值得留意 from the README as the prompt already says); `0.50–0.80` → Sonnet reads both and decides; `≥ 0.80` → fine. Fallback: today's CJK-count-only selection. Log each as `## [date] recapture | …` exactly as now.

### S1 `is_agent_asset` — draft SKILL.md for a new star (later)
Attaches to step 4 ("If the repo is itself an agent skill, Claude Code plugin, MCP server or OpenClaw skill, also draft…"). One request per new repo, batched with nothing else.

State: header + `{"full_name": "...", "description": "...", "topics": ["..."], "readme_head": "<first 100 lines>"}`.

```json
{
  "is_agent_asset": {
    "type": "noul",
    "instructions": "The repository is itself an agent skill (SKILL.md / agentskills.io format), a Claude Code plugin, an MCP server, or an OpenClaw skill that another agent could install and run."
  }
}
```

Thresholds: `≥ 0.80` draft; `0.50–0.80` Sonnet decides; `< 0.50` no draft. Fallback: Sonnet decides.

---

## vault-lint (Sonnet) — pilot 3

### L1 `near_duplicate` — near-duplicate titles
Attaches to check 5 ("near-duplicate titles"). Pre-filter pairs deterministically first (shared lowercase token ≥ 4 chars, or same `author`, or same host in `source_url`), then ask Jev once per surviving pair (≈ 20 a week).

State: header + `{"a": {"slug": "...", "title": "...", "type": "...", "source_url": "...", "summary_head": "<first two sentences of 摘要>"}, "b": {…}}` (≈ 200 tokens).

```json
{
  "near_duplicate": {
    "type": "noul",
    "instructions": "Entries a and b describe the same tool, repository, post or concept (the same thing captured twice, possibly from different platforms or share links), not two different items that merely share a word in the title."
  }
}
```

Thresholds: `≥ 0.80` → list under `## Suggested fixes` as a merge proposal (never merge automatically; the prompt already forbids it); `0.50–0.80` → Sonnet compares and decides; `< 0.50` → not mentioned. Fallback: Sonnet eyeballs as today.

### L2 `review_priority` — order the stale-draft list (later)
Attaches to check 6 ("draft entries older than 30 days (list them for Josep to review)"). Ordering only; nothing is removed.

State: header + `{"slug": "...", "type": "...", "title": "...", "captured_at": "...", "has_raw": true, "related_count": n, "summary": "<## 摘要>", "recent_captures": ["<titles of the last 20 hot.md items>"]}` (≈ 800 tokens).

```json
{
  "review_priority": {
    "type": "score",
    "instructions": "How much is this draft worth Josep's review time now? Rate on the five levels below.",
    "criteria": [
      "thin or placeholder summary, no raw text, no related links; likely to be deprecated",
      "complete but off the vault's current interests and not referenced by other pages",
      "complete and on-topic, no urgency",
      "complete, on-topic and related to items captured in the last two weeks",
      "complete, on-topic, referenced by other pages or a skill, and about a tool Josep is actively using"
    ]
  }
}
```

Use the score to sort the list in the report; Josep still decides.

---

## capture-link (Sonnet) — later, all five in one request per URL

Attaches to `skills/vault-capture/SKILL.md` §3 (type and topic), §4 (actionable), §1 Instagram / Facebook rows (substance_in_caption) and §3 Related (related_relevance). One request per captured URL with `type`, `topic`, `actionable` and, for IG / FB, `substance_in_caption`; `related_relevance` is one request per `vault-search` hit.

State: header + `{"title": "...", "author": "...", "platform": "x|threads|instagram|facebook|youtube|github|web", "text_head": "<first ~2,000 tokens of the raw text>", "user_note": "..."}`.

```json
{
  "type": {
    "type": "choice",
    "instructions": "Which vault type fits this item best? Use the definitions exactly.",
    "criteria": {
      "skill": "a reusable procedure/prompt/workflow",
      "tool": "a product/CLI/service",
      "repo": "GitHub repository",
      "concept": "an idea/pattern",
      "post": "content whose value is the discussion itself, published as a social post",
      "video": "content whose value is the discussion itself, published as a video",
      "article": "content whose value is the discussion itself, published as a long-form article"
    }
  },
  "topic": {
    "type": "choice",
    "instructions": "Only meaningful when type is post, video or article. Which single topic/* tag from the vault's fixed vocabulary fits best?",
    "criteria": {
      "topic/model-comparison": "comparing LLMs or model versions on cost, speed or quality",
      "topic/agent-platforms": "agent runtimes, APIs and platforms (OpenAI Agents, Claude Code, OpenClaw, Cursor)",
      "topic/agent-tooling": "tools, plugins, skills, MCP servers and libraries used by or with agents",
      "topic/repo-picks": "lists or picks of GitHub repositories",
      "topic/seo-geo": "search engine and generative engine optimisation",
      "topic/marketing-content": "copywriting, newsletters, social content and marketing prompts",
      "topic/video-gen": "AI video and motion-graphics generation",
      "topic/infra-devops": "hosting, VPS, CDN, CI, deployment and infrastructure",
      "topic/knowledge-mgmt": "note-taking, Obsidian, LLM wikis and personal knowledge management",
      "topic/sales-ops": "sales automation, prospecting, CRM and B2B operations",
      "topic/ai-news": "general AI industry news and announcements"
    }
  },
  "actionable": {
    "type": "noul",
    "instructions": "The source teaches a repeatable procedure an agent could follow (a prompt pattern, a workflow, a tool setup, a coding technique) with concrete steps. News, opinions and product announcements do not count."
  },
  "substance_in_caption": {
    "type": "noul",
    "instructions": "The caption itself carries the substance of the post (the tips, the list, the numbers), rather than being a teaser that points to a DM, a comment keyword, a link or the spoken audio for the real content."
  }
}
```

Thresholds: `type` / `topic` → use the top label when its probability is `≥ 0.60`, else Sonnet picks as today; `actionable` → `≥ 0.80` draft a skill, `0.50–0.80` Sonnet decides, `< 0.50` no draft; `substance_in_caption` → `≥ 0.80` `needs_manual_text: false`, `< 0.50` `true` (say so in Key facts), between → Sonnet decides. Fallback: Sonnet decides everything, exactly as today. The topic glosses above are working descriptions written for this reference; the vocabulary itself is fixed in `CLAUDE.md` and adding a topic is a `docs:` edit there, never here first.

### `related_relevance` — rank vault-search hits for `## Related`
One request per candidate page returned by `skills/vault-search/scripts/search.sh`.

State: header + `{"new": {"title": "...", "summary": "<## 摘要>"}, "candidate": {"slug": "...", "title": "...", "tags": ["..."], "summary_head": "<first sentence>"}}`.

```json
{
  "related_relevance": {
    "type": "score",
    "instructions": "How useful is it for a reader of the new page to follow a link to the candidate page? Rate on the five levels below.",
    "criteria": [
      "no meaningful connection beyond a shared generic word",
      "same broad area, different tool and different question",
      "same area and overlapping audience; a reader might browse to it",
      "same tool family, same problem or a direct comparison",
      "the same tool, the same source, a prerequisite or a direct follow-up"
    ]
  }
}
```

Take the top three with score `≥ 2` (0–4 scale), write the one-line reason yourself (Jev gives the score, not the sentence).
