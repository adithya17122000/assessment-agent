"""
Attempt schemas for request/response validation.
"""
from datetime import datetime

from pydantic import BaseModel, Field


class AttemptBase(BaseModel):
    """Base attempt schema with common attributes."""

    course: str = Field(description="Name of the associated course")
    score: int = Field(description="Score achieved (0-100)", ge=0, le=100)
    status: str = Field(description="Attempt status: 'passed' or 'failed'")
    attempted_on: datetime = Field(description="ISO 8601 timestamp of attempt")
    feedback: str = Field(description="AI-generated feedback for the attempt")


class AttemptInList(AttemptBase):
    """
    Attempt schema for single quiz attempt history.
    Used in GET /api/v1/quizzes/{quiz_id}/attempts
    """

    class Config:
        """Pydantic configuration."""

        from_attributes = True
        json_schema_extra = {
            "example": {
                "course": "Learning FastAPI Fundamentals",
                "score": 82,
                "status": "passed",
                "attempted_on": "2026-06-29T07:25:00Z",
                "feedback": "Solid understanding of routing and dependency injection.",
            }
        }


class AttemptWithQuizInfo(AttemptBase):
    """
    Attempt schema with quiz information for cross-quiz history.
    Used in GET /api/v1/employees/{employee_id}/quiz-attempts
    """

    quiz_id: str = Field(description="Unique identifier of the quiz")
    skill_id: str = Field(description="Skill being assessed (from shared ontology)")

    class Config:
        """Pydantic configuration."""

        from_attributes = True
        json_schema_extra = {
            "example": {
                "quiz_id": "Q101",
                "skill_id": "108",
                "course": "Learning FastAPI Fundamentals",
                "score": 82,
                "status": "passed",
                "attempted_on": "2026-06-29T07:25:00Z",
                "feedback": "Solid understanding of routing and dependency injection.",
            }
        }


class QuizAttemptsResponse(BaseModel):
    """
    Response for GET /api/v1/quizzes/{quiz_id}/attempts
    """

    employee_id: str
    quiz_id: str
    attempts: list[AttemptInList]
    pagination: dict

    class Config:
        """Pydantic configuration."""

        from_attributes = True


class EmployeeQuizAttemptsResponse(BaseModel):
    """
    Response for GET /api/v1/employees/{employee_id}/quiz-attempts
    """

    employee_id: str
    attempts: list[AttemptWithQuizInfo]
    pagination: dict

    class Config:
        """Pydantic configuration."""

        from_attributes = True


class AttemptCreate(BaseModel):
    """Schema for creating a new attempt."""

    employee_id: str
    quiz_id: str
    score: int = Field(ge=0, le=100)
    status: str = Field(pattern="^(passed|failed)$")
    feedback: str | None = None
