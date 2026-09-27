### this file contains the class with the method which allow the user 
from .generate_tool_definitions import ToolDefinitions

class WriteToTxt:
    def __init__(self):
        pass


    #write to file method
    @staticmethod
    def write_to_file(txt:str,filename):
        ## open the file
        try:

            with open(filename, "w",encoding="utf-8") as f:
                f.write(txt) ##write the text
                 #response
                result = f"File {filename} was created with success"
                return result
        except Exception as e:
           return f"Error while trying to write into the txt file: {e}"
        finally:
          f.close() ##close the write mode whatever happens


##create tool's definition
WriteToTxt.write_to_text_definitions = ToolDefinitions.function_to_tool_definition(WriteToTxt.write_to_file)
                