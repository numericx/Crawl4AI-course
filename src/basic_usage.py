"""
Basic usage tutorial for Crawl4AI library.

This example demonstrates how to crawl a webpage with error handling
and retry logic. It's designed as a beginner-friendly starting point
for learning the Crawl4AI library.
"""

import asyncio
from crawl4ai import AsyncWebCrawler
from typing import TYPE_CHECKING, cast

if TYPE_CHECKING:
    from crawl4ai.models import CrawlResultContainer


async def main() -> None:
    """
    Main function to demonstrate basic Crawl4AI usage.

    This function shows how to:
    - Create an async crawler instance
    - Fetch content from a URL
    - Handle errors gracefully with retry logic

    The example includes 3 retry attempts with exponential backoff
    to handle temporary network issues.
    """
    url: str = "https://example.com"
    max_retries: int = 3

    for attempt in range(max_retries):
        try:
            # Create crawler instance and fetch the webpage
            async with AsyncWebCrawler() as crawler:
                result = cast("CrawlResultContainer", await crawler.arun(url=url))

                # Check if crawl was successful
                if result.success:
                    print(result.markdown)
                else:
                    print(f"Error: {result.error}")

            break  # Success, exit retry loop

        except Exception as e:
            # Handle errors during crawling
            if attempt == max_retries - 1:
                # Last attempt failed - report final error
                print(f"Failed after {max_retries} attempts: {e}")
            else:
                # Intermediate failure - retry with backoff
                print(f"Attempt {attempt + 1} failed: {e}. Retrying...")
                await asyncio.sleep(2**attempt)  # Exponential backoff


if __name__ == "__main__":
    asyncio.run(main())
