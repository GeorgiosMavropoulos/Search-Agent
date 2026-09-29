###this file contains the mcp server as a subprocess
import asyncio
import os
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from dotenv import load_dotenv
from contextlib import asynccontextmanager
from function_tool.function_tool import FunctionTool,BaseTool
#load environmental variables
load_dotenv()

##create an instance of std input output server parameters
server_params = StdioServerParameters(
    command="uv",
    args=["run", "python", "-m", "mcp_implementation.mcp_server"]
   
)


def _extract_text_content(result) -> str:
    """Extract plain text from an MCP CallToolResult."""
    parts = []
    for item in getattr(result, "content", []) or []:
        text = getattr(item, "text", None)
        if text is not None:
            parts.append(text)
    return "\n".join(parts)


##this method creates the mcp tools using the FunctionTool wrapper I created
def _create_mcp_tool(mcp_tool, session) -> FunctionTool:
    """Create a FunctionTool that wraps an MCP tool."""

    async def call_mcp(**kwargs):      
       result = await session.call_tool(mcp_tool.name, kwargs)
       return _extract_text_content(result)

    tool_definition = {
        "type": "function",
        "function": {
            "name": mcp_tool.name,
            "description": mcp_tool.description,
            "parameters": mcp_tool.input_schema,
        }
    }

    return FunctionTool(
        func=call_mcp,
        name=mcp_tool.name,
        description=mcp_tool.description,
        tool_definition=tool_definition
    )

##this function lists all available tools
async def load_mcp_tools(session) -> list[BaseTool]:
    """Load tools from an MCP server and convert to FunctionTools."""
    tools = []

    
    mcp_tools = await session.list_tools()

    for mcp_tool in mcp_tools.tools:
       func_tool = _create_mcp_tool(mcp_tool, session)
       tools.append(func_tool)

    
    return tools

# The following function initializes a session with the mcp server, enabling read and write streams
@asynccontextmanager
async def client():
   
    async with stdio_client(server_params) as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as session:
            await session.initialize() 
            ##load all the available mcp tools
            tools = await load_mcp_tools(session)
            yield (session, tools) #keep session alive, and tools available as long as the session is active
            
