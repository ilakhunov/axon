import os
import sys

# Add project root to path for local run
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from axon import Agent, Context

def main():
    print("🧠 Testing Context/State Management...")
    
    agent = Agent("ResearchBot", system="You are a helpful research assistant.")
    
    # Register tools that use shared context
    @agent.tool
    def fetch_data(source: str, ctx: Context) -> str:
        """
        Fetch data from a source and store it in context.
        
        Args:
            source: The data source (e.g., 'database', 'api')
            ctx: Shared context (injected automatically)
        """
        # Simulate fetching data
        data = f"Data from {source}: [user_id: 123, name: Alice, age: 30]"
        
        # Store in context for other tools
        ctx.set("fetched_data", data)
        ctx.set("data_source", source)
        
        return f"✅ Fetched and stored data from {source}"
    
    @agent.tool
    def analyze_data(ctx: Context) -> str:
        """
        Analyze previously fetched data from context.
        
        Args:
            ctx: Shared context (injected automatically)
        """
        # Retrieve from context
        data = ctx.get("fetched_data")
        source = ctx.get("data_source", "unknown")
        
        if not data:
            return "❌ No data found in context. Please fetch data first."
        
        # Simulate analysis
        analysis = f"Analysis of data from {source}: Found 1 user (Alice, age 30)"
        
        # Store results
        ctx.set("analysis_result", analysis)
        
        return f"✅ {analysis}"
    
    @agent.tool
    def save_report(filename: str, ctx: Context) -> str:
        """
        Save analysis report to a file using data from context.
        
        Args:
            filename: Name of the file to save
            ctx: Shared context (injected automatically)
        """
        analysis = ctx.get("analysis_result")
        source = ctx.get("data_source")
        
        if not analysis:
            return "❌ No analysis found. Please analyze data first."
        
        # Simulate saving
        report = f"Report from {source}:\n{analysis}\n"
        
        return f"✅ Saved report to {filename} ({len(report)} chars)"
    
    # Check for API Key
    if not os.environ.get("OPENAI_API_KEY"):
        print("\n❌ Error: OPENAI_API_KEY not found.")
        return

    # Test multi-step workflow with shared context
    print("\n" + "="*60)
    print("TEST: Multi-step workflow with Context")
    print("="*60)
    
    task = """
    Please do the following steps:
    1. Fetch data from 'database'
    2. Analyze the fetched data  
    3. Save the analysis to 'report.txt'
    """
    
    print(f"\n📝 Task:\n{task}")
    print(f"\n🔧 Context before: {agent.context}")
    print()
    
    response = agent.ask(task)
    
    print(f"\n🤖 Final Response:\n{response}\n")
    print(f"🔧 Context after: {agent.context}")
    print(f"\n✅ Context keys: {agent.context.keys()}")
    
    # Verify context was used
    print("\n" + "="*60)
    print("VERIFICATION:")
    print("="*60)
    print(f"✅ Data fetched: {agent.context.has('fetched_data')}")
    print(f"✅ Data analyzed: {agent.context.has('analysis_result')}")
    print(f"✅ Source tracked: {agent.context.get('data_source')}")

if __name__ == "__main__":
    main()
