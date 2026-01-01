# Axon Marketing Materials 📢

## 🎯 Repository Topics (GitHub)
Run this command to add topics:
```bash
gh repo edit ilakhunov/axon --add-topic ai,agents,python,llm,openai,fastapi,framework,developer-tools,automation,ai-agents
```

---

## 📝 Announcement Text Templates

### Twitter/X Post
```
🧠 Introducing Axon - "FastAPI for AI Agents"

Build production-ready AI agents in 5 minutes, not 5 hours.

✨ Zero boilerplate
🔌 Plugin ecosystem
🎨 Beautiful DX
🆓 Open source (MIT)

Stop fighting with LangChain abstractions. Just write Python.

⭐ https://github.com/ilakhunov/axon

#AI #Python #OpenAI #DevTools
```

### Hacker News Title + Description
**Title:**
```
Axon – The "FastAPI" for AI Agents
```

**Description:**
```
We built Axon to solve the same pain point FastAPI solved for APIs: making development dead simple.

Instead of wrestling with LangChain's AbstractFactories or writing boilerplate for OpenAI's function calling, you just:

1. Write a Python function
2. Add @agent.tool decorator
3. Done

Features:
- Auto-generates OpenAI schemas from type hints
- Built-in web search (DuckDuckGo, no API key)
- Beautiful logging with Rich
- 5-minute quickstart promise

Inspired by the "Developer Experience is King" philosophy.

Feedback welcome! We're at v0.2 with plugin ecosystem.
```

### Reddit r/Python
**Title:**
```
[Project] Axon: Build AI agents as easily as FastAPI builds APIs
```

**Post:**
```
I got tired of the complexity in existing agent frameworks, so I built Axon.

**The Problem:**
Building AI agents today requires understanding chains, graphs, executors, and tons of boilerplate. 
LangChain is powerful but feels like "Java for LLMs."

**The Solution:**
Axon uses decorators (like FastAPI) for tools:

```python
from axon import Agent

agent = Agent("Assistant")

@agent.tool
def search_web(query: str) -> str:
    """Search the internet."""
    return duckduckgo_search(query)

agent.ask("Find latest AI news")
```

**Features:**
- Auto-schema generation from type hints
- Built-in plugins (web search, file ops)
- Rich console logging
- MIT licensed

**Repo:** https://github.com/ilakhunov/axon

Would love feedback! What features would make this more useful?
```

### Dev.to Article Outline
```markdown
# Building AI Agents Shouldn't Be This Hard - Introducing Axon

## The Pain Point
- LangChain vs Manual OpenAI API
- Developer experience matters
- FastAPI changed APIs, can we do the same for agents?

## Introducing Axon
- 5-minute quickstart
- Code examples
- Architecture philosophy

## Built-in Plugin Ecosystem
- Web search without API keys
- File operations
- How to create custom tools

## Roadmap
- v0.3: Axon Studio (visual debugging)
- v0.4: Multi-agent support
- Community plugins

## Call to Action
- Star on GitHub
- Contribute plugins
- Share feedback
```

---

## 🚀 Quick Actions

### 1. Add Topics (requires GitHub CLI)
```bash
gh repo edit ilakhunov/axon --add-topic ai,agents,python,llm,openai,fastapi,framework
```

### 2. Create Social Media Image
Use this command to generate a banner (requires ImageMagick):
```bash
convert -size 1200x630 -background "#1e1e2e" -fill "#89dceb" -font "DejaVu-Sans-Bold" \
  -pointsize 80 -gravity center label:"Axon\nThe FastAPI for AI Agents" \
  axon_banner.png
```

### 3. Analytics Setup
```bash
# Add GitHub star tracking
echo "## Stargazers over time" >> README.md
echo "[![Stargazers over time](https://starchart.cc/ilakhunov/axon.svg)](https://starchart.cc/ilakhunov/axon)" >> README.md
git add README.md && git commit -m "docs: add star chart" && git push
```

---

## 📊 Metrics to Track
- GitHub stars
- Weekly downloads (once on PyPI)
- Issues/PRs activity
- Twitter mentions
- Dev.to article views
