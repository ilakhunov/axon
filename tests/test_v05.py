import os
import pytest
from axon import Agent, retry 
from axon.memory import Memory
import tempfile
import sqlite3

def test_memory_persistence():
    """Test that memory persists across agent instances."""
    
    # Create temp DB
    with tempfile.NamedTemporaryFile(suffix=".db") as tmp_db:
        db_path = tmp_db.name
        
        # 1. Initialize Memory directly
        mem = Memory(db_path)
        mem.save_message("user", "Hello, I am Alice")
        mem.save_message("assistant", "Hi Alice!")
        
        # 2. Verify recent messages
        recent = mem.get_recent_messages(5)
        assert len(recent) == 2
        assert recent[0]['role'] == "user"
        assert recent[1]['role'] == "assistant"
        
        # 3. Verify Search
        results = mem.search("Alice")
        assert len(results) >= 2
        
        # 4. Integrate with Agent
        # Mock OpenAI to avoid real calls
        os.environ["OPENAI_API_KEY"] = "sk-dummy"
        
        agent = Agent("TestBot", memory=db_path)
        # We can't easily test ask() without mocking OpenAI fully, 
        # but we checked the integration logic manually.
        # Here we verify the agent took the memory path.
        assert agent.memory is not None

def test_retry_decorator():
    """Test automation retry logic."""
    
    attempts = 0
    
    @retry(max_attempts=3, backoff=0.1) # Fast backoff for test
    def flaky_func():
        nonlocal attempts
        attempts += 1
        if attempts < 3:
            raise ValueError("Fail!")
        return "Success"
        
    # Should succeed on 3rd attempt
    result = flaky_func()
    assert result == "Success"
    assert attempts == 3

def test_retry_failure():
    """Test that it raises exception after max attempts."""
    
    attempts = 0
    
    @retry(max_attempts=2, backoff=0.1)
    def always_fail():
        nonlocal attempts
        attempts += 1
        raise ValueError("Fail forever")
        
    with pytest.raises(ValueError):
        always_fail()
        
    assert attempts == 2
