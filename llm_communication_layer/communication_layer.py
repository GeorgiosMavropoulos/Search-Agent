### this file is the communication layer between LLMs and tools
from pydantic import BaseModel,Field, ConfigDict
from typing import List,Dict,Optional,Any
from litellm import acompletion
from models.model import ContentItem, BaseTool, Message, ToolCall, ToolResult
import json
   
    ##create lllm request class
class LLMRequest(BaseModel):
    """Request object for LLM calls."""
    model_config = ConfigDict(arbitrary_types_allowed=True)
    instructions: List[str] = Field(default_factory=list) #hold system prompt fragments
    contents: List[ContentItem] = Field(default_factory=list) ##this stores the content history as content items
    tools: List[BaseTool] = Field(default_factory=list) ##list all tools as BaseTool instances
    tool_choice: Optional[str] = None #setting this to None allows the LLM to freely select tools

class LlmResponse(BaseModel):
        """Response object from LLM calls."""
        content: List[ContentItem] = Field(default_factory=list) #stores what llm produced as content item
        error_message: Optional[str] = None #this field captures failures
        usage_metadata: Dict[str, Any] = Field(default_factory=dict)  #this stores how many tokens where consumed. If we use an LLM API we can manage costs more efficiently


class LlmClient:
        """Client for LLM API calls using LiteLLM."""

        def __init__(self, model: str, **config):
            self.model = model #model identifier
            self.config = config #config may contain temperature or max_tokens

        #this method orchestrtes the the LLM call in 3 steps:
        # 1. It builds the messages list from the request.
        # 2. It extracts tool definitions with a simple list comprehension.
        # 3. Calls LiteLLM’s acompletion and parses the response. If anything fails, it returns an LlmResponse with the error captured rather than crashing.
        async def generate(self, request: LLMRequest) -> LlmResponse:
            """Generate a response from the LLM."""
            try:
                messages = self._build_messages(request) #transform LLM request into message content in a format the LLM understands
                tools = [t.tool_definition for t in request.tools] if request.tools else None
                #generate llm's response
                response = await acompletion(
                    model=self.model,
                    messages=messages,
                    tools=tools,
                    **({"tool_choice": request.tool_choice} 
                    if request.tool_choice else {}),
                    **self.config
                )

                return self._parse_response(response)
            except Exception as e:
                return LlmResponse(error_message=str(e))


        def _build_messages(self, request: LLMRequest) -> List[dict]:
            """Convert LlmRequest to API message format."""
            messages = []

            #append instruction into the messages

            for instruction in request.instructions:
                messages.append({"role": "system", "content": instruction})

            #if it's a message append it on item's content
            for item in request.contents:
                if isinstance(item, Message):
                    messages.append({"role": item.role, "content": item.content})
                #add tool calls in a dictionary
                elif isinstance(item, ToolCall):
                    tool_call_dict = {
                        "id": item.tool_call_id,
                        "type": "function",
                        "function": {
                            "name": item.name,
                            "arguments": json.dumps(item.arguments)
                        }
                    }
                    # Append to previous assistant message if exists
                    if messages and messages[-1]["role"] == "assistant":
                        messages[-1].setdefault("tool_calls", []).append(tool_call_dict)
                    else:
                        messages.append({
                            "role": "assistant",
                            "content": None,
                            "tool_calls": [tool_call_dict]
                        })

                elif isinstance(item, ToolResult):
                    messages.append({
                        "role": "tool",
                        "tool_call_id": item.tool_call_id,
                        "content": str(item.content[0]) if item.content else ""
                    })

            return messages
        
        #this method converts the LLMs response into an API's compatible format
        def _parse_response(self, response) -> LlmResponse:
            """Convert API response to LlmResponse."""
            choice = response.choices[0]
            content_items = []

            if choice.message.content: #if it's a message we wrap it into Message base model
                content_items.append(Message(
                    role="assistant",
                    content=choice.message.content
                ))

            if choice.message.tool_calls: #if it's a tool call we wrap into ToolCall base model
                for tc in choice.message.tool_calls:
                    content_items.append(ToolCall(
                        tool_call_id=tc.id,
                        name=tc.function.name,
                        arguments=json.loads(tc.function.arguments)
                    ))

            #return the response
            return LlmResponse(
                content=content_items,
                usage_metadata={
                    "input_tokens": response.usage.prompt_tokens,
                    "output_tokens": response.usage.completion_tokens,
                }
            )