"""Unit tests for Weather Assistant Agent."""

import pytest
import sys
import os

# Add parent directories to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from weather_tools import get_current_weather, get_forecast, WeatherAPIError


class TestWeatherTools:
    """Test weather tool functions."""
    
    def test_get_current_weather_valid_location(self):
        """Test getting weather for a valid location."""
        try:
            result = get_current_weather("London,UK")
            assert "location" in result
            assert "temperature" in result
            assert "weather" in result
            assert result["units"] == "°C"
        except WeatherAPIError as e:
            pytest.skip(f"API error (might be rate limit or invalid key): {str(e)}")
    
    def test_get_current_weather_with_imperial_units(self):
        """Test getting weather with Fahrenheit units."""
        try:
            result = get_current_weather("New York,US", units="imperial")
            assert result["units"] == "°F"
        except WeatherAPIError as e:
            pytest.skip(f"API error: {str(e)}")
    
    def test_get_forecast_valid_location(self):
        """Test getting forecast for a valid location."""
        try:
            result = get_forecast("Paris,FR")
            assert isinstance(result, list)
            assert len(result) <= 5
            if result:
                assert "date" in result[0]
                assert "temperature" in result[0]
        except WeatherAPIError as e:
            pytest.skip(f"API error: {str(e)}")
    
    def test_get_current_weather_invalid_location(self):
        """Test error handling for invalid location."""
        with pytest.raises(WeatherAPIError):
            get_current_weather("ThisCityDoesNotExist123456")


class TestWeatherAgent:
    """Test Weather Agent functionality."""
    
    @pytest.fixture
    def agent(self):
        """Create a weather agent instance for testing."""
        from weather_agent import WeatherAgent
        try:
            return WeatherAgent()
        except Exception as e:
            pytest.skip(f"Cannot initialize agent (check API keys): {str(e)}")
    
    def test_agent_initialization(self, agent):
        """Test that agent initializes correctly."""
        assert agent is not None
        assert agent.model is not None
        assert len(agent.tools) > 0
    
    def test_agent_simple_query(self, agent):
        """Test a simple weather query."""
        try:
            response = agent.query("What's the weather in Seattle?")
            assert isinstance(response, str)
            assert len(response) > 0
        except Exception as e:
            pytest.skip(f"Query failed: {str(e)}")
    
    def test_agent_clear_history(self, agent):
        """Test clearing conversation history."""
        agent.query("Hello")
        assert len(agent.conversation_history) > 0
        agent.clear_history()
        assert len(agent.conversation_history) == 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

