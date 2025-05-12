from datetime import datetime

from mcp.server.fastmcp import FastMCP

from functions.crawler import crawl_web
from functions.embeddings import addToVectorDB, getVectorDB
from functions.search import generate_links
from zerodha import getCurrentHoldings

mcp = FastMCP("Portfolio-Analyzer")


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


@mcp.tool()
async def getStockContext(stock: str):
    stock = stock.capitalize() + "STOCK"
    current_year = datetime.now().year
    keywords = [stock, str(current_year), str(current_year - 1)]
    links, search_list = generate_links(keywords)
    crawled_result = await crawl_web(links)
    _, collections = getVectorDB()
    addToVectorDB(crawled_result)
    query = collections.query(query_texts=search_list, n_results=10)
    sources = query.get("metadatas")
    context = query.get("documents")

    return str(context) + str(sources)


if __name__ == "__main__":
    mcp.run(transport="stdio")
