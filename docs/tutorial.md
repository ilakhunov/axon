# Tutorial: Build "Jarvis" in 10 Minutes 🤖

In this tutorial, we will build a personal assistant that remembers you and can search the web.

## 1. Setup

```bash
pip install axon-framework duckduckgo-search
```

## 2. Basic Agent

Create `jarvis.py`:

```python
from axon import Agent

jarvis = Agent(
    name="Jarvis",
    system="You are Jarvis, a helpful AI assistant. Be concise."
)

print(jarvis.ask("Hello Jarvis!"))
```

## 3. Adding Tools (Web Search)

To make Jarvis smart, let's give him access to the internet.

```python
from axon import Agent, tool
from duckduckgo_search import DDGS

@tool
def search_web(query: str) -> str:
    """Search DuckDuckGo for a query."""
    with DDGS() as ddgs:
        results = [r for r in ddgs.text(query, max_results=3)]
    return str(results)

jarvis = Agent(name="Jarvis")
jarvis.tools["search_web"] = search_web  # Use improved registration in future

print(jarvis.ask("Who won the Super Bowl in 2024?"))
```

## 4. Adding Memory

Now let's verify he remembers us.

```python
from axon import Agent

# This creates a local SQLite database 'jarvis.db'
jarvis = Agent(name="Jarvis", memory="jarvis.db")

jarvis.ask("My name is Tony Stark.")
print(jarvis.ask("What is my name?"))
```

Congratulations! You have a persistent, tool-using agent.
