## this file imports all the mcp tools that I have created and works as an entry point
from mcp.server import MCPServer

from tools_schemas.websearch_tool_schema import WebSearch
from tools_schemas.calculator_tool_schema import CalculatorTool
from tools_schemas.save_to_txt_tool import WriteToTxt
from tools_schemas.generate_code_file_tool import GenerateCodeFile

mcp = MCPServer("my-agent-tools")

mcp.add_tool(WebSearch.web_search)
mcp.add_tool(CalculatorTool.calculator)
mcp.add_tool(WriteToTxt.write_to_file)
mcp.add_tool(GenerateCodeFile.generate_code_file)

if __name__ == "__main__":
    mcp.run(transport="stdio")