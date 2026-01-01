import os
import sys

# Add project root to path for local run
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from axon import Agent
from axon_tools import web_search, write_file

def main():
    print("🔬 Initializing Research Agent...")
    
    agent = Agent(
        name="WebResearcher",
        system="""You are a helpful research assistant with access to web search and file writing tools.

IMPORTANT INSTRUCTIONS:
1. When asked to research and save information, you MUST follow this workflow:
   - First, use web_search to find information
   - Then, ALWAYS use write_file to save a summary
2. Your summary should be clear, well-formatted, and include sources (URLs)
3. Never tell the user you "cannot find" information without trying web_search first
4. Always confirm when you've written to a file"""
    )

    print("🛠️  Registering tools...")
    
    # Register web search tool
    agent.tool(web_search)
    
    # Register file writing tool
    agent.tool(write_file)
    
    # Check for API Key
    if not os.environ.get("OPENAI_API_KEY"):
        print("\n❌ Error: OPENAI_API_KEY not found.")
        print("Set it using: export OPENAI_API_KEY='sk-...'")
        print("Or create a .env file in the project root.")
        return

    # More explicit, step-by-step task
    prompt = """Please complete this 2-step task:
1. Search the web for 'Python AI frameworks 2024' 
2. Write a summary of what you found to 'ai_research.txt'

Make sure to complete BOTH steps."""
    
    print(f"\n🗣️  Task: {prompt}\n")
    
    response = agent.ask(prompt)
    
    print(f"\n🤖 Final Response:\n{response}\n")
    
    # Verify file was created
    if os.path.exists("ai_research.txt"):
        print("✅ SUCCESS! File 'ai_research.txt' was created.")
        print("\nFile contents:")
        print("-" * 50)
        with open("ai_research.txt", "r") as f:
            print(f.read())
        print("-" * 50)
    else:
        print("❌ Warning: File 'ai_research.txt' was not created")

if __name__ == "__main__":
    main()
