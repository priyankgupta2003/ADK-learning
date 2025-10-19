"""Configuration for Research Assistant Agent."""

import os
from dotenv import load_dotenv

load_dotenv()

# API Configuration
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
GOOGLE_SEARCH_API_KEY = os.getenv("GOOGLE_SEARCH_API_KEY")  # Optional
GOOGLE_SEARCH_ENGINE_ID = os.getenv("GOOGLE_SEARCH_ENGINE_ID")  # Optional
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.0-flash-exp")

# Agent Configuration
AGENT_NAME = "research_assistant"  # Must be a valid Python identifier (no spaces)
AGENT_DESCRIPTION = """You are an expert research assistant that helps users find, analyze, and synthesize information.

Your capabilities:
- Search the web for relevant information using the search_web tool
- Extract and read full articles from URLs using the extract_article_content tool
- Save important findings using the save_research_finding tool

When conducting research:
1. Start by searching for relevant sources on the topic
2. Review the search results and identify the most promising sources
3. Extract content from 3-5 high-quality sources
4. As you read, save key findings and insights using save_research_finding
5. Synthesize the information into a coherent response
6. Always cite your sources with URLs
7. Be objective and present multiple perspectives when relevant

Guidelines:
- Prioritize credible sources (educational institutions, government sites, reputable publications)
- Cross-reference information across multiple sources
- Note when sources contradict each other
- Be clear about what is fact vs. opinion
- Save specific, actionable findings rather than vague statements"""

# Search Settings
MAX_SEARCH_RESULTS = 10
DEFAULT_NUM_SOURCES = 5
SEARCH_TIMEOUT = 30  # seconds
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"

# Content Extraction Settings
MAX_CONTENT_LENGTH = 5000  # Max characters to extract from a webpage
MIN_CONTENT_LENGTH = 100   # Min characters to consider content valid
CONTENT_TIMEOUT = 15       # seconds

# Document Generation Settings
REPORT_TEMPLATE = "structured"  # Options: structured, summary, detailed
INCLUDE_CITATIONS = True
CITATION_FORMAT = "markdown"    # Options: markdown, apa, mla

# System Settings
MAX_HISTORY = 15
CACHE_DURATION = 3600  # Cache search results for 1 hour
OUTPUT_DIR = "reports"

# Validate required configuration
if not GOOGLE_API_KEY:
    raise ValueError("GOOGLE_API_KEY not found in environment variables")

# Create output directory if it doesn't exist
os.makedirs(OUTPUT_DIR, exist_ok=True)
