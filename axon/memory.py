"""
Persistent memory for agents using SQLite.
Enables agents to remember conversations across sessions.
"""
import sqlite3
import json
from datetime import datetime
from typing import List, Dict, Any, Optional
import os

class Memory:
    """
    Long-term memory storage for agents.
    Stores conversations in SQLite and provides search capabilities.
    """
    
    def __init__(self, db_path: str):
        """
        Initialize memory with SQLite database.
        
        Args:
            db_path: Path to SQLite database file
        """
        self.db_path = db_path
        self._init_db()
    
    def _init_db(self):
        """Create database schema if it doesn't exist."""
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
        
        # Conversations table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS conversations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                start_time TEXT NOT NULL,
                summary TEXT
            )
        """)
        
        # Create indexes for performance
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_messages_timestamp 
            ON messages(timestamp DESC)
        """)
        
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_messages_conversation 
            ON messages(conversation_id)
        """)
        
        conn.commit()
        conn.close()
    
    def save_message(
        self, 
        role: str, 
        content: str, 
        metadata: Optional[Dict[str, Any]] = None,
        conversation_id: Optional[int] = None
    ):
        """
        Save a message to long-term memory.
        
        Args:
            role: Message role (user, assistant, system)
            content: Message content
            metadata: Optional metadata dictionary
            conversation_id: Optional conversation ID
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        timestamp = datetime.now().isoformat()
        metadata_json = json.dumps(metadata) if metadata else None
        
        cursor.execute("""
            INSERT INTO messages (timestamp, role, content, metadata, conversation_id)
            VALUES (?, ?, ?, ?, ?)
        """, (timestamp, role, content, metadata_json, conversation_id))
        
        conn.commit()
        conn.close()
    
    def search(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        """
        Search past messages using substring matching.
        
        Args:
            query: Search query
            limit: Maximum number of results
            
        Returns:
            List of matching messages with metadata
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT * FROM messages
            WHERE content LIKE ?
            ORDER BY timestamp DESC
            LIMIT ?
        """, (f"%{query}%", limit))
        
        results = []
        for row in cursor.fetchall():
            results.append({
                "id": row["id"],
                "timestamp": row["timestamp"],
                "role": row["role"],
                "content": row["content"],
                "metadata": json.loads(row["metadata"]) if row["metadata"] else None
            })
        
        conn.close()
        return results
    
    def get_relevant_context(
        self, 
        current_prompt: str, 
        limit: int = 3
    ) -> str:
        """
        Get relevant past messages for current prompt.
        Uses simple keyword matching.
        
        Args:
            current_prompt: Current user prompt
            limit: Maximum number of relevant messages
            
        Returns:
            Formatted string with relevant context
        """
        # Search for relevant messages
        results = self.search(current_prompt, limit=limit)
        
        if not results:
            return ""
        
        # Format as context
        context = "Relevant past context:\n"
        for msg in results:
            context += f"- [{msg['role']}]: {msg['content'][:100]}...\n"
        
        return context
    
    def get_recent_messages(self, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Get recent messages from memory.
        
        Args:
            limit: Number of recent messages to retrieve
            
        Returns:
            List of recent messages
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT * FROM messages
            ORDER BY timestamp DESC
            LIMIT ?
        """, (limit,))
        
        results = []
        for row in cursor.fetchall():
            results.append({
                "id": row["id"],
                "timestamp": row["timestamp"],
                "role": row["role"],
                "content": row["content"]
            })
        
        conn.close()
        return list(reversed(results))  # Return in chronological order
    
    def clear(self):
        """Clear all messages from memory."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM messages")
        cursor.execute("DELETE FROM conversations")
        conn.commit()
        conn.close()
    
    def stats(self) -> Dict[str, int]:
        """
        Get memory statistics.
        
        Returns:
            Dictionary with message counts
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM messages")
        total = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM messages WHERE role = 'user'")
        user_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM messages WHERE role = 'assistant'")
        assistant_count = cursor.fetchone()[0]
        
        conn.close()
        
        return {
            "total_messages": total,
            "user_messages": user_count,
            "assistant_messages": assistant_count
        }
