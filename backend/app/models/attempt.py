"""
Attempt model for database.
"""
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text, Enum as SQLEnum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

from app.db.base import Base


class AttemptStatus(str, enum.Enum):
    """Attempt status enumeration."""
    
    PASSED = "passed"
    FAILED = "failed"


class Attempt(Base):
    """
    Attempt model representing quiz attempts by employees.
    """

    __tablename__ = "attempts"

    attempt_id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    employee_id = Column(String, ForeignKey("employees.employee_id"), nullable=False, index=True)
    quiz_id = Column(String, ForeignKey("quizzes.quiz_id"), nullable=False, index=True)
    
    score = Column(Integer, nullable=False)  # 0-100
    status = Column(SQLEnum(AttemptStatus), nullable=False)
    feedback = Column(Text, nullable=True)
    attempted_on = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    
    # Relationships
    employee = relationship("Employee", back_populates="quiz_attempts")
    quiz = relationship("Quiz", back_populates="attempts")

    def __repr__(self) -> str:
        return (
            f"<Attempt(attempt_id={self.attempt_id}, employee_id={self.employee_id}, "
            f"quiz_id={self.quiz_id}, score={self.score}, status={self.status})>"
        )
