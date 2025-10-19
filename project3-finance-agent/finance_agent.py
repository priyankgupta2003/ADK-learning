"""Personal Finance Agent using Google ADK."""

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
from finance_tools import (
    add_transaction,
    get_spending_summary,
    manage_budget,
    manage_goal,
    analyze_spending_patterns
)


class FinanceAgent:
    """A personal finance assistant agent powered by Google ADK."""
    
    def __init__(self):
        """Initialize the Finance Agent using ADK."""
        self.logger = setup_logging("FinanceAgent")
        
        # Tools are plain Python functions - ADK reads docstrings automatically
        finance_tools = [
            add_transaction,
            get_spending_summary,
            manage_budget,
            manage_goal,
            analyze_spending_patterns
        ]
        
        # Create the ADK Agent
        agent = Agent(
            name=AGENT_NAME,
            model=GEMINI_MODEL,
            instruction=AGENT_DESCRIPTION,
            description="A helpful personal finance assistant that tracks expenses, manages budgets, and helps achieve financial goals.",
            tools=finance_tools
        )
        
        # Create session service and runner
        self.session_service = InMemorySessionService()
        self.runner = Runner(
            app_name="finance_assistant_app",
            agent=agent,
            session_service=self.session_service
        )
        
        # Create initial session
        self.user_id = "default_user"
        self.session_id = "finance_session"
        self.app_name = "finance_assistant_app"
        self.session_service.create_session_sync(
            app_name=self.app_name,
            user_id=self.user_id,
            session_id=self.session_id
        )
        
        self.logger.info(f"{AGENT_NAME} initialized successfully with Google ADK")
    
    def query(self, user_message: str) -> str:
        """
        Send a query to the finance agent and get a response.
        
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
                    self.logger.warning(f"Session {self.session_id} not found, creating new session")
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
    
    def reset(self):
        """Reset the agent's conversation state."""
        import uuid
        self.session_id = f"finance_session_{uuid.uuid4().hex[:8]}"
        self.session_service.create_session_sync(
            app_name=self.app_name,
            user_id=self.user_id,
            session_id=self.session_id
        )
        self.logger.info(f"Started new session: {self.session_id}")


def main():
    """Main function to run the finance assistant in interactive mode."""
    print_success("Personal Finance Agent Starting...")
    print("I can help you manage your finances!")
    print("Examples:")
    print("  - I spent $45 on groceries")
    print("  - Show me my spending this month")
    print("  - Create a $500 budget for food")
    print("  - I want to save $5000 for vacation")
    print("\nType 'quit' or 'exit' to stop.\n")
    
    try:
        agent = FinanceAgent()
        
        while True:
            try:
                user_input = input("\n[Finance] You: ").strip()
                
                if not user_input:
                    continue
                
                if user_input.lower() in ['quit', 'exit', 'bye']:
                    print_success("Goodbye! Keep up the good financial habits!")
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
                print_success("Goodbye! Keep up the good financial habits!")
                break
            except Exception as e:
                print_error(f"Error: {str(e)}")
    
    except Exception as e:
        print_error(f"Failed to initialize agent: {str(e)}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())
