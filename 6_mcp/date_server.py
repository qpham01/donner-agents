from mcp.server.fastmcp import FastMCP
from accounts import Account
from datetime import datetime as dt

mcp = FastMCP("accounts_server")

@mcp.tool()
async def get_date_today() -> str:
    """Get today's date in the format YYYY-MM-DD."""
    return dt.now().strftime("%Y-%m-%d")

if __name__ == "__main__":
    mcp.run()
