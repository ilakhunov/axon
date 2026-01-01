import logging
from axon import Agent
from rich.logging import RichHandler

# 1. Configure Logging to DEBUG level
# We need to set it explicitly because Axon initializes it to INFO by default
logging.getLogger("axon").setLevel(logging.DEBUG)
logging.getLogger("openai").setLevel(logging.DEBUG)
logging.getLogger("httpcore").setLevel(logging.DEBUG)
logging.getLogger("httpx").setLevel(logging.DEBUG)

def main():
    print("🐛 Axon Debugging Demo")
    print("Check the console output for verbose logs...\n")

    # 2. Create Agent
    agent = Agent("DebugBot", model="gpt-4o")

    # 3. internal state inspection
    print(f"Agent Config: {agent.config}")
    print(f"Tools Registered: {list(agent.tools.keys())}")

    # 4. Run detailed query
    response = agent.ask("Calculate 12 * 12")
    
    print(f"\nFinal Response: {response}")

if __name__ == "__main__":
    main()
