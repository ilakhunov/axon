import os
os.environ["OPENAI_API_KEY"] = "sk-dummy" # Prevent OpenAI client from crashing

from axon import Agent
import json

def test_tool_registration():
    agent = Agent("TestBot")

    @agent.tool
    def calculator(a: int, b: int) -> int:
        """Adds two numbers."""
        return a + b

    print("Verifying tool registration...")
    assert "calculator" in agent.tools
    tool = agent.tools["calculator"]
    
    print("Verifying schema...")
    schema = tool.schema_['function']
    print(json.dumps(schema, indent=2))
    
    assert schema['name'] == 'calculator'
    assert schema['description'] == 'Adds two numbers.'
    assert "a" in schema['parameters']['properties']
    assert "b" in schema['parameters']['properties']
    
    print("\nVerifying execution...")
    result = tool.func(a=5, b=10)
    assert result == 15
    print(f"Result: {result}")
    
    print("\nALL SYSTEM GO! 🚀")

if __name__ == "__main__":
    test_tool_registration()
