# Module 2: Installation and Setup

**Type**: Technical Setup

## Learning Objectives

By the end of this module, students will be able to:

1. Install Crawl4AI using pip with all dependencies
2. Set up Playwright and verify browser automation works
3. Use `crawl4ai-doctor` to diagnose installation issues
4. Configure Docker for Crawl4AI deployment
5. Set up a proper development environment (VS Code/Jupyter)

## Topics Covered

### 2.1 Installing Crawl4AI via pip

**Basic Installation**

```bash
pip install crawl4ai
```

**Installation with All Dependencies**

```bash
pip install crawl4ai[all]
```

**Installation Components**:

| Component | Purpose | Installed With |
|-----------|---------|----------------|
| `crawl4ai` | Core package | `pip install crawl4ai` |
| `playwright` | Browser automation | Auto-installed |
| `unclecode-litellm` | Multi-provider LLM | `pip install crawl4ai[all]` |
| `chromium` | Default browser | `playwright install chromium` |

**Verifying Installation**

```python
import crawl4ai
print(crawl4ai.__version__)
```

### 2.2 Playwright Installation and Browser Dependencies

**Why Playwright?**

- Headless browser automation
- Cross-browser support (Chromium, Firefox, WebKit)
- Native async support
- Built-in waiting mechanisms

**Installing Playwright Browsers**

```bash
# Install Chromium only (recommended for most use cases)
playwright install chromium

# Install all browsers
playwright install

# Install with system dependencies
playwright install --with-deps chromium
```

**System Dependencies (Linux)**

```bash
# Ubuntu/Debian
sudo apt-get install -y \
    libglib2.0-0 \
    libnss3 \
    libnspr4 \
    libdbus-1-3 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libcups2 \
    libdrm2 \
    libxkbcommon0 \
    libxcomposite1 \
    libxdamage1 \
    libxfixes3 \
    libxrandr2 \
    libgbm1 \
    libasound2t64 \
    libpango-1.0-0 \
    libcairo2 \
    libatspi2.0-0 \
    libxshmfence1 \
    libwayland-client0
```

**Windows/Mac**: Generally handles dependencies automatically.

### 2.3 Verification with crawl4ai-doctor

**What is crawl4ai-doctor?**

A diagnostic tool that checks:

- Python version compatibility
- Required packages installation
- Playwright installation status
- Browser availability
- LLM provider configurations

**Running the Doctor**

```bash
crawl4ai-doctor
```

**Expected Output**

```
Crawl4AI Doctor v1.0.0
=======================
✓ Python version: 3.12+
✓ Playwright installed: 1.40.0
✓ Chromium browser: Installed
✓ Browser launch: OK
✗ OpenAI API key: Not configured (optional)
✗ Anthropic API key: Not configured (optional)

Run Status: PASS (with warnings)
```

**Troubleshooting Common Issues**

| Issue | Diagnosis | Solution |
|-------|-----------|----------|
| `playwright` not found | Package missing | `pip install playwright` |
| Browser not installed | Playwright incomplete | `playwright install chromium` |
| Browser launch fails | System deps missing | `playwright install --with-deps` |
| Import error | Python path issue | Check virtual environment |

### 2.4 Alternative Installation Methods

**Docker Installation**

```bash
# Pull pre-built image
docker pull uncornai/crawl4ai:latest

# Run with volume mounting
docker run -v $(pwd):/workspace -p 8000:8000 uncornai/crawl4ai:latest

# Run interactive
docker run -it -v $(pwd):/workspace uncornai/crawl4ai:latest bash
```

**Dockerfile Example**

```dockerfile
FROM uncornai/crawl4ai:latest

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["python", "main.py"]
```

**Installing from Source**

```bash
# Clone repository
git clone https://github.com/uncornai/crawl4ai.git
cd crawl4ai

# Install in development mode
pip install -e ".[dev]"

# Install browser dependencies
playwright install chromium
```

**conda/mamba Environment**

```bash
# Create environment from environment.yaml
conda env create -f environment.yaml
conda activate crawl4ai-py312
playwright install chromium
```

### 2.5 Setting Up Development Environment

**VS Code Configuration**

1. Install Python extension
2. Create `.vscode/settings.json`:

```json
{
    "python.defaultInterpreterPath": "crawl4ai-course/bin/python",
    "python.linting.enabled": true,
    "python.linting.pylintEnabled": true,
    "jupyter.kernel.specs": [
        {
            "kernelspec": {
                "display_name": "Crawl4AI Course",
                "language": "python",
                "name": "crawl4ai-course"
            }
        }
    ]
}
```

**Jupyter Notebook Setup**

```bash
# Install Jupyter in virtual environment
pip install jupyter ipykernel
ipython kernel install --name=crawl4ai-course --user

# Or use the environment directly
python -m ipykernel install --user --name=crawl4ai-course
```

**Recommended Extensions**

- Python (Microsoft)
- Jupyter (Microsoft)
- Pylance (Microsoft)
- GitLens (optional)

**Project Structure Template**

```
crawl4ai-course/
├── notebooks/          # Jupyter notebooks
├── src/               # Python source code
├── data/              # Crawled data output
├── config/            # Configuration files
├── .env               # API keys (gitignored)
├── .gitignore
├── requirements.txt
└── README.md
```

## Hands-on Exercise: Complete Installation

### Exercise: Set Up Production-Ready Environment

**Objective**: Create a fully functional Crawl4AI development environment

**Instructions**:

1. **Create Project with uv**

```bash
uv init crawl4ai-course
cd crawl4ai-course
```

2. **Install Crawl4AI with All Dependencies**

```bash
uv add crawl4ai[all] jupyter ipython
```

3. **Install Playwright Browser**

```bash
playwright install chromium
```

4. **Run Doctor and Fix Issues**

```bash
crawl4ai-doctor
```

5. **Create Jupyter Kernel**

```bash
python -m ipykernel install --user --name=crawl4ai-course
```

6. **Create Configuration File**

Create `config.py`:

```python
import os

# LLM Provider API Keys (use environment variables in production!)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")

# Crawling Configuration
HEADLESS = True
VIEWPORT_WIDTH = 1920
VIEWPORT_HEIGHT = 1080

# Output Configuration
OUTPUT_DIR = "data"
```

7. **Test Your Setup**

Create `test_setup.py`:

```python
import asyncio
from crawl4ai import AsyncWebCrawler

async def test_crawl():
    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun("https://example.com")
        print(f"Success: {result.success}")
        print(f"Markdown length: {len(result.markdown)}")
        return result.success

if __name__ == "__main__":
    success = asyncio.run(test_crawl())
    print(f"\nSetup {'✓' if success else '✗'} Working!")
```

Run it:

```bash
python test_setup.py
```

**Deliverables**:

1. Screenshot of `crawl4ai-doctor` output
2. Output from `test_setup.py`
3. Project directory structure listing

## Quiz Questions

1. What command installs Crawl4AI with all optional dependencies?
2. How do you verify that Chromium browser is installed for Playwright?
3. What does `crawl4ai-doctor` check for?
4. Name two differences between Docker installation and pip installation
5. Why is it recommended to use a virtual environment for Crawl4AI?

## Key Takeaways

- Crawl4AI requires Playwright for browser automation
- `crawl4ai-doctor` is your first troubleshooting tool
- Docker is available for containerized deployments
- Virtual environments are essential for dependency management

## Next Module Preview

Module 3 covers basic crawling fundamentals, including AsyncWebCrawler, markdown extraction, and configuration basics.