"""
Database tools for SQLite queries.
"""
import sqlite3
from typing import List, Dict, Any, Optional
import os

def query_db(database_path: str, query: str, params: Optional[tuple] = None) -> str:
    """
    Execute a SQL query on a SQLite database.
    
    Args:
        database_path: Path to SQLite database file
        query: SQL query to execute (SELECT, INSERT, UPDATE, DELETE)
        params: Optional tuple of parameters for parameterized queries
    
    Returns:
        Query results as formatted string or error message
    """
    # Check if database exists
    if not os.path.exists(database_path):
        return f"Error: Database file '{database_path}' not found"
    
    try:
        conn = sqlite3.connect(database_path)
        conn.row_factory = sqlite3.Row  # Return rows as dicts
        cursor = conn.cursor()
        
        # Execute query
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        
        # Handle different query types
        query_upper = query.strip().upper()
        
        if query_upper.startswith('SELECT'):
            # Fetch results for SELECT
            rows = cursor.fetchall()
            
            if not rows:
                return "Query executed successfully. No rows returned."
            
            # Convert to list of dicts
            results = [dict(row) for row in rows]
            
            # Format output
            output = f"Found {len(results)} row(s):\n\n"
            for i, row in enumerate(results, 1):
                output += f"Row {i}:\n"
                for key, value in row.items():
                    output += f"  {key}: {value}\n"
                output += "\n"
            
            conn.close()
            return output.strip()
        
        else:
            # For INSERT, UPDATE, DELETE
            conn.commit()
            affected = cursor.rowcount
            conn.close()
            return f"Query executed successfully. {affected} row(s) affected."
    
    except sqlite3.Error as e:
        return f"Database error: {str(e)}"
    except Exception as e:
        return f"Error executing query: {str(e)}"

def create_table(database_path: str, table_name: str, columns: str) -> str:
    """
    Create a table in SQLite database.
    
    Args:
        database_path: Path to SQLite database file
        table_name: Name of the table to create
        columns: Column definitions (e.g., "id INTEGER PRIMARY KEY, name TEXT")
    
    Returns:
        Success or error message
    """
    try:
        conn = sqlite3.connect(database_path)
        cursor = conn.cursor()
        
        query = f"CREATE TABLE IF NOT EXISTS {table_name} ({columns})"
        cursor.execute(query)
        
        conn.commit()
        conn.close()
        
        return f"Table '{table_name}' created successfully (or already exists)"
    
    except sqlite3.Error as e:
        return f"Database error: {str(e)}"
    except Exception as e:
        return f"Error creating table: {str(e)}"
