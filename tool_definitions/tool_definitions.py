### this file contains the tool definition functions which extract tool's schema definitions
import inspect
class ToolDefinitions:
    def __init__(self):
        pass

    ##this function defines input schema and tool's signature
    def function_to_input_schema(func) -> dict:
        type_map = {
            str: "string",
            int: "integer",
            float: "number",
            bool: "boolean",
            list: "array",
            dict: "object",
            type(None): "null",
        }

        try:
            signature = inspect.signature(func)  #1
        except ValueError as e:
            raise ValueError(
                f"Failed to get signature for function {func.__name__}: {str(e)}"
                
            )

        parameters = {}
        for param in signature.parameters.values():
            try:
                param_type = type_map.get(param.annotation, "string") #2
            except KeyError as e:
                raise KeyError(
                    f"Unknown type annotation {param.annotation} for parameter {param.name}: {str(e)}"
                    
                )
            parameters[param.name] = {"type": param_type} #2

        required = [
            param.name  #3
            for param in signature.parameters.values()  #3
            if param.default == inspect._empty  #3
        ]

        return {
                "type": "object",
                "properties": parameters,
                "required": required,
            }

     #this method formats tool's schema
    def format_tool_definition(name: str, description: str, parameters: dict) -> dict:
        return {
            "type": "function",
            "function": {
                "name": name,
                "description": description,
                "parameters": parameters,
            },
        }

    ##this method creates the final tool definition schema
    def function_to_tool_definition(func) -> dict:
        return ToolDefinitions.format_tool_definition(
            func.__name__,
            func.__doc__ or "",
            ToolDefinitions.function_to_input_schema(func)
        )