from typing import Any, Callable, Optional, Union, Dict, List
from pydantic import BaseModel, Field, ConfigDict

class Tool(BaseModel):
    name: str
    description: str
    func: Callable
    schema_: Dict[str, Any] = Field(alias="schema")

    model_config = ConfigDict(arbitrary_types_allowed=True)

class AgentConfig(BaseModel):
    name: str
    model: str = "gpt-4o"
    system_prompt: str = "You are a helpful AI assistant."
    temperature: float = 0.7
