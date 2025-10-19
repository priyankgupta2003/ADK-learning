"""Specialized agent definitions for Multi-Agent Orchestrator."""

from google.adk.agents import Agent
from config import (
    GEMINI_MODEL,
    RESEARCH_AGENT_CONFIG,
    ANALYSIS_AGENT_CONFIG,
    CODE_AGENT_CONFIG,
    REPORT_AGENT_CONFIG
)


def create_research_agent() -> Agent:
    """Create the research specialist agent."""
    
    # Research tools - plain Python functions
    def web_search(query: str) -> str:
        """Search the web for information.
        
        Args:
            query: Search query
        """
        return f"Research results for: {query}\n- Found multiple sources on this topic\n- Key information gathered"
    
    return Agent(
        name=RESEARCH_AGENT_CONFIG["name"],
        model=GEMINI_MODEL,
        description=RESEARCH_AGENT_CONFIG["description"],
        instruction=RESEARCH_AGENT_CONFIG["description"],
        tools=[web_search]
    )


def create_analysis_agent() -> Agent:
    """Create the analysis specialist agent."""
    
    # Analysis tools
    def analyze_data(data: str, analysis_type: str = "general") -> str:
        """Analyze data and provide insights.
        
        Args:
            data: Data to analyze
            analysis_type: Type of analysis (general, statistical, trend)
        """
        return f"Analysis of data ({analysis_type}):\n- Key patterns identified\n- Insights generated\n- Recommendations provided"
    
    return Agent(
        name=ANALYSIS_AGENT_CONFIG["name"],
        model=GEMINI_MODEL,
        description=ANALYSIS_AGENT_CONFIG["description"],
        instruction=ANALYSIS_AGENT_CONFIG["description"],
        tools=[analyze_data]
    )


def create_code_agent() -> Agent:
    """Create the code specialist agent."""
    
    # Code tools
    def generate_code(task: str, language: str = "python") -> str:
        """Generate code for a given task.
        
        Args:
            task: Description of what the code should do
            language: Programming language
        """
        return f"Code for: {task}\nLanguage: {language}\n\n# Implementation would go here"
    
    return Agent(
        name=CODE_AGENT_CONFIG["name"],
        model=GEMINI_MODEL,
        description=CODE_AGENT_CONFIG["description"],
        instruction=CODE_AGENT_CONFIG["description"],
        tools=[generate_code]
    )


def create_report_agent() -> Agent:
    """Create the report specialist agent."""
    
    # Report tools
    def format_report(content: str, format_type: str = "markdown") -> str:
        """Format content into a structured report.
        
        Args:
            content: Content to format into a report
            format_type: Report format (markdown, html, text)
        """
        return f"# Report ({format_type})\n\n{content}\n\n---\nFormatted and structured for presentation"
    
    return Agent(
        name=REPORT_AGENT_CONFIG["name"],
        model=GEMINI_MODEL,
        description=REPORT_AGENT_CONFIG["description"],
        instruction=REPORT_AGENT_CONFIG["description"],
        tools=[format_report]
    )
