# Publishing Axon to PyPI

This guide explains how to publish Axon to PyPI so everyone can `pip install axon-ai`.

## Prerequisites

1. Create PyPI account: https://pypi.org/account/register/
2. Install build tools:
```bash
pip install build twine
```

## Build the Package

```bash
# From project root
python -m build
```

This creates:
- `dist/axon_ai-0.5.0-py3-none-any.whl`
- `dist/axon-ai-0.5.0.tar.gz`

## Test on TestPyPI (Recommended First)

1. Register on TestPyPI: https://test.pypi.org/account/register/

2. Upload to TestPyPI:
```bash
twine upload --repository testpypi dist/*
```

3. Test installation:
```bash
pip install --index-url https://test.pypi.org/simple/ axon-ai
```

## Publish to Real PyPI

```bash
twine upload dist/*
```

Enter your PyPI credentials when prompted.

## After Publishing

Users can install with:
```bash
pip install axon-ai
```

Then use:
```python
from axon import Agent

agent = Agent("MyBot")
# ...
```

## Version Updates

1. Update version in `pyproject.toml`
2. Create git tag: `git tag v0.5.1`
3. Rebuild and upload: 
```bash
python -m build
twine upload dist/*
```

## Notes

- Package name on PyPI: `axon-ai` (because `axon` was taken)
- Import name stays: `import axon`
- Version: Update in `pyproject.toml` only

## Security

For CI/CD, use API tokens:
1. Generate token on PyPI: Account Settings → API tokens
2. Use in GitHub Actions or CI
