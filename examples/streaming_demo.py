import os
import sys
import time

# Add project root to path for local run
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from axon import Agent

def main():
    print("🌊 Testing Streaming Responses...\n")
    
    agent = Agent("StreamBot", system="You are a helpful assistant.")
    
    # Check for API Key
    if not os.environ.get("OPENAI_API_KEY"):
        print("❌ Error: OPENAI_API_KEY not found.")
        return

    # Test 1: Simple streaming
    print("="*60)
    print("TEST 1: Simple Question (Streaming)")
    print("="*60)
    question = "Explain what AI agents are in 2-3 sentences."
    print(f"\n🗣️  Question: {question}\n")
    print("🌊 Streaming response:")
    print("-" * 60)
    
    for chunk in agent.ask_stream(question):
        print(chunk, end="", flush=True)
    
    print("\n" + "-" * 60)
    print("✅ Streaming complete!\n")
    
    # Test 2: Longer response
    print("="*60)
    print("TEST 2: Long Response (Shows Streaming Value)")
    print("="*60)
    question2 = "Write a short story about a robot learning to code (3 paragraphs)."
    print(f"\n🗣️  Question: {question2}\n")
    print("🌊 Streaming response:")
    print("-" * 60)
    
    start_time = time.time()
    char_count = 0
    
    for chunk in agent.ask_stream(question2):
        print(chunk, end="", flush=True)
        char_count += len(chunk)
    
    elapsed = time.time() - start_time
    
    print("\n" + "-" * 60)
    print(f"✅ Streaming complete!")
    print(f"📊 Stats: {char_count} chars in {elapsed:.1f}s ({char_count/elapsed:.0f} chars/sec)\n")
    
    # Test 3: With tools
    print("="*60)
    print("TEST 3: Streaming with Tool Calls")
    print("="*60)
    
    @agent.tool
    def get_weather(city: str) -> str:
        """Get current weather for a city."""
        return f"Weather in {city}: Sunny, 22°C"
    
    question3 = "What's the weather in Paris and tell me a fun fact about the city?"
    print(f"\n🗣️  Question: {question3}\n")
    print("🌊 Streaming response:")
    print("-" * 60)
    
    for chunk in agent.ask_stream(question3):
        print(chunk, end="", flush=True)
    
    print("\n" + "-" * 60)
    print("✅ Streaming complete!\n")
    
    # Comparison with non-streaming
    print("="*60)
    print("COMPARISON: Streaming vs Non-Streaming UX")
    print("="*60)
    print("\n✅ Streaming (ask_stream):")
    print("   - User sees text appear in real-time")
    print("   - Feels responsive and interactive")
    print("   - No waiting period")
    print("\n❌ Non-streaming (ask):")
    print("   - User waits 5-30+ seconds")
    print("   - No feedback during generation")
    print("   - Feels slow")
    print("\n🎯 Streaming provides MUCH better UX!")

if __name__ == "__main__":
    main()
