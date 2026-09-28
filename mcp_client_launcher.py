###this file contains the mcp server as a subprocess
import asyncio
import os
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from dotenv import load_dotenv
from contextlib import asynccontextmanager

#load environmental variables
load_dotenv()

##create an instance of std input output server parameters
server_params = StdioServerParameters(
    command="uv",
    args=["run", "python", "mcp_server.py"]
   
)

# The following function initializes a session with the mcp server, enabling read and write streams
@asynccontextmanager
async def client():
    async with stdio_client(server_params) as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as session:
            await session.initialize() 
            yield session
            
    

            
