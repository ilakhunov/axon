import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, Optional

from .core import Agent

# Request Models
class ChatRequest(BaseModel):
    message: str
    stream: bool = False

def create_app(agent: Agent) -> FastAPI:
    """Create a FastAPI app for the agent."""
    app = FastAPI(
        title=f"Axon Agent: {agent.name}",
        version="0.1.0",
        description=f"API for agent {agent.name}"
    )

    @app.get("/")
    async def root():
        return {"status": "ok", "agent": agent.name, "model": agent.model}

    @app.post("/chat")
    async def chat(request: ChatRequest):
        """Standard chat endpoint."""
        try:
            # TODO: Add streaming support later
            if request.stream:
                raise HTTPException(status_code=400, detail="Streaming not yet supported via API")
                
            response = agent.ask(request.message)
            return {"response": response}
            
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    return app

def serve(agent: Agent, host: str = "0.0.0.0", port: int = 8000):
    """Serve the agent as a REST API."""
    app = create_app(agent)
    print(f"🚀 Serving agent '{agent.name}' on http://{host}:{port}")
    uvicorn.run(app, host=host, port=port)
