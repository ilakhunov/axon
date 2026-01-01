import inspect
import json
from typing import Callable, Dict, Any, List, Optional, Type
from pydantic import TypeAdapter
from openai import OpenAI
from openai.types.chat import ChatCompletionMessageParam, ChatCompletionToolParam
from dotenv import load_dotenv

from .types import AgentConfig, Tool
from .utils import get_logger

load_dotenv() # Load environment variables from .env file

logger = get_logger()

class Agent:
    def __init__(self, name: str, system: str = "You are a helpful assistant.", model: str = "gpt-4o"):
        self.config = AgentConfig(name=name, system_prompt=system, model=model)
        self.tools: Dict[str, Tool] = {}
        # We assume OPENAI_API_KEY is set in environment, or user passes client. 
        # For simplicity in MVP, we instantiate default client.
        self.history: List[ChatCompletionMessageParam] = [
            {"role": "system", "content": system}
        ]
        
        # Lazy load client to allow Agent instantiation without keys (for tool testing etc)
        try:
            self.client = OpenAI()
        except Exception:
            self.client = None # type: ignore

    def tool(self, func: Callable) -> Callable:
        """
        Decorator to register a function as a tool.
        """
        name = func.__name__
        description = (func.__doc__ or "").strip()
        
        # simple schema generation - this is a simplified version
        # In a real framework we'd iterate over params and use TypeAdapter
        sig = inspect.signature(func)
        params = {}
        required = []
        
        for param_name, param in sig.parameters.items():
            if param_name == 'self': continue
            
            # Map python types to JSON types is complex, 
            # for MVP we will use a simplified approach or pydantic if possible.
            # Here we just treat everything as string if not annotated, 
            # but we should respect annotations.
            
            param_type = param.annotation
            if param_type == inspect.Parameter.empty:
                param_type = str
            
            # Use Pydantic to get JSON schema for the type
            try:
                type_schema = TypeAdapter(param_type).json_schema()
            except Exception:
                type_schema = {"type": "string"}

            params[param_name] = type_schema
            if param.default == inspect.Parameter.empty:
                required.append(param_name)

        tool_schema = {
            "type": "function",
            "function": {
                "name": name,
                "description": description,
                "parameters": {
                    "type": "object",
                    "properties": params,
                    "required": required
                }
            }
        }

        self.tools[name] = Tool(
            name=name,
            description=description,
            func=func,
            schema=tool_schema
        )
        logger.info(f"Registered tool: [bold cyan]{name}[/]")
        return func

    def ask(self, prompt: str) -> str:
        """
        Send a message to the agent and get a response.
        Handles tool calls automatically.
        """
        logger.info(f"User asking: [bold green]{prompt}[/]")
        self.history.append({"role": "user", "content": prompt})

        # Prepare tools
        oai_tools: List[ChatCompletionToolParam] = [t.schema_ for t in self.tools.values()] # type: ignore
        if not oai_tools:
            oai_tools = None # type: ignore

        if not self.client:
             try:
                 self.client = OpenAI()
             except Exception:
                 return "❌ Error: Missing OPENAI_API_KEY. Please set it in your environment."

        while True:
            response = self.client.chat.completions.create(
                model=self.config.model,
                messages=self.history,
                tools=oai_tools,
            )
            
            msg = response.choices[0].message
            # self.history.append(msg) # OpenAI object... needs to be dict or handled. 
            # Let's convert to dict to be safe
            msg_dict = msg.model_dump(exclude_none=True)
            self.history.append(msg_dict) # type: ignore

            if msg.tool_calls:
                logger.info(f"Agent decided to call {len(msg.tool_calls)} tools")
                for tool_call in msg.tool_calls:
                    fn_name = tool_call.function.name
                    fn_args = json.loads(tool_call.function.arguments)
                    
                    if fn_name in self.tools:
                        logger.info(f"Calling [bold cyan]{fn_name}[/] with {fn_args}")
                        tool_result = self.tools[fn_name].func(**fn_args)
                        logger.info(f"Result: {tool_result}")
                        
                        self.history.append({
                            "role": "tool",
                            "tool_call_id": tool_call.id,
                            "content": str(tool_result)
                        })
                    else:
                        logger.error(f"Tool {fn_name} not found!")
                        self.history.append({
                            "role": "tool",
                            "tool_call_id": tool_call.id,
                            "content": f"Error: Tool {fn_name} not found"
                        })
            else:
                # Final answer
                content = msg.content or ""
                logger.info(f"Agent Answer: [bold blue]{content}[/]")
                return content
