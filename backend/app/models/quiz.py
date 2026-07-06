"""
Quiz model for database.
"""
from sqlalchemy import Column, Integer, String, Enum as SQLEnum
from sqlalchemy.orm import relationship
import enum

from app.db.base import Base, TimestampMixin


class QuizStatus(str, enum.Enum):
    """Quiz status enumeration."""
    
    PASSED = "passed"
    FAILED = "failed"
    IN_PROGRESS = "in_progress"
    NOT_STARTED = "not_started"


class Quiz(Base, TimestampMixin):
    """
    Quiz model representing assessment quizzes in the system.
    """

    __tablename__ = "quizzes"

    quiz_id = Column(String, primary_key=True, index=True)
    skill_id = Column(String, nullable=False, index=True)  # From Team 1's skill ontology
    course = Column(String, nullable=False)
    pass_threshold = Column(Integer, default=60, nullable=False)
    
    # Relationships
    attempts = relationship("Attempt", back_populates="quiz", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"<Quiz(quiz_id={self.quiz_id}, skill_id={self.skill_id}, course={self.course})>"
