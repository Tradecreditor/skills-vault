---
slug: 20260924-model-vs-harness-claude-code-explained
source_url: "https://www.instagram.com/reel/Dds27dKtVo6/"
canonical_id: "instagram:Dds27dKtVo6"
fetched_at: "2026-10-04T20:56:32Z"
reader: "jina"
---
```json
{"author": "aiwithbuntyshah", "displayName": "Bunty Shah | GenAI Architect | Startup Founder", "posted": "2026-09-24 (Jina: 1w ago)", "likes": "2.3K", "comments": 40}
```

Claude, GPT, Gemini… people talk about them like the model does all the work. It doesn't. 🧠

On its own a model can only do one thing: take text in and send text out. It can't open a file, run a command or execute a single test. The software wrapped around it — the harness — is what gives it hands.

Claude Code is the cleanest example: Claude is the model, Claude Code is the harness.

What the harness adds 👇 
🔧 Tools — the model writes a tool request, the harness runs it and feeds the result back 
🔁 The loop — think → act → observe → repeat (1 failed → fix → 42 passed) 📚 Context — the model is stateless, so every turn the harness rebuilds what it sees and decides what stays, gets summarized or gets reloaded 
🔐 Permissions — allow / ask / deny 🤖 Sub-agents — each with its own fresh context window, only a summary comes back

That's why the same model feels brilliant in one app and clumsy in another. 

One 2026 study: model fixed, harness changed → +13.7 points on Terminal-Bench 2.0.

A brilliant model with no harness is a brain in a jar.

Which harness are you using right now? 👇

#aiagents #claudecode #aiharness #llm #softwareengineering #agenticai #genai
