"""Code Review Agent using Google ADK."""

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
from code_analyzer import analyze_code, check_code_metrics, detect_issues


class CodeReviewAgent:
    """A code review assistant agent powered by Google ADK."""
    
    def __init__(self):
        """Initialize the Code Review Agent using ADK."""
        self.logger = setup_logging("CodeReviewAgent")
        
        # Tools are plain Python functions
        code_tools = [
            analyze_code,
            check_code_metrics,
            detect_issues
        ]
        
        # Create the ADK Agent
        agent = Agent(
            name=AGENT_NAME,
            model=GEMINI_MODEL,
            instruction=AGENT_DESCRIPTION,
            description="An expert code reviewer that analyzes code quality, detects issues, and suggests improvements.",
            tools=code_tools
        )
        
        # Create session service and runner
        self.session_service = InMemorySessionService()
        self.runner = Runner(
            app_name="code_review_app",
            agent=agent,
            session_service=self.session_service
        )
        
        # Create initial session
        self.user_id = "default_user"
        self.session_id = "code_review_session"
        self.app_name = "code_review_app"
        self.session_service.create_session_sync(
            app_name=self.app_name,
            user_id=self.user_id,
            session_id=self.session_id
        )
        
        self.logger.info(f"{AGENT_NAME} initialized successfully with Google ADK")
    
    def review_file(self, file_path: str) -> str:
        """
        Review a code file and provide comprehensive feedback.
        
        Args:
            file_path: Path to the code file
        
        Returns:
            Review feedback
        """
        prompt = f"""Please perform a comprehensive code review of the file: {file_path}

Follow these steps:
1. Use analyze_code to understand the structure
2. Use check_code_metrics to evaluate complexity
3. Use detect_issues to find problems
4. Provide a detailed review with:
   - Summary of the code
   - Issues found (grouped by severity)
   - Specific suggestions for improvement
   - Overall code quality assessment"""
        
        return self.query(prompt)
    
    def query(self, user_message: str) -> str:
        """
        Send a query to the code review agent.
        
        Args:
            user_message: The user's question or request
        
        Returns:
            The agent's response
        """
        try:
            message_content = types.Content(
                role="user",
                parts=[types.Part(text=user_message)]
            )
            
            try:
                response_text = ""
                for event in self.runner.run(
                    user_id=self.user_id,
                    session_id=self.session_id,
                    new_message=message_content
                ):
                    if hasattr(event, 'content') and event.content:
                        for part in event.content.parts:
                            if hasattr(part, 'text') and part.text:
                                response_text += part.text
                
                return response_text if response_text else "No response received."
            
            except ValueError as ve:
                if "Session not found" in str(ve):
                    self.session_service.create_session_sync(
                        app_name=self.app_name,
                        user_id=self.user_id,
                        session_id=self.session_id
                    )
                    return self.query(user_message)
                else:
                    raise
        
        except Exception as e:
            self.logger.error(f"Error processing query: {str(e)}")
            return f"I apologize, but I encountered an error: {str(e)}"


def main():
    """Main function to run the code review agent."""
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
        print_success(f"Code Review Agent - Reviewing: {file_path}")
        
        try:
            agent = CodeReviewAgent()
            review = agent.review_file(file_path)
            print_agent_message(AGENT_NAME, review)
        except Exception as e:
            print_error(f"Failed to review code: {str(e)}")
    else:
        print_error("Usage: python code_review_agent.py <file_path>")
        print("Example: python code_review_agent.py ../project1-weather-assistant/weather_agent.py")


if __name__ == "__main__":
    main()
