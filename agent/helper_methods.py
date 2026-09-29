### this file contains the following helper methods:
"""
The helper methods handle completion detection and result extraction. 
The _is_final_response() method checks whether an event represents a final answer by examining its contents. 
An event is final when it contains neither tool calls nor tool results, meaning that the LLM provided a direct answer.
 The _extract_final_result() method iterates through the event's content to find the assistant's message.
"""
from execution_context.execution_context import Event
from models.model import ToolResult,ToolCall,Message
class AgentHelperMethod:
    def __init__(self):
        pass

    ###this method validates whether the response sent by the llm is final or not
    def _is_final_response(self, event: Event) -> bool:
        """Check if this event contains a final response."""
        has_tool_calls = any(isinstance(c, ToolCall) for c in event.content)
        has_tool_results = any(isinstance(c, ToolResult) for c in event.content)
        return not has_tool_calls and not has_tool_results

    def _extract_final_result(self, event: Event) -> str: ###this method extracts the final result by iterating assistant's message
        for item in event.content:
            if isinstance(item, Message) and item.role == "assistant":
                return item.content
        return None