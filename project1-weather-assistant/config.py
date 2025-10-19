"""Configuration for Weather Assistant Agent."""

import os
from dotenv import load_dotenv

load_dotenv()

# API Configuration
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.0-flash-exp")

# Weather API Settings
# Using Open-Meteo API - 100% FREE, no API key required!
# API: https://open-meteo.com/
DEFAULT_UNITS = "metric"  # metric (Celsius) or imperial (Fahrenheit)

# Agent Configuration
AGENT_NAME = "weather_assistant"  # Must be a valid Python identifier (no spaces)
AGENT_DESCRIPTION = """You are a helpful weather assistant that provides accurate and timely weather information.
You have access to tools that can get current weather, forecasts, and weather alerts for any location in the world.

When a user asks about weather:
1. Use the appropriate tool to fetch the weather data
2. Present the information in a clear, conversational way
3. Provide relevant context (like if it's unusually hot/cold, if rain is expected, etc.)
4. Offer helpful suggestions when appropriate (like bringing an umbrella if rain is forecasted)

Always be friendly and helpful. Format temperatures with the appropriate unit (°C or °F)."""

# System Settings
MAX_HISTORY = 10  # Maximum conversation history to maintain
CACHE_DURATION = 300  # Cache weather data for 5 minutes

# Validate configuration
if not GOOGLE_API_KEY:
    raise ValueError("GOOGLE_API_KEY not found in environment variables")
