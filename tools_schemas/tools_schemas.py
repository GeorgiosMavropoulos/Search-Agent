### tool class containing all tools and schemas
import inspect #import this module to automatically create tool definitions
from typing import Literal, get_args, get_origin
class CalculatorTool:
    def __init__(self):
        pass
    @staticmethod
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
        return CalculatorTool.format_tool_definition(
            func.__name__,
            func.__doc__ or "",
            CalculatorTool.function_to_input_schema(func)
        )

   

    
    #create the calculator function
    def calculator(operator: Literal["add", "subtract", "multiply", "divide"],
                first_number: float, second_number: float):
        ##define the operations
        if operator == "add": #addition
            return first_number + second_number
        elif operator == "subtract": #subsctraction
            return first_number - second_number
        elif operator == "multiply": #multiplication 
            return first_number * second_number
        elif operator == 'divide': # division
            ##return an error if user tries to divide by zero
            if second_number == 0:
                raise ValueError("Cannot divide by 0")
            return first_number/ second_number
        else: #return an error an invalid operator was provided
            raise ValueError(f"Unsupported operator: {operator}")


     ##generate the schema for calculator's function
CalculatorTool.calculator_definition = CalculatorTool.function_to_tool_definition(
    CalculatorTool.calculator
)


