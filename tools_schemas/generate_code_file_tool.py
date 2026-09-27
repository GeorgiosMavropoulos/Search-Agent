#### this file contains the class with the method that enables the agent to write into the file


class GenerateCodeFile:
    def __init__(self):
        pass

    #write to file method
    @staticmethod
    def generate_code_file(text,filename):
        """Generate and save code content to a file.
            Args:
            text: The source code to write into the file.
            filename: The name of the output file, including the appropriate
                  file extension, e.g. 'main.py', 'script.js', or 'index.html'.
        Returns:
        A message indicating whether the file was created successfully.
        
        """
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


