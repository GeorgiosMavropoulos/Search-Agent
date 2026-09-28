### Define models to enable structured output both for llms and user's input
from pydantic import BaseModel,Field
from typing import Literal, Union, List
import uuid
from datetime import datetime
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

