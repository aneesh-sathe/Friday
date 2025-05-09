from mcp.server.fastmcp import FastMCP

from holdings import getCurrentHoldings

mcp = FastMCP("Demo")


# Add an addition tool
@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b


@mcp.tool()
def getPortfolio(qty: str = "false", avg_price: str = "false") -> list:
    """
    Get portfolio information.

    Parameters:
    - qty: Whether to include quantity information ("true" or "false")
    - avg_price: Whether to include average price information ("true" or "false")

    Returns:
    - List of portfolio items with requested information
    """
    ticker_objs = getCurrentHoldings()
    result = []

    include_qty = qty.lower() == "true"
    include_avg_price = avg_price.lower() == "true"

    for item in ticker_objs:
        portfolio_item = []
        portfolio_item.append(item.ticker)

        if include_qty:
            portfolio_item.append(item.qty)

        if include_avg_price:
            portfolio_item.append(item.avg_price)

        result.append(portfolio_item)

    return result


if __name__ == "__main__":
    a = getPortfolio("true", "true")
    print(a)
    mcp.run(transport="stdio")
