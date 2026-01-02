"""
Test for response_model structured output.
Reproduces bug where response_model returns str instead of Pydantic model.
"""
import pytest
from pydantic import BaseModel
from axon import Agent


class UserInfo(BaseModel):
    name: str
    age: int
    email: str


def test_response_model_returns_pydantic_instance():
    """Test that response_model always returns the specified Pydantic model."""
    agent = Agent("TestBot", model="gpt-4o-mini")
    
    result = agent.ask(
        "Extract: John Doe, 30 years old, john@example.com",
        response_model=UserInfo
    )
    
    # CRITICAL: Must return UserInfo instance, not str
    assert isinstance(result, UserInfo), f"Expected UserInfo, got {type(result)}"
    assert result.name == "John Doe"
    assert result.age == 30
    assert result.email == "john@example.com"


def test_response_model_with_invalid_data():
    """Test error handling when LLM returns invalid data."""
    agent = Agent("TestBot", model="gpt-4o-mini")
    
    # This should either raise ValidationError or return error message
    result = agent.ask(
        "Just say hello",  # Intentionally vague to confuse LLM
        response_model=UserInfo
    )
    
    # Should NOT return a plain string
    assert not isinstance(result, str) or result.startswith("Error:"), \
        "Should return error or raise exception, not plain text"
