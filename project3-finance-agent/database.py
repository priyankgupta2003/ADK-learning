"""Database models and operations for Personal Finance Agent."""

from sqlalchemy import create_engine, Column, Integer, Float, String, DateTime, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import enum
from typing import List, Dict, Optional
from config import DATABASE_PATH

Base = declarative_base()


class TransactionType(enum.Enum):
    """Transaction type enum."""
    INCOME = "income"
    EXPENSE = "expense"


class Transaction(Base):
    """Transaction model."""
    __tablename__ = 'transactions'
    
    id = Column(Integer, primary_key=True)
    date = Column(DateTime, default=datetime.now)
    amount = Column(Float, nullable=False)
    category = Column(String(50), nullable=False)
    description = Column(String(200))
    transaction_type = Column(Enum(TransactionType), nullable=False)
    created_at = Column(DateTime, default=datetime.now)


class Budget(Base):
    """Budget model."""
    __tablename__ = 'budgets'
    
    id = Column(Integer, primary_key=True)
    category = Column(String(50), nullable=False)
    amount = Column(Float, nullable=False)
    period = Column(String(20), default="monthly")  # monthly, yearly
    start_date = Column(DateTime, default=datetime.now)
    end_date = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.now)


class Goal(Base):
    """Financial goal model."""
    __tablename__ = 'goals'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    target_amount = Column(Float, nullable=False)
    current_amount = Column(Float, default=0.0)
    target_date = Column(DateTime, nullable=True)
    status = Column(String(20), default="active")  # active, achieved, cancelled
    created_at = Column(DateTime, default=datetime.now)


class DatabaseManager:
    """Manage database operations."""
    
    def __init__(self, db_path: str = DATABASE_PATH):
        """Initialize database manager."""
        self.engine = create_engine(f'sqlite:///{db_path}')
        Base.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
    
    def add_transaction(
        self,
        amount: float,
        category: str,
        description: str,
        transaction_type: TransactionType,
        date: Optional[datetime] = None
    ) -> Transaction:
        """Add a new transaction."""
        transaction = Transaction(
            amount=amount,
            category=category,
            description=description,
            transaction_type=transaction_type,
            date=date or datetime.now()
        )
        self.session.add(transaction)
        self.session.commit()
        return transaction
    
    def get_transactions(
        self,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        category: Optional[str] = None,
        transaction_type: Optional[TransactionType] = None
    ) -> List[Transaction]:
        """Get transactions with optional filters."""
        query = self.session.query(Transaction)
        
        if start_date:
            query = query.filter(Transaction.date >= start_date)
        if end_date:
            query = query.filter(Transaction.date <= end_date)
        if category:
            query = query.filter(Transaction.category == category)
        if transaction_type:
            query = query.filter(Transaction.transaction_type == transaction_type)
        
        return query.order_by(Transaction.date.desc()).all()
    
    def get_spending_by_category(
        self,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> Dict[str, float]:
        """Get total spending by category."""
        transactions = self.get_transactions(
            start_date=start_date,
            end_date=end_date,
            transaction_type=TransactionType.EXPENSE
        )
        
        spending = {}
        for t in transactions:
            spending[t.category] = spending.get(t.category, 0.0) + t.amount
        
        return spending
    
    def get_total_income(
        self,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> float:
        """Get total income for a period."""
        transactions = self.get_transactions(
            start_date=start_date,
            end_date=end_date,
            transaction_type=TransactionType.INCOME
        )
        return sum(t.amount for t in transactions)
    
    def get_total_expenses(
        self,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> float:
        """Get total expenses for a period."""
        transactions = self.get_transactions(
            start_date=start_date,
            end_date=end_date,
            transaction_type=TransactionType.EXPENSE
        )
        return sum(t.amount for t in transactions)
    
    def create_budget(
        self,
        category: str,
        amount: float,
        period: str = "monthly"
    ) -> Budget:
        """Create a new budget."""
        # Deactivate old budgets for this category
        old_budgets = self.session.query(Budget).filter(
            Budget.category == category,
            Budget.end_date.is_(None)
        ).all()
        
        for budget in old_budgets:
            budget.end_date = datetime.now()
        
        # Create new budget
        budget = Budget(
            category=category,
            amount=amount,
            period=period
        )
        self.session.add(budget)
        self.session.commit()
        return budget
    
    def get_budgets(self, active_only: bool = True) -> List[Budget]:
        """Get budgets."""
        query = self.session.query(Budget)
        if active_only:
            query = query.filter(Budget.end_date.is_(None))
        return query.all()
    
    def create_goal(
        self,
        name: str,
        target_amount: float,
        current_amount: float = 0.0,
        target_date: Optional[datetime] = None
    ) -> Goal:
        """Create a new financial goal."""
        goal = Goal(
            name=name,
            target_amount=target_amount,
            current_amount=current_amount,
            target_date=target_date
        )
        self.session.add(goal)
        self.session.commit()
        return goal
    
    def update_goal_progress(self, goal_id: int, amount: float) -> Goal:
        """Update progress on a goal."""
        goal = self.session.query(Goal).filter(Goal.id == goal_id).first()
        if goal:
            goal.current_amount = amount
            if goal.current_amount >= goal.target_amount:
                goal.status = "achieved"
            self.session.commit()
        return goal
    
    def get_goals(self, active_only: bool = True) -> List[Goal]:
        """Get financial goals."""
        query = self.session.query(Goal)
        if active_only:
            query = query.filter(Goal.status == "active")
        return query.all()
    
    def close(self):
        """Close the database session."""
        self.session.close()

