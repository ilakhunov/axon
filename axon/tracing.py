import json
import time
import uuid
from dataclasses import dataclass, field
from typing import Any, Dict, Optional, List, Protocol

@dataclass
class Event:
    """A single event in the execution trace."""
    type: str  # e.g., "call_start", "tool_call", "agent_response", "error"
    agent_name: str
    data: Dict[str, Any]
    timestamp: float = field(default_factory=time.time)
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    parent_id: Optional[str] = None

class Tracer(Protocol):
    """Protocol for tracing implementations."""
    def log(self, event: Event) -> None:
        ...

class FileTracer:
    """Simple tracer that writes events to a JSONL file."""
    
    def __init__(self, filepath: str = "trace.jsonl"):
        self.filepath = filepath
        # Clear file on init
        with open(self.filepath, "w") as f:
            f.write("")
    
    def log(self, event: Event) -> None:
        """Log an event to the file."""
        entry = {
            "id": event.id,
            "type": event.type,
            "timestamp": event.timestamp,
            "agent": event.agent_name,
            "data": event.data,
            "parent_id": event.parent_id
        }
        with open(self.filepath, "a") as f:
            f.write(json.dumps(entry) + "\n")

class ConsoleTracer:
    """Tracer that prints to console (debug)."""
    def log(self, event: Event) -> None:
        pass # We already use rich for console, so this might be redundant or for raw debug
