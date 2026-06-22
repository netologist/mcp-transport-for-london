"""
Pydantic AI Client for London Bus MCP Server
Interactive client to query London bus information
"""
from otel import enable_tracing
from agent import create_agent

if __name__ == "__main__":
    enable_tracing()
    agent = create_agent()
    # # Search Bus Stops
    # res = agent.run_sync("Find bus stops near Piccadilly Circus")
    # print("Result:\n")
    # print(res.output)

    # Get Route Info
    res = agent.run_sync("Tell me about bus route 190")
    print("Result:\n")
    print(res.output)
