"""
Basic markdown extraction tutorial for Crawl4AI library.

This example demonstrates how to:
- Extract markdown content from a webpage
- Access metadata (title, description, etc.)
- Handle crawl results gracefully

Designed as a beginner-friendly starting point for learning Crawl4AI.
"""

import asyncio
from crawl4ai import AsyncWebCrawler
from typing import TYPE_CHECKING, cast


if TYPE_CHECKING:
    from crawl4ai.models import CrawlResultContainer


async def extract_markdown() -> None:
    """
    Extract and display markdown content from a webpage.

    This function demonstrates how to:
    - Create an async crawler instance
    - Fetch content from a URL
    - Access markdown and metadata from the result
    """
    url: str = "https://example.com"

    async with AsyncWebCrawler() as crawler:
        result = cast("CrawlResultContainer", await crawler.arun(url=url))

        if result.success:
            title = result.metadata.get("title", "Unknown")
            print(f"Title: {title}")
            print(f"Content:\n{result.markdown}")
        else:
            print(f"Crawl failed: {result.error}")


if __name__ == "__main__":
    asyncio.run(extract_markdown())
