"""Pydantic schemas for request/response validation."""

from app.schemas.pagination import PaginationParams, PaginationMeta, PaginatedResponse
from app.schemas.employee import Employee, EmployeeBase, EmployeeCreate
from app.schemas.quiz import QuizBase, QuizInList, QuizListResponse, QuizCreate, QuizUpdate
from app.schemas.attempt import (
    AttemptBase,
    AttemptInList,
    AttemptWithQuizInfo,
    QuizAttemptsResponse,
    EmployeeQuizAttemptsResponse,
    AttemptCreate,
)

__all__ = [
    # Pagination
    "PaginationParams",
    "PaginationMeta",
    "PaginatedResponse",
    # Employee
    "Employee",
    "EmployeeBase",
    "EmployeeCreate",
    # Quiz
    "QuizBase",
    "QuizInList",
    "QuizListResponse",
    "QuizCreate",
    "QuizUpdate",
    # Attempt
    "AttemptBase",
    "AttemptInList",
    "AttemptWithQuizInfo",
    "QuizAttemptsResponse",
    "EmployeeQuizAttemptsResponse",
    "AttemptCreate",
]
