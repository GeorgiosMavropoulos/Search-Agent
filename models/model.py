### Define models to enable structured output both for llms and user's input
from pydantic import BaseModel,Field
from typing import Literal, Union, Callable,List, Dict,Any,TYPE_CHECKING
import uuid
from datetime import datetime
from abc import ABC,abstractmethod

import inspect
from tool_definitions.tool_definitions import ToolDefinitions
from litellm import acompletion
if TYPE_CHECKING:
    from execution_context.execution_context import ExecutionContext
## create extracted info class for testing
class ExtractedInfo(BaseModel):
     name: str
     email: str
     phone: str | None = None


#create a model to experiment with GAIA
class GaiaOutput(BaseModel):
     is_solvable: bool
     unsolvable_reason: str = ""
     final_answer: str = ""



class QuestionRequest(BaseModel):
    question: str


##Type field in each of the following classes works as a discriminator in order to be able to identify with what kind of content we are working with
## Create a default Base class Message
class Message(BaseModel):
    """A text message in the conversation."""
    type: Literal["message"] = "message"
    role: Literal["system", "user", "assistant"]
    content: str


class BaseTool(ABC):
    """Abstract base class for all tools."""

    def __init__(
        self, 
        name: str = None, 
        description: str = None, 
        tool_definition: Dict[str, Any] = None,
    ):
        self.name = name or self.__class__.__name__
        self.description = description or self.__doc__ or ""
        self._tool_definition = tool_definition

    @property
    def tool_definition(self) -> Dict[str, Any] | None:
        return self._tool_definition

    @abstractmethod
    async def execute(self, context: 'ExecutionContext', **kwargs) -> Any:
        pass

    async def __call__(self, context:'ExecutionContext', **kwargs) -> Any:
        return await self.execute(context, **kwargs)


#The following classes help for debugging and create an execution context for the agent
##Base Class for tool calling
class ToolCall(BaseModel):
    """LLM's request to execute a tool."""
    type: Literal["tool_call"] = "tool_call"
    tool_call_id: str
    name: str
    arguments: dict

##create a base model to store tool results
class ToolResult(BaseModel):
    """Result from tool execution."""
    type: Literal["tool_result"] = "tool_result"
    tool_call_id: str
    name: str
    status: Literal["success", "error"]
    content: list


#Unify ToolResult, ToolCall and Message classes
ContentItem = Union[Message, ToolCall, ToolResult]

##The event class works as an event capturer in order to be able to identify who produced each piece of content and when
class Event(BaseModel):
    """A recorded occurrence during agent execution."""
    id: str = Field(default_factory=lambda: str(uuid.uuid4())) ##create a unique id for each execution
    execution_id: str #group all events from a single agent run to be able to trace an entire problem solving session
    timestamp: float = Field(default_factory=lambda: datetime.now().timestamp()) 
    author: str  # "user" or agent name
    content: List[ContentItem] = Field(default_factory=list)##store which method was called



#Base tool function
class FunctionTool(BaseTool):
    """Wraps a Python function as a BaseTool."""

    def __init__(
        self, 
        func: Callable, 
        name: str = None, 
        description: str = None,
        tool_definition: Dict[str, Any] = None
    ):
        self.func = func
        self.needs_context = 'context' in inspect.signature(func).parameters

        name = name or func.__name__
        description = description or (func.__doc__ or "").strip()
        tool_definition = tool_definition or self._generate_definition()

        super().__init__(
            name=name, 
            description=description, 
            tool_definition=tool_definition
        )

    async def execute(self, context: 'ExecutionContext', **kwargs) -> Any:
        """Execute the wrapped function."""
        if self.needs_context:
            result = self.func(context=context, **kwargs)
        else:
            result = self.func(**kwargs)

        # Handle both sync and async functions
        if inspect.iscoroutine(result):
            return await result
        return result

    def _generate_definition(self) -> Dict[str, Any]:
        """Generate tool definition from function signature."""
        parameters = ToolDefinitions.function_to_input_schema(self.func)
        return ToolDefinitions.format_tool_definition(self.name, self.description, parameters)



