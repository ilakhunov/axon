from axon import Agent, Swarm, tool, Handoff, Context
from rich.console import Console
from rich.panel import Panel

console = Console()

# --- Tools Definition ---

@tool
def refund_order(ctx: Context):
    """Process a refund for the order found in context."""
    order_id = ctx.get("order_id")
    if not order_id:
        return "❌ Error: No order ID found in context. Ask user for order ID."
    return f"✅ Refund processed for Order #{order_id}."

@tool
def save_order_context(ctx: Context, order_id: str):
    """Save order ID to shared context."""
    ctx.set("order_id", order_id)
    return f"Saved order ID {order_id} to context."

@tool
def check_logs(service: str):
    """Check system logs for a service."""
    return f"📊 Logs for {service}: [WARN] Memory usage at 85%."

@tool
def transfer_to_billing(reason: str) -> Handoff:
    """Transfer the user to the Billing department."""
    return Handoff(target_agent="Billing", context=reason)

@tool
def transfer_to_tech(reason: str) -> Handoff:
    """Transfer the user to Technical Support."""
    return Handoff(target_agent="Tech", context=reason)

# --- Agents Setup ---

# 1. Triage Agent: The Front Desk
triage = Agent(
    name="Triage",
    system="""You are the front desk receptionist. 
    Identify if the user has a billing issue or a technical issue.
    IMMEDIATELY transfer them to the correct department using tools.
    Do not try to solve the problem yourself.""",
    model="gpt-4o"
)
triage.register_tool(transfer_to_billing)
triage.register_tool(transfer_to_tech)
triage.register_tool(save_order_context)

# 2. Billing Agent: The Specialist
billing = Agent(
    name="Billing",
    system="You are a billing specialist. You can process refunds.",
    model="gpt-4o"
)
billing.register_tool(refund_order)

# 3. Tech Agent: The Engineer
tech = Agent(
    name="Tech",
    system="You are a DevOps engineer. You check logs and fix server issues.",
    model="gpt-4o"
)
tech.register_tool(check_logs)

# --- Swarm Execution ---

def main():
    console.print(Panel.fit("[bold blue]Axon Swarm Demo[/] 🐝\nMulti-Agent Orchestration"))
    
    # Initialize the Swarm with all available agents
    swarm = Swarm(agents=[triage, billing, tech])
    
    # Scenario 1: Billing Issue
    console.print("\n[bold yellow]--- Scenario 1: User asks for a refund ---[/]")
    swarm.run(starting_agent=triage, prompt="I want my money back for order #555!")
    
    # Scenario 2: Technical Issue
    console.print("\n[bold yellow]--- Scenario 2: User reports a crash ---[/]")
    swarm.run(starting_agent=triage, prompt="The payment API is throwing 500 errors.")

if __name__ == "__main__":
    main()
