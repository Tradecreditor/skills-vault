---
name: evaluating-llms-with-promptfoo
description: Evaluates LLM prompts, agents, and RAGs using promptfoo; runs red teaming and vulnerability scans. Use when testing prompts, comparing models, securing AI apps, running LLM evals in CI/CD, or scanning for LLM vulnerabilities.
metadata:
  source_url: "https://github.com/promptfoo/promptfoo"
  source_platform: "github"
  author: "promptfoo"
  captured_at: "2026-09-23"
  engagement: "stars=24793 forks=2258"
  origin_type: "repo"
  vault_status: "reviewer-approved"
  reviewed_at: "2026-11-12T07:51:49Z"
  reviewed_by: "routine:skill-review"
  review_hash: "1a046af3d94ed935f161233ff3704243d1b4d0a2121809368e5399eee5119152"
  review_report: "outputs/skill-reviews/2026-11-12-evaluating-llms-with-promptfoo.md"
---

# evaluating-llms-with-promptfoo

Test prompts, agents, and RAG pipelines with declarative configs; scan for vulnerabilities via red teaming.

## When to use

- You need to evaluate prompt quality or compare model outputs
- You want to red-team an LLM app for security vulnerabilities
- You need LLM testing integrated into CI/CD
- You want to compare GPT, Claude, Gemini, Bedrock side-by-side

## Steps

### 1. Install

```sh
npm install -g promptfoo
# or
brew install promptfoo
# or
pip install promptfoo
# or run without installing:
npx promptfoo@latest
```

### 2. Initialize a project

```sh
promptfoo init --example getting-started
cd getting-started
```

### 3. Set API key(s)

```sh
export OPENAI_API_KEY=sk-...
export ANTHROPIC_API_KEY=sk-ant-...
```

### 4. Run evaluations

```sh
promptfoo eval
```

### 5. View results

```sh
promptfoo view
```

### 6. Red teaming / vulnerability scan

```sh
promptfoo redteam init       # set up red team config
promptfoo redteam run        # run the scan
promptfoo redteam report     # view vulnerability report
```

### 7. CI/CD integration

Add to your pipeline:

```sh
promptfoo eval --fail-on-error
```

Per the CLI docs, `promptfoo eval` exits with code 100 when at least one test case fails or the pass rate is below `PROMPTFOO_PASS_RATE_THRESHOLD`, and 1 for other errors; use it with GitHub Actions, GitLab CI, Jenkins, etc.

## Pitfalls

- Datacenter IPs may be rate-limited by some LLM providers; use local keys
- The eval runner is local, but prompts and test cases are sent to whichever model provider you configure: with OpenAI or Anthropic keys (steps 3-4) they go to those APIs. A local provider such as Ollama keeps requests on your machine. Sharing (`--share`, `promptfoo share`) creates an online URL, and promptfoo documents telemetry and hosted generation fallbacks (`PROMPTFOO_DISABLE_REMOTE_GENERATION`) as separate controls, so check them before using sensitive data
- Red team scans can be slow depending on model and attack surface

## Source

https://github.com/promptfoo/promptfoo — MIT license
