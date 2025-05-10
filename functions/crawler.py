import asyncio

from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig
from crawl4ai.content_filter_strategy import BM25ContentFilter
from crawl4ai.markdown_generation_strategy import DefaultMarkdownGenerator


async def main(url: str):
    browser_config = BrowserConfig(
        verbose=True, headless=True, text_mode=True, light_mode=True
    )
    run_config = CrawlerRunConfig(
        markdown_generator=DefaultMarkdownGenerator(
            content_filter=BM25ContentFilter(
                bm25_threshold=0.8,
                user_query="Financial Performance",
            ),
            options={"ignore_links": True},
        ),
        excluded_tags=["nav", "header"],
        exclude_external_links=True,
    )
    async with AsyncWebCrawler(config=browser_config) as crawler:
        result = await crawler.arun(url=url, config=run_config)
        print(result.markdown.fit_markdown)


asyncio.run(
    main(
        url="https://www.tatamotors.com/press-releases/tata-motors-consolidated-q4-fy24-results/"
    )
)
