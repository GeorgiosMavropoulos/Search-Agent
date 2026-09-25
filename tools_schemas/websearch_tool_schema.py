###import the tavily modules
from tavily import TavilyClient#import tavily to implemenet web search
from .calculator_tool_schema import function_to_tool_definition
from dotenv import load_dotenv
import os
##define the WebSearchClass
class WebSearch:
    def __init__(self):
        pass

    #initialize tavily client
    tavily_client = TavilyClient(os.getenv("TAVILY_API_KEY"))

    #web search method implementation. This method retrieves data from the web and return the results
