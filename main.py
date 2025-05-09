from mcp.server.fastmcp import FastMCP

from holdings import Holding, getCurrentHoldings

mcp = FastMCP("Demo")


# Add an addition tool
@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b


@mcp.tool()
def getPortfolio() -> list[Holding]:
    ticket_objs = getCurrentHoldings()
    return [{x.ticker, x.qty} for x in ticket_objs]


if __name__ == "__main__":
    mcp.run(transport="stdio")
