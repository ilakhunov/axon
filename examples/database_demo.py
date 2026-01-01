import os
import sys
import sqlite3

# Add project root to path for local run
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from axon import Agent
from axon_tools import query_db, create_table

def main():
    print("🗄️  Testing Database Tools...\n")
    
    # Create a test database
    db_path = "./test_users.db"
    
    # Clean up old database if exists
    if os.path.exists(db_path):
        os.remove(db_path)
        print(f"♻️  Cleaned up old database\n")
    
    agent = Agent("DataBot", system="You are a helpful database assistant.")
    
    # Register database tools
    agent.tool(query_db)
    agent.tool(create_table)
    
    # Check for API Key
    if not os.environ.get("OPENAI_API_KEY"):
        print("❌ Error: OPENAI_API_KEY not found.")
        return

    # Test 1: Create table
    print("="*60)
    print("TEST 1: Create Table")
    print("="*60)
    
    task1 = f"""Create a table called 'users' in the database '{db_path}' with these columns:
- id (INTEGER PRIMARY KEY)
- name (TEXT)
- email (TEXT)
- age (INTEGER)"""
    
    print(f"\n📝 Task: {task1}\n")
    response = agent.ask(task1)
    print(f"🤖 Response:\n{response}\n")
    
    # Insert some data directly (not through agent for speed)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.executemany(
        "INSERT INTO users (name, email, age) VALUES (?, ?, ?)",
        [
            ("Alice Smith", "alice@example.com", 28),
            ("Bob Johnson", "bob@example.com", 35),
            ("Charlie Brown", "charlie@example.com", 42),
            ("Diana Prince", "diana@example.com", 30)
        ]
    )
    conn.commit()
    conn.close()
    print("✅ Inserted test data (4 users)\n")
    
    # Test 2: Query data
    print("="*60)
    print("TEST 2: Query All Users")
    print("="*60)
    
    task2 = f"Get all users from the '{db_path}' database and show their names and emails"
    print(f"\n📝 Task: {task2}\n")
    
    response = agent.ask(task2)
    print(f"🤖 Response:\n{response}\n")
    
    # Test 3: Filtered query
    print("="*60)
    print("TEST 3: Filtered Query (Age > 30)")
    print("="*60)
    
    task3 = f"From database '{db_path}', find all users who are older than 30 years"
    print(f"\n📝 Task: {task3}\n")
    
    response = agent.ask(task3)
    print(f"🤖 Response:\n{response}\n")
    
    # Test 4: Analytics
    print("="*60)
    print("TEST 4: Analytics Query")
    print("="*60)
    
    task4 = f"From database '{db_path}', calculate the average age of all users"
    print(f"\n📝 Task: {task4}\n")
    
    response = agent.ask(task4)
    print(f"🤖 Response:\n{response}\n")
    
    # Summary
    print("="*60)
    print("DATABASE TOOLS CAPABILITIES")
    print("="*60)
    print("\n✅ query_db:")
    print("   - Execute any SQL query (SELECT, INSERT, UPDATE, DELETE)")
    print("   - Returns formatted results")
    print("   - Supports parameterized queries")
    print("\n✅ create_table:")
    print("   - Create tables with custom schemas")
    print("   - Safe (uses IF NOT EXISTS)")
    print("\n🎯 Use Cases:")
    print("   - Analytics and reporting")
    print("   - User data management")
    print("   - Application databases")
    print("   - Data analysis tasks")
    
    # Cleanup
    if os.path.exists(db_path):
        os.remove(db_path)
        print(f"\n♻️  Cleaned up test database")

if __name__ == "__main__":
    main()
