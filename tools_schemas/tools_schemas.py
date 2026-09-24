### tool class containing all tools and schemas

class CalculatorTool:
    def __init__(self):
        pass



    ##Calculator schema
    calculator_definition = {
        #define tools' type
        "type":"function",
        "function":{
            "name":"calculator", #tool's name
            "description":"Perform basic arithmetic operations", #tool's description
            "parameters":{ ##define what parameters this function accepts
             "type":"object",
             "properties":{
                 #argument 1
                 "operator":{
                     #value's type
                     "type":"string",
                     "description":"Arithmetic operation to perform",
                     #force the model to use only the following arguments as values for operator
                     "enum": ["add", "subtract", "multiply", "divide"] 

                 },
                 #argument 2, the first number of the mathematical operation
                 "first_number": {
                    "type": "number",
                    "description": "First number for the calculation"
                },
                #argument 3, the second number of the mathematican operation
                 "second_number": {
                    "type": "number",
                    "description": "Second number for the calculation"
                }
             },
             ##force the model to use those arguments always
             "required": ["operator", "first_number", "second_number"],
            }

        }
    }

    #create the calculator function
    def calculator(operator:str,first_number:float,second_number:float):
        ##define the operations
        if operator == "add": #addition
            return first_number + second_number
        elif operator == "subsctract": #subsctraction
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
