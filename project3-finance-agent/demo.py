"""Interactive demo of the Personal Finance Agent."""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from shared import print_colored, print_success, Colors
from finance_agent import FinanceAgent


def run_demo():
    """Run a demonstration of the finance assistant."""
    print_colored("\n" + "="*70, Colors.HEADER)
    print_colored("  Personal Finance Agent - Demo", Colors.HEADER)
    print_colored("="*70 + "\n", Colors.HEADER)
    
    print("This demo shows the Personal Finance Agent in action.")
    print("The agent can track expenses, manage budgets, and help with financial goals.\n")
    
    # Initialize agent
    print("Initializing agent...")
    agent = FinanceAgent()
    print_success("Agent ready!\n")
    
    # Demo queries
    demo_queries = [
        "I spent $75 on groceries yesterday",
        "I received my salary of $3000",
        "Show me my spending this month",
        "I want to save $5000 for a vacation"
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
    
    print_colored("\n" + "="*70, Colors.HEADER)
    print_colored("Demo Complete!", Colors.OKGREEN)
    print_colored("="*70 + "\n", Colors.HEADER)
    
    print("You can now try your own financial queries!")
    print("Run: python finance_agent.py\n")


if __name__ == "__main__":
    try:
        run_demo()
    except KeyboardInterrupt:
        print("\n\nDemo interrupted by user.")
    except Exception as e:
        print(f"\nDemo error: {str(e)}")

