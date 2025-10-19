"""Weather Assistant Agent using Google ADK."""

import sys
import os
from google.genai import types

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from google.adk.agents import Agent
from google.adk import Runner
from google.adk.sessions import InMemorySessionService
from shared import setup_logging, print_agent_message, print_error, print_success
from config import GOOGLE_API_KEY, GEMINI_MODEL, AGENT_DESCRIPTION, AGENT_NAME
from weather_tools import (
    get_current_weather,
    get_forecast,
    get_weather_alerts
)


class WeatherAgent:
    """A weather assistant agent powered by Google ADK."""
    
    def __init__(self):
        """Initialize the Weather Agent using ADK Runner."""
        self.logger = setup_logging("WeatherAgent")
        
        # In Google ADK, tools are simply Python functions
        # The agent automatically detects function signatures and docstrings
        weather_tools = [
            get_current_weather,
            get_forecast,
            get_weather_alerts
        ]
        
        # Create the ADK Agent
        agent = Agent(
            name=AGENT_NAME,
            model=GEMINI_MODEL,
            instruction=AGENT_DESCRIPTION,
            description="A helpful weather assistant that provides accurate weather information for any location.",
            tools=weather_tools
        )
        
        # Create session service
        self.session_service = InMemorySessionService()
        
        # Create a Runner (proper high-level interface for ADK)
        self.runner = Runner(
            app_name="weather_assistant_app",
            agent=agent,
            session_service=self.session_service
        )
        
        # Session management - create initial session
        self.user_id = "default_user"
        self.session_id = "weather_session"
        self.app_name = "weather_assistant_app"
        self.session_service.create_session_sync(
            app_name=self.app_name,
            user_id=self.user_id,
            session_id=self.session_id
        )
        
        self.logger.info(f"{AGENT_NAME} initialized successfully with Google ADK")
    
    def query(self, user_message: str) -> str:
        """
        Send a query to the weather agent and get a response.
        
        Args:
            user_message: The user's question or request
        
        Returns:
            The agent's response
        """
        try:
            # Create a Content object from the message
            message_content = types.Content(
                role="user",
                parts=[types.Part(text=user_message)]
            )
            
            # Ensure session exists - create if not found
            try:
                # Use Runner.run() which returns a generator of events
                response_text = ""
                for event in self.runner.run(
                    user_id=self.user_id,
                    session_id=self.session_id,
                    new_message=message_content
                ):
                    # Extract text from response events
                    if hasattr(event, 'content') and event.content:
                        for part in event.content.parts:
                            if hasattr(part, 'text') and part.text:
                                response_text += part.text
                
                return response_text if response_text else "No response received."
            
            except ValueError as ve:
                if "Session not found" in str(ve):
                    # Session was deleted/expired, create a new one
                    self.logger.warning(f"Session {self.session_id} not found, creating new session")
                    self.session_service.create_session_sync(
                        app_name=self.app_name,
                        user_id=self.user_id,
                        session_id=self.session_id
                    )
                    # Retry with recreated session
                    return self.query(user_message)
                else:
                    raise
        
        except Exception as e:
            self.logger.error(f"Error processing query: {str(e)}")
            import traceback
            traceback.print_exc()
            return f"I apologize, but I encountered an error: {str(e)}"
    
    def reset(self):
        """Reset the agent's conversation state by starting a new session."""
        import uuid
        # Create a new session ID and create it
        self.session_id = f"weather_session_{uuid.uuid4().hex[:8]}"
        self.session_service.create_session_sync(
            app_name=self.app_name,
            user_id=self.user_id,
            session_id=self.session_id
        )
        self.logger.info(f"Started new session: {self.session_id}")


def main():
    """Main function to run the weather assistant in interactive mode."""
    print_success("Weather Assistant Agent Starting...")
    print("Ask me about the weather in any location!")
    print("Examples:")
    print("  - What's the weather in New York?")
    print("  - Give me a 5-day forecast for Tokyo")
    print("  - Will it rain in London tomorrow?")
    print("\nType 'quit' or 'exit' to stop.\n")
    
    try:
        agent = WeatherAgent()
        
        while True:
            try:
                user_input = input("\n🌤️  You: ").strip()
                
                if not user_input:
                    continue
                
                if user_input.lower() in ['quit', 'exit', 'bye']:
                    print_success("Goodbye! Stay weather-aware! ☀️")
                    break
                
                if user_input.lower() in ['clear', 'reset']:
                    agent.reset()
                    print_success("Conversation reset!")
                    continue
                
                # Get response from agent
                response = agent.query(user_input)
                print_agent_message(AGENT_NAME, response)
            
            except KeyboardInterrupt:
                print("\n")
                print_success("Goodbye! Stay weather-aware! ☀️")
                break
            except Exception as e:
                print_error(f"Error: {str(e)}")
    
    except Exception as e:
        print_error(f"Failed to initialize agent: {str(e)}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())
