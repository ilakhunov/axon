import pytest
from unittest.mock import MagicMock, patch
from axon import Agent, Swarm, Handoff, Context, tool

# --- Mocks & Fixtures ---

@pytest.fixture
def mock_agent_a():
    agent = Agent(name="AgentA", model="gpt-4o")
    # Mocking the client to avoid real API calls
    agent.client = MagicMock()
    return agent

@pytest.fixture
def mock_agent_b():
    agent = Agent(name="AgentB", model="gpt-4o")
    agent.client = MagicMock()
    return agent

# --- Tests ---

def test_handoff_primitive():
    """Test the Handoff model initialization."""
    handoff = Handoff(target_agent="Billing", context="Refund")
    assert handoff.target_agent == "Billing"
    assert handoff.context == "Refund"

def test_swarm_initialization(mock_agent_a, mock_agent_b):
    """Test that Swarm initializes correctly and shares context."""
    swarm = Swarm([mock_agent_a, mock_agent_b])
    
    assert "AgentA" in swarm.agents
    assert "AgentB" in swarm.agents
    
    # Check shared context
    assert isinstance(swarm.context, Context)
    assert mock_agent_a.context is swarm.context
    assert mock_agent_b.context is swarm.context

def test_shared_context_persistence(mock_agent_a, mock_agent_b):
    """Test that context is truly shared between agents."""
    swarm = Swarm([mock_agent_a, mock_agent_b])
    
    # Agent A writes to context
    mock_agent_a.context.set("session_id", "12345")
    
    # Agent B reads from context
    assert mock_agent_b.context.get("session_id") == "12345"

def test_swarm_handoff_flow(mock_agent_a, mock_agent_b):
    """
    Test the full Handoff flow:
    Agent A -> returns Handoff -> Swarm switches -> Agent B returns Final Answer
    """
    swarm = Swarm([mock_agent_a, mock_agent_b])
    
    # Mock Agent A to return a Handoff object
    # We mock the ask() method directly to bypass OpenAI call
    handoff_signal = Handoff(target_agent="AgentB", context="Transfering")
    mock_agent_a.ask = MagicMock(return_value=handoff_signal)
    
    # Mock Agent B to return a final string
    mock_agent_b.ask = MagicMock(return_value="Hello from Agent B")
    
    # Run Swarm
    result = swarm.run(starting_agent=mock_agent_a, prompt="Start")
    
    # Assertions
    mock_agent_a.ask.assert_called_once() # Agent A was called
    mock_agent_b.ask.assert_called_once() # Agent B was called (transition happened)
    assert result == "Hello from Agent B" # Final result came from Agent B

def test_swarm_agent_not_found(mock_agent_a):
    """Test error handling when handing off to a non-existent agent."""
    swarm = Swarm([mock_agent_a])
    
    # Agent A tries to handoff to a ghost
    handoff_signal = Handoff(target_agent="GhostAgent", context="Boo")
    mock_agent_a.ask = MagicMock(return_value=handoff_signal)
    
    result = swarm.run(starting_agent=mock_agent_a, prompt="Start")
    
    assert "Error: Agent 'GhostAgent' not found" in result

def test_swarm_error_handling(mock_agent_a):
    """Test that Swarm catches exceptions raised by agents."""
    swarm = Swarm([mock_agent_a])
    
    # Agent A raises an exception
    mock_agent_a.ask = MagicMock(side_effect=Exception("API Down"))
    
    result = swarm.run(starting_agent=mock_agent_a, prompt="Start")
    
    assert "Error executing AgentA" in result
    assert "API Down" in result
