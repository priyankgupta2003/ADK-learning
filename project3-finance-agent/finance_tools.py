"""Financial analysis tools for Personal Finance Agent."""

from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
from database import DatabaseManager, TransactionType
from config import CURRENCY_SYMBOL
import calendar


def add_transaction(
    amount: float,
    category: str,
    description: str,
    transaction_type: str,
    date: Optional[str] = None
) -> str:
    """Add a new transaction (income or expense).
    
    Args:
        amount: Transaction amount (positive number)
        category: Category of the transaction  
        description: Description of the transaction
        transaction_type: "income" or "expense"
        date: Optional date in YYYY-MM-DD format
    """
    try:
        db = DatabaseManager()
        
        # Convert string to enum
        trans_type = TransactionType.INCOME if transaction_type.lower() == "income" else TransactionType.EXPENSE
        
        # Parse date if provided
        trans_date = datetime.strptime(date, "%Y-%m-%d") if date else None
        
        transaction = db.add_transaction(
            amount=float(amount),
            category=category,
            description=description,
            transaction_type=trans_type,
            date=trans_date
        )
        
        db.close()
        
        return f"Successfully added {transaction_type}: {CURRENCY_SYMBOL}{amount:.2f} for {category} - {description}"
    
    except Exception as e:
        return f"Error adding transaction: {str(e)}"


def get_spending_summary(period: str = "month") -> str:
    """Get spending summary for a period showing income, expenses, and spending by category.
    
    Args:
        period: "week", "month", or "year"
    """
    try:
        db = DatabaseManager()
        
        # Calculate date range
        end_date = datetime.now()
        if period == "week":
            start_date = end_date - timedelta(days=7)
        elif period == "year":
            start_date = end_date - timedelta(days=365)
        else:  # month
            start_date = end_date - timedelta(days=30)
        
        # Get data
        total_income = db.get_total_income(start_date, end_date)
        total_expenses = db.get_total_expenses(start_date, end_date)
        spending_by_category = db.get_spending_by_category(start_date, end_date)
        
        db.close()
        
        # Format as readable string
        summary = f"Spending Summary ({period}):\n\n"
        summary += f"Total Income: {CURRENCY_SYMBOL}{total_income:.2f}\n"
        summary += f"Total Expenses: {CURRENCY_SYMBOL}{total_expenses:.2f}\n"
        summary += f"Net Savings: {CURRENCY_SYMBOL}{(total_income - total_expenses):.2f}\n\n"
        
        if spending_by_category:
            summary += "Spending by Category:\n"
            for category, amount in sorted(spending_by_category.items(), key=lambda x: x[1], reverse=True):
                percentage = (amount / total_expenses * 100) if total_expenses > 0 else 0
                summary += f"  - {category}: {CURRENCY_SYMBOL}{amount:.2f} ({percentage:.1f}%)\n"
        
        return summary
    
    except Exception as e:
        return f"Error getting spending summary: {str(e)}"


def manage_budget(
    action: str,
    category: Optional[str] = None,
    amount: Optional[float] = None
) -> str:
    """Create or view budgets.
    
    Args:
        action: "create" or "view"
        category: Budget category (required for create)
        amount: Budget amount (required for create)
    """
    try:
        db = DatabaseManager()
        
        if action == "create":
            if not category or not amount:
                return "Error: Category and amount required for creating budget"
            
            budget = db.create_budget(category, float(amount))
            db.close()
            
            return f"Created budget: {CURRENCY_SYMBOL}{amount:.2f}/month for {category}"
        
        else:  # view
            budgets = db.get_budgets()
            
            # Get current month spending
            now = datetime.now()
            month_start = datetime(now.year, now.month, 1)
            spending = db.get_spending_by_category(month_start, now)
            
            db.close()
            
            if not budgets:
                return "No budgets set yet. Create a budget to start tracking!"
            
            result = "Current Budgets:\n\n"
            for budget in budgets:
                spent = spending.get(budget.category, 0.0)
                remaining = budget.amount - spent
                percentage = (spent / budget.amount * 100) if budget.amount > 0 else 0
                
                result += f"{budget.category}:\n"
                result += f"  Budget: {CURRENCY_SYMBOL}{budget.amount:.2f}\n"
                result += f"  Spent: {CURRENCY_SYMBOL}{spent:.2f} ({percentage:.1f}%)\n"
                result += f"  Remaining: {CURRENCY_SYMBOL}{remaining:.2f}\n\n"
            
            return result
    
    except Exception as e:
        return f"Error managing budget: {str(e)}"


def manage_goal(
    action: str,
    name: Optional[str] = None,
    target_amount: Optional[float] = None,
    current_amount: Optional[float] = None,
    goal_id: Optional[int] = None
) -> str:
    """Create, view, or update financial savings goals.
    
    Args:
        action: "create", "view", or "update"
        name: Goal name (required for create)
        target_amount: Target amount (required for create)
        current_amount: Current saved amount (for create/update)
        goal_id: Goal ID (required for update)
    """
    try:
        db = DatabaseManager()
        
        if action == "create":
            if not name or not target_amount:
                return "Error: Name and target_amount required for creating goal"
            
            goal = db.create_goal(name, float(target_amount), float(current_amount or 0))
            db.close()
            
            return f"Created goal: {name} - Save {CURRENCY_SYMBOL}{target_amount:.2f}"
        
        elif action == "update":
            if not goal_id or current_amount is None:
                return "Error: goal_id and current_amount required for updating"
            
            goal = db.update_goal_progress(int(goal_id), float(current_amount))
            db.close()
            
            if goal:
                achieved_msg = " - GOAL ACHIEVED!" if goal.status == "achieved" else ""
                return f"Updated goal: {goal.name} - {CURRENCY_SYMBOL}{goal.current_amount:.2f} of {CURRENCY_SYMBOL}{goal.target_amount:.2f}{achieved_msg}"
            else:
                return "Error: Goal not found"
        
        else:  # view
            goals = db.get_goals()
            db.close()
            
            if not goals:
                return "No financial goals set yet. Create a goal to start saving!"
            
            result = "Your Financial Goals:\n\n"
            for goal in goals:
                percentage = (goal.current_amount / goal.target_amount * 100) if goal.target_amount > 0 else 0
                remaining = goal.target_amount - goal.current_amount
                
                result += f"Goal #{goal.id}: {goal.name}\n"
                result += f"  Target: {CURRENCY_SYMBOL}{goal.target_amount:.2f}\n"
                result += f"  Current: {CURRENCY_SYMBOL}{goal.current_amount:.2f} ({percentage:.1f}%)\n"
                result += f"  Remaining: {CURRENCY_SYMBOL}{remaining:.2f}\n"
                result += f"  Status: {goal.status}\n\n"
            
            return result
    
    except Exception as e:
        return f"Error managing goal: {str(e)}"


def analyze_spending_patterns(months: int = 3) -> str:
    """Analyze spending patterns and trends over multiple months.
    
    Args:
        months: Number of months to analyze
    """
    try:
        db = DatabaseManager()
        
        end_date = datetime.now()
        start_date = end_date - timedelta(days=months * 30)
        
        transactions = db.get_transactions(start_date, end_date, transaction_type=TransactionType.EXPENSE)
        
        # Group by month and category
        monthly_spending = {}
        category_trends = {}
        
        for t in transactions:
            month_key = t.date.strftime("%Y-%m")
            
            if month_key not in monthly_spending:
                monthly_spending[month_key] = 0.0
            monthly_spending[month_key] += t.amount
            
            if t.category not in category_trends:
                category_trends[t.category] = {}
            if month_key not in category_trends[t.category]:
                category_trends[t.category][month_key] = 0.0
            category_trends[t.category][month_key] += t.amount
        
        db.close()
        
        # Calculate insights
        monthly_avg = sum(monthly_spending.values()) / len(monthly_spending) if monthly_spending else 0
        
        result = f"Spending Analysis (last {months} months):\n\n"
        result += f"Monthly Average: {CURRENCY_SYMBOL}{monthly_avg:.2f}\n\n"
        
        result += "Monthly Spending:\n"
        for month, amount in sorted(monthly_spending.items()):
            result += f"  {month}: {CURRENCY_SYMBOL}{amount:.2f}\n"
        
        result += "\nTop Spending Categories:\n"
        category_totals = {cat: sum(months_data.values()) for cat, months_data in category_trends.items()}
        for category, total in sorted(category_totals.items(), key=lambda x: x[1], reverse=True)[:5]:
            result += f"  {category}: {CURRENCY_SYMBOL}{total:.2f}\n"
        
        return result
    
    except Exception as e:
        return f"Error analyzing spending patterns: {str(e)}"

