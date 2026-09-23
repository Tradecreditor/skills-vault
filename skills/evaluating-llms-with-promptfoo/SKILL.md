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
  vault_status: "draft"
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
promptfoo eval --ci
```

Returns non-zero exit code on failures; use with GitHub Actions, CircleCI, etc.

## Pitfalls

- Datacenter IPs may be rate-limited by some LLM providers; use local keys
- Evals run 100% locally — no data leaves your machine, but you need valid API keys
- Red team scans can be slow depending on model and attack surface

## Source

https://github.com/promptfoo/promptfoo — MIT license
