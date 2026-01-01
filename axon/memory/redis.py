import json
from typing import List, Dict, Any, Optional
from datetime import datetime

try:
    import redis
except ImportError:
    redis = None

class RedisMemory:
    """
    Redis backend for Axon memory.
    Requires 'redis' library.
    
    Structure:
    - Lists for message history: axon:memory:{session_id}:messages
    """
    
    def __init__(self, redis_url: str = "redis://localhost:6379/0", session_id: str = "default", ttl: int = None):
        if not redis:
            raise ImportError("Please install 'redis' to use RedisMemory: pip install axon-framework[redis]")
        
        self.client = redis.from_url(redis_url, decode_responses=True)
        self.session_id = session_id
        self.ttl = ttl
        
        # Key for this session's messages
        self.key = f"axon:memory:{session_id}:messages"
    
    def add(self, role: str, content: str, metadata: Optional[Dict[str, Any]] = None):
        """Add a message to memory (append to list)."""
        msg = {
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat(),
            "metadata": metadata
        }
        
        # Redis List: Push to head (LPUSH) so index 0 is newest? 
        # Or Push to tail (RPUSH) so order is chronological?
        # get_recent usually wants newest.
        # Let's use RPUSH (append) so 0 is oldest, -1 is newest.
        
        self.client.rpush(self.key, json.dumps(msg))
        
        if self.ttl:
            self.client.expire(self.key, self.ttl)
            
    def get_recent(self, k: int = 10) -> List[Dict[str, Any]]:
        """Get k most recent messages."""
        # Get last k elements: from -k to -1
        # range is inclusive in redis
        if k <= 0: return []
        
        raw_msgs = self.client.lrange(self.key, -k, -1)
        
        results = []
        for raw in raw_msgs:
            msg = json.loads(raw)
            results.append(msg)
            
        # Results are chronological [-k...-1]
        # Our interface usually expects reversed (newest first)? 
        # Sqlite impl returns: list(reversed(results)) where results were SELECT ... ORDER BY timestamp DESC
        # So sqlite returns newest first.
        # Let's verify: 
        # Sqlite: ORDER BY timestamp DESC LIMIT k -> [Newest, ..., Oldest]
        # Then returns reversed -> [Oldest, ..., Newest] (Chronological)
        # Wait, let's check core.py usage.
        
        # core.py: 
        # recent_messages = self.memory.get_recent(k=10)
        # for msg in recent_messages: self.history.append(...) 
        # This implies get_recent should return CHRONOLOGICAL order (Old -> New).
        
        # My Redis implementation (RPUSH + LRANGE) returns Chronological order. 
        # So I do NOT need to reverse.
        
        return results

    def search(self, query: str, k: int = 5) -> List[Dict[str, Any]]:
        """
        Naive search in Redis (scan all items).
        warning: Performance heavy for large history. 
        For true search, use Redis Stack (RediSearch), but we keep it simple here.
        """
        all_msgs_raw = self.client.lrange(self.key, 0, -1)
        
        matches = []
        for raw in reversed(all_msgs_raw): # Search newest first
            msg = json.loads(raw)
            if query.lower() in msg["content"].lower():
                matches.append(msg)
                if len(matches) >= k:
                    break
        
        return matches
