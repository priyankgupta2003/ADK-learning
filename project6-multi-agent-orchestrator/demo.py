"""Interactive demo of the Multi-Agent Orchestrator."""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from shared import print_colored, print_success, Colors
from orchestrator import MultiAgentOrchestrator


def run_demo():
    """Run a demonstration of the multi-agent orchestrator."""
    print_colored("\n" + "="*70, Colors.HEADER)
    print_colored("  Multi-Agent Orchestrator - Demo", Colors.HEADER)
    print_colored("="*70 + "\n", Colors.HEADER)
    
    print("This demo shows multiple specialized agents working together.")
    print("The coordinator delegates tasks to the appropriate agents.\n")
    
    # Initialize orchestrator
    print("Initializing multi-agent system...")
    orchestrator = MultiAgentOrchestrator()
    print_success("\nAll agents ready!\n")
    
    # Demo tasks
    demo_tasks = [
        "Research the benefits of AI agents and create a summary",
        "Explain how to build a simple calculator in Python"
    ]
    
    print_colored("Running demo tasks...\n", Colors.OKBLUE)
    
    for i, task in enumerate(demo_tasks, 1):
        print_colored(f"\n[Task {i}] {task}", Colors.OKCYAN)
        print("-" * 70)
        
        try:
            result = orchestrator.execute_task(task)
            print(result)
        except Exception as e:
            print(f"Error: {str(e)}")
        
        if i < len(demo_tasks):
            input("\nPress Enter to continue...")
    
    print_colored("\n" + "="*70, Colors.HEADER)
    print_colored("Demo Complete!", Colors.OKGREEN)
    print_colored("="*70 + "\n", Colors.HEADER)
    
    print("The coordinator successfully delegated tasks to specialized agents!")
    print("Run: python orchestrator.py '<your task>'\n")


if __name__ == "__main__":
    try:
        run_demo()
    except KeyboardInterrupt:
        print("\n\nDemo interrupted by user.")
    except Exception as e:
        print(f"\nDemo error: {str(e)}")

