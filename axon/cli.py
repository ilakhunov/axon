import click
import os
from rich.console import Console
from rich.panel import Panel

console = Console()

@click.group()
def cli():
    """Axon Framework CLI 🚀"""
    pass

@cli.command()
@click.argument("project_name")
def new(project_name):
    """Create a new Axon project."""
    if os.path.exists(project_name):
        console.print(f"[bold red]Error:[/bold red] Directory '{project_name}' already exists.")
        return

    console.print(f"[bold green]Creating new Axon project: {project_name}[/bold green]")
    
    os.makedirs(project_name)
    
    # helper to write file
    def write(path, content):
        with open(os.path.join(project_name, path), "w") as f:
            f.write(content.strip() + "\n")
            
    # 1. app.py
    write("app.py", """
from axon import Agent

# Initialize your agent
agent = Agent(
    name="MyAgent",
    system="You are a helpful AI assistant built with Axon."
)

if __name__ == "__main__":
    # Choose your mode:
    
    # 1. Chat in console
    response = agent.ask("Hello, who are you?")
    print(response)
    
    # 2. Or serve via API
    # agent.serve()
""")

    # 2. .env.example
    write(".env.example", """
OPENAI_API_KEY=sk-...
""")

    # 3. README.md
    write("README.md", f"""
# {project_name}

Powered by [Axon Framework](https://github.com/param/axon).

## Setup

1. Install dependencies:
   ```bash
   pip install axon-framework
   ```

2. Set API Key:
   ```bash
   cp .env.example .env
   # Edit .env with your OpenAI key
   ```

3. Run:
   ```bash
   python app.py
   # or
   axon run app.py
   ```
""")

    console.print(Panel(f"""
[bold]Success! 🚀[/bold]

Your project is ready at [cyan]./{project_name}[/cyan]

To get started:
  cd {project_name}
  python app.py
""", title="Axon CLI", border_style="green"))


@cli.command()
@click.argument("script", default="app.py")
def run(script):
    """Run an Axon agent script."""
    if not os.path.exists(script):
        console.print(f"[bold red]Error:[/bold red] File '{script}' not found.")
        return
        
    console.print(f"[bold blue]Running {script}...[/bold blue]")
    os.system(f"python3 {script}")

if __name__ == "__main__":
    cli()
