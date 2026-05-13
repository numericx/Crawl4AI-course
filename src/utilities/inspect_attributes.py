#!/usr/bin/env python3
"""
Utility script to inspect the attributes of CrawlResult object.

This script demonstrates:
- How to inspect available attributes on CrawlResult
- What data is extracted during crawling
- Useful for debugging and understanding Crawl4AI capabilities

Usage:
    python src/utilities/inspect_attributes.py
"""

import asyncio
from typing import Any

from crawl4ai import AsyncWebCrawler


async def inspect_attributes(url: str = "https://example.com") -> list[str]:
    """
    Crawl a URL and inspect all available attributes of the CrawlResult object.

    Args:
        url: The URL to crawl and inspect result attributes from.

    Returns:
        A list of public attribute names available on the CrawlResult object.
    """
    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(url=url)

        # Get all public attributes (not starting with underscore)
        attributes = [attr for attr in dir(result) if not attr.startswith("_")]

        # Print inspection results
        print(f"\n{'=' * 60}")
        print(f"CrawlResult Attribute Inspection for: {url}")
        print(f"{'=' * 60}")
        print(f"\nTotal Attributes Found: {len(attributes)}\n")

        # Display attributes in a formatted way
        print("Available Attributes:")
        print("-" * 60)

        for i, attr in enumerate(attributes, 1):
            try:
                value = getattr(result, attr)
                value_type = type(value).__name__
                value_str = (
                    str(value)[:50] + "..." if len(str(value)) > 50 else str(value)
                )
                print(f"{i:2}. {attr:25} | Type: {value_type:15} | Value: {value_str}")
            except (AttributeError, Exception) as e:
                print(f"{i:2}. {attr:25} | Error accessing: {e}")

        print("-" * 60)

        # Show key attributes specifically
        print(f"\nKey Attributes Summary:")
        key_attrs = [
            "success",
            "markdown",
            "html",
            "links",
            "media",
            "metadata",
            "status_code",
        ]
        for attr in key_attrs:
            if hasattr(result, attr):
                value = getattr(result, attr)
                if attr == "markdown" and isinstance(value, str):
                    print(f"  {attr:15}: {len(value)} characters")
                elif attr == "links" and isinstance(value, dict):
                    link_count = len(value.get("internal", [])) + len(
                        value.get("external", [])
                    )
                    print(f"  {attr:15}: {link_count} total links")
                elif attr == "media" and isinstance(value, dict):
                    media_count = sum(
                        len(v) for v in value.values() if isinstance(v, (list, tuple))
                    )
                    print(f"  {attr:15}: {media_count} media items")
                else:
                    print(f"  {attr:15}: {value}")

        print(f"\n{'=' * 60}\n")

        return attributes


async def main() -> None:
    """Main entry point for the attribute inspection utility."""
    await inspect_attributes()


if __name__ == "__main__":
    asyncio.run(main())
