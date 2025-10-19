"""Shared utility functions for all ADK projects."""

import os
import logging
from typing import Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


def setup_logging(name: str, level: str = "INFO") -> logging.Logger:
    """Set up logging for a project."""
    logging.basicConfig(
        level=getattr(logging, level),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Suppress verbose logging from Google ADK and related libraries
    logging.getLogger('google_adk').setLevel(logging.ERROR)
    logging.getLogger('google_genai').setLevel(logging.ERROR)
    logging.getLogger('google.adk').setLevel(logging.ERROR)
    logging.getLogger('google.genai').setLevel(logging.ERROR)
    
    return logging.getLogger(name)


def get_api_key(key_name: str) -> Optional[str]:
    """Get API key from environment variables."""
    api_key = os.getenv(key_name)
    if not api_key:
        raise ValueError(f"{key_name} not found in environment variables. Please check your .env file.")
    return api_key


def validate_environment():
    """Validate that all required environment variables are set."""
    required_keys = ["GOOGLE_API_KEY"]
    missing_keys = [key for key in required_keys if not os.getenv(key)]
    
    if missing_keys:
        raise ValueError(
            f"Missing required environment variables: {', '.join(missing_keys)}\n"
            "Please copy .env.example to .env and fill in your API keys."
        )


class Colors:
    """ANSI color codes for terminal output."""
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def print_colored(message: str, color: str = Colors.OKBLUE):
    """Print colored message to terminal."""
    # Handle Windows encoding issues
    try:
        print(f"{color}{message}{Colors.ENDC}")
    except UnicodeEncodeError:
        # Fallback without color codes if terminal doesn't support them
        print(message)


def print_agent_message(agent_name: str, message: str):
    """Print a formatted agent message."""
    try:
        print(f"\n{Colors.OKGREEN}[{agent_name}]{Colors.ENDC} {message}")
    except UnicodeEncodeError:
        print(f"\n[{agent_name}] {message}")


def print_error(message: str):
    """Print an error message."""
    try:
        print(f"\n{Colors.FAIL}[ERROR]{Colors.ENDC} {message}")
    except UnicodeEncodeError:
        print(f"\n[ERROR] {message}")


def print_success(message: str):
    """Print a success message."""
    try:
        print(f"\n{Colors.OKGREEN}[SUCCESS]{Colors.ENDC} {message}")
    except UnicodeEncodeError:
        print(f"\n[SUCCESS] {message}")

