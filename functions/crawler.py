import asyncio

from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig
from crawl4ai.content_filter_strategy import BM25ContentFilter
from crawl4ai.markdown_generation_strategy import DefaultMarkdownGenerator
from search import generate_links


async def main(url: str, user_query: str):
    browser_config = BrowserConfig(
        verbose=True, headless=True, text_mode=True, light_mode=True
    )
    run_config = CrawlerRunConfig(
        markdown_generator=DefaultMarkdownGenerator(
            content_filter=BM25ContentFilter(
                bm25_threshold=0.8,
                user_query=user_query,
            ),
            options={"ignore_links": True},
        ),
        excluded_tags=["nav", "header"],
        exclude_external_links=True,
    )
    async with AsyncWebCrawler(config=browser_config) as crawler:
        result = await crawler.arun(url=url, config=run_config)
        return result


links = generate_links()
print(asyncio.run(main()))
