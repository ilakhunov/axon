import asyncio
import time
from axon import AsyncAgent, tool

# Initialize Async Agent
agent = AsyncAgent(
    name="Speedy",
    system="You are a helpful assistant. Use tools to fetch data.",
    model="gpt-4o"
)

@tool
async def fetch_stock_price(ticker: str) -> str:
    """Fetch stock price asynchronously (simulated)."""
    print(f"⏳ Fetching price for {ticker}...")
    await asyncio.sleep(2) # Simulate network delay
    return f"Price of {ticker} is $150.00"

@tool
async def fetch_weather(city: str) -> str:
    """Fetch weather asynchronously (simulated)."""
    print(f"⏳ Fetching weather for {city}...")
    await asyncio.sleep(2) # Simulate network delay
    return f"Weather in {city} is Sunny 25°C"

agent.register_tool(fetch_stock_price)
agent.register_tool(fetch_weather)

async def main():
    print("🚀 Starting Async Demo...")
    start_time = time.time()
    
    # The agent should be able to call tools.
    # Note: Currently Agent.ask executes tools sequentially even in async mode 
    # unless we parallelize the loop in core.py. 
    # But the outer call is non-blocking to the main thread event loop!
    
    response = await agent.ask("What is the stock price of AAPL and the weather in Tokyo?")
    
    end_time = time.time()
    print(f"\n🤖 Agent Response: {response}")
    print(f"⏱️ Total Time: {end_time - start_time:.2f}s")

if __name__ == "__main__":
    asyncio.run(main())
