#### this file contains the class with the method that enables the agent to write into the file
from .generate_tool_definitions import ToolDefinitions
from pathlib import Path
class WriteToFile:
    def __init__(self):
        pass

    #write to file method
    @staticmethod
    def generate_code_file(text,filename):
        """Use this method to write into a txt file"""
        try:
            with open(filename,"w",encoding="utf-8") as f:
                f.write(text) ##write the text
                #response
                result = "File {filename} was created with success"
                return result
        except Exception as e:
            return f"Error while trying to write into the txt file: {e}"
        finally:
            f.close() ##close the write mode whatever happens

##define a tool definition
WriteToFile.write_to_file_definition =   ToolDefinitions.function_to_tool_definition(WriteToFile.generate_code_file)
