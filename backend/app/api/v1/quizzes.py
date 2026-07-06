"""
Quiz API routes for Team 4 Assessment & Quiz Agent.

Endpoints:
- GET /quizzes/{quiz_id}/attempts - Get all attempts for a specific quiz
"""
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.core.dependencies import get_db, validate_pagination_params
from app.models.attempt import Attempt
from app.models.quiz import Quiz
from app.schemas.attempt import QuizAttemptsResponse, AttemptInList
from app.schemas.pagination import PaginationMeta

router = APIRouter(prefix="/quizzes", tags=["quizzes"])


@router.get("/{quiz_id}/attempts", response_model=QuizAttemptsResponse)
def get_quiz_attempts(
    quiz_id: str,
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_db),
    pagination: dict = Depends(validate_pagination_params),
):
    """
    Get all attempts for a specific quiz.
    
    Supports pagination only (no search) — attempts on a single quiz are typically few
    and scoped to one employee.
    
    **Path Parameters:**
    - `quiz_id`: Unique identifier of the quiz
    
    **Query Parameters:**
    - `limit`: Maximum items per page (default: 20, max: 100)
    - `offset`: Number of items to skip (default: 0)
    
    **Returns:**
    - Employee ID
    - Quiz ID
    - List of attempts (most recent first)
    - Pagination metadata
    
    **Status Codes:**
    - 200: Success
    - 401: Unauthorized (invalid or expired token)
    - 403: Forbidden (quiz belongs to another employee)
    - 404: Not Found (quiz not found)
    """
    # Verify quiz exists
    quiz = db.query(Quiz).filter(Quiz.quiz_id == quiz_id).first()
    if not quiz:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Quiz with id '{quiz_id}' not found",
        )
    
    # Get total count
    total = db.query(func.count(Attempt.attempt_id)).filter(
        Attempt.quiz_id == quiz_id
    ).scalar()
    
    # Get attempts (most recent first)
    attempts = (
        db.query(Attempt)
        .filter(Attempt.quiz_id == quiz_id)
        .order_by(Attempt.attempted_on.desc())
        .limit(limit)
        .offset(offset)
        .all()
    )
    
    # Get employee_id from first attempt (all attempts for a quiz belong to same employee)
    employee_id = attempts[0].employee_id if attempts else "unknown"
    
    # Format attempts
    attempt_list = [
        AttemptInList(
            course=quiz.course,
            score=attempt.score,
            status=attempt.status.value,
            attempted_on=attempt.attempted_on,
            feedback=attempt.feedback or "",
        )
        for attempt in attempts
    ]
    
    return QuizAttemptsResponse(
        employee_id=employee_id,
        quiz_id=quiz_id,
        attempts=attempt_list,
        pagination=PaginationMeta.create(limit, offset, total).model_dump(),
    )
