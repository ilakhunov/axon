import os
import sys

# Add project root to path for local run
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from axon import Agent
from axon_tools import http_get, http_post

def main():
    print("🌐 Testing HTTP/API Tools...\n")
    
    agent = Agent("APIBot", system="You are a helpful assistant that can interact with web APIs.")
    
    # Register HTTP tools
    agent.tool(http_get)
    agent.tool(http_post)
    
    # Check for API Key
    if not os.environ.get("OPENAI_API_KEY"):
        print("❌ Error: OPENAI_API_KEY not found.")
        return

    # Test 1: GET request to public API
    print("="*60)
    print("TEST 1: GET Request to JSONPlaceholder API")
    print("="*60)
    
    task1 = "Get user data from https://jsonplaceholder.typicode.com/users/1 and tell me the user's name and email"
    print(f"\n📝 Task: {task1}\n")
    
    response = agent.ask(task1)
    print(f"\n🤖 Response:\n{response}\n")
    
    # Test 2: POST request
    print("="*60)
    print("TEST 2: POST Request")
    print("="*60)
    
    task2 = """Make a POST request to https://jsonplaceholder.typicode.com/posts with this data:
    - title: "Axon Framework is Amazing"
    - body: "Testing HTTP tools"
    - userId: 1
    
Let me know if it was successful."""
    
    print(f"\n📝 Task: {task2}\n")
    
    response = agent.ask(task2)
    print(f"\n🤖 Response:\n{response}\n")
    
    # Test 3: Multiple API calls
    print("="*60)
    print("TEST 3: Multiple API Calls (User + Posts)")
    print("="*60)
    
    task3 = """Do the following:
1. Get user info for user ID 2 from https://jsonplaceholder.typicode.com/users/2
2. Get their posts from https://jsonplaceholder.typicode.com/posts?userId=2
3. Tell me the user's name and how many posts they have"""
    
    print(f"\n📝 Task: {task3}\n")
    
    response = agent.ask(task3)
    print(f"\n🤖 Response:\n{response}\n")
    
    # Summary
    print("="*60)
    print("HTTP TOOLS CAPABILITIES")
    print("="*60)
    print("\n✅ http_get:")
    print("   - Make GET requests to any URL")
    print("   - Optional headers and query params")
    print("   - Auto JSON parsing")
    print("\n✅ http_post:")
    print("   - Make POST requests with data")
    print("   - Support for form data and JSON")
    print("   - Custom headers")
    print("\n🎯 Use Cases:")
    print("   - GitHub API integration")
    print("   - Slack/Discord bots")
    print("   - Any REST API")
    print("   - Webhooks")

if __name__ == "__main__":
    main()
