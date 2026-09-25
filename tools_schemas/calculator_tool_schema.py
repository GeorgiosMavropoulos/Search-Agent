### tool class containing all tools and schemas
import inspect #import this module to automatically create tool definitions
from typing import Literal, get_args, get_origin
from .generate_tool_definitions import ToolDefinitions
class CalculatorTool:
    def __init__(self):
        pass


     
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
CalculatorTool.calculator_definition = ToolDefinitions.function_to_tool_definition(
    CalculatorTool.calculator
)


##create the web search tool
class WebSearchTool:
    def __init__(self):
        pass


    #method to implement basic websearch and return the results

