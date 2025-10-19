# Project 3: Personal Finance Agent

An intermediate-level project that builds a personal finance assistant using Google ADK with data persistence and analysis capabilities.

## 🎯 Learning Objectives

- Implement data persistence with SQLite
- Manage agent state across sessions
- Perform data analysis within agents
- Handle privacy and security considerations
- Create visualization-ready outputs
- Use ADK for financial advisory tasks

## 🌟 Features

- Track income and expenses
- Categorize transactions automatically
- Budget creation and monitoring
- Spending pattern analysis
- Financial goal tracking
- Monthly/yearly financial summaries
- Budget recommendations based on spending habits

## 📋 Prerequisites

- Completed Project 1 and 2
- Python 3.10+
- Google API key with Gemini access
- Google ADK installed
- Basic understanding of databases (SQLite)

## 🚀 Setup

1. Ensure Google ADK is installed:
```bash
pip install google-adk
```

2. Add to your `.env` file:
```
GOOGLE_API_KEY=your_google_api_key
GEMINI_MODEL=gemini-2.0-flash-exp
```

3. Install dependencies (from project root):
```bash
pip install -r requirements.txt
```

4. Initialize the database:
```bash
python finance_agent.py init
```

## 🎮 Usage

### Interactive Mode
```bash
python finance_agent.py
```

Then interact with your finance agent:
- "Add an expense of $50 for groceries"
- "Show my spending this month"
- "Create a budget for next month"
- "What are my top spending categories?"
- "Set a savings goal of $5000 for a vacation"

### Programmatic Mode
```python
from finance_agent import FinanceAgent

agent = FinanceAgent()

# Add transaction
agent.query("I spent $45.50 on dinner at a restaurant")

# Get analysis
agent.query("Show me my spending breakdown for this month")

# Set goals
agent.query("I want to save $10,000 for a house down payment")
```

## 📚 Key Concepts

### 1. Stateful Agents with ADK
Combine ADK agents with persistent storage:
```python
agent = Agent(
    name="Finance Assistant",
    model="gemini-2.0-flash-exp",
    tools=[
        add_transaction_tool,
        get_spending_summary_tool,
        create_budget_tool,
        analyze_patterns_tool
    ]
)
```

### 2. Data Persistence
Use SQLite for storing financial data:
- Transactions table
- Budgets table
- Goals table
- Categories table

### 3. Financial Analysis
Tools that perform calculations and analysis:
- Spending by category
- Monthly trends
- Budget vs. actual comparison
- Goal progress tracking

### 4. Privacy & Security
- Local database storage
- No cloud sync of financial data
- Secure handling of sensitive information

## 🔧 Project Structure

```
project3-finance-agent/
├── README.md                 # This file
├── finance_agent.py          # Main agent implementation with ADK
├── database.py               # Database schema and operations
├── finance_tools.py          # Financial analysis tools
├── config.py                 # Configuration settings
├── demo.py                   # Interactive demo
├── data/
│   └── finance.db           # SQLite database (created on first run)
└── tests/
    └── test_finance_agent.py # Unit tests
```

## 🧪 Testing

Run the tests:
```bash
cd project3-finance-agent
pytest tests/
```

## 📖 Learning Path

1. **Study database integration:** See how ADK agents work with persistent storage
2. **Understand financial logic:** Review the analysis tools
3. **Explore state management:** Learn how conversation state is maintained
4. **Experiment with queries:** Try different financial questions
5. **Extend features:** Add new financial tools

## 💡 Extension Ideas

- Add recurring transaction support
- Implement bill reminders
- Add investment tracking
- Create financial reports (PDF/Excel)
- Add multi-currency support
- Implement data export/import
- Add receipt scanning (OCR integration)
- Create spending alerts
- Add financial advice using LLM analysis

## 🐛 Troubleshooting

**Database Issues:**
```bash
# Reset database
python finance_agent.py reset-db
```

**Import Errors:**
```bash
pip install --upgrade google-adk sqlalchemy pandas
```

**Permission Errors:**
- Ensure you have write permissions in the project directory
- The database file is created in `data/finance.db`

## 📝 Notes

- All financial data is stored locally in SQLite
- No data is sent to external services (except LLM queries)
- Regular backups of `data/finance.db` are recommended
- Transaction data is never included in LLM prompts, only summaries

## 🔒 Security Considerations

- Database is stored locally
- No credentials or account numbers stored
- Sensitive data is not sent to LLM
- Use encryption for production deployments

## 🔗 Resources

- [Google ADK GitHub](https://github.com/google/adk-python)
- [Google ADK Documentation](https://google.github.io/adk-docs/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)

## ⏭️ Next Steps

After mastering this project, move on to:
- **Project 4:** Code Review Agent (code parsing and analysis with ADK)

