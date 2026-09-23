---
slug: 20260923-promptfoo
source_url: "https://github.com/promptfoo/promptfoo"
canonical_id: "github:promptfoo/promptfoo"
fetched_at: "2026-09-23T00:00:00Z"
reader: "exa"
---
{"name":"promptfoo","full_name":"promptfoo/promptfoo","html_url":"https://github.com/promptfoo/promptfoo","description":"Test your prompts, agents, and RAGs. Red teaming/pentesting/vulnerability scanning for AI. Compare performance of GPT, Claude, Gemini, DeepSeek, and more. Simple declarative configs with command line and CI/CD integration. Used by OpenAI and Anthropic.","homepage":"https://promptfoo.dev","language":"TypeScript","stargazers_count":24793,"forks_count":2258,"created_at":"2023-04-28T15:48:49Z","pushed_at":"2026-09-03T23:47:15Z","license":"MIT","topics":["ci","ci-cd","cicd","evaluation","evaluation-framework","llm","llm-eval","llm-evaluation","llm-evaluation-framework","llmops","pentesting","prompt-engineering","prompt-testing","prompts","rag","red-teaming","testing","vulnerability-scanners"]}

# Promptfoo: LLM evals & red teaming

promptfoo is a CLI and library for evaluating and red-teaming LLM apps. Stop the trial-and-error approach - start shipping secure, reliable AI apps.

Website · Getting Started · Red Teaming · Documentation · Discord

## Quick Start

```sh
npm install -g promptfoo
promptfoo init --example getting-started
```

Also available via `brew install promptfoo` and `pip install promptfoo`. You can also use `npx promptfoo@latest` to run any command without installing.

Most LLM providers require an API key. Set yours as an environment variable:

```sh
export OPENAI_API_KEY=sk-abc123
```

Once you're in the example directory, run an eval and view results:

```sh
cd getting-started
promptfoo eval
promptfoo view
```

See Getting Started (evals) or Red Teaming (vulnerability scanning) for more.

## What can you do with Promptfoo?

- **Test your prompts and models** with automated evaluations
- **Secure your LLM apps** with red teaming and vulnerability scanning
- **Compare models** side-by-side (OpenAI, Anthropic, Azure, Bedrock, Ollama, and more)
- **Automate checks** in CI/CD
- **Review pull requests** for LLM-related security and compliance issues with code scanning
- **Share results** with your team

## Why Promptfoo?

- **Developer-first**: Fast, with features like live reload and caching
- **Private**: LLM evals run 100% locally - your prompts never leave your machine
- **Flexible**: Works with any LLM API or programming language
- **Battle-tested**: Powers LLM apps serving 10M+ users in production
- **Data-driven**: Make decisions based on metrics, not gut feel
- **Open source**: MIT licensed, with an active community
