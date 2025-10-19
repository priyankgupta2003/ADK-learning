# Project 2: Research Assistant Agent

An intermediate-level project that builds a research assistant capable of searching the web, analyzing content, and generating comprehensive reports.

## 🎯 Learning Objectives

- Implement multi-step reasoning and planning
- Integrate web scraping and search capabilities
- Manage complex agent memory and context
- Generate structured documents
- Handle multiple data sources

## 🌟 Features

- Web search integration (Google Custom Search)
- Article scraping and content extraction
- Multi-source research synthesis
- Structured report generation
- Citation management
- Summary and key points extraction
- Conversation memory for follow-up questions

## 📋 Prerequisites

- Completed Project 1 (Weather Assistant)
- Python 3.10+
- Google API key with Gemini access
- (Optional) BeautifulSoup4 for real web scraping: `pip install beautifulsoup4`

**Note:** Project works without BeautifulSoup using simulated search results for learning purposes!

## 🚀 Setup

1. Add to your `.env` file:
```
GOOGLE_API_KEY=your_google_api_key
```

2. Install dependencies (from project root):
```bash
pip install -r requirements.txt
```

3. (Optional) For real web scraping, install BeautifulSoup4:
```bash
pip install beautifulsoup4
```

**Note:** Project works out-of-the-box with simulated search results for learning!

## 🎮 Usage

### Interactive Mode
```bash
python research_agent.py
```

Then ask research questions like:
- "Research the latest developments in quantum computing"
- "What are the top programming languages in 2024?"
- "What are the benefits of AI agents?"
- "Compare different cloud platforms"

**📝 Note:** By default, the agent uses simulated search results for learning purposes. This allows you to focus on learning Google ADK concepts without dealing with web scraping complexity.

**For real web search:** Install BeautifulSoup4 with `pip install beautifulsoup4`

### Programmatic Mode
```python
from research_agent import ResearchAgent

agent = ResearchAgent()
report = agent.research("What is the impact of AI on job markets?")
print(report)
```

### Generate Report
```python
agent = ResearchAgent()
report = agent.generate_report(
    topic="Climate Change Solutions",
    num_sources=5,
    output_file="climate_report.md"
)
```

## 📚 Key Concepts

### 1. Multi-Step Reasoning
The agent breaks down research tasks into steps:
- Formulate search queries
- Gather information
- Analyze and synthesize
- Generate structured output

### 2. Web Scraping
Extract relevant content from web pages:
```python
def scrape_article(url: str) -> Dict:
    # Extract title, content, author, date
    pass
```

### 3. Context Management
Maintain research context across multiple queries:
- Source tracking
- Citation management
- Related information linking

### 4. Document Generation
Create structured research reports:
- Executive summary
- Main findings
- Detailed analysis
- Citations and references

## 🔧 Project Structure

```
project2-research-assistant/
├── README.md                    # This file
├── research_agent.py            # Main agent implementation
├── search_tools.py              # Web search and scraping tools
├── document_generator.py        # Report generation utilities
├── config.py                    # Configuration settings
├── demo.py                      # Interactive demo
├── examples/
│   ├── sample_report.md         # Example output
│   └── research_queries.txt     # Example queries
└── tests/
    └── test_research_agent.py   # Unit tests
```

## 🧪 Testing

Run the tests:
```bash
cd project2-research-assistant
pytest tests/
```

## 📖 Learning Path

1. **Study search integration:** Examine how the agent formulates queries
2. **Understand scraping:** Learn web content extraction techniques
3. **Analyze reasoning:** See how multi-step plans are executed
4. **Experiment with reports:** Generate different types of research documents
5. **Extend capabilities:** Add new sources or output formats

## 💡 Extension Ideas

- Add scholarly article search (Google Scholar, arXiv)
- Implement PDF document analysis
- Add image and video content extraction
- Create comparative analysis features
- Add fact-checking capabilities
- Integrate with note-taking systems
- Add multi-language support

## 🐛 Troubleshooting

**Search API Issues:**
- Without Custom Search API, falls back to web scraping
- Web scraping may be slower and less reliable
- Some sites may block automated requests

**Rate Limits:**
- Free tier Custom Search: 100 queries/day
- Implement caching to reduce API calls
- Add delays between requests

**Content Extraction:**
- Some websites have dynamic content (requires Selenium)
- Paywalled content cannot be accessed
- Respect robots.txt and terms of service

## 📝 Notes

- Always cite sources properly
- Respect copyright and fair use
- Be aware of information accuracy and bias
- Verify critical information from multiple sources

## ⏭️ Next Steps

After mastering this project, move on to:
- **Project 3:** Personal Finance Agent (adds data persistence and analysis)

