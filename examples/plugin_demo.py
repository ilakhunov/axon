import os
import sys

# Add project root to path for local run
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from axon import Agent
from plugin_example_email import send_email, send_notification

def main():
    print("📧 Testing Email Plugin Example...\n")
    
    agent = Agent("EmailBot", system="You are a helpful assistant that can send emails.")
    
    # Register email tools
    agent.tool(send_email)
    agent.tool(send_notification)
    
    print("="*60)
    print("EMAIL PLUGIN DEMO")
    print("="*60)
    print("\nThis demonstrates how to create an Axon plugin.")
    print("\n📦 Plugin Structure:")
    print("   - plugin_example_email.py: Tool implementations")
    print("   - Type hints + docstrings")
    print("   - Error handling")
    print("   - Environment variable config")
    
    print("\n🔧 Registered Tools:")
    print("   1. send_email - Full email with subject/body")
    print("   2. send_notification - Quick notification")
    
    print("\n💡 Usage in Agent:")
    print("   agent.tool(send_email)")
    print("   agent.ask('Send an email to john@example.com')")
    
    print("\n📝 To actually send emails, set:")
    print("   export SMTP_SERVER='smtp.gmail.com'")
    print("   export SMTP_FROM_EMAIL='your-email@gmail.com'")
    print("   export SMTP_PASSWORD='your-app-password'")
    
    # Check for API Key
    if not os.environ.get("OPENAI_API_KEY"):
        print("\n❌ OPENAI_API_KEY not set. Skipping agent test.")
    else:
        print("\n" + "="*60)
        print("AGENT INTEGRATION TEST")
        print("="*60)
        
        # Note: This will fail without SMTP credentials, but shows how it works
        task = "Explain what the send_email tool can do"
        print(f"\n📝 Task: {task}\n")
        
        response = agent.ask(task)
        print(f"🤖 Response:\n{response}\n")
    
    print("="*60)
    print("PLUGIN CREATION GUIDE")
    print("="*60)
    print("\n✅ To create your own plugin:")
    print("   1. Create a .py file with your tools")
    print("   2. Add type hints to all parameters")
    print("   3. Write clear docstrings")
    print("   4. Handle errors gracefully")
    print("   5. Return strings or JSON-serializable types")
    
    print("\n✅ To share your plugin:")
    print("   1. Create a PyPI package (axon-plugin-yourname)")
    print("   2. Or share on GitHub")
    print("   3. Users: pip install axon-plugin-yourname")
    
    print("\n📚 See docs/PLUGIN_GUIDE.md for full details")

if __name__ == "__main__":
    main()
