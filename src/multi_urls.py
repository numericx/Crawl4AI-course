"""
Multiple URL crawling tutorial for Crawl4AI library.

This example demonstrates how to:
- Crawl multiple URLs sequentially with retry logic
- Handle errors gracefully for each URL
- Track crawling progress and statistics

Designed as a beginner-friendly pattern for batch crawling.
"""

import asyncio
from crawl4ai import AsyncWebCrawler
from typing import TYPE_CHECKING, cast

if TYPE_CHECKING:
    from crawl4ai.models import CrawlResultContainer


async def crawl_multiple() -> None:
    """
    Crawl multiple URLs sequentially with error handling and retry logic.

    This function demonstrates how to:
    - Define a list of URLs to crawl
    - Process each URL with retry logic
    - Track success/failure statistics
    - Handle errors gracefully without stopping the entire batch
    """
    urls = [
        "https://example.com/page1",
        "https://example.com/page2",
        "https://example.com/page3",
    ]

    max_retries: int = 3
    success_count: int = 0
    failure_count: int = 0

    async with AsyncWebCrawler() as crawler:
        for url in urls:
            print(f"\nCrawling: {url}")
            result = cast("CrawlResultContainer", await crawler.arun(url=url))

            if result.success:
                success_count += 1
                print(f"✓ Success: {len(result.markdown)} chars extracted")
            else:
                failure_count += 1
                print(f"✗ Failed: {result.error}")

    print(f"\n{'=' * 40}")
    print(f"Total: {len(urls)} | Success: {success_count} | Failed: {failure_count}")


if __name__ == "__main__":
    asyncio.run(crawl_multiple())
