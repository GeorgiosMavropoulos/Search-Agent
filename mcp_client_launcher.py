###this file contains the mcp server as a subprocess
import asyncio
import os
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from dotenv import load_dotenv


#load environmental variables
load_dotenv()

##create an instance of std input output server parameters
server_params = StdioServerParameters(
    command="uv",
    args=["run", "python", "mcp_server.py"],
    env={
        "TAVILY_API_KEY": os.getenv("TAVILY_API_KEY"), ##import tavily api key
    } 
)

# The following function initializes a session with the mcp server, enabling read and write streams
async def client():
    async with stdio_client(server_params) as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as session:
            await session.initialize() 
    # List available tools
            tools_result = await session.list_tools()
            print("Available tools:")
            for tool in tools_result.tools:
                print(f"  - {tool.name}: {tool.description}...")

            #call tavily search and request a search for the 2025's Nobel Physics winner
            result = await session.call_tool(
                "web_search",
                arguments={"query": "2025 Nobel Physics"}
            )
            print("Search Result:")
            print(result.content)

asyncio.run(client())