"""Research Assistant Agent using Google ADK."""

import sys
import os
from google.genai import types

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from google.adk.agents import Agent
from google.adk import Runner
from google.adk.sessions import InMemorySessionService
from shared import setup_logging, print_agent_message, print_error, print_success
from config import GOOGLE_API_KEY, GEMINI_MODEL, AGENT_DESCRIPTION, AGENT_NAME, DEFAULT_NUM_SOURCES
from search_tools import search_web, extract_article_content, SearchError
from document_generator import DocumentGenerator


class ResearchAgent:
    """A research assistant agent powered by Google ADK."""
    
    def __init__(self):
        """Initialize the Research Agent using ADK."""
        self.logger = setup_logging("ResearchAgent")
        self.research_context = {
            "sources": [],
            "findings": [],
            "current_topic": None
        }
        
        # Create tool functions with proper wrappers
        def search_web_tool(query: str, num_results: int = 5) -> str:
            """Search the web for information. Returns a list of search results with titles, URLs, and snippets.
            
            Args:
                query: The search query to look up
                num_results: Number of search results to return (default: 5)
            """
            try:
                self.logger.info(f"Searching for: {query}")
                results = search_web(query, num_results)
                
                # Save sources to research context
                for result in results:
                    if result not in self.research_context["sources"]:
                        self.research_context["sources"].append(result)
                
                if results:
                    formatted = f"Found {len(results)} results:\n\n"
                    for i, result in enumerate(results, 1):
                        formatted += f"{i}. {result['title']}\n"
                        formatted += f"   URL: {result['link']}\n"
                        formatted += f"   Summary: {result['snippet']}\n\n"
                    return formatted
                else:
                    return "No search results found."
            except SearchError as e:
                return f"Search error: {str(e)}"
        
        def extract_article_tool(url: str) -> str:
            """Extract and read the full content from a web page URL. Returns the article title and content.
            
            Args:
                url: The URL of the web page to extract content from
            """
            try:
                self.logger.info(f"Extracting content from: {url}")
                content = extract_article_content(url)
                
                formatted = f"Article: {content['title']}\n"
                formatted += f"Source: {content['source']}\n"
                formatted += f"Content length: {content['length']} characters\n\n"
                formatted += f"Content:\n{content['content'][:3000]}"
                
                return formatted
            except SearchError as e:
                return f"Extraction error: {str(e)}"
        
        def save_finding_tool(finding: str, source_url: str = "") -> str:
            """Save an important finding or key insight from your research. Helps organize research for the final report.
            
            Args:
                finding: The finding or insight to save
                source_url: The URL where this finding was discovered (optional)
            """
            try:
                self.logger.info(f"Saving finding: {finding[:100]}...")
                self.research_context["findings"].append({
                    "finding": finding,
                    "source": source_url
                })
                return f"Finding saved successfully. Total findings: {len(self.research_context['findings'])}"
            except Exception as e:
                return f"Error saving finding: {str(e)}"
        
        # Create the ADK Agent with tool functions
        agent = Agent(
            name=AGENT_NAME,
            model=GEMINI_MODEL,
            instruction=AGENT_DESCRIPTION,
            description="An expert research assistant that searches the web, analyzes content, and generates comprehensive research reports.",
            tools=[search_web_tool, extract_article_tool, save_finding_tool]
        )
        
        # Create session service and runner
        self.session_service = InMemorySessionService()
        self.runner = Runner(
            app_name="research_assistant_app",
            agent=agent,
            session_service=self.session_service
        )
        
        # Create initial session
        self.user_id = "default_user"
        self.session_id = "research_session"
        self.app_name = "research_assistant_app"
        self.session_service.create_session_sync(
            app_name=self.app_name,
            user_id=self.user_id,
            session_id=self.session_id
        )
        
        self.doc_generator = DocumentGenerator()
        
        self.logger.info(f"{AGENT_NAME} initialized successfully with Google ADK")
    
    def query(self, user_message: str) -> str:
        """
        Send a query to the research agent and get a response.
        
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
    
    def generate_report(self, topic: str, num_sources: int = DEFAULT_NUM_SOURCES, output_file: str = None) -> str:
        """
        Generate a comprehensive research report on a topic.
        
        Args:
            topic: The research topic
            num_sources: Number of sources to consult
            output_file: Optional filename to save the report
        
        Returns:
            The generated report
        """
        self.logger.info(f"Generating report on: {topic}")
        
        # Clear previous research context
        self.research_context = {
            "sources": [],
            "findings": [],
            "current_topic": topic
        }
        
        # Conduct research
        research_prompt = f"""Please conduct comprehensive research on the topic: "{topic}"

Follow these steps:
1. Search for reliable sources on this topic (aim for {num_sources} sources)
2. Extract and read content from the most promising sources
3. Save key findings as you discover them using the save_finding_tool
4. After gathering information, provide a comprehensive summary

Focus on factual information from credible sources."""
        
        response = self.query(research_prompt)
        
        # Generate the report
        findings_list = [f["finding"] for f in self.research_context["findings"]]
        
        report = self.doc_generator.generate_report(
            topic=topic,
            summary=response,
            findings=findings_list,
            sources=self.research_context["sources"]
        )
        
        # Save if requested
        if output_file:
            filepath = self.doc_generator.save_report(report, output_file)
            self.logger.info(f"Report saved to: {filepath}")
        
        return report
    
    def reset(self):
        """Reset the agent and clear research context."""
        import uuid
        self.research_context = {
            "sources": [],
            "findings": [],
            "current_topic": None
        }
        self.session_id = f"research_session_{uuid.uuid4().hex[:8]}"
        self.session_service.create_session_sync(
            app_name=self.app_name,
            user_id=self.user_id,
            session_id=self.session_id
        )
        self.logger.info(f"Started new session: {self.session_id}")


def main():
    """Main function to run the research assistant in interactive mode."""
    print_success("Research Assistant Agent Starting...")
    print("Ask me to research any topic!")
    print("Examples:")
    print("  - Research the latest developments in quantum computing")
    print("  - What are the environmental impacts of electric vehicles?")
    print("  - Compare different approaches to renewable energy")
    print("\nType 'report <topic>' to generate a full research report")
    print("Type 'quit' or 'exit' to stop.\n")
    
    try:
        agent = ResearchAgent()
        
        while True:
            try:
                user_input = input("\n[Research] You: ").strip()
                
                if not user_input:
                    continue
                
                if user_input.lower() in ['quit', 'exit', 'bye']:
                    print_success("Goodbye! Happy researching!")
                    break
                
                if user_input.lower() in ['clear', 'reset']:
                    agent.reset()
                    print_success("Research context cleared!")
                    continue
                
                # Check if user wants a full report
                if user_input.lower().startswith('report '):
                    topic = user_input[7:].strip()
                    if topic:
                        print_agent_message(AGENT_NAME, f"Generating comprehensive report on: {topic}")
                        print("This may take a minute...\n")
                        
                        report = agent.generate_report(topic, output_file=f"research-{topic[:30]}")
                        print_agent_message(AGENT_NAME, report)
                    else:
                        print_error("Please specify a topic for the report")
                    continue
                
                # Regular query
                response = agent.query(user_input)
                print_agent_message(AGENT_NAME, response)
            
            except KeyboardInterrupt:
                print("\n")
                print_success("Goodbye! Happy researching!")
                break
            except Exception as e:
                print_error(f"Error: {str(e)}")
    
    except Exception as e:
        print_error(f"Failed to initialize agent: {str(e)}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())
