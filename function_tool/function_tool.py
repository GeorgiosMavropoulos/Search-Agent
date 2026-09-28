## This class contains the Base tool function and the function tool function which describes important schemas for the agent
from abc import ABC, abstractmethod
from execution_context.execution_context import ExecutionContext
from typing import Dict, Any,Callable
import inspect
from tool_definitions.tool_definitions import ToolDefinitions
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
     ##the agent passes the execution context to every tool
     @abstractmethod
     async def execute(self, context: ExecutionContext, **kwargs) -> Any:
        pass

     async def __call__(self, context: ExecutionContext, **kwargs) -> Any:
        return await self.execute(context, **kwargs)


#implement the function tool class
#FunctionTool acts as an adapter that wraps existing functions with the BaseTool interface
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

    #this method executes the wrapped function
    async def execute(self, context: ExecutionContext, **kwargs) -> Any:
        """Execute the wrapped function."""
        if self.needs_context:
            result = self.func(context=context, **kwargs)
        else:
            result = self.func(**kwargs)

        # Handle both sync and async functions
        if inspect.iscoroutine(result):
            return await result
        return result

    ##method to generate definitions through the tool_definition methods created in ToolDefinitions class
    def _generate_definition(self) -> Dict[str, Any]:
        """Generate tool definition from function signature."""
        parameters = ToolDefinitions.function_to_input_schema(self.func)
        return ToolDefinitions.format_tool_definition(self.name, self.description, parameters)
   