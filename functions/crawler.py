from dataclasses import dataclass

from crawl4ai import (
    AsyncWebCrawler,
    BrowserConfig,
    CacheMode,
    CrawlerRunConfig,
    DefaultMarkdownGenerator,
    PruningContentFilter,
)


@dataclass
class CrawledResult:
    url: str
    text: str


async def crawl_web(urls: list[str]) -> list[CrawledResult]:
    '''llm_config = LLMConfig(provider="ollama/qwen3:4b")
    filter = LLMContentFilter(
        llm_config=llm_config,  # or your preferred provider
        instruction="""
    You are an expert financial document analyst.

    Your task is to extract only the content directly related to a company’s financials, performance, and material business developments from the provided scraped text.

    Include content related to:
    - Quarterly or annual earnings (revenue, profit/loss, EBITDA, margins)
    - Financial guidance, forecasts, or revisions
    - Stock performance commentary
    - Management commentary on financial results
    - M&A, divestitures, strategic investments, or capital expenditures
    - Credit ratings, analyst upgrades/downgrades with financial rationale
    - Macroeconomic factors impacting company performance

    Exclude:
    - Hyperlinks and any other links
    - Repeated or filler content

    Output must be:
    - Clean, well-structured **Markdown**
    - Free of broken lines, redundant text, and empty sections
    - Only the filtered relevant text, no additional explanation
    """,
        chunk_token_threshold=1024,
        verbose=True,
    )

    md_generator = DefaultMarkdownGenerator(
        content_filter=filter, options={"ignore_links": True}
    )'''

    prune_filter = PruningContentFilter(
        threshold=0.45, threshold_type="dynamic", min_word_threshold=5
    )
    md_generator = DefaultMarkdownGenerator(content_filter=prune_filter)

    browser_config = BrowserConfig(
        verbose=False, headless=True, text_mode=True, light_mode=True
    )
    run_config = CrawlerRunConfig(
        markdown_generator=md_generator,
        excluded_tags=["nav", "header", "form", "a", "img", "footer"],
        exclude_external_links=True,
        exclude_all_images=True,
        exclude_internal_links=True,
        cache_mode=CacheMode.BYPASS,
        only_text=True,
    )

    async with AsyncWebCrawler(config=browser_config) as crawler:
        results = []
        try:
            for url in urls:
                result = await crawler.arun(url=url, config=run_config)
                results.append(
                    CrawledResult(url=result.url, text=result.markdown.fit_markdown)
                )
        except Exception as e:
            #print(e)
        return results
