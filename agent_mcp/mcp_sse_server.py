from mcp.server.fastmcp import FastMCP
import uvicorn


mcp = FastMCP("MCP Server")

@mcp.tool()
def get_account_balance(account_id: str) -> dict:
    """Fetch current account balance and currency."""
    return {
        "account_id": account_id,
        "available_balance": 2450.75,
        "currency": "EUR",
        "last_updated": "2026-03-02T10:42:00Z"
    }

if __name__ == "__main__":
    app = mcp.sse_app()
    uvicorn.run(app, host="0.0.0.0", port=8001)