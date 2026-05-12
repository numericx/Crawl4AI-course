"""Test script to verify Crawl4AI setup and basic functionality."""
import asyncio
from typing import Optional
from crawl4ai import AsyncWebCrawler


async def test_crawl(timeout: int = 30) -> bool:
    """Test basic Crawl4AI setup by crawling a simple page.

    Args:
        timeout: Timeout in seconds for the crawl operation.

    Returns:
        bool: True if crawl succeeds and returns valid content, False otherwise.
    """
    try:
        async with AsyncWebCrawler() as crawler:
            result = await asyncio.wait_for(
                crawler.arun("https://example.com"),
                timeout=timeout
            )

            if not result.success:
                print(f"✗ Crawl failed: {result.error}")
                return False

            if not result.markdown or len(result.markdown) == 0:
                print("✗ No content extracted")
                return False

            print(f"✓ Success: {result.success}")
            print(f"✓ Markdown length: {len(result.markdown)}")
            links_count = len(result.links) if result.links else 0
            print(f"✓ Links found: {links_count}")
            return True
    except asyncio.TimeoutError:
        print(f"✗ Timeout: Crawl exceeded {timeout} seconds")
        return False
    except Exception as e:
        print(f"✗ Error: {type(e).__name__}: {e}")
        return False


if __name__ == "__main__":
    success = asyncio.run(test_crawl())
    print(f"\nSetup {'✓ Working!' if success else '✗ Not Working!'}")