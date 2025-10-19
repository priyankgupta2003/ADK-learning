"""Customer Support Agent using Google ADK with RAG."""

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
from knowledge_base import search_knowledge_base, KnowledgeBase
from ticket_system import create_ticket, get_ticket, update_ticket


class SupportAgent:
    """A customer support assistant agent powered by Google ADK with RAG."""
    
    def __init__(self):
        """Initialize the Support Agent using ADK."""
        self.logger = setup_logging("SupportAgent")
        
        # Initialize knowledge base
        self.kb = KnowledgeBase()
        
        # Tools are plain Python functions
        support_tools = [
            search_knowledge_base,
            create_ticket,
            get_ticket,
            update_ticket
        ]
        
        # Create the ADK Agent
        agent = Agent(
            name=AGENT_NAME,
            model=GEMINI_MODEL,
            instruction=AGENT_DESCRIPTION,
            description="An intelligent customer support assistant with knowledge base access and ticket management.",
            tools=support_tools
        )
        
        # Create session service and runner
        self.session_service = InMemorySessionService()
        self.runner = Runner(
            app_name="support_assistant_app",
            agent=agent,
            session_service=self.session_service
        )
        
        # Create initial session
        self.user_id = "default_user"
        self.session_id = "support_session"
        self.app_name = "support_assistant_app"
        self.session_service.create_session_sync(
            app_name=self.app_name,
            user_id=self.user_id,
            session_id=self.session_id
        )
        
        self.logger.info(f"{AGENT_NAME} initialized successfully with Google ADK")
    
    def query(self, user_message: str) -> str:
        """
        Send a query to the support agent.
        
        Args:
            user_message: The customer's question or request
        
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
    """Main function to run the support agent."""
    print_success("Customer Support Agent Starting...")
    print("How can I help you today?")
    print("I can answer questions from our knowledge base and create support tickets.")
    print("\nType 'quit' or 'exit' to stop.\n")
    
    try:
        agent = SupportAgent()
        
        while True:
            try:
                user_input = input("\n[Support] You: ").strip()
                
                if not user_input:
                    continue
                
                if user_input.lower() in ['quit', 'exit', 'bye']:
                    print_success("Goodbye! Have a great day!")
                    break
                
                response = agent.query(user_input)
                print_agent_message(AGENT_NAME, response)
            
            except KeyboardInterrupt:
                print("\n")
                print_success("Goodbye! Have a great day!")
                break
            except Exception as e:
                print_error(f"Error: {str(e)}")
    
    except Exception as e:
        print_error(f"Failed to initialize agent: {str(e)}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())
