### tool class containing all tools and schemas

from typing import Literal, get_args, get_origin


class CalculatorTool:
    def __init__(self):
        pass


     
    #create the calculator function
    def calculator(operator: Literal["add", "subtract", "multiply", "divide"],    
                first_number: float, second_number: float):
        """Perform a basic arithmetic operation on two numbers.
        Args:

        operator: The arithmetic operation to perform.
            Must be one of: "add", "subtract", "multiply", or "divide".
        first_number: The first number used in the operation.
        second_number: The second number used in the operation.

        Returns:
        The result of the arithmetic operation.

         Raises:
        ValueError: If the operator is unsupported or if division by zero
                    is attempted.

        
        
         """
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








