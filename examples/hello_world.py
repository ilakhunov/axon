import os
import sys

# Add project root to path for local run
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from axon import Agent

def main():
    # 1. Initialize
    print("🧠 Initializing Axon...")
    agent = Agent("MathWhiz", system="You are a helpful math tutor. Use tools for calculations.")

    # 2. Register Tool
    print("🛠️  Registering tools...")
    
    @agent.tool
    def add(a: int, b: int) -> int:
        """Adds two integers."""
        print(f"   [Tool Side Effect] Adding {a} + {b}...")
        return a + b

    # 3. Check for API Key
    if not os.environ.get("OPENAI_API_KEY"):
        print("\n❌ Error: OPENAI_API_KEY not found.")
        print("Address this by running: export OPENAI_API_KEY='sk-...'")
        return

    # 4. Run
    prompt = "If I have 5 apples and buy 10 more, how many do I have?"
    print(f"\n🗣️  Asking: '{prompt}'\n")
    
    response = agent.ask(prompt)
    
    print(f"\n🤖 Answer: {response}\n")

if __name__ == "__main__":
    main()
