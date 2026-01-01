# Axon v0.4.0 - Production Tools Release 🎉

**Release Date:** January 1, 2026

## 🚀 What's New

Axon v0.4 transforms the framework into a **production-ready library** with essential tools that cover 80-90% of real-world use cases.

### ⚡ Streaming Responses
Real-time text generation with `ask_stream()`:
```python
for chunk in agent.ask_stream("Write an essay"):
    print(chunk, end="", flush=True)
    # Text appears as it's generated! (~238 chars/sec)
```

**Impact:** 10x better UX - users see responses immediately instead of waiting 30+ seconds.

---

### 🌐 HTTP/API Tools
Interact with any REST API:
```python
from axon_tools import http_get, http_post

agent.tool(http_get)
agent.tool(http_post)

agent.ask("Get data from https://api.github.com/users/octocat")
```

**Features:**
- GET and POST requests
- Custom headers and parameters
- Automatic JSON parsing
- Error handling with timeouts

**Use Cases:** GitHub API, Slack bots, webhooks, any REST integration

---

### 🗄️ Database Tools
Query SQLite databases:
```python
from axon_tools import query_db, create_table

agent.tool(query_db)

agent.ask("From database users.db, find all users older than 30")
```

**Features:**
- Execute SQL queries (SELECT, INSERT, UPDATE, DELETE)
- Create tables with custom schemas
- Analytics and reporting
- Formatted result output

**Use Cases:** Data analysis, user management, application databases

---

## 📦 What's Included

### Built-in Tools (Batteries Included)
- ✅ Web Search (DuckDuckGo)
- ✅ File System (read/write)
- ✅ HTTP/API (GET/POST)
- ✅ Database (SQLite queries)

### Core Features (from v0.3)
- ✅ Structured Outputs (Pydantic models)
- ✅ History Management (auto-truncation)
- ✅ Context/State (shared tool state)

### Developer Experience
- ✅ Zero boilerplate
- ✅ Beautiful logging (Rich console)
- ✅ Type-safe with Pydantic
- ✅ 5-minute quickstart

---

## 📊 Stats

- **7 demos** in `examples/` directory
- **8 built-in tools** ready to use
- **Covers 80-90%** of real-world agent use cases
- **Production-ready** with proper error handling

---

## 🔄 Breaking Changes

None! v0.4 is fully backward compatible with v0.3.

---

## 📝 Migration Guide

### From v0.3 to v0.4

No changes needed! Just install new dependencies:

```bash
pip install tiktoken requests
```

All v0.3 code works without modifications.

### New Features (Optional)

Add streaming for better UX:
```python
# Before (v0.3)
response = agent.ask("Write essay")

# After (v0.4)
for chunk in agent.ask_stream("Write essay"):
    print(chunk, end="", flush=True)
```

---

## 🙏 Acknowledgments

Special thanks to:
- OpenAI for the amazing API
- FastAPI for inspiration
- All early testers and contributors

---

## 🗺️ What's Next?

**v0.5 Roadmap:**
- Persistent memory (SQLite/vector search)
- Error retry decorators
- Better async support
- Plugin ecosystem expansion

---

**Full Changelog:** https://github.com/ilakhunov/axon/compare/v0.3.0...v0.4.0
