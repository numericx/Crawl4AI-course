# Module 3: Basic Crawling Fundamentals

**Type**: Core Concepts + Hands-on

## Learning Objectives

By the end of this module, students will be able to:

1. Initialize and use AsyncWebCrawler for web crawling
2. Configure basic BrowserConfig and CrawlerRunConfig options
3. Extract markdown content from web pages
4. Handle crawl results and errors properly
5. Extract links, media, and metadata from crawled pages

## Topics Covered

### 3.1 Understanding AsyncWebCrawler

**Architecture Overview**

```
AsyncWebCrawler
    ├── BrowserContext (Playwright browser instance)
    ├── PageManager (manages page lifecycle)
    └── CrawlerStrategy (determines how to crawl)
```

**Basic Usage Pattern**

```python
import asyncio
from crawl4ai import AsyncWebCrawler

async def main():
    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(url="https://example.com")
        print(result.markdown)

asyncio.run(main())
```

**Context Manager Pattern**

- Ensures proper resource cleanup
- Handles browser lifecycle automatically
- Supports async context manager protocol

**Async/Await Fundamentals**

```python
# Synchronous approach (don't do this)
crawler = AsyncWebCrawler()
result = crawler.arun(url)  # Returns coroutine, not result!

# Async approach (correct)
async with AsyncWebCrawler() as crawler:
    result = await crawler.arun(url)
```

### 3.2 Simple Crawl Example

**Basic Markdown Extraction**

```python
import asyncio
from crawl4ai import AsyncWebCrawler

async def extract_markdown():
    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(
            url="https://example.com"
        )

        if result.success:
            print("Title:", result.metadata.get("title"))
            print("Content:", result.markdown[:500])
        else:
            print(f"Crawl failed: {result.error}")

asyncio.run(extract_markdown())
```

**Result Object Structure**

```python
@dataclass
class CrawlResult:
    success: bool                    # Whether crawl succeeded
    markdown: str                    # Extracted markdown
    html: str                        # Raw HTML
    links: List[Dict[str, str]]      # Extracted links
    media: Dict[str, List]           # Images, videos, audio
    metadata: Dict[str, Any]         # Page metadata
    error: Optional[str]             # Error message if failed
    status_code: int                 # HTTP status code
    headers: Dict[str, str]          # Response headers
```

**Multi-URL Crawling**

```python
import asyncio
from crawl4ai import AsyncWebCrawler

async def crawl_multiple():
    urls = [
        "https://example.com/page1",
        "https://example.com/page2",
        "https://example.com/page3"
    ]

    async with AsyncWebCrawler() as crawler:
        for url in urls:
            result = await crawler.arun(url=url)
            if result.success:
                print(f"✓ {url}: {len(result.markdown)} chars")

asyncio.run(crawl_multiple())
```

### 3.3 Basic Configuration

**BrowserConfig**

Controls browser behavior and capabilities.

```python
from crawl4ai import BrowserConfig, AsyncWebCrawler

browser_config = BrowserConfig(
    headless=True,               # Run browser in headless mode
    verbose=True,                # Enable verbose logging
    user_agent="Mozilla/5.0",    # Custom user agent
    viewport_width=1920,         # Browser viewport width
    viewport_height=1080,        # Browser viewport height
)
```

**CrawlerRunConfig**

Controls how crawling is performed.

```python
from crawl4ai import CrawlerRunConfig

crawl_config = CrawlerRunConfig(
    cache_mode="BYPASS",         # BYPASS, ENABLED, DISABLED
    delay_before_return_html=0,  # Delay before extraction
    page_timeout=30000,          # Page load timeout (ms)
    maxRetries=3,                # Retry attempts on failure
)
```

**Chaining Configurations**

```python
from crawl4ai import BrowserConfig, CrawlerRunConfig, AsyncWebCrawler

browser_config = BrowserConfig(
    headless=True,
    viewport_width=1280,
    viewport_height=720
)

crawl_config = CrawlerRunConfig(
    cache_mode="BYPASS",
    page_timeout=45000
)

async with AsyncWebCrawler(config=browser_config) as crawler:
    result = await crawler.arun(
        url="https://example.com",
        config=crawl_config
    )
```

### 3.4 Handling Crawl Results

**Success Checking**

```python
async with AsyncWebCrawler() as crawler:
    result = await crawler.arun(url="https://example.com")

    # Method 1: Boolean flag
    if result.success:
        process_result(result)
    else:
        handle_error(result.error)

    # Method 2: Status code
    if result.status_code == 200:
        process_result(result)
```

**Error Handling Patterns**

```python
from crawl4ai import AsyncWebCrawler

async def robust_crawl():
    async with AsyncWebCrawler() as crawler:
        try:
            result = await crawler.arun(url="https://example.com")

            if not result.success:
                raise Exception(f"Crawl failed: {result.error}")

            return result

        except Exception as e:
            print(f"Error during crawl: {e}")
            return None

        finally:
            # Cleanup if needed
            pass
```

**Extracting Metadata**

```python
result = await crawler.arun(url="https://example.com")

# Common metadata fields
title = result.metadata.get("title")
description = result.metadata.get("description")
og_image = result.metadata.get("og_image")
published_date = result.metadata.get("published_date")
author = result.metadata.get("author")
```

### 3.5 Extracting Links, Media, and Metadata

**Link Extraction**

```python
result = await crawler.arun(url="https://example.com")

# All links
for link in result.links:
    print(f"URL: {link['href']}")
    print(f"Text: {link['text']}")
    print(f"Type: {link.get('type', 'unknown')}")

# Filter links by type
internal_links = [l for l in result.links if l.get('type') == 'internal']
external_links = [l for l in result.links if l.get('type') == 'external']
```

**Media Extraction**

```python
result = await crawler.arun(url="https://example.com")

# All media
media = result.media
print("Images:", media.get("images", []))
print("Videos:", media.get("videos", []))
print("Audio:", media.get("audio", []))

# Image details
for img in media.get("images", []):
    print(f"  - URL: {img['src']}")
    print(f"    Alt: {img.get('alt', 'No alt text')}")
    print(f"    Size: {img.get('width')}x{img.get('height')}")
```

**Complete Example with All Extractors**

```python
import asyncio
from crawl4ai import AsyncWebCrawler

async def comprehensive_crawl():
    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(url="https://example.com")

        print("=" * 50)
        print("CRAWL RESULTS")
        print("=" * 50)

        print(f"\n[Metadata]")
        for key, value in result.metadata.items():
            print(f"  {key}: {value}")

        print(f"\n[Content]")
        print(f"  Markdown length: {len(result.markdown)} chars")
        print(f"  First 200 chars: {result.markdown[:200]}...")

        print(f"\n[Links] ({len(result.links)} total)")
        for link in result.links[:5]:
            print(f"  - {link['text']}: {link['href']}")

        print(f"\n[Media]")
        print(f"  Images: {len(result.media.get('images', []))}")
        print(f"  Videos: {len(result.media.get('videos', []))}")

        print(f"\n[HTTP Info]")
        print(f"  Status: {result.status_code}")
        print(f"  Headers: {list(result.headers.keys())}")

asyncio.run(comprehensive_crawl())
```

## Hands-on Exercise: Build a Blog Scraper

### Exercise: Basic Blog Site Scraper

**Objective**: Build a scraper that extracts articles from a blog site

**Setup**:

1. Use a sample blog (e.g., https://blog.python.org or similar)
2. Or use example.com for testing

**Instructions**:

1. **Basic Crawler**

```python
import asyncio
from crawl4ai import AsyncWebCrawler

async def simple_blog_crawl():
    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun("https://example.com/blog")

        if result.success:
            print(result.markdown)

asyncio.run(simple_blog_crawl())
```

2. **Extract Article Links**

```python
async def extract_article_links():
    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun("https://example.com/blog")

        articles = []
        for link in result.links:
            if "/blog/" in link["href"] and "example.com" in link["href"]:
                articles.append({
                    "title": link["text"],
                    "url": link["href"]
                })

        return articles
```

3. **Create Article Extractor Class**

```python
from dataclasses import dataclass
from typing import List, Optional

@dataclass
class Article:
    title: str
    url: str
    content: Optional[str] = None
    author: Optional[str] = None
    date: Optional[str] = None

class BlogScraper:
    def __init__(self):
        self.crawler = None

    async def __aenter__(self):
        self.crawler = AsyncWebCrawler()
        await self.crawler.__aenter__()
        return self

    async def __aexit__(self, *args):
        if self.crawler:
            await self.crawler.__aexit__(*args)

    async def get_articles(self, blog_url: str, max_articles: int = 5) -> List[Article]:
        # Get article links first
        result = await self.crawler.arun(blog_url)
        # Parse and crawl individual articles
        # Return list of Article objects
        pass

    async def get_article_content(self, url: str) -> Optional[str]:
        result = await self.crawler.arun(url)
        return result.markdown if result.success else None
```

4. **Save Results to JSON**

```python
import json

async def save_articles(articles: List[Article], filename: str):
    with open(filename, "w") as f:
        json.dump([vars(a) for a in articles], f, indent=2)
```

**Bonus Challenge**: Add date parsing and author extraction.

**Deliverables**:

1. Working scraper that extracts articles
2. JSON file with scraped data
3. Console output showing extraction stats

## Quiz Questions

1. Why is `await` necessary when calling `crawler.arun()`?
2. What does the `success` property in CrawlResult indicate?
3. How do you configure the browser viewport size?
4. What's the difference between `cache_mode="BYPASS"` and `cache_mode="DISABLED"`?
5. How would you extract only internal links from a crawl result?

## Key Takeaways

- AsyncWebCrawler uses Python's async/await for non-blocking operations
- BrowserConfig controls browser behavior, CrawlerRunConfig controls crawling behavior
- Always check `result.success` before processing content
- Links and media are extracted automatically during crawling

## Next Module Preview

Module 4 dives deep into configuration options, covering advanced BrowserConfig settings, CSS/XPath selectors, and LLM provider configuration.