import sqlite3
import json
from datetime import datetime
from typing import List, Dict, Any, Optional

class SqliteMemory:
    """
    SQLite backend for Axon memory.
    """
    
    def __init__(self, db_path: str):
        self.db_path = db_path
        self._init_db()
    
    def _init_db(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Messages table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                role TEXT NOT NULL,
                content TEXT NOT NULL,
                metadata TEXT,
                conversation_id INTEGER
            )
        """)
        
        # Create indexes
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_messages_timestamp ON messages(timestamp DESC)")
        conn.commit()
        conn.close()
    
    def add(self, role: str, content: str, metadata: Optional[Dict[str, Any]] = None):
        """Add a message to memory."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        timestamp = datetime.now().isoformat()
        metadata_json = json.dumps(metadata) if metadata else None
        
        cursor.execute("""
            INSERT INTO messages (timestamp, role, content, metadata)
            VALUES (?, ?, ?, ?)
        """, (timestamp, role, content, metadata_json))
        
        conn.commit()
        conn.close()
    
    def get_recent(self, k: int = 10) -> List[Dict[str, Any]]:
        """Get k most recent messages."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT * FROM messages
            ORDER BY timestamp DESC
            LIMIT ?
        """, (k,))
        
        results = []
        for row in cursor.fetchall():
            results.append({
                "role": row["role"],
                "content": row["content"],
                "timestamp": row["timestamp"]
            })
        
        conn.close()
        return list(reversed(results))
    
    def search(self, query: str, k: int = 5) -> List[Dict[str, Any]]:
        """Search messages by content."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT * FROM messages
            WHERE content LIKE ?
            ORDER BY timestamp DESC
            LIMIT ?
        """, (f"%{query}%", k))
        
        results = []
        for row in cursor.fetchall():
            results.append({
                "role": row["role"],
                "content": row["content"],
                "timestamp": row["timestamp"]
            })
        
        conn.close()
        return results

    # Backward Compatibility Aliases
    save_message = add
    get_recent_messages = get_recent

    def get_relevant_context(self, current_prompt: str, limit: int = 3) -> str:
        """Legacy method for retrieving context."""
        results = self.search(current_prompt, k=limit)
        if not results:
            return ""
        context = "Relevant past context:\n"
        for msg in results:
            context += f"- [{msg['role']}]: {msg['content'][:100]}...\n"
        return context
