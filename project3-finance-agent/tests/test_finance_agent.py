"""Unit tests for Personal Finance Agent."""

import pytest
import sys
import os
from datetime import datetime

# Add parent directories to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from finance_tools import add_transaction, get_spending_summary, manage_budget, manage_goal
from database import DatabaseManager, TransactionType


class TestFinanceTools:
    """Test finance tool functions."""
    
    def test_add_expense(self):
        """Test adding an expense transaction."""
        result = add_transaction(
            amount=50.0,
            category="Food & Dining",
            description="Groceries",
            transaction_type="expense"
        )
        
        assert result["success"] == True
        assert "transaction_id" in result
    
    def test_add_income(self):
        """Test adding an income transaction."""
        result = add_transaction(
            amount=1000.0,
            category="Salary",
            description="Monthly salary",
            transaction_type="income"
        )
        
        assert result["success"] == True
    
    def test_get_spending_summary(self):
        """Test getting spending summary."""
        result = get_spending_summary(period="month")
        
        assert result["success"] == True
        assert "total_income" in result
        assert "total_expenses" in result
        assert "spending_by_category" in result
    
    def test_manage_budget_create(self):
        """Test creating a budget."""
        result = manage_budget(
            action="create",
            category="Food & Dining",
            amount=500.0
        )
        
        assert result["success"] == True
        assert "budget_id" in result
    
    def test_manage_budget_view(self):
        """Test viewing budgets."""
        result = manage_budget(action="view")
        
        assert result["success"] == True
        assert "budgets" in result
    
    def test_manage_goal_create(self):
        """Test creating a financial goal."""
        result = manage_goal(
            action="create",
            name="Emergency Fund",
            target_amount=5000.0
        )
        
        assert result["success"] == True
        assert "goal_id" in result
    
    def test_manage_goal_view(self):
        """Test viewing goals."""
        result = manage_goal(action="view")
        
        assert result["success"] == True
        assert "goals" in result


class TestDatabase:
    """Test database operations."""
    
    @pytest.fixture
    def db(self):
        """Create a test database instance."""
        # Use a test database
        test_db_path = "test_finance.db"
        db = DatabaseManager(test_db_path)
        yield db
        db.close()
        # Cleanup
        if os.path.exists(test_db_path):
            os.remove(test_db_path)
    
    def test_add_and_get_transaction(self, db):
        """Test adding and retrieving transactions."""
        transaction = db.add_transaction(
            amount=100.0,
            category="Shopping",
            description="Test purchase",
            transaction_type=TransactionType.EXPENSE
        )
        
        assert transaction.id is not None
        assert transaction.amount == 100.0
        
        transactions = db.get_transactions()
        assert len(transactions) > 0
    
    def test_spending_by_category(self, db):
        """Test getting spending by category."""
        db.add_transaction(50, "Food & Dining", "Test", TransactionType.EXPENSE)
        db.add_transaction(30, "Food & Dining", "Test", TransactionType.EXPENSE)
        
        spending = db.get_spending_by_category()
        assert "Food & Dining" in spending
        assert spending["Food & Dining"] == 80.0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

