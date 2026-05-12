# Module 4: Configuration Deep Dive

**Type**: Technical Deep Dive

## Learning Objectives

By the end of this module, students will be able to:

1. Configure BrowserConfig with advanced options (proxies, user agents, storage states)
2. Use CrawlerRunConfig for caching, timeouts, and CSS/XPath selectors
3. Set up LLMConfig with multiple providers (OpenAI, Anthropic, Ollama, Azure)
4. Chain configurations for complex crawling scenarios
5. Implement persistent browser contexts and storage states

## Topics Covered

### 4.1 BrowserConfig Advanced Options

**Headless Mode**

```python
from crawl4ai import BrowserConfig

# Default headless
config = BrowserConfig(headless=True)

# Non-headless (visible browser)
config = BrowserConfig(headless=False)

# Stealth mode (reduces detection)
config = BrowserConfig(
    headless=True,
    stealth=True  # Hides automation signals
)
```

**Viewport Configuration**

```python
config = BrowserConfig(
    viewport_width=1920,
    viewport_height=1080,
    screen_width=1920,
    screen_height=1080
)

# Mobile viewport
config = BrowserConfig(
    viewport_width=375,
    viewport_height=812,
    device_scale_factor=2.0,
    is_mobile=True,
    has_touch=True
)
```

**User Agent Configuration**

```python
# Custom user agent string
config = BrowserConfig(
    user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
)

# Rotate user agents
import random

user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"
]

def get_random_ua():
    return random.choice(user_agents)

config = BrowserConfig(user_agent=get_random_ua())
```

**Proxy Configuration**

```python
# HTTP proxy
config = BrowserConfig(
    proxy="http://proxy.example.com:8080"
)

# HTTPS proxy with authentication
config = BrowserConfig(
    proxy="http://user:password@proxy.example.com:8080"
)

# SOCKS5 proxy
config = BrowserConfig(
    proxy="socks5://proxy.example.com:1080"
)

# Rotating proxies
def get_next_proxy():
    proxies = [
        "http://proxy1.example.com:8080",
        "http://proxy2.example.com:8080",
        "http://proxy3.example.com:8080"
    ]
    return random.choice(proxies)

config = BrowserConfig(proxy=get_next_proxy())
```

**Browser Context Options**

```python
config = BrowserConfig(
    browser_type="chromium",    # chromium, firefox, webkit
    headless=True,
    ignore_https_errors=True,   # Handle SSL issues
    java_script_enabled=True,
    safe_mode=False             # Disable safety features for speed
)
```

### 4.2 CrawlerRunConfig Deep Dive

**Cache Modes**

```python
from crawl4ai import CrawlerRunConfig, CacheMode

# Disable caching entirely
config = CrawlerRunConfig(cache_mode=CacheMode.DISABLED)

# Enable caching (respect cache headers)
config = CrawlerRunConfig(cache_mode=CacheMode.ENABLED)

# Bypass cache (always fetch fresh)
config = CrawlerRunConfig(cache_mode=CacheMode.BYPASS)

# Default (use if available, otherwise fetch)
config = CrawlerRunConfig(cache_mode=CacheMode.READ_WRITE)
```

| Cache Mode | Description | When to Use |
|------------|-------------|-------------|
| `DISABLED` | No caching at all. Every request fetches fresh data and nothing is stored. | Testing, debugging, or when you need guaranteed fresh data every time. |
| `ENABLED` | Respects HTTP cache headers (e.g., `Cache-Control`, `ETag`). Reuses cached content if still valid. | Production crawling where you want to respect server cache policies and reduce bandwidth. |
| `BYPASS` | Ignores cached content and always fetches fresh, but writes result to cache afterward. | When you need the latest data but still want to populate the cache for future runs. |
| `READ_WRITE` | Default mode. Uses cached content if available, otherwise fetches and caches the result. | General purpose crawling where speed matters and slightly stale data is acceptable. |

**Timeout Configuration**

```python
config = CrawlerRunConfig(
    page_timeout=60000,         # Page load timeout (ms)
    navigation_timeout=30000,   # Navigation timeout (ms)
    execution_timeout=45000,    # Script execution timeout (ms)
    max_retries=3,              # Number of retry attempts
    retry_delay=2000            # Delay between retries (ms)
)
```

**CSS and XPath Selectors**

```python
# CSS selector for content extraction
config = CrawlerRunConfig(
    css_selector="article.content",        # Extract only article content
    excluded_selector="nav, footer, .ads"  # Exclude elements
)

# XPath selector
config = CrawlerRunConfig(
    xpath_selector="//div[@class='article-body']"
)

# Combined approach
config = CrawlerRunConfig(
    css_selector=".main-content",
    excluded_selector=[
        "script",
        "style",
        ".sidebar",
        ".comments"
    ]
)
```

**Wait Conditions**

```python
from crawl4ai import WaitForStrategy

config = CrawlerRunConfig(
    wait_for="networkidle",        # Wait until network is idle
    wait_for_selector=".content",  # Wait for specific selector
    wait_for_timeout=10000         # Wait timeout (ms)
)

# WaitForStrategy options
config = CrawlerRunConfig(
    wait_for=WaitForStrategy.SELECTOR,
    wait_for_selector=".dynamic-content[data-loaded='true']"
)
```

**Scroll Configuration**

```python
config = CrawlerRunConfig(
    scroll_interval=1.0,        # Seconds between scrolls
    scroll_max_amount=5,        # Maximum scroll actions
    scroll_sensitivity=0.8,     # Scroll sensitivity (0-1)
    remove_overlay_elements=True
)
```

**Complete Configuration Example**

```python
from crawl4ai import CrawlerRunConfig

config = CrawlerRunConfig(
    # Caching
    cache_mode="BYPASS",

    # Timeouts
    page_timeout=60000,
    max_retries=3,

    # Content selection
    css_selector="main.article",
    excluded_selector="nav, footer, .ads, .sidebar",

    # Wait conditions
    wait_for="networkidle",
    wait_for_timeout=15000,

    # Scrolling
    scroll_interval=1.0,
    scroll_max_amount=3,

    # Other
    verbose=True,
    remove_overlay_elements=True
)
```

### 4.3 LLMConfig: Provider Configuration

**OpenAI Configuration**

```python
from crawl4ai import LLMConfig

llm_config = LLMConfig(
    provider="openai/gpt-4",
    api_key=os.getenv("OPENAI_API_KEY"),
    temperature=0.7,
    max_tokens=2000
)
```

**Anthropic (Claude) Configuration**

```python
llm_config = LLMConfig(
    provider="anthropic/claude-3-sonnet-20240229",
    api_key=os.getenv("ANTHROPIC_API_KEY"),
    temperature=0.7,
    max_tokens=4000
)
```

**Ollama (Local) Configuration**

```python
llm_config = LLMConfig(
    provider="ollama/llama2",
    base_url="http://localhost:11434",
    temperature=0.7
)

# Ollama with custom model
llm_config = LLMConfig(
    provider="ollama/mistral",
    base_url="http://localhost:11434",
    temperature=0.7,
    num_ctx=4096  # Context window size
)
```

**Azure OpenAI Configuration**

```python
llm_config = LLMConfig(
    provider="azure/gpt-4",
    api_key=os.getenv("AZURE_OPENAI_KEY"),
    api_base="https://your-resource.openai.azure.com",
    api_version="2023-05-15",
    temperature=0.7
)
```

**Multi-Provider with Fallback**

```python
def get_llm_config():
    if os.getenv("ANTHROPIC_API_KEY"):
        return LLMConfig(
            provider="anthropic/claude-3-sonnet-20240229",
            api_key=os.getenv("ANTHROPIC_API_KEY")
        )
    elif os.getenv("OPENAI_API_KEY"):
        return LLMConfig(
            provider="openai/gpt-4",
            api_key=os.getenv("OPENAI_API_KEY")
        )
    else:
        return LLMConfig(
            provider="ollama/llama2",
            base_url="http://localhost:11434"
        )
```

### 4.4 Chaining Configurations

**Configuration Stacking**

```python
from crawl4ai import BrowserConfig, CrawlerRunConfig, LLMConfig

# Base browser configuration
browser_config = BrowserConfig(
    headless=True,
    viewport_width=1920,
    viewport_height=1080
)

# Crawling configuration
crawl_config = CrawlerRunConfig(
    cache_mode="BYPASS",
    page_timeout=45000,
    css_selector="main"
)

# LLM configuration
llm_config = LLMConfig(
    provider="openai/gpt-4",
    api_key=os.getenv("OPENAI_API_KEY")
)

# Use all configurations
async with AsyncWebCrawler(config=browser_config) as crawler:
    result = await crawler.arun(
        url="https://example.com",
        config=crawl_config,
        llm_config=llm_config
    )
```

**Factory Pattern for Reusable Configs**

```python
class CrawlConfigFactory:
    @staticmethod
    def fast_crawl():
        return CrawlerRunConfig(
            cache_mode="BYPASS",
            page_timeout=15000,
            max_retries=1
        )

    @staticmethod
    def thorough_crawl():
        return CrawlerRunConfig(
            cache_mode="ENABLED",
            page_timeout=60000,
            max_retries=3,
            scroll_interval=2.0,
            scroll_max_amount=10
        )

    @staticmethod
    def llm_extraction():
        return CrawlerRunConfig(
            cache_mode="BYPASS",
            page_timeout=90000
        )

# Usage
config = CrawlConfigFactory.thorough_crawl()
```

### 4.5 Persistent Browser Contexts

**Storage States**

```python
# Save browser state (cookies, localStorage)
browser_config = BrowserConfig(
    storage_state="session.json"  # Save to file
)

# Load existing session
browser_config = BrowserConfig(
    storage_state="session.json"  # Load from file
)
```

**Session Management**

```python
import json
from crawl4ai import AsyncWebCrawler, BrowserConfig

async def login_and_crawl():
    # Step 1: Login to site
    async with AsyncWebCrawler() as crawler:
        await crawler.browser_context.new_page()
        await crawler.page.goto("https://example.com/login")
        # Fill login form
        await crawler.page.fill("#username", "user@example.com")
        await crawler.page.fill("#password", "password123")
        await crawler.page.click("#login-button")
        await crawler.page.wait_for_navigation()

        # Step 2: Save storage state
        state = await crawler.browser_context.get_storage_state()
        with open("session.json", "w") as f:
            json.dump(state, f)

    # Step 3: Use saved session for subsequent crawls
    browser_config = BrowserConfig(storage_state="session.json")
    async with AsyncWebCrawler(config=browser_config) as crawler:
        result = await crawler.arun("https://example.com/protected")
```

**Context Isolation**

```python
# Create multiple isolated contexts
browser_config = BrowserConfig()

async with AsyncWebCrawler(config=browser_config) as crawler:
    # Context 1: User 1
    context1 = await crawler.browser_context.new_context(
        user_agent="User-Agent-1",
        viewport={"width": 1920, "height": 1080}
    )

    # Context 2: User 2
    context2 = await crawler.browser_context.new_context(
        user_agent="User-Agent-2",
        viewport={"width": 375, "height": 812}
    )
```

## Hands-on Exercise: Configure Custom Crawler

### Exercise: Multi-Configuration Crawler with Proxy and Auth

**Objective**: Build a configurable crawler that supports proxies, custom headers, and session persistence

**Instructions**:

1. **Create Configuration Module**

```python
# config.py
import os
from dataclasses import dataclass
from crawl4ai import BrowserConfig, CrawlerRunConfig, LLMConfig

@dataclass
class CrawlerConfig:
    headless: bool = True
    proxy: str = None
    user_agent: str = None
    cache_mode: str = "BYPASS"
    page_timeout: int = 30000
    storage_state: str = None

    def to_browser_config(self):
        return BrowserConfig(
            headless=self.headless,
            proxy=self.proxy,
            user_agent=self.user_agent,
            storage_state=self.storage_state
        )

    def to_crawl_config(self):
        return CrawlerRunConfig(
            cache_mode=self.cache_mode,
            page_timeout=self.page_timeout
        )
```

2. **Add Custom Headers Support**

```python
class AdvancedCrawlerConfig(CrawlerConfig):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.headers = {}

    def add_header(self, key: str, value: str):
        self.headers[key] = value

    def to_crawl_config(self):
        config = super().to_crawl_config()
        config.extra_headers = self.headers
        return config
```

3. **Implement Session Manager**

```python
import json

class SessionManager:
    def __init__(self, session_file="session.json"):
        self.session_file = session_file

    def save(self, context):
        state = await context.get_storage_state()
        with open(self.session_file, "w") as f:
            json.dump(state, f)

    def load(self):
        if os.path.exists(self.session_file):
            return self.session_file
        return None
```

4. **Create Crawler Class**

```python
from crawl4ai import AsyncWebCrawler

class ConfigurableCrawler:
    def __init__(self, config: CrawlerConfig):
        self.config = config
        self.crawler = None

    async def __aenter__(self):
        self.crawler = AsyncWebCrawler(config=self.config.to_browser_config())
        await self.crawler.__aenter__()
        return self

    async def __aexit__(self, *args):
        await self.crawler.__aexit__(*args)

    async def crawl(self, url: str) -> dict:
        result = await self.crawler.arun(
            url=url,
            config=self.config.to_crawl_config()
        )
        return result
```

**Bonus Challenge**: Add rotating proxy support with session management.

**Deliverables**:

1. Complete configuration module
2. Working crawler with session persistence
3. Test output showing different configurations

## Quiz Questions

1. How do you configure a rotating proxy in BrowserConfig?
2. What's the difference between `cache_mode="BYPASS"` and `cache_mode="DISABLED"`?
3. How would you set up Ollama as a local LLM provider?
4. What is the purpose of `storage_state` in BrowserConfig?
5. How do you chain multiple configurations in a single crawl operation?

## Key Takeaways

- BrowserConfig handles browser-level settings (viewport, proxy, user agent)
- CrawlerRunConfig controls crawling behavior (caching, selectors, timeouts)
- LLMConfig supports multiple providers with fallback options
- Storage states enable session persistence across crawls
- Factory patterns simplify configuration reuse

## Next Module Preview

Module 5 explores data extraction strategies, covering CSS/XPath selectors and LLM-based extraction with multiple providers.