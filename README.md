# Axon 🧠

<div align="center">

**The "FastAPI" for AI Agents**

Build typed, production-ready AI agents in minutes, not hours.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)

[Quick Start](#-quick-start) •
[Features](#-features) •
[Examples](#-examples) •
[Documentation](#-documentation)

</div>

---

## 🎯 Why Axon?

**The Problem:** Building AI agents today feels like configuring Apache in 1999.
- LangChain? Powerful but complex (AbstractFactories everywhere).
- Manual OpenAI API? Too much boilerplate for tools and state management.

**The Solution:** Axon makes agent development as simple as FastAPI makes API development.

```python
from axon import Agent

agent = Agent("ResearchBot")

@agent.tool
def search_web(query: str) -> str:
    """Search the internet."""
    return duckduckgo_search(query)

response = agent.ask("Find the latest AI news")
```

No chains. No graphs. No configurations. **Just Python.**

---

## ⚡ Quick Start

### Installation

```bash
pip install openai pydantic rich python-dotenv duckduckgo-search
```

### Create Your First Agent (60 seconds)

**1. Set up environment:**
```bash
echo "OPENAI_API_KEY=sk-your-key-here" > .env
```

**2. Create `app.py`:**
```python
from axon import Agent

bot = Agent("Assistant", system="You are a helpful AI assistant.")

@bot.tool
def calculate(a: int, b: int) -> int:
    """Add two numbers."""
    return a + b

print(bot.ask("What is 15 + 27?"))
```

**3. Run:**
```bash
python app.py
```

That's it! 🎉

---

## 🛠 Features

### 🚀 Zero Boilerplate
- **Auto-schema generation**: Type hints → OpenAI function schemas
- **Decorator-based tools**: Just use `@agent.tool`
- **`.env` support**: No manual environment handling

### 🎨 Beautiful DX
- **Rich console logging**: See agent reasoning in real-time
- **Helpful errors**: No cryptic stack traces
- **5-minute promise**: From zero to working agent in 5 minutes

### 🔌 Plugin Ecosystem
Built-in tools, no API keys needed:
- **Web Search** (`axon_tools.web_search`): DuckDuckGo integration
- **File System** (`axon_tools.read_file`, `write_file`): Read/write files

### 🧪 Type-Safe
- Pydantic validation for inputs and outputs
- Full type inference support
- Structured output parsing

---

## 📚 Examples

### Basic Math Agent
```python
from axon import Agent

agent = Agent("MathBot")

@agent.tool
def multiply(a: int, b: int) -> int:
    """Multiply two numbers."""
    return a * b

print(agent.ask("What's 12 times 8?"))
# Agent calls multiply(12, 8) → "The result is 96"
```

### Web Research Agent
```python
from axon import Agent
from axon_tools import web_search, write_file

agent = Agent("Researcher")
agent.tool(web_search)
agent.tool(write_file)

agent.ask("Search for Python AI frameworks and save a summary to report.txt")
# ✅ Searches web, writes formatted report
```

**More examples:** See [`examples/`](examples/) directory

---

## 🔌 Built-in Tools

### Web Search
```python
from axon_tools import web_search

@agent.tool
def search(query: str) -> str:
    return web_search(query, max_results=5)
```
- Uses DuckDuckGo (no API key!)
- Returns formatted results with URLs

### File Operations
```python
from axon_tools import read_file, write_file

@agent.tool
def save_data(filename: str, content: str) -> str:
    return write_file(filename, content)
```

---

## 📦 Project Structure

```
axon/
├── axon/              # Core framework
│   ├── core.py        # Agent class
│   ├── types.py       # Type definitions
│   └── utils.py       # Logging & utilities
├── axon_tools/        # Built-in plugins
│   ├── web.py         # Web search
│   └── filesystem.py  # File operations
├── examples/          # Demo scripts
│   ├── hello_world.py
│   ├── web_researcher.py
│   └── simple_file_demo.py
└── tests/             # Test suite
```

---

## 🤝 Contributing

We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

**Quick contributions:**
- 🐛 Report bugs via [Issues](#)
- 💡 Request features via [Discussions](#)
- 🔧 Submit PRs for fixes or new tools

---

## 🗺️ Roadmap

- [x] **v0.1**: Core Agent + Tool decorator
- [x] **v0.2**: Plugin ecosystem (Web Search, File System)
- [ ] **v0.3**: Axon Studio (Visual debugging UI)
- [ ] **v0.4**: Multi-agent support (Swarms)
- [ ] **v0.5**: Streaming & async tools
- [ ] **v1.0**: Production-ready with full docs

---

## 📖 Documentation

### Core Concepts

#### Agent
The main orchestrator. Manages LLM calls, tool execution, and conversation history.

```python
agent = Agent(
    name="MyBot",
    system="You are...",  # System prompt
    model="gpt-4o"        # OpenAI model
)
```

#### Tools
Functions that agents can call. Automatically registered with `@agent.tool`:

```python
@agent.tool
def my_function(param: str) -> str:
    """This docstring becomes the tool description."""
    return f"Result: {param}"
```

**Requirements:**
- Must have type hints
- Must have a docstring
- Return value should be string or serializable

---

## ⚖️ License

MIT License - see [LICENSE](LICENSE) for details

---

## 🌟 Star History

If Axon saves you time, give us a star! ⭐

---

## 🙏 Acknowledgments

Inspired by:
- **FastAPI**: For proving that DX matters
- **LangChain**: For pioneering agent frameworks
- **OpenAI**: For making this possible

---

<div align="center">

**Built with ❤️ by developers, for developers**

[Report Bug](#) • [Request Feature](#) • [Join Discord](#)

</div>
