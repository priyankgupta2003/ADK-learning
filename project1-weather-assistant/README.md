# Project 1: Weather Assistant Agent

A beginner-friendly introduction to **Google ADK (Agent Development Kit)** by building a weather information agent.

## 🎯 Learning Objectives

- Set up and configure Google ADK
- Create your first AI agent using ADK
- Implement custom tools for function calling
- Integrate external APIs with ADK agents
- Handle user queries naturally with ADK's orchestration

## 🌟 Features

- Get current weather for any location
- Fetch 5-day weather forecast
- Get weather alerts and warnings
- Answer natural language weather queries
- Temperature unit conversion (Celsius/Fahrenheit)

## 📋 Prerequisites

- Python 3.10+
- Google API key with Gemini access
- Google ADK installed (`pip install google-adk`)
- **No weather API key needed!** (Uses free Open-Meteo API)

## 🚀 Setup

1. Install Google ADK:
```bash
pip install google-adk
```

2. Add to your `.env` file:
```
GOOGLE_API_KEY=your_google_api_key
GEMINI_MODEL=gemini-2.0-flash-exp
```

**Note:** This project uses [Open-Meteo API](https://open-meteo.com/) which is completely free and requires no API key! 🎉

4. Install other dependencies (from project root):
```bash
pip install -r requirements.txt
```

## 🎮 Usage

### Interactive Mode
```bash
python weather_agent.py
```

Then ask questions like:
- "What's the weather in New York?"
- "Will it rain in London tomorrow?"
- "Give me a 5-day forecast for Tokyo"
- "What's the temperature in Paris in Fahrenheit?"

### Programmatic Mode
```python
from weather_agent import WeatherAgent

agent = WeatherAgent()
response = agent.query("What's the weather in San Francisco?")
print(response)
```

## 📚 Key Concepts

### 1. ADK Agent Architecture
The agent is built using Google ADK's `Agent` class:
```python
from google.adk.agents import Agent
from google.adk.tools import Tool

agent = Agent(
    name="Weather Assistant",
    model="gemini-2.0-flash-exp",
    instruction="You are a helpful weather assistant...",
    tools=[weather_tools]  # Custom tools
)
```

### 2. Custom Tools in ADK
Define tools that the agent can use:
```python
Tool(
    name="get_current_weather",
    func=get_current_weather_function,
    description="Get current weather for a location",
    parameters={...},
    required=[...]
)
```

### 3. Agent Orchestration
ADK automatically handles:
- Tool selection and execution
- Response generation
- Error handling
- Conversation flow

### 4. External API Integration
Integrate real-world APIs (like OpenWeather) as ADK tools.

## 🔧 Project Structure

```
project1-weather-assistant/
├── README.md                 # This file
├── weather_agent.py          # Main agent implementation using ADK
├── weather_tools.py          # Weather API integration functions
├── config.py                 # Configuration settings
├── demo.py                   # Interactive demo
└── tests/
    └── test_weather_agent.py # Unit tests
```

## 🧪 Testing

Run the tests:
```bash
cd project1-weather-assistant
pytest tests/
```

## 📖 Learning Path

1. **Understand ADK basics:** Read through `weather_agent.py` to see how ADK agents are created
2. **Examine tools:** Check `weather_tools.py` to understand custom tool creation
3. **Experiment:** Modify the agent's behavior and add new features
4. **Extend:** Add more weather data sources or features

## 💡 Extension Ideas

- Add air quality information tool
- Include UV index data tool
- Add sunrise/sunset times
- Create weather comparison between cities
- Add weather-based recommendations (umbrella, jacket, etc.)
- Implement tool confirmation (HITL - Human In The Loop)

## 🐛 Troubleshooting

**Import Error with google-adk:**
```bash
pip install google-adk
# Or for development version:
pip install git+https://github.com/google/adk-python.git@main
```

**API Key Issues:**
- Make sure your `.env` file is in the project root
- Verify GOOGLE_API_KEY is valid and active
- The weather API (Open-Meteo) requires no API key!

**Rate Limits:**
- Open-Meteo API: Free and no rate limits for reasonable use
- Google Gemini API: Check your quota at Google AI Studio

**Module Not Found:**
- Run from project root or adjust PYTHONPATH
- Ensure all dependencies are installed

## 📝 Notes

- This project uses the official **Google ADK** framework from https://github.com/google/adk-python
- ADK provides built-in agent orchestration, tool management, and evaluation capabilities
- The agent automatically decides when to use which tool based on user queries
- **Weather API is 100% free** with no API key required (Open-Meteo)

## 🔗 Resources

- [Google ADK GitHub](https://github.com/google/adk-python)
- [Google ADK Documentation](https://google.github.io/adk-docs/)
- [Open-Meteo API Docs](https://open-meteo.com/en/docs) - Free weather API

## ⏭️ Next Steps

After mastering this project, move on to:
- **Project 2:** Research Assistant Agent (adds web scraping and multi-step reasoning)
