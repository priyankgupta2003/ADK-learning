"""Multi-Agent Task Orchestrator using Google ADK."""

import sys
import os
from google.genai import types

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from google.adk.agents import Agent
from google.adk import Runner
from google.adk.sessions import InMemorySessionService
from shared import setup_logging, print_agent_message, print_error, print_success, print_colored, Colors
from config import GOOGLE_API_KEY, GEMINI_MODEL, COORDINATOR_NAME, COORDINATOR_DESCRIPTION
from specialized_agents import (
    create_research_agent,
    create_analysis_agent,
    create_code_agent,
    create_report_agent
)


class MultiAgentOrchestrator:
    """Orchestrator for multi-agent task coordination using Google ADK."""
    
    def __init__(self):
        """Initialize the Multi-Agent Orchestrator."""
        self.logger = setup_logging("MultiAgentOrchestrator")
        
        # Create specialized agents
        print("Initializing specialized agents...")
        research_agent = create_research_agent()
        print("  [OK] Research Agent ready")
        
        analysis_agent = create_analysis_agent()
        print("  [OK] Analysis Agent ready")
        
        code_agent = create_code_agent()
        print("  [OK] Code Agent ready")
        
        report_agent = create_report_agent()
        print("  [OK] Report Agent ready")
        
        # Create coordinator agent with sub-agents
        print("\nInitializing coordinator...")
        coordinator = Agent(
            name=COORDINATOR_NAME,
            model=GEMINI_MODEL,
            instruction=COORDINATOR_DESCRIPTION,
            description="Coordinates a team of specialized agents to complete complex tasks",
            sub_agents=[
                research_agent,
                analysis_agent,
                code_agent,
                report_agent
            ]
        )
        print("  [OK] Coordinator ready")
        
        # Create session service and runner
        self.session_service = InMemorySessionService()
        self.runner = Runner(
            app_name="multi_agent_orchestrator_app",
            agent=coordinator,
            session_service=self.session_service
        )
        
        # Create initial session
        self.user_id = "default_user"
        self.session_id = "orchestrator_session"
        self.app_name = "multi_agent_orchestrator_app"
        self.session_service.create_session_sync(
            app_name=self.app_name,
            user_id=self.user_id,
            session_id=self.session_id
        )
        
        self.logger.info(f"{COORDINATOR_NAME} initialized with 4 specialized agents")
    
    def execute_task(self, task: str) -> str:
        """
        Execute a complex task using the multi-agent system.
        
        Args:
            task: Description of the task to complete
        
        Returns:
            Result from the coordinated agent execution
        """
        try:
            print_colored(f"\nTask: {task}", Colors.OKCYAN)
            print_colored("="*70, Colors.OKCYAN)
            
            message_content = types.Content(
                role="user",
                parts=[types.Part(text=task)]
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
                    return self.execute_task(task)
                else:
                    raise
        
        except Exception as e:
            self.logger.error(f"Error executing task: {str(e)}")
            return f"Error executing task: {str(e)}"


def main():
    """Main function to run the multi-agent orchestrator."""
    print_colored("\n" + "="*70, Colors.HEADER)
    print_colored("  Multi-Agent Task Orchestrator", Colors.HEADER)
    print_colored("  Powered by Google ADK", Colors.HEADER)
    print_colored("="*70 + "\n", Colors.HEADER)
    
    # Check for command line task
    if len(sys.argv) > 1:
        task = " ".join(sys.argv[1:])
        
        try:
            orchestrator = MultiAgentOrchestrator()
            print_success("\nAll agents initialized successfully!\n")
            
            result = orchestrator.execute_task(task)
            
            print_colored("\n" + "="*70, Colors.OKGREEN)
            print_colored("  RESULT", Colors.OKGREEN)
            print_colored("="*70, Colors.OKGREEN)
            print(result)
            print()
            
        except Exception as e:
            print_error(f"Failed to execute task: {str(e)}")
            return 1
    
    else:
        # Interactive mode
        print("This orchestrator coordinates multiple specialized agents:")
        print("  - Research Agent - Information gathering")
        print("  - Analysis Agent - Data analysis and insights")
        print("  - Code Agent - Software development")
        print("  - Report Agent - Documentation and reporting")
        print("\nGive me a complex task and I'll coordinate the team to complete it!")
        print("\nExamples:")
        print("  - Research AI trends and create a summary report")
        print("  - Analyze customer data and suggest improvements")
        print("  - Write a Python script to analyze log files")
        print("\nType 'quit' or 'exit' to stop.\n")
        
        try:
            orchestrator = MultiAgentOrchestrator()
            print_success("\nAll agents initialized successfully!\n")
            
            while True:
                try:
                    user_input = input("[Orchestrator] Task: ").strip()
                    
                    if not user_input:
                        continue
                    
                    if user_input.lower() in ['quit', 'exit', 'bye']:
                        print_success("Goodbye! Great working with the team!")
                        break
                    
                    result = orchestrator.execute_task(user_input)
                    print_agent_message("Coordinator", result)
                
                except KeyboardInterrupt:
                    print("\n")
                    print_success("Goodbye! Great working with the team!")
                    break
                except Exception as e:
                    print_error(f"Error: {str(e)}")
        
        except Exception as e:
            print_error(f"Failed to initialize orchestrator: {str(e)}")
            return 1
    
    return 0


if __name__ == "__main__":
    exit(main())
