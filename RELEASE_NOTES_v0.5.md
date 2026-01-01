# Axon v0.5.0 - Intelligence & Memory Release 🧠

**Release Date:** January 2, 2026

## 🎯 What's New

Axon v0.5 brings **true intelligence** to AI agents with persistent memory, automatic error recovery, and a thriving plugin ecosystem. Agents are no longer stateless - they remember, learn, and become more reliable over time.

---

## 🚀 Major Features

### 🧠 Persistent Memory
**The killer feature competitors don't have!**

Agents now remember conversations across sessions:

```python
# Session 1
agent = Agent("MemoryBot", memory="./memory.db")
agent.ask("My name is Alice, I'm a software engineer")
agent.ask("I love Python and AI")

# Session 2 (restart/new instance)
agent2 = Agent("MemoryBot", memory="./memory.db")
agent2.ask("What's my name?")
# → "Your name is Alice" ✨

agent2.ask("What do I love?")
# → "You love Python and AI" ✨
```

**How it works:**
- SQLite backend for conversation storage
- Automatic loading of last 10 messages on startup
- Search past conversations: `memory.search("Python")`
- Stats API: `memory.stats()`

**Impact:** Agents become "smarter" over time by learning from interactions!

---

### 🔄 Error Retry Logic
**Production-ready reliability**

Automatic retry with exponential backoff:

```python
from axon import Agent, retry

agent = Agent("ReliableBot")

@agent.tool
@retry(max_attempts=3, backoff=2.0)
def flaky_api_call(url: str) -> str:
    """Call unreliable API with auto-retry."""
    return requests.get(url, timeout=10).json()

# Automatically retries on failure:
# Attempt 1: fails → wait 1.0s
# Attempt 2: fails → wait 2.0s  
# Attempt 3: success! ✅
```

**Features:**
- `@retry` - General retry decorator
- `@retry_on_rate_limit` - Specialized for API 429 errors
- Configurable: max_attempts, backoff multiplier, exception types
- Smart logging of retry attempts

**Use cases:** API calls, database queries, network operations

---

### 🔌 Plugin Ecosystem
**Community-driven extensibility**

Complete infrastructure for creating and sharing plugins:

**Documentation:**
- `docs/PLUGIN_GUIDE.md` - Comprehensive guide for plugin creators
- `docs/PLUGIN_TEMPLATE.md` - Template for new plugins
- Example plugin: Email notifications (`examples/plugin_example_email.py`)

**Plugin creation is simple:**
```python
# my_plugin.py
def my_tool(param: str) -> str:
    """Your tool description."""
    return process(param)

# Use it
from axon import Agent
from my_plugin import my_tool

agent = Agent("Bot")
agent.tool(my_tool)
```

**Community can now extend Axon with:**
- Slack/Discord integrations
- Cloud services (AWS, GCP, Azure)
- Analytics tools
- Custom data sources
- And more!

---

## 📊 What's Included

### Core Features (from previous versions)
- ✅ Streaming responses (v0.4)
- ✅ HTTP/API tools (v0.4)
- ✅ Database tools (v0.4)
- ✅ Structured outputs (v0.3)
- ✅ History management (v0.3) 
- ✅ Context/State (v0.3)
- ✅ Web search + File system (v0.2)

### New in v0.5
- ✅ **Persistent memory** across sessions
- ✅ **Error retry** with exponential backoff
- ✅ **Plugin ecosystem** documentation + examples

---

## 🎯 Stats

- **12 working demos** in `examples/`
- **8+ built-in tools** ready to use
- **Memory system** with SQLite + search
- **Retry decorators** for reliability
- **Plugin guide** for community

---

## 🔄 Breaking Changes

**None!** v0.5 is fully backward compatible with v0.4 and v0.3.

---

## 📝 Migration Guide

### From v0.4 to v0.5

No changes required! All v0.4 code works without modifications.

### New Features (Optional)

#### Enable Memory
```python
# Before (v0.4)
agent = Agent("Bot")

# After (v0.5) - optional memory
agent = Agent("Bot", memory="./bot_memory.db")
```

#### Add Retry to Tools
```python
from axon import retry

@agent.tool
@retry(max_attempts=3)
def my_tool(param: str) -> str:
    return process(param)
```

---

## 🆕 New Examples

1. **`examples/memory_demo.py`** - Persistent memory across sessions
2. **`examples/retry_demo.py`** - Error retry with flaky tools
3. **`examples/plugin_demo.py`** - Plugin creation guide
4. **`examples/plugin_example_email.py`** - Email plugin example

---

## 🎓 Documentation Updates

- Added `docs/PLUGIN_GUIDE.md` - Complete plugin development guide
- Added `docs/PLUGIN_TEMPLATE.md` - Template for new plugins
- Updated README with v0.5 features and examples

---

## 💡 Why v0.5 is Special

### Unique Differentiators

1. **Persistent Memory**
   - LangChain doesn't have this out of the box
   - Agents actually "learn" from past conversations
   - Simple SQLite backend (no complex setup)

2. **Error Retry**
   - Production-ready reliability
   - Simple decorator pattern
   - Works with any tool

3. **Plugin Ecosystem**
   - Community can extend Axon
   - Simple plugin creation (just Python functions)
   - Clear documentation and examples

**Result:** Axon is now a **truly production-ready** framework!

---

## 🙏 Acknowledgments

Special thanks to:
- OpenAI for the amazing API
- FastAPI for inspiration  
- Early testers and contributors
- The Python community

---

## 🗺️ What's Next?

**v0.6 Roadmap:**
- Multi-agent collaboration
- Vector search for memories
- Better async support
- Official plugin registry

**v1.0 Goals:**
- Axon Studio (visual debugging UI)
- Enterprise features
- Full production deployment guides

---

## 🐛 Known Issues

None reported yet!

---

**Full Changelog:** https://github.com/ilakhunov/axon/compare/v0.4.0...v0.5.0

---

Built with ❤️ by developers, for developers.

Axon v0.5 - **The Future of AI Agents** 🚀
