"""
Context class for sharing state between tools.
"""
from typing import Any, Dict, Optional

class Context:
    """
    Shared context that can be passed to tools for state management.
    
    Example:
        >>> ctx = Context()
        >>> ctx.set("user_name", "Alice")
        >>> ctx.get("user_name")
        'Alice'
    """
    
    def __init__(self):
        self._data: Dict[str, Any] = {}
    
    def set(self, key: str, value: Any) -> None:
        """Store a value in the context."""
        self._data[key] = value
    
    def get(self, key: str, default: Any = None) -> Any:
        """Retrieve a value from the context."""
        return self._data.get(key, default)
    
    def has(self, key: str) -> bool:
        """Check if a key exists in the context."""
        return key in self._data
    
    def delete(self, key: str) -> None:
        """Remove a key from the context."""
        self._data.pop(key, None)
    
    def clear(self) -> None:
        """Clear all context data."""
        self._data.clear()
    
    def keys(self) -> list:
        """Get all keys in the context."""
        return list(self._data.keys())
    
    def __repr__(self) -> str:
        return f"Context({self._data})"
