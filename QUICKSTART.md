# Quick Start Guide - Google ADK Learning Projects

Get started with Google ADK in under 5 minutes!

## Prerequisites

- Python 3.10 or higher
- Google account (for Gemini API key)

## Installation (3 Steps)

### 1. Install Google ADK

```bash
pip install google-adk
```

### 2. Install Project Dependencies

```bash
pip install -r requirements.txt
```

### 3. Set Up API Key

Create a `.env` file in the project root:

```
GOOGLE_API_KEY=your_google_api_key_here
GEMINI_MODEL=gemini-2.0-flash-exp
```

**Get your API key:** Visit [Google AI Studio](https://aistudio.google.com/app/apikey) and create a new key.

## Test Your First Agent (Project 1)

```bash
cd project1-weather-assistant
python weather_agent.py
```

Then ask: **"What's the weather in London?"**

You should get a response like:
```
The weather in London, United Kingdom is currently 12.5°C. 
It feels like 11.8°C due to the overcast conditions...
```

That's it! 🎉 Your first Google ADK agent is running!

## How Google ADK Works

### The Basics

```python
from google.adk.agents import Agent
from google.adk import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

# 1. Define your tools (plain Python functions)
def get_weather(location: str) -> str:
    """Get weather for a location."""
    return f"Weather in {location}: Sunny, 25°C"

# 2. Create an Agent
agent = Agent(
    name="weather_bot",  # Must be valid identifier
    model="gemini-2.0-flash-exp",
    tools=[get_weather]  # List of functions
)

# 3. Create a Runner (manages sessions)
session_service = InMemorySessionService()
runner = Runner(
    app_name="my_app",
    agent=agent,
    session_service=session_service
)

# 4. Create a session
session_service.create_session_sync(
    app_name="my_app",
    user_id="user123",
    session_id="session123"
)

# 5. Send a message
message = types.Content(
    role="user",
    parts=[types.Part(text="What's the weather in Paris?")]
)

# 6. Get response
for event in runner.run(
    user_id="user123",
    session_id="session123",
    new_message=message
):
    if hasattr(event, 'content') and event.content:
        for part in event.content.parts:
            if hasattr(part, 'text'):
                print(part.text)
```

## Key Concepts

### 1. Tools are Python Functions
```python
def my_tool(param: str) -> str:
    """Tool description (ADK reads this)."""
    return "result"
```

### 2. Agent Names are Identifiers
```python
# ❌ WRONG
name="My Agent"  # Has space

# ✅ CORRECT
name="my_agent"  # Valid identifier
```

### 3. Use Runner, Not Direct Agent Calls
```python
# ❌ WRONG
response = agent.run(message)  # Doesn't exist

# ✅ CORRECT
runner = Runner(agent=agent, ...)
for event in runner.run(...):
    # Process events
```

### 4. Create Sessions Explicitly
```python
session_service.create_session_sync(
    app_name="app",
    user_id="user",
    session_id="session"
)
```

## All Projects Use Free APIs!

- **Project 1:** Open-Meteo API (weather, no key needed)
- **Project 2:** DuckDuckGo (web search, no key needed)
- **Project 3:** SQLite (local database)
- **Project 4:** Python AST (built-in)
- **Project 5:** ChromaDB (local vector DB)
- **Project 6:** Multi-agent (no external API)

**Only Google API key required!**

## Project Learning Order

1. **Project 1** (2-3h) - Weather Assistant: Basic agents and tools
2. **Project 2** (4-5h) - Research Assistant: Web search and synthesis
3. **Project 3** (4-6h) - Finance Agent: Data persistence
4. **Project 4** (6-8h) - Code Review: Code analysis
5. **Project 5** (6-8h) - Support Agent: RAG and vector DB
6. **Project 6** (8-10h) - Multi-Agent: Orchestration

## Troubleshooting

### "Module google.adk not found"
```bash
pip install google-adk
```

### "API key not found"
Make sure `.env` file exists with `GOOGLE_API_KEY=...`

### "Agent name must be valid identifier"
Use underscores, not spaces: `my_agent` not `My Agent`

## Next Steps

1. ✅ Complete Project 1 
2. 📚 Read `GETTING_STARTED.md` for detailed info
3. 🚀 Try Projects 2-6 in order
4. 📖 Check `FIXES_APPLIED.md` for common issues

## Resources

- [Google ADK GitHub](https://github.com/google/adk-python)
- [ADK Documentation](https://google.github.io/adk-docs/)
- [Get API Key](https://aistudio.google.com/app/apikey)

---

**Ready to build AI agents? Start with Project 1!** 🚀

