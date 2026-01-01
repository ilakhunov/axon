from typing import List, Protocol, Dict, Any, Optional
from dataclasses import dataclass

@dataclass
class Message:
    role: str
    content: str

class MemoryBackend(Protocol):
    """Protocol for memory backends."""
    
    def add(self, message: Dict[str, Any]) -> None:
        """Add a message to memory."""
        ...

    def get_recent(self, k: int = 10) -> List[Dict[str, Any]]:
        """Get the k most recent messages."""
        ...

    def search(self, query: str, k: int = 5) -> List[Dict[str, Any]]:
        """Search for relevant messages."""
        ...
