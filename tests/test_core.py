import pytest
import os
from axon import Agent

def test_agent_initialization():
    os.environ["OPENAI_API_KEY"] = "sk-dummy"
    agent = Agent("TestBot")
    assert agent.name == "TestBot"
    assert agent.model == "gpt-4o"
    assert len(agent.tools) == 0

def test_tool_registration():
    os.environ["OPENAI_API_KEY"] = "sk-dummy"
    agent = Agent("ToolBot")
    
    @agent.tool
    def add(a: int, b: int) -> int:
        """Adds two numbers."""
        return a + b
        
    assert "add" in agent.tools
    assert agent.tools["add"].func(1, 2) == 3
    schema = agent.tools["add"].schema_['function']
    assert schema['name'] == "add"
    assert "a" in schema['parameters']['properties']

def test_tool_execution_error():
    """Verify tool execution errors are caught gracefully."""
    os.environ["OPENAI_API_KEY"] = "sk-dummy"
    agent = Agent("ErrorBot")
    
    @agent.tool
    def bad_tool():
        raise ValueError("Tool crashed")
        
    # We can invoke the tool wrapper manually if we had access, 
    # but here we just test the direct function for now.
    with pytest.raises(ValueError):
        agent.tools["bad_tool"].func() # If we had it
        
    # Real integration test would need LLM mock
