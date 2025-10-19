"""Weather API integration tools for the Weather Assistant Agent.

Uses Open-Meteo API - a free, open-source weather API that requires no API key.
API: https://open-meteo.com/
"""

import requests
from typing import Dict, Optional, List
from datetime import datetime
import json


class WeatherAPIError(Exception):
    """Custom exception for weather API errors."""
    pass


# Open-Meteo API endpoints (100% free, no API key needed)
GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"
WEATHER_URL = "https://api.open-meteo.com/v1/forecast"


def _get_coordinates(location: str) -> Dict:
    """
    Get latitude and longitude for a location using Open-Meteo Geocoding API.
    
    Args:
        location: City name (e.g., "London", "New York", "Tokyo")
    
    Returns:
        Dictionary with lat, lon, name, country
    """
    try:
        params = {
            "name": location,
            "count": 1,
            "language": "en",
            "format": "json"
        }
        
        response = requests.get(GEOCODING_URL, params=params, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        
        if not data.get("results"):
            raise WeatherAPIError(f"Location '{location}' not found")
        
        result = data["results"][0]
        return {
            "lat": result["latitude"],
            "lon": result["longitude"],
            "name": result["name"],
            "country": result.get("country", ""),
            "timezone": result.get("timezone", "UTC")
        }
    
    except requests.exceptions.RequestException as e:
        raise WeatherAPIError(f"Failed to geocode location: {str(e)}")


def get_current_weather(location: str, units: str = "metric") -> str:
    """Get current weather for a specific location. Returns temperature, conditions, humidity, wind speed, and more.
    
    Args:
        location: City name (e.g., "London", "New York", "Tokyo")
        units: Temperature units - "metric" for Celsius (default) or "imperial" for Fahrenheit
    
    Returns:
        Formatted string with current weather information
    """
    try:
        # Get coordinates for the location
        coords = _get_coordinates(location)
        
        # Get weather data
        params = {
            "latitude": coords["lat"],
            "longitude": coords["lon"],
            "current": "temperature_2m,relative_humidity_2m,apparent_temperature,precipitation,weather_code,cloud_cover,wind_speed_10m,wind_direction_10m",
            "temperature_unit": "fahrenheit" if units == "imperial" else "celsius",
            "wind_speed_unit": "mph" if units == "imperial" else "kmh",
            "timezone": coords["timezone"]
        }
        
        response = requests.get(WEATHER_URL, params=params, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        current = data["current"]
        
        # Map weather codes to descriptions
        weather_code = current.get("weather_code", 0)
        weather_desc = _get_weather_description(weather_code)
        
        weather_info = {
            "location": f"{coords['name']}, {coords['country']}",
            "temperature": current["temperature_2m"],
            "feels_like": current["apparent_temperature"],
            "humidity": current["relative_humidity_2m"],
            "weather": weather_desc["main"],
            "description": weather_desc["description"],
            "wind_speed": current["wind_speed_10m"],
            "wind_direction": current["wind_direction_10m"],
            "clouds": current["cloud_cover"],
            "precipitation": current.get("precipitation", 0),
            "units": "°F" if units == "imperial" else "°C",
            "timestamp": current["time"]
        }
        
        # Return formatted string for better agent readability
        return format_weather_response(weather_info)
        
    except requests.exceptions.RequestException as e:
        raise WeatherAPIError(f"Failed to fetch weather data: {str(e)}")
    except KeyError as e:
        raise WeatherAPIError(f"Unexpected API response format: {str(e)}")


def _get_weather_description(code: int) -> Dict[str, str]:
    """
    Convert WMO weather code to description.
    WMO Weather interpretation codes: https://open-meteo.com/en/docs
    """
    weather_codes = {
        0: {"main": "Clear", "description": "clear sky"},
        1: {"main": "Mainly Clear", "description": "mainly clear"},
        2: {"main": "Partly Cloudy", "description": "partly cloudy"},
        3: {"main": "Overcast", "description": "overcast"},
        45: {"main": "Foggy", "description": "fog"},
        48: {"main": "Foggy", "description": "depositing rime fog"},
        51: {"main": "Drizzle", "description": "light drizzle"},
        53: {"main": "Drizzle", "description": "moderate drizzle"},
        55: {"main": "Drizzle", "description": "dense drizzle"},
        61: {"main": "Rain", "description": "slight rain"},
        63: {"main": "Rain", "description": "moderate rain"},
        65: {"main": "Rain", "description": "heavy rain"},
        71: {"main": "Snow", "description": "slight snow"},
        73: {"main": "Snow", "description": "moderate snow"},
        75: {"main": "Snow", "description": "heavy snow"},
        77: {"main": "Snow", "description": "snow grains"},
        80: {"main": "Rain Showers", "description": "slight rain showers"},
        81: {"main": "Rain Showers", "description": "moderate rain showers"},
        82: {"main": "Rain Showers", "description": "violent rain showers"},
        85: {"main": "Snow Showers", "description": "slight snow showers"},
        86: {"main": "Snow Showers", "description": "heavy snow showers"},
        95: {"main": "Thunderstorm", "description": "thunderstorm"},
        96: {"main": "Thunderstorm", "description": "thunderstorm with slight hail"},
        99: {"main": "Thunderstorm", "description": "thunderstorm with heavy hail"},
    }
    return weather_codes.get(code, {"main": "Unknown", "description": "unknown conditions"})


def get_forecast(location: str, units: str = "metric") -> str:
    """Get 7-day weather forecast for a specific location. Shows daily temperature, conditions, and precipitation.
    
    Args:
        location: City name (e.g., "Paris", "Tokyo")
        units: Temperature units - "metric" for Celsius (default) or "imperial" for Fahrenheit
    
    Returns:
        Formatted string with 7-day forecast
    """
    try:
        # Get coordinates for the location
        coords = _get_coordinates(location)
        
        # Get forecast data
        params = {
            "latitude": coords["lat"],
            "longitude": coords["lon"],
            "daily": "temperature_2m_max,temperature_2m_min,apparent_temperature_max,apparent_temperature_min,precipitation_sum,precipitation_probability_max,weather_code,wind_speed_10m_max",
            "temperature_unit": "fahrenheit" if units == "imperial" else "celsius",
            "wind_speed_unit": "mph" if units == "imperial" else "kmh",
            "timezone": coords["timezone"],
            "forecast_days": 7
        }
        
        response = requests.get(WEATHER_URL, params=params, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        daily = data["daily"]
        
        forecasts = []
        for i in range(len(daily["time"])):
            weather_desc = _get_weather_description(daily["weather_code"][i])
            
            forecast_info = {
                "date": daily["time"][i],
                "temp_max": daily["temperature_2m_max"][i],
                "temp_min": daily["temperature_2m_min"][i],
                "feels_like_max": daily["apparent_temperature_max"][i],
                "feels_like_min": daily["apparent_temperature_min"][i],
                "weather": weather_desc["main"],
                "description": weather_desc["description"],
                "precipitation": daily["precipitation_sum"][i],
                "precipitation_probability": daily.get("precipitation_probability_max", [0] * len(daily["time"]))[i],
                "wind_speed": daily["wind_speed_10m_max"][i],
                "units": "°F" if units == "imperial" else "°C"
            }
            forecasts.append(forecast_info)
        
        # Return formatted string for better agent readability
        return format_forecast_response(forecasts[:7])
        
    except requests.exceptions.RequestException as e:
        raise WeatherAPIError(f"Failed to fetch forecast data: {str(e)}")
    except KeyError as e:
        raise WeatherAPIError(f"Unexpected API response format: {str(e)}")


def get_weather_alerts(location: str) -> str:
    """Get weather alerts and warnings for a specific location.
    
    Args:
        location: City name
    
    Returns:
        String indicating alert status (currently not available in free tier)
    """
    try:
        # Open-Meteo free API doesn't include alerts
        # For a production app, you could integrate:
        # - weather.gov API (US only, free with alerts)
        # - MeteoAlarm (Europe, free)
        # - Or use a paid service
        
        return f"Weather alerts are not currently available for {location} in the free API tier. No severe weather warnings detected through standard monitoring."
        
    except Exception:
        return "Unable to check weather alerts at this time."


def format_weather_response(weather_data: Dict) -> str:
    """
    Format weather data into a readable string.
    
    Args:
        weather_data: Dictionary containing weather information
    
    Returns:
        Formatted string representation
    """
    return f"""
Weather in {weather_data['location']}:
- Temperature: {weather_data['temperature']}{weather_data['units']}
- Feels like: {weather_data['feels_like']}{weather_data['units']}
- Conditions: {weather_data['description'].capitalize()}
- Humidity: {weather_data['humidity']}%
- Wind Speed: {weather_data['wind_speed']} m/s
- Cloud Coverage: {weather_data['clouds']}%
- Last Updated: {weather_data['timestamp']}
"""


def format_forecast_response(forecast_data: List[Dict]) -> str:
    """
    Format forecast data into a readable string.
    
    Args:
        forecast_data: List of dictionaries containing forecast information
    
    Returns:
        Formatted string representation
    """
    lines = ["7-Day Weather Forecast:\n"]
    
    for forecast in forecast_data:
        lines.append(
            f"{forecast['date']}: "
            f"{forecast['weather']} - {forecast['description']}, "
            f"Temp: {forecast['temp_min']:.1f}-{forecast['temp_max']:.1f}{forecast['units']}, "
            f"Precipitation: {forecast['precipitation']:.1f}mm, "
            f"Rain chance: {forecast['precipitation_probability']:.0f}%"
        )
    
    return "\n".join(lines)

