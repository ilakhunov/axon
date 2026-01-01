from axon import Agent, tool
from axon.tracing import FileTracer

# Initialize Tracer
tracer = FileTracer("trace.jsonl")

# Initialize Agent with Tracer
agent = Agent(
    name="TracerBot",
    tracer=tracer,
    system="You are a helpful assistant."
)

@tool
def calculate(a: int, b: int) -> int:
    """Add two numbers."""
    return a + b

agent.register_tool(calculate)

print("🤖 Running TracerBot...")
response = agent.ask("What is 100 + 250?")
print(f"Response: {response}")
print("\n✅ Trace saved to trace.jsonl")
