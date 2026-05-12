"""
Extract all available data from a webpage using Crawl4AI.

This example demonstrates how to:
- Extract comprehensive data from a single URL
- Display metadata, content, links, media, and HTTP information
- Handle errors with retry logic
"""

import argparse
import asyncio
from crawl4ai import AsyncWebCrawler
from typing import TYPE_CHECKING, cast

if TYPE_CHECKING:
    from crawl4ai.models import CrawlResultContainer


async def comprehensive_crawl(url: str) -> None:
    """
    Crawl a single URL and display all extracted data.

    This function demonstrates how to:
    - Extract and display metadata, content, links, media, and HTTP info
    - Handle errors with retry logic (3 attempts with exponential backoff)
    - Verify crawl success before accessing result data

    Args:
        url: The URL to crawl
    """
    max_retries: int = 3

    for attempt in range(max_retries):
        try:
            async with AsyncWebCrawler() as crawler:
                result = cast("CrawlResultContainer", await crawler.arun(url=url))

                if not result.success:
                    raise Exception(f"Crawl failed: {result.error}")

                print("=" * 50)
                print("CRAWL RESULTS")
                print("=" * 50)

                print(f"\n[Metadata]")
                for key, value in result.metadata.items():
                    print(f" {key}: {value}")

                print(f"\n[Content]")
                print(f" Markdown length: {len(result.markdown)} chars")
                print(f" First 200 chars: {result.markdown[:200]}...")

                # Combine internal and external links
                all_links = result.links.get("internal", []) + result.links.get(
                    "external", []
                )
                print(f"\n[Links] ({len(all_links)} total)")
                for link in all_links[:5]:
                    print(f" - {link.get('text', '')}: {link.get('href', '')}")

                print(f"\n[Media]")
                print(f" Images: {len(result.media.get('images', []))}")
                print(f" Videos: {len(result.media.get('videos', []))}")

                print(f"\n[HTTP Info]")
                print(f" Status: {result.status_code}")
                print(f" Headers: {list(result.response_headers.keys())}")

                break  # Success, exit retry loop

        except Exception as e:
            if attempt == max_retries - 1:
                print(f"Failed after {max_retries} attempts: {e}")
            else:
                print(f"Attempt {attempt + 1} failed: {e}. Retrying...")
                await asyncio.sleep(2**attempt)


def parse_args() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Extract all available data from a webpage using Crawl4AI."
    )
    parser.add_argument(
        "--url",
        type=str,
        required=True,
        help="URL to crawl",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    asyncio.run(comprehensive_crawl(args.url))
