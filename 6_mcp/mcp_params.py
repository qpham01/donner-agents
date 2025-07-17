import os
from dotenv import load_dotenv
from market import is_paid_polygon, is_realtime_polygon
from agents.mcp.server import MCPServerStdioParams

load_dotenv(override=True)

brave_api_key = os.getenv("BRAVE_API_KEY") or ""
brave_env = {"BRAVE_API_KEY": brave_api_key}
polygon_api_key = os.getenv("POLYGON_API_KEY") or ""

# The MCP server for the Trader to read Market Data

if is_paid_polygon or is_realtime_polygon:
    market_mcp = MCPServerStdioParams(command="uvx", args=["--from", "git+https://github.com/polygon-io/mcp_polygon@v0.1.0", "mcp_polygon"], env={"POLYGON_API_KEY": polygon_api_key})
else:
    market_mcp = MCPServerStdioParams(command="uv", args=["run", "market_server.py"])


# The full set of MCP servers for the trader: Accounts, Push Notification and the Market

trader_mcp_server_params = [
    MCPServerStdioParams(command="uv", args=["run", "accounts_server.py"]),
    MCPServerStdioParams(command="uv", args=["run", "push_server.py"]),
    MCPServerStdioParams(command="uvx", args=["--from", "git+https://github.com/polygon-io/mcp_polygon@v0.1.0", "mcp_polygon"], env={"POLYGON_API_KEY": polygon_api_key}),
]

# The full set of MCP servers for the researcher: Fetch, Brave Search and Memory


def researcher_mcp_server_params(name: str):
    return [
        MCPServerStdioParams(command="uvx", args=["mcp-server-fetch"]),
        MCPServerStdioParams(command="npx", args=["-y", "@modelcontextprotocol/server-brave-search"], env=brave_env),
        MCPServerStdioParams(command="npx", args=["-y", "mcp-memory-libsql"], env={"LIBSQL_URL": f"file:./memory/{name}.db"}),
    ]
