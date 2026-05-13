#!/usr/bin/env python3
"""
Utility script to inspect the structure of links extracted by Crawl4AI.

This script demonstrates:
- How to access link data from CrawlResult
- The structure of the links dictionary (internal/external)
- Useful for debugging and understanding Crawl4AI output

Usage:
    python src/utilities/inspect_links.py
"""

import asyncio
from typing import Any

from crawl4ai import AsyncWebCrawler


async def inspect_links(url: str = "https://example.com") -> dict[str, Any]:
    """
    Crawl a URL and inspect the structure of extracted links.

    Args:
        url: The URL to crawl and inspect links from.

    Returns:
        A dictionary containing link structure information.
    """
    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(url=url)

        if not result.success:
            print(f"✗ Crawl failed: {getattr(result, 'error', 'Unknown error')}")
            return {}

        # Extract link information
        links_info = {
            "url": url,
            "type": type(result.links).__name__,
            "is_dict": isinstance(result.links, dict),
        }

        if isinstance(result.links, dict):
            links_info["keys"] = list(result.links.keys())
            links_info["internal_count"] = len(result.links.get("internal", []))
            links_info["external_count"] = len(result.links.get("external", []))

        # Print inspection results
        print(f"\n{'=' * 60}")
        print(f"Link Inspection Results for: {url}")
        print(f"{'=' * 60}")
        print(f"Type: {links_info['type']}")
        print(f"Is Dictionary: {links_info['is_dict']}")

        if links_info["is_dict"]:
            print(f"\nKeys: {links_info['keys']}")
            print(f"\nLink Counts:")
            print(f"  Internal links: {links_info['internal_count']}")
            print(f"  External links: {links_info['external_count']}")

            # Show first external link as example
            external_links = result.links.get("external", [])
            if external_links:
                print(f"\nExample External Link:")
                example = external_links[0]
                print(f"  URL: {example.get('href', 'N/A')}")
                print(f"  Text: {example.get('text', 'N/A')}")

        print(f"{'=' * 60}\n")

        return links_info


async def main() -> None:
    """Main entry point for the link inspection utility."""
    await inspect_links()


if __name__ == "__main__":
    asyncio.run(main())
