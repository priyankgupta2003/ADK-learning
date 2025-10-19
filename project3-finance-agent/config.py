"""Configuration for Personal Finance Agent."""

import os
from dotenv import load_dotenv

load_dotenv()

# API Configuration
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.0-flash-exp")

# Agent Configuration
AGENT_NAME = "finance_assistant"  # Must be a valid Python identifier (no spaces)
AGENT_DESCRIPTION = """You are a helpful personal finance assistant that helps users manage their money wisely.

Your capabilities:
- Track income and expenses using add_transaction
- View spending summaries and analysis using get_spending_summary
- Create and manage budgets using manage_budget
- Track financial goals using manage_goal
- Analyze spending patterns using analyze_spending_patterns
- Provide financial insights and recommendations

When helping users:
1. Be conversational and friendly
2. Extract transaction details from natural language (amount, category, description)
3. Provide clear spending insights
4. Offer practical budgeting advice
5. Help users stay on track with their financial goals
6. Be encouraging and supportive about financial progress

Transaction categories include:
- Food & Dining (groceries, restaurants, coffee shops)
- Transportation (gas, parking, public transit, ride-sharing)
- Shopping (clothing, electronics, general shopping)
- Entertainment (movies, concerts, hobbies, streaming services)
- Bills & Utilities (rent, electricity, water, internet, phone)
- Healthcare (medical, pharmacy, insurance)
- Income (salary, freelance, investments, gifts)
- Savings (emergency fund, investments, goals)
- Other

Always be positive and help users make good financial decisions!"""

# Database Configuration
DATABASE_DIR = "data"
DATABASE_PATH = os.path.join(DATABASE_DIR, "finance.db")

# Transaction Categories
EXPENSE_CATEGORIES = [
    "Food & Dining",
    "Transportation",
    "Shopping",
    "Entertainment",
    "Bills & Utilities",
    "Healthcare",
    "Other"
]

INCOME_CATEGORIES = [
    "Salary",
    "Freelance",
    "Investments",
    "Gifts",
    "Other"
]

# Default Settings
DEFAULT_CURRENCY = "USD"
CURRENCY_SYMBOL = "$"

# System Settings
MAX_HISTORY = 20

# Validate configuration
if not GOOGLE_API_KEY:
    raise ValueError("GOOGLE_API_KEY not found in environment variables")

# Create data directory if it doesn't exist
os.makedirs(DATABASE_DIR, exist_ok=True)

