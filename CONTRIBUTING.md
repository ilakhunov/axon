# Contributing to Axon 🤝

Thank you for considering contributing to Axon! This document outlines how you can help make Axon better.

## 🌟 Ways to Contribute

### 1. Report Bugs 🐛
Found a bug? Help us fix it!
- Check [existing issues](#) first to avoid duplicates
- Include: Python version, OS, error messages, minimal reproduction code
- Use issue templates when available

### 2. Suggest Features 💡
Have an idea? We'd love to hear it!
- Open a discussion or issue describing the feature
- Explain the use case and why it's valuable
- Consider if it fits Axon's philosophy (simplicity, DX-first)

### 3. Write Code 🔧

#### Great First Contributions
- Add new tools to `axon_tools/` (e.g., HTTP client, database tools)
- Improve error messages
- Add tests
- Fix typos in documentation

#### Pull Request Process
1. **Fork** the repository
2. **Create a branch**: `git checkout -b feature/amazing-tool`
3. **Make changes** following our style guide
4. **Test** your changes locally
5. **Commit** with clear messages: `feat: add SQL query tool`
6. **Push** and create a PR

### 4. Improve Documentation 📖
- Fix typos or unclear explanations
- Add examples to README
- Write tutorials or blog posts

---

## 🛠 Development Setup

```bash
# Clone the repo
git clone https://github.com/yourusername/axon.git
cd axon

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\\Scripts\\activate

# Install dependencies
pip install -r requirements.txt

# Install in development mode
pip install -e .

# Run tests
python -m pytest tests/
```

---

## 📝 Code Style

### Python Style
- Follow PEP 8
- Use type hints everywhere
- Write docstrings for all functions (especially tools!)
- Keep functions small and focused

### Example Tool Template
```python
def my_tool(param: str, optional: int = 10) -> str:
    """
    Brief description of what the tool does.
    
    Args:
        param: Description of param
        optional: Description of optional parameter (default: 10)
    
    Returns:
        Description of return value
    """
    # Implementation
    return result
```

### Commit Messages
Use conventional commits:
- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation changes
- `refactor:` Code refactoring
- `test:` Adding tests

---

## 🧪 Testing

### Running Tests
```bash
pytest tests/
```

### Writing Tests
- Add tests for all new features
- Test edge cases and error conditions
- Use descriptive test names

Example:
```python
def test_tool_registration_with_type_hints():
    agent = Agent("TestBot")
    
    @agent.tool
    def calculator(a: int, b: int) -> int:
        """Adds two numbers."""
        return a + b
    
    assert "calculator" in agent.tools
```

---

## 🎯 Philosophy & Guidelines

### Core Principles
1. **DX is King**: Every change should improve developer experience
2. **5-Minute Promise**: Keep the getting-started time under 5 minutes
3. **No Surprises**: Explicit is better than implicit
4. **Type Safety**: Leverage Python's type system

### What We Accept
✅ New tools that are generally useful  
✅ Performance improvements  
✅ Better error messages  
✅ Documentation improvements  

### What We Don't Accept
❌ Features that complicate the core API  
❌ Tools that require paid API keys (without free alternatives)  
❌ Breaking changes without migration path  

---

## 📋 Checklist Before Submitting PR

- [ ] Tests pass locally
- [ ] Code follows style guide
- [ ] Docstrings added/updated
- [ ] README updated (if needed)
- [ ] No breaking changes (or documented in PR)
- [ ] Commit messages follow convention

---

## 💬 Questions?

- **General questions**: Open a [Discussion](#)
- **Bugs**: Open an [Issue](#)
- **Security**: Email security@axon-framework.dev

---

## 📜 License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

**Thank you for making Axon better!** 🎉
