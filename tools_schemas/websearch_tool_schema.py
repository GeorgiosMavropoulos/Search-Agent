###import the tavily modules
from tavily import TavilyClient#import tavily to implemenet web search
from .generate_tool_definitions import ToolDefinitions
from dotenv import load_dotenv
import os
##define the WebSearchClass
class WebSearch:
    def __init__(self):
     pass


    #web search method implementation. This method retrieves data from the web and return the results
    @staticmethod
    def web_search(query:str,max_results: int = 5, topic: str = "general",time_range: str | None = None)-> list | str:
       """Search the web for current or specific information.
        Use for recent events, news, or facts that may have changed.
        """
       try:
            tavily_client = TavilyClient(os.getenv("TAVILY_API_KEY")) #initialize tavily client to access the API for web search
            result = tavily_client.search( query,
            max_results=max_results,
            topic=topic,
            time_range=time_range,)
            
            ##get the retrieved results
            final_results = result.get("results")
            #print the returned results
            print(final_results)
            #return the final results
            return final_results
        #return an error message if query fails
       except Exception as e:
            return f"Error: Search failed - {e}"


#generate tool's definition
WebSearch.web_search_definition = ToolDefinitions.function_to_tool_definition(WebSearch.web_search)


