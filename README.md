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
pip install openai pydantic rich python-dotenv duckduckgo-search tiktoken requests
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

### 🔌 Production Tools (v0.4 🆕)
Built-in batteries for real-world apps:
- **Web Search** (`web_search`): DuckDuckGo integration, no API key
- **File System** (`read_file`, `write_file`): Safe file operations
- **HTTP/API** (`http_get`, `http_post`): REST API integration
- **Database** (`query_db`, `create_table`): SQLite queries & analytics

### 🧪 Type-Safe & Production-Ready (v0.3)
- **Structured Outputs**: Return typed Pydantic models instead of strings
- **History Management**: Auto-truncates conversation to stay within token limits
- **Context/State**: Share data between tools without manual passing
- **Streaming Responses** (v0.4): Real-time text generation
- Full type inference support

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

### Structured Output (v0.3 🆕)
```python
from axon import Agent
from pydantic import BaseModel

class Email(BaseModel):
    address: str
    confidence: float

agent = Agent("EmailBot")
result = agent.ask(
    "Extract email from: contact me at john@example.com",
    response_model=Email
)
print(result.address)  # "john@example.com"
print(result.confidence)  # 0.95
```

### Context/State Management (v0.3 🆕)
```python
from axon import Agent, Context

agent = Agent("DataBot")

@agent.tool
def fetch_data(source: str, ctx: Context) -> str:
    """Fetch data and store in context."""
    data = get_data(source)
    ctx.set("data", data)  # Share with other tools
    return "Data fetched"

@agent.tool
def analyze(ctx: Context) -> str:
    """Analyze data from context."""
    data = ctx.get("data")  # Access shared state
    return f"Analysis: {analyze(data)}"

# Agent automatically passes data between tools!
agent.ask("Fetch data from database and analyze it")
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

## 🎯 Advanced Features

### History Management (v0.3)
Control conversation token usage to prevent context overflow:

```python
agent = Agent(
    "LongConversationBot",
    max_history_tokens=4000  # Auto-truncates when exceeded
)

# After many questions, old messages are automatically removed
# System message is always preserved
```

### Custom Configuration
```python
agent = Agent(
    name="CustomBot",
    system="You are a helpful assistant specialized in...",
    model="gpt-4o",  # or "gpt-4o-mini"
    max_history_tokens=2000
)
```

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
- 🐛 Report bugs via [Issues](https://github.com/ilakhunov/axon/issues)
- 💡 Request features via [Discussions](https://github.com/ilakhunov/axon/discussions)
- 🔧 Submit PRs for fixes or new tools

---

## 🗺️ Roadmap

- [x] **v0.1**: Core Agent + Tool decorator
- [x] **v0.2**: Plugin ecosystem (Web Search, File System)
- [x] **v0.3**: Production essentials (Structured Outputs, History Management, Context/State) ✨
- [ ] **v0.4**: Streaming & async support
- [ ] **v0.5**: Multi-agent collaboration
- [ ] **v1.0**: Axon Studio (Visual debugging UI) + Full production readiness

---

## 📖 Documentation

### Core Concepts

#### Agent
The main orchestrator. Manages LLM calls, tool execution, and conversation history.

```python
agent = Agent(
    name="MyBot",
    system="You are...",         # System prompt
    model="gpt-4o",               # OpenAI model
    max_history_tokens=4000       # Token limit (v0.3)
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

#### Structured Outputs (v0.3)
Return typed Pydantic models instead of strings:

```python
from pydantic import BaseModel

class Person(BaseModel):
    name: str
    age: int
    email: str

result = agent.ask(
    "Extract person info from: John Doe, 30, john@example.com",
    response_model=Person
)
# result is a Person instance with validated fields
print(result.name)  # "John Doe"
```

#### Context/State (v0.3)
Share data between tools:

```python
from axon import Context

@agent.tool
def step_one(data: str, ctx: Context) -> str:
    """Process data and store result."""
    result = process(data)
    ctx.set("result", result)  # Store for next tool
    return "Done"

@agent.tool
def step_two(ctx: Context) -> str:
    """Use data from previous tool."""
    result = ctx.get("result")  # Retrieve
    return f"Final: {result}"
```

**Context API:**
- `ctx.set(key, value)` - Store value
- `ctx.get(key, default=None)` - Retrieve value
- `ctx.has(key)` - Check if key exists
- `ctx.delete(key)` - Remove key
- `ctx.clear()` - Clear all data
- `ctx.keys()` - Get all keys

#### History Management (v0.3)
Automatic conversation truncation:

```python
agent = Agent("Bot", max_history_tokens=2000)

# When token count exceeds limit:
# - System message is preserved
# - Oldest messages are removed
# - Automatic truncation on each ask()
```

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

[Report Bug](https://github.com/ilakhunov/axon/issues/new) • [Request Feature](https://github.com/ilakhunov/axon/discussions/new?category=ideas) • [⭐ Star](https://github.com/ilakhunov/axon)

</div>


---

## ⭐ Stargazers over time

[![Stargazers over time](https://starchart.cc/ilakhunov/axon.svg?variant=adaptive)](https://starchart.cc/ilakhunov/axon)
