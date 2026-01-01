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

## 3. Creating a Swarm (Multi-Agent)

Chain agents together.

```python
from axon import Agent, Swarm

researcher = Agent(name="Researcher", system="Find information.")
writer = Agent(name="Writer", system="Write a post based on info.")

swarm = Swarm(agents=[researcher, writer])
# ... defined handoffs ...
```
