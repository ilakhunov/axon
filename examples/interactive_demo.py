import os
import sys
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from axon import Agent

# Setup beautiful console
console = Console()

def main():
    # 1. Clear screen for clean video start
    os.system('cls' if os.name == 'nt' else 'clear')
    
    console.print(Panel.fit(
        "[bold blue]Axon v0.5[/] - Persistent Memory Demo",
        subtitle="[dim]Type 'exit' to quit[/]"
    ))

    # 2. Initialize Agent with Memory
    # using a local file 'demo.db' so it persists between runs
    agent = Agent(
        name="MemBot", 
        model="gpt-4o",
        memory="demo_memory.db"
    )

    console.print("[green]✓[/] Agent initialized with [bold]SQLite Memory[/]\n")

    # 3. Interactive Loop
    while True:
        try:
            user_input = console.input("[bold green]You:[/]\n")
            if user_input.lower() in ['exit', 'quit']:
                break
            
            # Show a nice spinner while thinking (Axon does this internally? No, we add it here for effect)
            with console.status("[bold blue]Thinking...[/]"):
                response = agent.ask(user_input)
            
            console.print(f"\n[bold blue]Axon:[/]\n{response}\n")
            
        except KeyboardInterrupt:
            break

    console.print("\n[dim]Session ended.[/]")

if __name__ == "__main__":
    main()
