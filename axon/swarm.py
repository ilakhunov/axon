from typing import List, Dict, Any, Optional
from .core import Agent
from .types import Handoff
from .utils import get_logger
from .context import Context

logger = get_logger()

class Swarm:
    def __init__(self, agents: List[Agent]):
        self.agents: Dict[str, Agent] = {a.name: a for a in agents}
        self.history: List[Dict[str, Any]] = []
        
        # Share context across all agents
        self.context = Context()
        for agent in self.agents.values():
            agent.context = self.context
        
    def run(self, starting_agent: Agent, prompt: str) -> str:
        """
        Run the swarm starting with a specific agent.
        """
        current_agent = starting_agent
        current_prompt = prompt
        
        logger.info(f"🐝 Swarm started with [bold cyan]{current_agent.name}[/]")
        
        while True:
            # Add message to global history
            self.history.append({"role": "user", "agent": current_agent.name, "content": current_prompt})
            
            # Ask the current agent
            try:
                response = current_agent.ask(current_prompt)
            except Exception as e:
                logger.error(f"🔥 Error in agent {current_agent.name}: {e}")
                return f"Error executing {current_agent.name}: {e}"
            
            # Check for Handoff
            if isinstance(response, Handoff):
                target_name = response.target_agent
                
                if target_name not in self.agents:
                    return f"❌ Error: Agent '{target_name}' not found in swarm."
                
                logger.info(f"🔄 Handing off from [bold cyan]{current_agent.name}[/] to [bold cyan]{target_name}[/]")
                logger.info(f"   Reason: {response.context}")
                
                # Switch agent
                current_agent = self.agents[target_name]
                
                # Prepare prompt for the next agent with context
                # We prepend context to help the next agent understand why they were called
                if response.context:
                    current_prompt = f"[Transferred from {starting_agent.name}]: {response.context}\n\nTask: {prompt}"
                else:
                    current_prompt = prompt # Or should we pass the last output?
                    
                # Simplification: For now, we pass the original prompt + context. 
                # In v0.7 we should pass full history.
                
                continue
            
            # If standard response, we are done (for this turn)
            # In a full chat loop, we might output and wait for user, 
            # but for a Swarm.run() single turn, this is the result.
            self.history.append({"role": "assistant", "agent": current_agent.name, "content": str(response)})
            return str(response)
