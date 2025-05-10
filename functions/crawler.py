import asyncio

from crawl4ai import AsyncWebCrawler


async def main(url: str):
    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(url=url)

        print(result.markdown)


asyncio.run(main(url="abc"))
