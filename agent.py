import os

from pydantic_ai import Agent
from pydantic_ai.toolsets.fastmcp import FastMCPToolset

# Use HTTP mode if SERVER_MODE env var is set
server_mode = os.getenv("SERVER_MODE", "stdio")

def create_agent():    
    if server_mode == "http":
        # For HTTP mode - requires server running with --http flag
        tfl_mcp_toolset = FastMCPToolset("http://127.0.0.1:8000")
    else:
        # For stdio mode - launches server process directly
        tfl_mcp_toolset = FastMCPToolset("server.py")
        
    return Agent(
        name="tfl_agent",
        model="anthropic:claude-haiku-4-5",
        instructions="""You are a helpful assistant make use of the tools available to respond to the user.""",
        toolsets=[tfl_mcp_toolset],
    )