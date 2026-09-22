from fastmcp import FastMCP
import network_map

mcp = FastMCP("Paraverse Copilot")

network_map.fetch_module(mcp)

if "__name__" == "__main__":
    mcp.run(transport="websocket", host="localhost", port=8000)