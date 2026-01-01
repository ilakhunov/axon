# Axon Plugin Template

This is a template for creating Axon plugins that can be shared with the community.

## 🚀 Quick Start

1. Clone this template:
```bash
git clone https://github.com/yourusername/axon-plugin-template.git
cd axon-plugin-template
```

2. Rename the package:
```bash
mv axon_plugin_template axon_your_feature
```

3. Update `pyproject.toml` with your plugin details

4. Implement your tools in `axon_your_feature/tools.py`

5. Test your plugin:
```bash
pip install -e .
python examples/demo.py
```

6. Publish to PyPI:
```bash
pip install build twine
python -m build
twine upload dist/*
```

## 📦 Package Structure

```
axon-plugin-yourfeature/
├── pyproject.toml          # Package metadata
├── README.md               # Plugin documentation
├── LICENSE                 # MIT License
├── axon_your_feature/      # Main package
│   ├── __init__.py        # Exports
│   └── tools.py           # Tool implementations
├── examples/              # Usage examples
│   └── demo.py
└── tests/                 # Unit tests
    └── test_tools.py
```

## 🔧 Implementation Guidelines

### Tool Requirements

1. **Type Hints**: All parameters and return values must have type annotations
2. **Docstrings**: Clear description of what the tool does
3. **Error Handling**: Handle errors gracefully and return informative messages
4. **Serializable**: Return strings, dicts, lists, or JSON-serializable types

### Example Tool

```python
from axon import retry, Context

@retry(max_attempts=3, backoff=2.0)
def my_tool(param: str, ctx: Context = None) -> str:
    \"\"\"
    Brief description of what this tool does.
    
    Args:
        param: Description of parameter
        ctx: Optional context for state sharing
        
    Returns:
        Description of return value
    \"\"\"
    try:
        result = process(param)
        
        # Optionally store in context
        if ctx:
            ctx.set("last_result", result)
        
        return f"Success: {result}"
    except Exception as e:
        return f"Error: {e}"
```

## 📝 Documentation

Update README.md with:
- What your plugin does
- Installation instructions
- Usage examples
- API documentation
- Requirements and dependencies

## 🧪 Testing

Write tests for your tools:

```python
# tests/test_tools.py
from axon_your_feature import my_tool

def test_my_tool():
    result = my_tool("test input")
    assert "Success" in result
```

Run tests:
```bash
pytest tests/
```

## 📄 License

MIT License - see LICENSE file

## 🤝 Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Submit a pull request

## 📧 Support

- GitHub Issues: [Report bugs](https://github.com/yourusername/axon-plugin-yourfeature/issues)
- Discussions: [Ask questions](https://github.com/ilakhunov/axon/discussions)

---

Built with ❤️ for the Axon community
