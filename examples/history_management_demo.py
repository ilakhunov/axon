import os
import sys

# Add project root to path for local run
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from axon import Agent

def main():
    print("🧠 Testing History Management...")
    
    # Create agent with very low token limit for testing
    agent = Agent(
        "HistoryBot",
        system="You are a helpful assistant.",
        max_history_tokens=200  # Very low to trigger truncation quickly
    )
    
    # Check for API Key
    if not os.environ.get("OPENAI_API_KEY"):
        print("\n❌ Error: OPENAI_API_KEY not found.")
        return

    print(f"\n📊 Max history tokens: {agent.max_history_tokens}")
    print(f"📝 Initial history size: {len(agent.history)} messages\n")
    
    # Have a long conversation to trigger truncation
    questions = [
        "What is the capital of France?",
        "What is 2 + 2?",
        "Tell me a joke about programming.",
        "What is the meaning of life?",
        "Explain quantum physics in one sentence.",
        "What's the weather like on Mars?",
        "Write a haiku about AI.",
        "What color is the sky?",
    ]
    
    for i, question in enumerate(questions, 1):
        print(f"{'='*60}")
        print(f"Question {i}/{len(questions)}: {question}")
        
        # Count tokens before
        tokens_before = agent._count_tokens(agent.history)
        msgs_before = len(agent.history)
        
        response = agent.ask(question)
        
        # Count tokens after
        tokens_after = agent._count_tokens(agent.history)
        msgs_after = len(agent.history)
        
        print(f"\n📊 Stats:")
        print(f"  Messages: {msgs_before} → {msgs_after}")
        print(f"  Tokens: {tokens_before} → {tokens_after}")
        print(f"  Max: {agent.max_history_tokens}")
        
        if tokens_after < tokens_before:
            print(f"  ✂️  TRUNCATION OCCURRED!")
        
        print(f"\n🤖 Response: {response[:80]}...")
        print()
    
    print(f"\n{'='*60}")
    print(f"✅ Final history: {len(agent.history)} messages, {agent._count_tokens(agent.history)} tokens")
    print(f"✅ Stayed under limit: {agent._count_tokens(agent.history) <= agent.max_history_tokens}")

if __name__ == "__main__":
    main()
