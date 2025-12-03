"""
Pydantic AI Client for London Bus MCP Server
Interactive client to query London bus information
"""

from pydantic_ai import Agent
from pydantic_ai.toolsets.fastmcp import FastMCPToolset
import otel
import os

# Use HTTP mode if SERVER_MODE env var is set
server_mode = os.getenv("SERVER_MODE", "stdio")

if server_mode == "http":
    # For HTTP mode - requires server running with --http flag
    tfl_mcp_toolset = FastMCPToolset("http://127.0.0.1:8000")
else:
    # For stdio mode - launches server process directly
    tfl_mcp_toolset = FastMCPToolset("server.py")


agent = Agent(
    name="tfl_agent",
    model="anthropic:claude-haiku-4-5",
    instructions="""You are a helpful assistant make use of the tools available to respond to the user.""",
    toolsets=[tfl_mcp_toolset],
)

if __name__ == '__main__':
    # Search Bus Stops
    res = agent.run_sync("Find bus stops near Piccadilly Circus")
    print("Result:\n")
    print(res.output)
    
    # # Get Route Info
    # res = agent.run_sync("Tell me about bus route 190")
    # print("Result:\n")
    # print(res.output)

