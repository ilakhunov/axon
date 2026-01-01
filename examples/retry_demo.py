import os
import sys
import time

# Add project root to path for local run
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from axon import Agent, retry

def main():
    print("🔄 Testing Error Retry Logic...\n")
    
    # Counter to simulate flaky behavior
    call_count = {"api": 0, "db": 0}
    
    agent = Agent("RetryBot", system="You are a helpful assistant that works with unreliable tools.")
    
    # Test 1: Flaky API that fails first 2 times
    @agent.tool
    @retry(max_attempts=3, backoff=1.0)
    def flaky_api_call(endpoint: str) -> str:
        """
        Call a flaky API endpoint that may fail.
        
        Args:
            endpoint: API endpoint to call
        """
        call_count["api"] += 1
        
        # Simulate failure on first 2 attempts
        if call_count["api"] < 3:
            raise ConnectionError(f"API temporarily unavailable (attempt {call_count['api']})")
        
        return f"✅ Success! API {endpoint} returned data after {call_count['api']} attempts"
    
    # Test 2: Database query with occasional timeouts
    @agent.tool
    @retry(max_attempts=4, backoff=0.5)
    def unreliable_db_query(query: str) -> str:
        """
        Execute database query that may timeout.
        
        Args:
            query: SQL query to execute
        """
        call_count["db"] += 1
        
        # Fail on attempt 1 and 2
        if call_count["db"] <= 2:
            raise TimeoutError(f"Database timeout (attempt {call_count['db']})")
        
        return f"✅ Query executed: Found 42 results for '{query}' (after {call_count['db']} attempts)"
    
    # Test 3: Function that always fails (to test max attempts)
    @agent.tool
    @retry(max_attempts=2, backoff=0.5)
    def always_fails(task: str) -> str:
        """
        A tool that always fails (for testing).
        
        Args:
            task: Task to attempt
        """
        raise RuntimeError("This task cannot be completed")
    
    # Check for API Key
    if not os.environ.get("OPENAI_API_KEY"):
        print("❌ Error: OPENAI_API_KEY not found.")
        print("Testing retry decorator directly instead...\n")
        
        # Direct tests without agent
        print("="*60)
        print("TEST 1: Flaky API (will succeed on 3rd attempt)")
        print("="*60)
        try:
            result = flaky_api_call.func("users")  # Access original function
            print(f"\n{result}\n")
        except Exception as e:
            print(f"\n❌ Failed: {e}\n")
        
        print("="*60)
        print("TEST 2: Unreliable Database")
        print("="*60)
        try:
            result = unreliable_db_query.func("SELECT * FROM users")
            print(f"\n{result}\n")
        except Exception as e:
            print(f"\n❌ Failed: {e}\n")
        
        print("="*60)
        print("TEST 3: Always Fails (should give up after 2 attempts)")
        print("="*60)
        try:
            result = always_fails.func("impossible")
            print(f"\n{result}\n")
        except Exception as e:
            print(f"\n❌ Expected failure after retries: {e}\n")
        
    else:
        # Tests with agent
        print("="*60)
        print("TEST 1: Flaky API Call")
        print("="*60)
        task1 = "Call the flaky_api_call for endpoint 'users'"
        print(f"\n📝 Task: {task1}\n")
        response = agent.ask(task1)
        print(f"\n🤖 Response:\n{response}\n")
        
        print("="*60)
        print("TEST 2: Unreliable Database Query")
        print("="*60)
        task2 = "Query the database for 'active users'"
        print(f"\n📝 Task: {task2}\n")
        response = agent.ask(task2)
        print(f"\n🤖 Response:\n{response}\n")
    
    # Summary
    print("="*60)
    print("RETRY CAPABILITIES")
    print("="*60)
    print("\n✅ @retry decorator:")
    print("   - Automatic retry on failure")
    print("   - Exponential backoff (1s, 2s, 4s, ...)")
    print("   - Configurable max attempts")
    print("   - Custom exception handling")
    
    print("\n✅ @retry_on_rate_limit:")
    print("   - Specialized for API rate limits")
    print("   - Smart detection of 429 errors")
    print("   - Longer backoff times")
    
    print("\n🎯 Benefits:")
    print("   - Production-ready error handling")
    print("   - Resilient to temporary failures")
    print("   - No manual retry logic needed")
    print("   - Better reliability for users")

if __name__ == "__main__":
    main()
