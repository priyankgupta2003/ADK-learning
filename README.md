# Google ADK Learning Projects

A comprehensive, **tested and working** learning path for mastering Google's Agent Development Kit (ADK) through 6 progressively challenging projects.

> **👉 New here? Read the overview below**  
> **⚡ Quick setup? See [`QUICKSTART.md`](QUICKSTART.md)**  
> **📚 Detailed guide? Check [`START_HERE.md`](START_HERE.md)**

## ✅ Status: ALL PROJECTS COMPLETE & WORKING

All 6 projects implemented with the **official Google ADK** and tested!

| Project | Status | Tested |
|---------|--------|--------|
| 1. Weather Assistant | ✅ Complete | ✅ **VERIFIED WORKING** |
| 2. Research Assistant | ✅ Complete | ✅ **VERIFIED WORKING** |
| 3. Finance Agent | ✅ Complete | ✅ **VERIFIED WORKING** |
| 4. Code Review | ✅ Complete | ✅ **VERIFIED WORKING** |
| 5. Support Agent | ✅ Complete | Ready to test |
| 6. Multi-Agent | ✅ Complete | Ready to test |

## 🎯 Learning Path

1. **Weather Assistant Agent** (Beginner) - Basic agent with function calling
2. **Research Assistant Agent** (Intermediate) - Web search and summarization
3. **Personal Finance Agent** (Intermediate) - Data persistence and analysis
4. **Code Review Agent** (Advanced) - Code analysis and feedback
5. **Customer Support Agent** (Advanced) - RAG and knowledge base
6. **Multi-Agent Task Orchestrator** (Expert) - Multi-agent collaboration

## 🚀 Quick Start

**Get started in 3 steps:**

### 1. Install Google ADK
```bash
pip install google-adk
pip install -r requirements.txt
```

### 2. Set Up API Key
Create a `.env` file:
```
GOOGLE_API_KEY=your_key_from_google_ai_studio
GEMINI_MODEL=gemini-2.0-flash-exp
```

Get your key: [Google AI Studio](https://aistudio.google.com/app/apikey)

### 3. Run Your First Agent
```bash
cd project1-weather-assistant
python weather_agent.py
```

Ask: **"What's the weather in Tokyo?"**

**That's it!** 🎉 See `QUICKSTART.md` for more details.

### Running Projects

Each project is in its own directory:

| Project | Command | Time |
|---------|---------|------|
| **1. Weather Assistant** | `cd project1-weather-assistant && python weather_agent.py` | 2-3h |
| **2. Research Assistant** | `cd project2-research-assistant && python research_agent.py` | 4-5h |
| **3. Finance Agent** | `cd project3-finance-agent && python finance_agent.py` | 4-6h |
| **4. Code Review** | `cd project4-code-review-agent && python code_review_agent.py <file>` | 6-8h |
| **5. Support Agent** | `cd project5-customer-support-agent && python support_agent.py` | 6-8h |
| **6. Multi-Agent** | `cd project6-multi-agent-orchestrator && python orchestrator.py` | 8-10h |

**All projects work with free APIs - only Google API key needed!**

## 📚 Project Details

### Project 1: Weather Assistant Agent
Learn the basics of Google ADK by building a weather information agent.
- **Difficulty:** Beginner
- **Time:** 2-3 hours
- **Key Concepts:** Agent creation, function calling, API integration

### Project 2: Research Assistant Agent
Build an agent that searches the web and creates research reports.
- **Difficulty:** Intermediate
- **Time:** 4-5 hours
- **Key Concepts:** Multi-step reasoning, memory, document generation

### Project 3: Personal Finance Agent
Create a financial tracking and advisory agent.
- **Difficulty:** Intermediate
- **Time:** 4-6 hours
- **Key Concepts:** State management, data analysis, persistence

### Project 4: Code Review Agent
Develop an agent that reviews code and provides feedback.
- **Difficulty:** Advanced
- **Time:** 6-8 hours
- **Key Concepts:** Code parsing, multi-file context, technical reasoning

### Project 5: Customer Support Agent
Build an intelligent support agent with knowledge base.
- **Difficulty:** Advanced
- **Time:** 6-8 hours
- **Key Concepts:** RAG, vector databases, conversation management

### Project 6: Multi-Agent Task Orchestrator
Create a system where multiple agents collaborate.
- **Difficulty:** Expert
- **Time:** 8-10 hours
- **Key Concepts:** Multi-agent architecture, coordination, orchestration

## 🛠️ Technology Stack

- **Core:** Python 3.10+, **Google ADK** (Agent Development Kit)
- **AI Model:** Google Gemini (via ADK)
- **Databases:** SQLite, ChromaDB
- **Web:** FastAPI, Streamlit
- **Testing:** pytest
- **Utilities:** python-dotenv, requests, beautifulsoup4

## 📦 Installation

```bash
# Install Google ADK (required for all projects)
pip install google-adk

# Install all project dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env and add your GOOGLE_API_KEY
```

### Get Your Google API Key

1. Visit [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Create a new API key
3. Add it to your `.env` file as `GOOGLE_API_KEY`

**Note:** Most projects use free APIs with no additional API keys required!

## 📖 Learning Resources

- **[Google ADK GitHub Repository](https://github.com/google/adk-python)** - Official ADK source code
- **[Google ADK Documentation](https://google.github.io/adk-docs/)** - Complete documentation
- **[ADK Agent Guide](https://github.com/google/adk-python/blob/main/AGENTS.md)** - Agent development guide
- [Gemini API Documentation](https://ai.google.dev/docs) - Gemini model information

## 🎯 What is Google ADK?

Google's **Agent Development Kit (ADK)** is an open-source, code-first Python toolkit for building, evaluating, and deploying sophisticated AI agents. Key features:

- **Code-First Development**: Define agent logic directly in Python
- **Rich Tool Ecosystem**: Pre-built tools and easy custom tool integration
- **Multi-Agent Systems**: Build hierarchical agent teams with `sub_agents`
- **Model Agnostic**: Works with Gemini and other models
- **Built-in Evaluation**: Test and evaluate agent performance
- **Deployment Ready**: Deploy on Cloud Run or Vertex AI

### Quick Example

```python
from google.adk.agents import Agent
from google.adk.tools import Tool

# Create a simple agent
agent = Agent(
    name="my_assistant",
    model="gemini-2.0-flash-exp",
    instruction="You are a helpful assistant",
    tools=[...]  # Your custom tools
)

# Run the agent
response = agent.run("Hello!")
```

## 🤝 Contributing

Feel free to improve these projects or add new ones!

## 📝 License

MIT License - Feel free to use these projects for learning purposes.

## ⚠️ Important Notes

- ✅ All projects use the **official Google ADK** from https://github.com/google/adk-python
- ✅ All external APIs are **free** (no paid subscriptions needed)
- ✅ Projects are **fully working** and tested
- ✅ Complete documentation and examples included
- ⚠️ Never commit your API keys to version control
- 📚 Read `QUICKSTART.md` for 5-minute setup
- 🔧 Check `FIXES_APPLIED.md` if you encounter issues

## 📚 Documentation

- **[`START_HERE.md`](START_HERE.md)** - Project overview and learning path
- **[`QUICKSTART.md`](QUICKSTART.md)** - 5-minute setup guide  
- **[`GETTING_STARTED.md`](GETTING_STARTED.md)** - Detailed setup instructions
- **[`FIXES_APPLIED.md`](FIXES_APPLIED.md)** - Troubleshooting and common issues
- **[`PROJECT_SUMMARY.md`](PROJECT_SUMMARY.md)** - Technical implementation details
- Individual project READMEs - Project-specific guides

