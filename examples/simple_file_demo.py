import os
import sys

# Add project root to path for local run
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from axon import Agent
from axon_tools import web_search, write_file

def main():
    print("🔬 Initializing Simple Web Agent...")
    
    agent = Agent(
        name="SimpleResearcher",
        system="You are a helpful assistant. When asked to save information, you MUST use the write_file tool."
    )

    print("🛠️  Registering tools...")
    
    # Register tools
    agent.tool(web_search)
    agent.tool(write_file)
    
    # Check for API Key
    if not os.environ.get("OPENAI_API_KEY"):
        print("\n❌ Error: OPENAI_API_KEY not found.")
        print("Set it using: export OPENAI_API_KEY='sk-...'")
        return

    # Simpler, more direct task
    prompt = "Write 'Hello from Axon AI Agent!' to a file called greeting.txt"
    print(f"\n🗣️  Task: '{prompt}'\n")
    
    response = agent.ask(prompt)
    
    print(f"\n🤖 Result:\n{response}\n")
    
    # Verify file was created
    if os.path.exists("greeting.txt"):
        print("✅ SUCCESS! File created. Contents:")
        with open("greeting.txt", "r") as f:
            print(f"   '{f.read()}'")
    else:
        print("❌ File was not created")

if __name__ == "__main__":
    main()
