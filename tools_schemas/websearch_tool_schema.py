###import the tavily modules
from tavily import TavilyClient#import tavily to implemenet web search

from dotenv import load_dotenv
import os
from mcp.server import MCPServer
##define the WebSearchClass
class WebSearch:
    def __init__(self):
     pass



    mcp = MCPServer("custom-tavily-search") #initialize fastmcp instance


    #web search method implementation. This method retrieves data from the web and return the results
    @mcp.tool()
    def web_search(query:str,max_results: int = 5, topic: str = "general",time_range: str | None = None)-> list | str:
       """Search the web using Tavily API.
          Args:
          query: Search query string
          max_results: Maximum number of results to return (default: 5)

          Returns:
          Search results as formatted string
        """
       try:
            tavily_client = TavilyClient(os.getenv("TAVILY_API_KEY")) #initialize tavily client to access the API for web search
            result = tavily_client.search( query,
            max_results=max_results,
            topic=topic,
            time_range=time_range,)
            
            ##get the retrieved results
            final_results = result.get("results")
            
            #return the final results
            return final_results
        #return an error message if query fails
       except Exception as e:
            return f"Error: Search failed - {e}"


#generate tool's definition
if __name__ == "__main__":
    WebSearch.mcp.run(transport='stdio')


