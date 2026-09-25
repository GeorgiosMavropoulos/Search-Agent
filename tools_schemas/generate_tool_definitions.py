###this class contains the methods to generate tool definitions for the LLM
from typing import Literal, get_args, get_origin
import inspect
class ToolDefinitions:
    def __init__(self):
        pass

    def function_to_input_schema(func) -> dict:
            type_map = {str: "string", int: "integer", float: "number", bool: "boolean"}
    
            signature = inspect.signature(func)
            parameters = {}
            for param in signature.parameters.values():
                if get_origin(param.annotation) is Literal:
                    # Literal["add","subtract",...] -> enum
                    parameters[param.name] = {
                        "type": "string",
                        "enum": list(get_args(param.annotation))
                    }
                else:
                    param_type = type_map.get(param.annotation, "string")
                    parameters[param.name] = {"type": param_type}
    
            required = [p.name for p in signature.parameters.values() if p.default == inspect._empty]
            return {"type": "object", "properties": parameters, "required": required}
    
        
        #generate tool auto definition function
    @staticmethod
    def format_tool_definition(name: str, description: str, parameters: dict) -> dict:
            return { ##return tool's type, function's name, description and the required parameters
                "type": "function",
                "function": {
                    "name": name,
                    "description": description,
                    "parameters": parameters,
                },
            }
    
        ##this method returns the tool definition
    @staticmethod
    def function_to_tool_definition(func) -> dict:
            return ToolDefinitions.format_tool_definition(
                func.__name__,
                func.__doc__ or "",
                ToolDefinitions.function_to_input_schema(func)
            )
    