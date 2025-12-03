
"""
London Bus MCP Server using FastMCP
Provides real-time London bus information via TfL API
"""

import httpx
import sys
from datetime import datetime
from fastmcp import FastMCP

mcp = FastMCP("London Bus Info")

TFL_API_BASE = "https://api.tfl.gov.uk"


@mcp.tool()
async def search_bus_stops(query: str) -> str:
    """
    Search for bus stops by name or postcode.
    
    Args:
        query: Stop name or postcode (e.g., 'Oxford Circus', 'SW1A 1AA')
    
    Returns:
        List of matching bus stops with IDs
    """
    url = f"{TFL_API_BASE}/StopPoint/Search"
    params = {
        "query": query,
        "modes": "bus",
        "maxResults": 10
    }
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            response = await client.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            
            matches = data.get('matches', [])
            
            if not matches:
                return f"❌ No stops found for '{query}'."
            
            result = f"🔍 Bus stops found for '{query}':\n\n"
            
            for stop in matches:
                name = stop['name']
                stop_id = stop['id']
                lat = stop.get('lat', 'N/A')
                lon = stop.get('lon', 'N/A')
                
                result += f"🚏 {name}\n"
                result += f"   ID: {stop_id}\n"
                result += f"   Location: {lat}, {lon}\n\n"
            
            return result
            
        except httpx.HTTPError as e:
            return f"❌ API error: {str(e)}"


if __name__ == "__main__":
    mcp.settings.debug = True
    transport = "stdio"  # Default to stdio for MCP Inspector compatibility
    
    if len(sys.argv) > 1 and sys.argv[1] == "--http":
        transport = "streamable-http"
        print("Starting server with streamable-http transport on port 8000")
        mcp.run(transport="streamable-http", host="127.0.0.1", port=8000)
    else:
        print("Starting server with stdio transport (for MCP Inspector)")
        mcp.run(transport="stdio")