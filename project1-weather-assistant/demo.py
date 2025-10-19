"""Interactive demo of the Weather Assistant Agent."""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from shared import print_colored, print_success, Colors
from weather_agent import WeatherAgent


def run_demo():
    """Run a demonstration of the weather assistant."""
    print_colored("\n" + "="*60, Colors.HEADER)
    print_colored("  Weather Assistant Agent - Demo", Colors.HEADER)
    print_colored("="*60 + "\n", Colors.HEADER)
    
    print("This demo shows the Weather Assistant Agent in action.")
    print("The agent can answer weather questions using real-time data.\n")
    
    # Initialize agent
    print("Initializing agent...")
    agent = WeatherAgent()
    print_success("Agent ready!\n")
    
    # Demo queries
    demo_queries = [
        "What's the weather like in Paris right now?",
        "Will it be sunny in Tokyo tomorrow?",
        "Give me a 5-day forecast for New York",
        "What's the temperature in London in Fahrenheit?"
    ]
    
    print_colored("Running demo queries...\n", Colors.OKBLUE)
    
    for i, query in enumerate(demo_queries, 1):
        print_colored(f"\n[Query {i}] {query}", Colors.OKCYAN)
        print("-" * 60)
        
        try:
            response = agent.query(query)
            print(response)
        except Exception as e:
            print(f"Error: {str(e)}")
        
        if i < len(demo_queries):
            input("\nPress Enter to continue...")
    
    print_colored("\n" + "="*60, Colors.HEADER)
    print_colored("Demo Complete!", Colors.OKGREEN)
    print_colored("="*60 + "\n", Colors.HEADER)
    
    print("You can now try your own queries!")
    print("Run: python weather_agent.py\n")


if __name__ == "__main__":
    try:
        run_demo()
    except KeyboardInterrupt:
        print("\n\nDemo interrupted by user.")
    except Exception as e:
        print(f"\nDemo error: {str(e)}")

