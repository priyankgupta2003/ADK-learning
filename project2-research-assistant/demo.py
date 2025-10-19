"""Interactive demo of the Research Assistant Agent."""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from shared import print_colored, print_success, Colors
from research_agent import ResearchAgent


def run_demo():
    """Run a demonstration of the research assistant."""
    print_colored("\n" + "="*70, Colors.HEADER)
    print_colored("  Research Assistant Agent - Demo", Colors.HEADER)
    print_colored("="*70 + "\n", Colors.HEADER)
    
    print("This demo shows the Research Assistant Agent in action.")
    print("The agent can search the web, extract content, and synthesize information.\n")
    
    # Initialize agent
    print("Initializing agent...")
    agent = ResearchAgent()
    print_success("Agent ready!\n")
    
    # Demo queries
    demo_queries = [
        "What is Google's Agent Development Kit (ADK)?",
        "Search for recent developments in AI agent technology"
    ]
    
    print_colored("Running demo queries...\n", Colors.OKBLUE)
    
    for i, query in enumerate(demo_queries, 1):
        print_colored(f"\n[Query {i}] {query}", Colors.OKCYAN)
        print("-" * 70)
        
        try:
            response = agent.query(query)
            print(response)
        except Exception as e:
            print(f"Error: {str(e)}")
        
        if i < len(demo_queries):
            input("\nPress Enter to continue...")
    
    # Demo report generation
    print_colored("\n\n[Report Generation Demo]", Colors.OKCYAN)
    print("-" * 70)
    print("Generating a research report (this may take a minute)...\n")
    
    try:
        report = agent.generate_report(
            topic="AI Agents in Software Development",
            num_sources=3,
            output_file="demo-ai-agents-report"
        )
        print(report[:500] + "...\n[Report truncated for demo]")
        print_success("Full report saved to reports/demo-ai-agents-report.md")
    except Exception as e:
        print(f"Report generation error: {str(e)}")
    
    print_colored("\n" + "="*70, Colors.HEADER)
    print_colored("Demo Complete!", Colors.OKGREEN)
    print_colored("="*70 + "\n", Colors.HEADER)
    
    print("You can now try your own research queries!")
    print("Run: python research_agent.py\n")


if __name__ == "__main__":
    try:
        run_demo()
    except KeyboardInterrupt:
        print("\n\nDemo interrupted by user.")
    except Exception as e:
        print(f"\nDemo error: {str(e)}")

