# Creating Axon Plugins

Welcome to the Axon Plugin Development Guide! This document will help you create your own tools and share them with the community.

## 🎯 What is an Axon Plugin?

An Axon plugin is simply a Python function (or set of functions) that can be used as tools by Axon agents. Plugins extend Axon's capabilities without modifying the core framework.

---

## 🚀 Quick Start

### 1. Basic Plugin Structure

Create a new Python file for your plugin:

```python
# my_plugin.py

def my_tool(param: str) -> str:
    """
    Brief description of what this tool does.
    
    Args:
        param: Description of the parameter
        
    Returns:
        Description of what is returned
    """
    # Your implementation here
    result = process(param)
    return result
```

### 2. Use Your Plugin

```python
from axon import Agent
from my_plugin import my_tool

agent = Agent("MyBot")
agent.tool(my_tool)

agent.ask("Use my_tool to process something")
```

That's it! 🎉

---

## 📋 Plugin Requirements

For your tool to work with Axon, it must have:

### ✅ Type Hints
All parameters and return value must have type annotations:
```python
def good_tool(name: str, count: int) -> str:  # ✅ Good
    return f"Processed {count} items for {name}"

def bad_tool(name, count):  # ❌ Bad - no type hints
    return f"Processed {count} items for {name}"
```

### ✅ Docstring
A clear docstring explaining what the tool does:
```python
def my_tool(query: str) -> str:
    """
    Search the knowledge base for information.  # ✅ Good docstring
    
    Args:
        query: The search query string
        
    Returns:
        Formatted search results
    """
    return search_kb(query)
```

### ✅ Serializable Return Type
Return strings, dicts, lists, or other JSON-serializable types:
```python
def get_weather(city: str) -> str:  # ✅ String - good
    return f"Weather in {city}: Sunny"

def get_data(id: int) -> dict:  # ✅ Dict - good
    return {"id": id, "value": 42}

def get_object(id: int) -> MyCustomClass:  # ❌ Custom object - bad
    return MyCustomClass(id)
```

---

## 🎨 Plugin Best Practices

### 1. Error Handling
Handle errors gracefully and return informative messages:
```python
def fetch_data(url: str) -> str:
    """Fetch data from a URL."""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.text
    except requests.Timeout:
        return f"Error: Request to {url} timed out"
    except requests.RequestException as e:
        return f"Error fetching data: {str(e)}"
```

### 2. Use Retry for Reliability
For flaky operations, use the `@retry` decorator:
```python
from axon import retry

@retry(max_attempts=3, backoff=2.0)
def unreliable_api_call(endpoint: str) -> str:
    """Call an API that might fail."""
    return requests.get(endpoint).json()
```

### 3. Use Context for State
Share data between tools using `Context`:
```python
from axon import Context

def fetch_user(user_id: int, ctx: Context) -> str:
    """Fetch user data and store in context."""
    user_data = get_user_from_db(user_id)
    ctx.set("current_user", user_data)
    return f"Fetched user: {user_data['name']}"

def send_email(message: str, ctx: Context) -> str:
    """Send email to current user."""
    user = ctx.get("current_user")
    send_email_to(user['email'], message)
    return f"Email sent to {user['email']}"
```

---

## 📦 Publishing Your Plugin

### Option 1: PyPI Package (Recommended)

1. Create a package structure:
```
axon-plugin-myfeature/
├── pyproject.toml
├── README.md
├── axon_my_feature/
│   ├── __init__.py
│   └── tools.py
```

2. In `pyproject.toml`:
```toml
[project]
name = "axon-plugin-myfeature"
version = "0.1.0"
description = "My feature for Axon"
dependencies = ["axon-ai"]
```

3. Publish to PyPI:
```bash
pip install build twine
python -m build
twine upload dist/*
```

### Option 2: GitHub Repository

Share your plugin on GitHub:
```bash
# Users can install directly from GitHub
pip install git+https://github.com/username/axon-plugin-myfeature.git
```

---

## 🌟 Plugin Examples

### Example 1: Slack Integration
```python
# axon_slack.py
import os
from slack_sdk import WebClient

slack_client = WebClient(token=os.environ['SLACK_TOKEN'])

def send_slack_message(channel: str, text: str) -> str:
    """
    Send a message to a Slack channel.
    
    Args:
        channel: Channel name (e.g., '#general')
        text: Message to send
        
    Returns:
        Success or error message
    """
    try:
        slack_client.chat_postMessage(channel=channel, text=text)
        return f"✅ Message sent to {channel}"
    except Exception as e:
        return f"❌ Error sending message: {e}"
```

### Example 2: GitHub Integration
```python
# axon_github.py
from github import Github
import os

gh = Github(os.environ['GITHUB_TOKEN'])

def create_github_issue(repo: str, title: str, body: str) -> str:
    """
    Create an issue on GitHub.
    
    Args:
        repo: Repository name (e.g., 'user/repo')
        title: Issue title
        body: Issue description
        
    Returns:
        Issue URL or error
    """
    try:
        repository = gh.get_repo(repo)
        issue = repository.create_issue(title=title, body=body)
        return f"✅ Created issue: {issue.html_url}"
    except Exception as e:
        return f"❌ Error: {e}"
```

---

## 🤝 Contributing to Official Plugins

Want your plugin to be part of the official `axon_tools` collection?

1. Fork the [Axon repository](https://github.com/ilakhunov/axon)
2. Add your tool to `axon_tools/`
3. Write tests for your tool
4. Submit a pull request

See [CONTRIBUTING.md](../CONTRIBUTING.md) for details.

---

## 💡 Plugin Ideas

Looking for inspiration? Here are plugin ideas:

- 📧 Email automation (Gmail, SendGrid)
- 💬 Chat platforms (Discord, Teams)
- 📊 Data visualization (matplotlib, plotly)
- 🗄️ Database connectors (PostgreSQL, MongoDB)
- ☁️ Cloud services (AWS, GCP, Azure)
- 📱 SMS/notifications (Twilio, Pushover)
- 🎵 Media processing (images, audio, video)
- 📈 Analytics (Google Analytics, Mixpanel)

---

## ❓ Need Help?

- 📚 Check the [documentation](../README.md)
- 💬 Ask in [Discussions](https://github.com/ilakhunov/axon/discussions)
- 🐛 Report issues on [GitHub](https://github.com/ilakhunov/axon/issues)

Happy plugin building! 🚀
