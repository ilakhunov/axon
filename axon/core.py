import inspect
import json
from typing import Any, Dict, List, Optional, Callable, Type, Coroutine, Union
from pydantic import BaseModel, TypeAdapter
from openai import OpenAI, AsyncOpenAI
from openai.types.chat import ChatCompletionMessageParam, ChatCompletionToolParam
from dotenv import load_dotenv
import tiktoken
from contextlib import contextmanager

from .types import AgentConfig, Tool, Handoff
from .utils import get_logger
from .context import Context
from .tracing import Tracer, Event
from .knowledge import KnowledgeBase
from .memory import MemoryBackend, SqliteMemory

load_dotenv() # Load environment variables from .env file

logger = get_logger()

def tool(func):
    """Decorator to mark a function as a tool."""
    return func

class Agent:
    def __init__(
        self, 
        name: str, 
        system: str = "You are a helpful assistant.", 
        model: str = "gpt-4o",
        max_history_tokens: int = 4000,
        memory: Optional[Union[str, MemoryBackend]] = None,
        client: Optional[OpenAI] = None,
        tracer: Optional[Tracer] = None,
        knowledge: Optional[str] = None  # RAG: Path to file or text
    ):
        """
        Initialize the Agent.
        
        Args:
            name: Name of the agent.
            system: System prompt.
            model: LLM model name (e.g. gpt-4o, gpt-3.5-turbo).
            max_history_tokens: Limit for memory context.
            memory: Path to SQLite database for persistent memory.
            client: Optional OpenAI client instance. Pass this for generic providers (Ollama, etc).
        """
        self.config = AgentConfig(name=name, system_prompt=system, model=model)
        self.tools: Dict[str, Tool] = {}
        self.max_history_tokens = max_history_tokens
        self.context = Context()
        
        # 1. Initialize Memory
        if memory:
            if isinstance(memory, str):
                self.memory = SqliteMemory(memory)
                logger.info(f"Memory enabled (SQLite): {memory}")
            else:
                self.memory = memory
                logger.info(f"Memory enabled (Custom Backend): {type(memory).__name__}")
        else:
            self.memory = None
        
        # 2. Initialize Tokenizer (Safe fallback)
        try:
            self.tokenizer = tiktoken.encoding_for_model(model)
        except KeyError:
            self.tokenizer = tiktoken.get_encoding("cl100k_base")
        
        # 3. Initialize History
        self.history: List[ChatCompletionMessageParam] = [
            {"role": "system", "content": system}
        ]
        
        # 4. Initialize Client (Dependency Injection)
        if client:
            self.client = client
        else:
            try:
                self.client = OpenAI()
            except Exception:
                self.client = None
        
        # 5. Initialize Tracer
        self.tracer = tracer
        
        # 6. Initialize Knowledge Base (RAG)
        self.knowledge = None
        if knowledge:
            self.knowledge = KnowledgeBase()
            # If it looks like a file path, load it
            if knowledge.endswith(('.txt', '.md', '.py', '.json')):
                try:
                    self.knowledge.load_from_file(knowledge)
                    logger.info(f"Loaded knowledge from file: {knowledge}")
                except Exception as e:
                    logger.error(f"Failed to load knowledge file: {e}")
            else:
                # Treat as raw text
                self.knowledge.load_from_text(knowledge)
                logger.info("Loaded knowledge from raw text string")

    @property
    def name(self) -> str:
        return self.config.name
        
    @property
    def model(self) -> str:
        return self.config.model
    
    def _count_tokens(self, messages: List[ChatCompletionMessageParam]) -> int:
        """Count tokens in message history."""
        count = 0
        for msg in messages:
            # Count tokens in content
            if isinstance(msg.get("content"), str):
                count += len(self.tokenizer.encode(msg["content"]))
            # Add overhead for message formatting (role, etc)
            count += 4  # Approximate overhead per message
        return count
    
    def _truncate_history(self):
        """Truncate old messages to stay within token limit."""
        if len(self.history) <= 1:
            return  # Keep at least system message
        
        current_tokens = self._count_tokens(self.history)
        
        if current_tokens <= self.max_history_tokens:
            return
        
        logger.info(f"History has {current_tokens} tokens, truncating to {self.max_history_tokens}...")
        
        # Keep system message (first) and remove oldest user/assistant messages
        system_msg = self.history[0]
        other_msgs = self.history[1:]
        
        # Remove from the beginning until we're under the limit
        while other_msgs and self._count_tokens([system_msg] + other_msgs) > self.max_history_tokens:
            removed = other_msgs.pop(0)
            logger.info(f"Removed message: {removed.get('role', 'unknown')[:20]}...")
        
        self.history = [system_msg] + other_msgs
        new_tokens = self._count_tokens(self.history)
        logger.info(f"✅ Truncated to {new_tokens} tokens ({len(self.history)} messages)")

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
            if param_name == 'self':
                continue
            
            # Skip 'ctx' parameter - it will be injected automatically
            if param_name == 'ctx' and param.annotation == Context:
                continue
            
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
    
    # Alias for explicit registration style
    register_tool = tool

    def ask(self, prompt: str, response_model: Optional[Type] = None) -> Any:
        """
        Send a message to the agent and get a response.
        Handles tool calls automatically.
        
        Args:
            prompt: The user's question or instruction
            response_model: Optional Pydantic model for structured output
            
        Returns:
            If response_model is provided, returns validated Pydantic instance.
            Otherwise, returns string.
        """
        logger.info(f"User asking: [bold green]{prompt}[/]")
        
        # Load relevant memories if available (first time only)
        if self.memory:
            # Check if this is the first user message in this session
            user_msg_count = sum(1 for msg in self.history if msg.get("role") == "user")
            if user_msg_count == 0:
                # Get recent conversation history to restore context
                recent_messages = self.memory.get_recent(k=10)
                if recent_messages:
                    logger.info(f"Loaded {len(recent_messages)} messages from memory")
                    # Add recent messages to history (excluding system)
                    for msg in recent_messages:
                        if msg['role'] != 'system':
                            self.history.append({
                                "role": msg['role'],
                                "content": msg['content']
                            })
        
        self.history.append({"role": "user", "content": prompt})
        
        # Save user message to memory
        if self.memory:
            self.memory.add("user", prompt)
        
        # Truncate history to stay within limits
        self._truncate_history()
        
        # RAG: Inject Relevant Context
        if self.knowledge:
            context = self.knowledge.query(prompt)
            if context:
                logger.info(f"Retrieved Context: {context[:200]}...")
                self.history.append({
                    "role": "system", 
                    "content": f"Relevant Context from Knowledge Base:\n{context}"
                })

        # Prepare tools
        oai_tools: List[ChatCompletionToolParam] = [t.schema_ for t in self.tools.values()] # type: ignore
        if not oai_tools:
            oai_tools = None # type: ignore

        if not self.client:
             try:
                 self.client = OpenAI()
             except Exception:
                 return "❌ Error: Missing OPENAI_API_KEY. Please set it in your environment."

        # Trace Start
        if self.tracer:
            self.tracer.log(Event("completion_start", self.name, {"prompt": prompt}))

        # If structured output is requested, use response_format
        extra_params = {}
        if response_model:
            # Use OpenAI's structured output feature (function calling hack)
            # We create a "fake" tool that represents the response schema
            response_schema = {
                "type": "function",
                "function": {
                    "name": "return_structured_response",
                    "description": "Return the response in the specified format",
                    "parameters": TypeAdapter(response_model).json_schema()
                }
            }
            # Force the model to use this tool
            if oai_tools:
                oai_tools.append(response_schema) # type: ignore
            else:
                oai_tools = [response_schema] # type: ignore

        while True:
            response = self.client.chat.completions.create(
                model=self.config.model,
                messages=self.history,
                tools=oai_tools,
                **extra_params
            )
            
            msg = response.choices[0].message
            
            # Check if this is a structured response FIRST (before adding to history)
            if response_model and msg.tool_calls:
                for tool_call in msg.tool_calls:
                    if tool_call.function.name == "return_structured_response":
                        logger.info(f"Parsing structured response: {response_model.__name__}")
                        fn_args = json.loads(tool_call.function.arguments)
                        try:
                            validated = response_model(**fn_args)
                            logger.info(f"✅ Validated response: {validated}")
                            return validated
                        except Exception as e:
                            logger.error(f"Failed to validate response: {e}")
                            return f"Error: Failed to parse structured response: {e}"
            
            # Add message to history
            msg_dict = msg.model_dump(exclude_none=True)
            self.history.append(msg_dict) # type: ignore

            if msg.tool_calls:
                logger.info(f"Agent decided to call {len(msg.tool_calls)} tools")
                handoff_signal = None

                for tool_call in msg.tool_calls:
                    fn_name = tool_call.function.name
                    fn_args = json.loads(tool_call.function.arguments)
                    
                    if fn_name in self.tools:
                        logger.info(f"Calling [bold cyan]{fn_name}[/] with {fn_args}")
                        
                        # Trace Tool Call
                        if self.tracer:
                            self.tracer.log(Event("tool_call", self.name, {"tool": fn_name, "args": fn_args}))

                        # Check if tool needs context injection
                        tool_func = self.tools[fn_name].func
                        sig = inspect.signature(tool_func)
                        
                        # Inject context if function has 'ctx' parameter
                        if 'ctx' in sig.parameters:
                            fn_args['ctx'] = self.context
                        
                        tool_result = tool_func(**fn_args)
                        logger.info(f"Result: {tool_result}")
                        
                        # Trace Tool Result
                        if self.tracer:
                            self.tracer.log(Event("tool_result", self.name, {"tool": fn_name, "result": str(tool_result)}))
                        
                        # Check for Handoff
                        if isinstance(tool_result, Handoff):
                            logger.info(f"🤝 Handoff signal detected -> {tool_result.target_agent}")
                            handoff_signal = tool_result
                            
                            # Trace Handoff
                            if self.tracer:
                                self.tracer.log(Event("handoff", self.name, {"target": tool_result.target_agent, "context": tool_result.context}))

                            # CRITICAL: We must still record the tool output in history
                            self.history.append({
                                "role": "tool",
                                "tool_call_id": tool_call.id,
                                "content": f"Transferred to {tool_result.target_agent}: {tool_result.context}"
                            })
                        else:
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
                
                # Use signal if found
                if handoff_signal:
                    return handoff_signal
            else:
                # Final answer
                content = msg.content or ""
                logger.info(f"Agent Answer: [bold blue]{content}[/]")
                
                # Trace Answer
                if self.tracer:
                    self.tracer.log(Event("agent_response", self.name, {"content": content}))

                # Save assistant response to memory
                if self.memory:
                    self.memory.add("assistant", content)
                
                # CRITICAL FIX: If response_model was requested but LLM didn't use tool
                if response_model:
                    logger.warning(f"LLM returned text instead of structured output. Attempting JSON parse...")
                    try:
                        # Try to parse content as JSON
                        import re
                        # Extract JSON from markdown code blocks if present
                        json_match = re.search(r'```(?:json)?\s*(\{.*?\})\s*```', content, re.DOTALL)
                        if json_match:
                            json_str = json_match.group(1)
                        else:
                            # Try to find raw JSON object
                            json_match = re.search(r'\{.*\}', content, re.DOTALL)
                            json_str = json_match.group(0) if json_match else content
                        
                        data = json.loads(json_str)
                        validated = response_model(**data)
                        logger.info(f"✅ Fallback parsing successful: {validated}")
                        return validated
                    except Exception as e:
                        error_msg = (
                            f"AxonTypeError: Expected {response_model.__name__}, got str.\n"
                            f"Reason: LLM returned unstructured text instead of calling tool.\n"
                            f"LLM Response: {content[:200]}...\n"
                            f"Suggestion: Try rephrasing prompt or use manual parsing.\n"
                            f"Parse Error: {e}"
                        )
                        logger.error(error_msg)
                        raise TypeError(error_msg)
                
                return content
    
    def serve(self, host: str = "0.0.0.0", port: int = 8000):
        """
        Serve the agent as a REST API.
        This blocks the main thread.
        """
        from .serve import serve
        serve(self, host, port)

    def ask_stream(self, prompt: str):
        """
        Stream agent responses in real-time.
        Yields text chunks as they're generated.
        
        Args:
            prompt: The user's question or instruction
            
        Yields:
            str: Text chunks as they arrive from the LLM
        """
        logger.info(f"User asking (streaming): [bold green]{prompt}[/]")
        self.history.append({"role": "user", "content": prompt})
        
        # Truncate history to stay within limits
        self._truncate_history()
        
        # Prepare tools
        oai_tools: List[ChatCompletionToolParam] = [t.schema_ for t in self.tools.values()] # type: ignore
        if not oai_tools:
            oai_tools = None # type: ignore

        if not self.client:
             try:
                 self.client = OpenAI()
             except Exception:
                 yield "❌ Error: Missing OPENAI_API_KEY. Please set it in your environment."
                 return

        while True:
            # Create stream
            stream = self.client.chat.completions.create(
                model=self.config.model,
                messages=self.history,
                tools=oai_tools,
                stream=True  # Enable streaming!
            )
            
            # Collect chunks
            full_content = ""
            tool_calls_data = []
            
            for chunk in stream:
                delta = chunk.choices[0].delta
                
                # Stream text content
                if delta.content:
                    full_content += delta.content
                    yield delta.content
                
                # Collect tool calls (can't stream these)
                if delta.tool_calls:
                    # Buffer tool calls
                    for tc in delta.tool_calls:
                        # Ensure we have enough space in list
                        while len(tool_calls_data) <= (tc.index or 0):
                            tool_calls_data.append({"id": None, "name": "", "arguments": ""})
                        
                        if tc.id:
                            tool_calls_data[tc.index or 0]["id"] = tc.id
                        if tc.function and tc.function.name:
                            tool_calls_data[tc.index or 0]["name"] = tc.function.name
                        if tc.function and tc.function.arguments:
                            tool_calls_data[tc.index or 0]["arguments"] += tc.function.arguments
            
            # Build message for history
            msg_dict: Dict[str, Any] = {"role": "assistant"}
            if full_content:
                msg_dict["content"] = full_content
            if tool_calls_data and tool_calls_data[0]["id"]:
                msg_dict["tool_calls"] = [
                    {
                        "id": tc["id"],
                        "type": "function",
                        "function": {
                            "name": tc["name"],
                            "arguments": tc["arguments"]
                        }
                    }
                    for tc in tool_calls_data if tc["id"]
                ]
            
            self.history.append(msg_dict) # type: ignore
            
            # Handle tool calls
            if tool_calls_data and tool_calls_data[0]["id"]:
                logger.info(f"Agent decided to call {len(tool_calls_data)} tools")
                
                for tc in tool_calls_data:
                    if not tc["id"]:
                        continue
                    
                    fn_name = tc["name"]
                    fn_args = json.loads(tc["arguments"])
                    
                    if fn_name in self.tools:
                        logger.info(f"Calling [bold cyan]{fn_name}[/] with {fn_args}")
                        
                        # Check if tool needs context injection
                        tool_func = self.tools[fn_name].func
                        sig = inspect.signature(tool_func)
                        
                        # Inject context if function has 'ctx' parameter
                        if 'ctx' in sig.parameters:
                            fn_args['ctx'] = self.context
                        
                        tool_result = tool_func(**fn_args)
                        logger.info(f"Result: {tool_result}")
                        
                        self.history.append({
                            "role": "tool",
                            "tool_call_id": tc["id"],
                            "content": str(tool_result)
                        })
                    else:
                        logger.error(f"Tool {fn_name} not found!")
                        self.history.append({
                            "role": "tool",
                            "tool_call_id": tc["id"],
                            "content": f"Error: Tool {fn_name} not found"
                        })
                
                # Continue loop to get response after tool calls
                continue
            else:
                # No tool calls, we're done
                logger.info(f"Streaming complete: {len(full_content)} chars")
                break

class AsyncAgent(Agent):
    """
    Asynchronous version of Agent.
    """
    def __init__(
        self, 
        name: str, 
        system: str = "You are a helpful assistant.", 
        model: str = "gpt-4o",
        max_history_tokens: int = 4000,
        memory: Optional[Union[str, MemoryBackend]] = None,
        client: Optional[AsyncOpenAI] = None
    ):
        super().__init__(name, system, model, max_history_tokens, memory)
        
        # Override client with AsyncClient
        if client:
            self.client = client
        else:
            try:
                self.client = AsyncOpenAI()
            except Exception:
                self.client = None

    async def ask(self, prompt: str, response_model: Optional[Type] = None) -> Any:
        """
        Send a message to the agent asynchronously.
        """
        logger.info(f"User asking (async): [bold green]{prompt}[/]")
        
        # Load memory (sync for now, sqlite is fast enough, or todo: make memory async)
        if self.memory:
            user_msg_count = sum(1 for msg in self.history if msg.get("role") == "user")
            if user_msg_count == 0:
                recent_messages = self.memory.get_recent(k=10)
                if recent_messages:
                    for msg in recent_messages:
                        if msg['role'] != 'system':
                            self.history.append({"role": msg['role'], "content": msg['content']})
        
        self.history.append({"role": "user", "content": prompt})
        
        if self.memory:
            self.memory.add("user", prompt)
            
        self._truncate_history()
        
        print(f"DEBUG: Checking knowledge in ask. self.knowledge is {self.knowledge}")
        # RAG: Inject Relevant Context
        if self.knowledge:
            print("DEBUG: Querying knowledge base...")
            context = self.knowledge.query(prompt)
            if context:
                logger.info(f"Retrieved Context: {context[:200]}...")
                # Inject as system message temporarily for this turn
                # Or append to user prompt. Let's append to system prompt for better adherence
                self.history.append({
                    "role": "system", 
                    "content": f"Relevant Context from Knowledge Base:\n{context}"
                })
        
        oai_tools = [t.schema_ for t in self.tools.values()] # type: ignore
        if not oai_tools: oai_tools = None # type: ignore
        
        if not self.client:
             try:
                 self.client = AsyncOpenAI()
             except Exception:
                 return "❌ Error: Missing OPENAI_API_KEY."

        # Structured output logic (same as sync)
        extra_params = {}
        if response_model:
            response_schema = {
                "type": "function",
                "function": {
                    "name": "return_structured_response",
                    "description": "Return the response in the specified format",
                    "parameters": TypeAdapter(response_model).json_schema()
                }
            }
            if oai_tools: oai_tools.append(response_schema) # type: ignore
            else: oai_tools = [response_schema] # type: ignore

        while True:
            # Await the API call
            response = await self.client.chat.completions.create(
                model=self.config.model,
                messages=self.history,
                tools=oai_tools,
                **extra_params
            )
            
            msg = response.choices[0].message
            
            # Helper logic for structured (same logic, just copy-paste for now for robustness)
            if response_model and msg.tool_calls:
                 for tool_call in msg.tool_calls:
                    if tool_call.function.name == "return_structured_response":
                        fn_args = json.loads(tool_call.function.arguments)
                        try:
                            validated = response_model(**fn_args)
                            return validated
                        except Exception as e:
                            return f"Error: {e}"

            msg_dict = msg.model_dump(exclude_none=True)
            self.history.append(msg_dict) # type: ignore

            if msg.tool_calls:
                logger.info(f"Agent decided to call {len(msg.tool_calls)} tools")
                handoff_signal = None
                
                for tool_call in msg.tool_calls:
                    fn_name = tool_call.function.name
                    fn_args = json.loads(tool_call.function.arguments)
                    
                    if fn_name in self.tools:
                        logger.info(f"Calling [bold cyan]{fn_name}[/] with {fn_args}")
                        tool_func = self.tools[fn_name].func
                        
                        # Context injection
                        sig = inspect.signature(tool_func)
                        if 'ctx' in sig.parameters:
                            fn_args['ctx'] = self.context
                        
                        # EXECUTE ASYNC OR SYNC
                        if inspect.iscoroutinefunction(tool_func):
                            tool_result = await tool_func(**fn_args)
                        else:
                            tool_result = tool_func(**fn_args)
                            
                        logger.info(f"Result: {tool_result}")
                        
                        if isinstance(tool_result, Handoff):
                            handoff_signal = tool_result
                            self.history.append({
                                "role": "tool", 
                                "tool_call_id": tool_call.id, 
                                "content": f"Transferred to {tool_result.target_agent}: {tool_result.context}"
                            })
                        else:
                            self.history.append({
                                "role": "tool",
                                "tool_call_id": tool_call.id,
                                "content": str(tool_result)
                            })
                    else:
                        self.history.append({
                            "role": "tool",
                            "tool_call_id": tool_call.id,
                            "content": f"Error: Tool {fn_name} not found"
                        })
                
                if handoff_signal:
                    return handoff_signal
            else:
                content = msg.content or ""
                logger.info(f"Agent Answer: [bold blue]{content}[/]")
                if self.memory:
                    self.memory.add("assistant", content)
                
                # CRITICAL FIX: If response_model was requested but LLM didn't use tool
                if response_model:
                    logger.warning(f"LLM returned text instead of structured output. Attempting JSON parse...")
                    try:
                        import re
                        json_match = re.search(r'```(?:json)?\s*(\{.*?\})\s*```', content, re.DOTALL)
                        if json_match:
                            json_str = json_match.group(1)
                        else:
                            json_match = re.search(r'\{.*\}', content, re.DOTALL)
                            json_str = json_match.group(0) if json_match else content
                        
                        data = json.loads(json_str)
                        validated = response_model(**data)
                        logger.info(f"✅ Fallback parsing successful: {validated}")
                        return validated
                    except Exception as e:
                        error_msg = (
                            f"AxonTypeError: Expected {response_model.__name__}, got str.\n"
                            f"Reason: LLM returned unstructured text instead of calling tool.\n"
                            f"LLM Response: {content[:200]}...\n"
                            f"Suggestion: Try rephrasing prompt or use manual parsing.\n"
                            f"Parse Error: {e}"
                        )
                        logger.error(error_msg)
                        raise TypeError(error_msg)
                
                return content
