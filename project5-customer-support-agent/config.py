"""Configuration for Customer Support Agent."""

import os
from dotenv import load_dotenv

load_dotenv()

# API Configuration
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.0-flash-exp")

# Agent Configuration
AGENT_NAME = "support_assistant"  # Must be a valid Python identifier (no spaces)
AGENT_DESCRIPTION = """You are a helpful customer support assistant.

Your capabilities:
- Search the knowledge base for answers using search_knowledge_base
- Create support tickets using create_ticket
- Update ticket status using update_ticket
- View ticket information using get_ticket

When helping customers:
1. First search the knowledge base for relevant information
2. Provide clear, friendly, and helpful responses
3. If you cannot help, create a support ticket for human review
4. Always be polite and empathetic
5. Ask clarifying questions if needed

Knowledge base contains:
- Product documentation
- FAQs
- Troubleshooting guides
- Policy information"""

# Vector Database Settings
VECTOR_DB_DIR = "data/vectordb"
KNOWLEDGE_BASE_DIR = "data/knowledge"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
TOP_K_RESULTS = 3

# Ticket System Settings
TICKETS_DIR = "data/tickets"
TICKET_STATUSES = ["open", "in_progress", "resolved", "closed"]

# Validate configuration
if not GOOGLE_API_KEY:
    raise ValueError("GOOGLE_API_KEY not found in environment variables")

# Create directories
os.makedirs(VECTOR_DB_DIR, exist_ok=True)
os.makedirs(KNOWLEDGE_BASE_DIR, exist_ok=True)
os.makedirs(TICKETS_DIR, exist_ok=True)

