# How-To Guides 📖

Recipes for common tasks.

## 1. Using PostgreSQL Memory

For production, switch from SQLite to Postgres.

```python
from axon import Agent
from axon.memory import PostgresMemory

# pip install "axon-framework[postgres]"
memory = PostgresMemory("postgresql://user:pass@localhost:5432/mydb")
agent = Agent(name="ProductionBot", memory=memory)
```

## 2. Streaming Responses to Frontend

Use `ask_stream` to get tokens in real-time.

```python
agent = Agent(name="Streamer")

for chunk in agent.ask_stream("Tell me a long story"):
    print(chunk, end="", flush=True)
```

## 3. Web Scraping

Use built-in scraper tool (v0.9+):

```python
from axon import Agent
from axon_tools.scraper import scrape_url

agent = Agent("Researcher")
agent.tool(scrape_url)

result = agent.ask("Scrape https://example.com and summarize")
```

## 4. Creating a Swarm (Multi-Agent)

Chain agents together.

```python
from axon import Agent, Swarm

researcher = Agent(name="Researcher", system="Find information.")
writer = Agent(name="Writer", system="Write a post based on info.")

swarm = Swarm(agents=[researcher, writer])
# ... defined handoffs ...
```

## 4. Troubleshooting Structured Output

If `response_model` returns a string instead of your Pydantic model:

**Cause:** LLM sometimes ignores the structured output tool and returns plain text.

**Solution (v0.9+):** Axon now has automatic fallback JSON parsing.

```python
from pydantic import BaseModel

class Post(BaseModel):
    title: str
    content: str

try:
    result = agent.ask("Create a post about AI", response_model=Post)
    # Will attempt JSON extraction if LLM returns text
    print(result.title)
except TypeError as e:
    # Parsing failed - use manual approach
    print(f"Fallback needed: {e}")
```

**Best Practice:** Be specific in your prompt:
```python
# ❌ Vague
agent.ask("Tell me about the user", response_model=UserInfo)

# ✅ Explicit
agent.ask("Extract user info in JSON format: name, age, email", response_model=UserInfo)
```
