# Getting Started with Google ADK Learning Projects

This guide will help you set up your environment and start learning Google ADK through hands-on projects.

## Prerequisites

- Python 3.10 or higher
- Basic understanding of Python programming
- A Google account (for API access)

## Setup Instructions

### Step 1: Install Python

Make sure you have Python 3.10+ installed:

```bash
python --version
```

If not installed, download from [python.org](https://www.python.org/downloads/)

### Step 2: Clone or Download This Repository

```bash
cd "ADK learning"
```

### Step 3: Create a Virtual Environment (Recommended)

```bash
# Create virtual environment
python -m venv venv

# Activate it
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### Step 4: Install Google ADK

```bash
pip install google-adk
```

This is the core dependency for all projects. Learn more at: https://github.com/google/adk-python

### Step 5: Install All Dependencies

```bash
pip install -r requirements.txt
```

This installs all additional packages needed for the projects.

### Step 6: Get Your Google API Key

1. Go to [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy your API key

### Step 7: Configure Environment Variables

Create a `.env` file in the project root:

```bash
# Copy the example file
cp .env.example .env
```

Edit `.env` and add your API key:

```
GOOGLE_API_KEY=your_api_key_here
GEMINI_MODEL=gemini-2.0-flash-exp
```

### Step 8: Additional API Keys (Optional)

Good news! Most projects use completely free APIs:

#### Project 1 (Weather Assistant):
- ✅ Uses **Open-Meteo API** - 100% free, no API key needed!

#### Project 2 (Research Assistant):
- ✅ Uses **DuckDuckGo** - Free web search, no API key needed!
- Optional: Google Custom Search API for enhanced results

All projects work out of the box with just your Google API key!

## Running Your First Project

Let's start with Project 1 - Weather Assistant:

```bash
cd project1-weather-assistant
python weather_agent.py
```

You should see:
```
Weather Assistant Agent Starting...
Ask me about the weather in any location!
```

Try asking:
```
What's the weather in New York?
```

## Project Learning Path

Follow this order for best learning experience:

### 1. Project 1: Weather Assistant (2-3 hours)
**Learn:** Basic agent creation, function calling, API integration

```bash
cd project1-weather-assistant
python weather_agent.py
```

### 2. Project 2: Research Assistant (4-5 hours)
**Learn:** Multi-step reasoning, web search, document generation

```bash
cd project2-research-assistant
python research_agent.py
```

### 3. Project 3: Personal Finance Agent (4-6 hours)
**Learn:** Data persistence, state management, data analysis

```bash
cd project3-finance-agent
python finance_agent.py
```

### 4. Project 4: Code Review Agent (6-8 hours)
**Learn:** Code parsing, multi-file context, technical reasoning

```bash
cd project4-code-review-agent
python code_review_agent.py ../project1-weather-assistant/weather_agent.py
```

### 5. Project 5: Customer Support Agent (6-8 hours)
**Learn:** RAG, vector databases, conversation management

```bash
cd project5-customer-support-agent
python support_agent.py
```

### 6. Project 6: Multi-Agent Orchestrator (8-10 hours)
**Learn:** Multi-agent systems, coordination, orchestration

```bash
cd project6-multi-agent-orchestrator
python orchestrator.py "Research AI trends and create a summary"
```

## Understanding Google ADK

### Core Concepts

#### 1. Agents
Agents are AI entities that can use tools and make decisions:

```python
from google.adk.agents import Agent

agent = Agent(
    name="assistant",
    model="gemini-2.0-flash-exp",
    instruction="You are helpful",
    tools=[tool1, tool2]
)
```

#### 2. Tools
Tools give agents capabilities:

```python
from google.adk.tools import Tool

def my_function(param: str) -> dict:
    return {"result": f"Processed {param}"}

tool = Tool(
    name="my_tool",
    func=my_function,
    description="Does something useful",
    parameters={...}
)
```

#### 3. Multi-Agent Systems
Agents can coordinate with sub-agents:

```python
coordinator = Agent(
    name="coordinator",
    model="gemini-2.0-flash-exp",
    sub_agents=[agent1, agent2, agent3]
)
```

## Troubleshooting

### "Module 'google.adk' not found"
```bash
pip install google-adk
```

### "API key not found"
- Check that `.env` file exists in project root
- Verify `GOOGLE_API_KEY` is set in `.env`
- Try: `echo $env:GOOGLE_API_KEY` (Windows) or `echo $GOOGLE_API_KEY` (Mac/Linux)

### "Rate limit exceeded"
- Free tier has usage limits
- Wait a few minutes and try again
- Consider upgrading your API quota

### Import errors
```bash
# Make sure you're in the virtual environment
# Reinstall dependencies
pip install -r requirements.txt --upgrade
```

## Next Steps

1. ✅ Complete Project 1 to understand ADK basics
2. ✅ Work through projects 2-6 in order
3. 📚 Read the [Google ADK documentation](https://google.github.io/adk-docs/)
4. 🔧 Experiment with your own agent ideas
5. 🚀 Build a real application using ADK

## Getting Help

- **Google ADK GitHub**: https://github.com/google/adk-python
- **Documentation**: https://google.github.io/adk-docs/
- **Issues**: Check project README files for specific troubleshooting

## Resources

- [Google ADK Repository](https://github.com/google/adk-python)
- [Agent Development Guide](https://github.com/google/adk-python/blob/main/AGENTS.md)
- [Google AI Studio](https://aistudio.google.com/)

---

Happy learning! 🚀 Start with Project 1 and work your way through all 6 projects to master Google ADK!

