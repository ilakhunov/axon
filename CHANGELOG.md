# Changelog

## [0.9.0] - 2026-01-03

### 🎯 Major Features
- **Enterprise Memory Backends**: PostgreSQL and Redis support for production deployments
- **Professional Documentation**: MkDocs site with tutorials, guides, and API reference
- **AI-Native Documentation**: `docs/llms.txt` for LLM consumption

### 🐛 Critical Fixes
- **response_model Reliability**: Added fallback JSON parsing when LLM returns text instead of structured output
- **Better Error Messages**: `TypeError` with actionable suggestions when structured output fails
- **Memory API**: Backward-compatible refactor to pluggable backend architecture

### ✨ New Features
- **Web Scraping Tool**: Built-in `axon_tools/scraper.py` with BeautifulSoup4
- **CI/CD Pipeline**: GitHub Actions for automated testing across Python 3.10, 3.11, 3.12
- **Dependency Management**: Strict `requirements.txt` and `MANIFEST.in` for reproducible builds

### 📚 Documentation
- Added troubleshooting guide for `response_model`
- Added web scraping examples
- Updated `llms.txt` with anti-patterns and best practices
- Automated docs deployment to GitHub Pages

### 🔧 Technical Improvements
- Refactored `axon/memory.py` → `axon/memory/` package
- Added `SqliteMemory`, `PostgresMemory`, `RedisMemory` classes
- Optional dependencies: `pip install axon-framework[postgres]` or `[redis]`
- Improved test coverage with `tests/test_response_model.py`

### 🚀 Developer Experience
- Better logging for structured output failures
- Fallback mechanisms for unreliable LLM responses
- Clear error messages with debugging hints

---

## [0.8.1] - 2026-01-01

### 🐛 Hotfix
- Fixed missing dependencies in PyPI package (`numpy`, `fastapi`, `uvicorn`, `click`)
- Added `MANIFEST.in` to include non-code files in distribution

---

## [0.8.0] - 2025-12-31

### ✨ Features
- Observability & Tracing
- FastAPI Serving (`agent.serve()`)
- LLM-as-a-Judge Evaluations
- RAG (Knowledge Base)
- CLI & Scaffolding (`axon new`, `axon run`)

---

## [0.6.0] - 2025-12-30

### ✨ Features
- Multi-Agent Swarms
- Intelligent Handoffs
- Shared Context

---

## [0.5.0] - 2025-12-29

### ✨ Features
- Persistent Memory (SQLite)
- Error Retry Decorator
- Plugin System
