"""
Quiz schemas for request/response validation.
"""
from pydantic import BaseModel, Field


class QuizBase(BaseModel):
    """Base quiz schema with common attributes."""

    quiz_id: str = Field(description="Unique identifier of the quiz")
    skill_id: str = Field(description="Skill being assessed (from shared ontology)")
    course: str = Field(description="Name of the associated course")


class QuizInList(QuizBase):
    """
    Quiz schema for list responses.
    Used in GET /api/v1/employees/{employee_id}/quizzes
    """

    last_score: int = Field(description="Most recent score (0-100)")
    pass_threshold: int = Field(description="Minimum score required to pass (0-100)")
    status: str = Field(
        description="Quiz status: 'passed', 'failed', 'in_progress', 'not_started'"
    )

    class Config:
        """Pydantic configuration."""

        from_attributes = True
        json_schema_extra = {
            "example": {
                "quiz_id": "Q101",
                "skill_id": "108",
                "course": "Learning FastAPI Fundamentals",
                "last_score": 82,
                "pass_threshold": 60,
                "status": "passed",
            }
        }


class QuizListResponse(BaseModel):
    """
    Response for GET /api/v1/employees/{employee_id}/quizzes
    """

    employee_id: str
    quizzes: list[QuizInList]
    pagination: dict

    class Config:
        """Pydantic configuration."""

        from_attributes = True


class QuizCreate(BaseModel):
    """Schema for creating a new quiz."""

    quiz_id: str
    skill_id: str
    course: str
    pass_threshold: int = Field(default=60, ge=0, le=100)


class QuizUpdate(BaseModel):
    """Schema for updating a quiz."""

    skill_id: str | None = None
    course: str | None = None
    pass_threshold: int | None = Field(default=None, ge=0, le=100)
