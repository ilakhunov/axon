import json
from datetime import datetime
from typing import List, Dict, Any, Optional

try:
    import psycopg
    from psycopg.rows import dict_row
except ImportError:
    psycopg = None

class PostgresMemory:
    """
    PostgreSQL backend for Axon memory.
    Requires 'psycopg' library.
    """
    
    def __init__(self, connection_string: str, table_name: str = "axon_messages"):
        if not psycopg:
            raise ImportError("Please install 'psycopg' to use PostgresMemory: pip install axon-framework[postgres]")
        
        self.conn_str = connection_string
        self.table_name = table_name
        self._init_db()
    
    def _get_conn(self):
        return psycopg.connect(self.conn_str, row_factory=dict_row)
    
    def _init_db(self):
        with self._get_conn() as conn:
            with conn.cursor() as cur:
                # Use JSONB for metadata if available in Postgres
                cur.execute(f"""
                    CREATE TABLE IF NOT EXISTS {self.table_name} (
                        id SERIAL PRIMARY KEY,
                        timestamp TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
                        role TEXT NOT NULL,
                        content TEXT NOT NULL,
                        metadata JSONB
                    )
                """)
                cur.execute(f"""
                    CREATE INDEX IF NOT EXISTS idx_{self.table_name}_timestamp 
                    ON {self.table_name}(timestamp DESC)
                """)
                # PGVector extension could be enabled here in future versions
            conn.commit()
    
    def add(self, role: str, content: str, metadata: Optional[Dict[str, Any]] = None):
        """Add a message to memory."""
        with self._get_conn() as conn:
            with conn.cursor() as cur:
                cur.execute(f"""
                    INSERT INTO {self.table_name} (role, content, metadata)
                    VALUES (%s, %s, %s)
                """, (role, content, json.dumps(metadata) if metadata else None))
            conn.commit()

    def get_recent(self, k: int = 10) -> List[Dict[str, Any]]:
        """Get k most recent messages."""
        with self._get_conn() as conn:
            with conn.cursor() as cur:
                cur.execute(f"""
                    SELECT role, content, timestamp 
                    FROM {self.table_name}
                    ORDER BY timestamp DESC
                    LIMIT %s
                """, (k,))
                results = cur.fetchall()
        
        return list(reversed([{
            "role": r["role"],
            "content": r["content"],
            "timestamp": r["timestamp"].isoformat()
        } for r in results]))

    def search(self, query: str, k: int = 5) -> List[Dict[str, Any]]:
        """Simple text search (LIKE)."""
        with self._get_conn() as conn:
            with conn.cursor() as cur:
                cur.execute(f"""
                    SELECT role, content, timestamp 
                    FROM {self.table_name}
                    WHERE content ILIKE %s
                    ORDER BY timestamp DESC
                    LIMIT %s
                """, (f"%{query}%", k))
                results = cur.fetchall()
        
        return [{
            "role": r["role"],
            "content": r["content"],
            "timestamp": r["timestamp"].isoformat()
        } for r in results]
