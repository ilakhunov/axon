# Welcome to Axon Framework 🐝

**Axon** is a developer-first framework for building Agentic AI systems. It is designed to be the "Django for Agents" — powerful, opinionated, and production-ready.

## Key Features

*   **🤖 Multi-Agent Swarms:** Orchestrate teams of agents with shared context and handoffs.
*   **💾 Enterprise Memory:** Pluggable backends (SQLite, PostgreSQL, Redis) for long-term intelligence.
*   **🚀 Production Ready:** Built-in Observability, Tracing, and FASTAPI serving.
*   **🧠 RAG Built-in:** Connect to your knowledge base in one line of code.

## Getting Started

```bash
pip install axon-framework
```

Create your first agent:

```python
from axon import Agent

agent = Agent(name="Jarvis", model="gpt-4o")
print(agent.ask("Hello! Who are you?"))
```

## Next Steps

*   [Tutorial](tutorial.md): Build your first AI assistant in 10 minutes.
*   [Guides](guides.md): Learn how to connect databases, tools, and more.
*   [Reference](reference.md): API documentation.
