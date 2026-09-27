### this file contains the class with the method which allow the user 

class WriteToTxt:
    def __init__(self):
        pass

    #write to file method
    @staticmethod
    def write_to_file(txt:str,filename):
        """Save text content to a .txt file.

         Args:
        txt: The text to write to the file.
        filename: The name of the text file, e.g. 'notes.txt'.
        """
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

