import os
import sys

# Add project root to path for local run
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from axon import Agent

def main():
    print("🧠 Testing Persistent Memory...\n")
    
    # Check for API Key
    if not os.environ.get("OPENAI_API_KEY"):
        print("❌ Error: OPENAI_API_KEY not found.")
        return

    memory_path = "./test_memory.db"
    
    # Clean up old database
    if os.path.exists(memory_path):
        os.remove(memory_path)
        print(f"♻️  Cleaned up old memory database\n")
    
    # Session 1: Teach the agent about yourself
    print("="*60)
    print("SESSION 1: Teaching the Agent")
    print("="*60)
    
    agent1 = Agent("MemoryBot", memory=memory_path)
    
    print("\n📝 Tell agent your name...")
    response = agent1.ask("My name is Alice and I'm a software engineer")
    print(f"🤖 {response}\n")
    
    print("📝 Tell agent your preferences...")
    response = agent1.ask("I love Python and AI, and my favorite color is blue")
    print(f"🤖 {response}\n")
    
    print("📝 Tell agent where you live...")
    response = agent1.ask("I live in San Francisco")
    print(f"🤖 {response}\n")
    
    # Show memory stats
    stats = agent1.memory.stats()
    print(f"💾 Memory stats: {stats}")
    print()
    
    # Session 2: NEW agent instance (simulates restart)
    print("="*60)
    print("SESSION 2: New Agent Instance (Simulating Restart)")
    print("="*60)
    print("\n🔄 Creating new agent with same memory...\n")
    
    agent2 = Agent("MemoryBot", memory=memory_path)
    
    print("📝 Ask about your name (should remember!)...")
    response = agent2.ask("What's my name?")
    print(f"🤖 {response}\n")
    
    print("📝 Ask about favorite color...")
    response = agent2.ask("What's my favorite color?")
    print(f"🤖 {response}\n")
    
    print("📝 Ask about location...")
    response = agent2.ask("Where do I live?")
    print(f"🤖 {response}\n")
    
    # Test memory search
    print("="*60)
    print("MEMORY SEARCH TEST")
    print("="*60)
    
    print("\n🔍 Searching for 'Python'...")
    results = agent2.memory.search("Python", limit=3)
    print(f"Found {len(results)} results:")
    for i, msg in enumerate(results, 1):
        print(f"\n  {i}. [{msg['role']}]: {msg['content'][:80]}...")
    print()
    
    # Get recent messages
    print("\n📜 Recent conversation history:")
    recent = agent2.memory.get_recent_messages(limit=6)
    for msg in recent:
        role_emoji = "👤" if msg['role'] == 'user' else "🤖"
        print(f"\n  {role_emoji} [{msg['role']}]: {msg['content'][:100]}")
    
    # Final stats
    print("\n" + "="*60)
    print("FINAL MEMORY STATS")
    print("="*60)
    stats = agent2.memory.stats()
    print(f"\n✅ Total messages: {stats['total_messages']}")
    print(f"✅ User messages: {stats['user_messages']}")
    print(f"✅ Assistant messages: {stats['assistant_messages']}")
    
    print("\n" + "="*60)
    print("MEMORY CAPABILITIES")
    print("="*60)
    print("\n✅ Persistent across sessions")
    print("✅ Automatic conversation storage")
    print("✅ Search past conversations")
    print("✅ Agent remembers you!")
    
    print("\n🎯 Killer Feature:")
    print("   Agent becomes smarter over time by learning from interactions")
    
    # Cleanup
    if os.path.exists(memory_path):
        os.remove(memory_path)
        print(f"\n♻️  Cleaned up test memory database")

if __name__ == "__main__":
    main()
