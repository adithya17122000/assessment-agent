"""
Employee API routes for Team 4 Assessment & Quiz Agent.

Endpoints:
- GET /employees/{employee_id}/quizzes - Get all quizzes for an employee
- GET /employees/{employee_id}/quiz-attempts - Get cross-quiz attempt history
"""
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import func, or_
from sqlalchemy.orm import Session, joinedload

from app.core.dependencies import get_db, validate_pagination_params
from app.models.attempt import Attempt
from app.models.employee import Employee
from app.models.quiz import Quiz
from app.schemas.attempt import EmployeeQuizAttemptsResponse, AttemptWithQuizInfo
from app.schemas.quiz import QuizListResponse, QuizInList
from app.schemas.pagination import PaginationMeta

router = APIRouter(prefix="/employees", tags=["employees"])


@router.get("/{employee_id}/quizzes", response_model=QuizListResponse)
def get_employee_quizzes(
    employee_id: str,
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    search: str | None = Query(default=None),
    db: Session = Depends(get_db),
    pagination: dict = Depends(validate_pagination_params),
):
    """
    Get all quizzes for an employee.
    
    Supports pagination and search by course name.
    
    **Path Parameters:**
    - `employee_id`: Unique identifier of the employee
    
    **Query Parameters:**
    - `limit`: Maximum items per page (default: 20, max: 100)
    - `offset`: Number of items to skip (default: 0)
    - `search`: Filter by course name (case-insensitive partial match)
    
    **Returns:**
    - Employee ID
    - List of quizzes with status and scores
    - Pagination metadata
    
    **Status Codes:**
    - 200: Success
    - 401: Unauthorized (invalid or expired token)
    - 403: Forbidden (user lacks permission)
    - 404: Not Found (employee not found)
    """
    # Verify employee exists (optional: create if not exists for demo purposes)
    employee = db.query(Employee).filter(Employee.employee_id == employee_id).first()
    if not employee:
        # For demo purposes, create employee if not exists
        # In production, this should integrate with Team 1's employee service
        employee = Employee(employee_id=employee_id)
        db.add(employee)
        db.commit()
    
    # Build base query
    query = db.query(Quiz)
    
    # Apply search filter
    if search:
        query = query.filter(Quiz.course.ilike(f"%{search}%"))
    
    # Get total count
    total = query.count()
    
    # Get quizzes with pagination
    quizzes = query.limit(limit).offset(offset).all()
    
    # Build response with quiz status
    quiz_list = []
    for quiz in quizzes:
        # Get latest attempt for this quiz
        latest_attempt = (
            db.query(Attempt)
            .filter(
                Attempt.employee_id == employee_id,
                Attempt.quiz_id == quiz.quiz_id
            )
            .order_by(Attempt.attempted_on.desc())
            .first()
        )
        
        if latest_attempt:
            last_score = latest_attempt.score
            status = latest_attempt.status.value
        else:
            last_score = 0
            status = "not_started"
        
        quiz_list.append(
            QuizInList(
                quiz_id=quiz.quiz_id,
                skill_id=quiz.skill_id,
                course=quiz.course,
                last_score=last_score,
                pass_threshold=quiz.pass_threshold,
                status=status,
            )
        )
    
    return QuizListResponse(
        employee_id=employee_id,
        quizzes=quiz_list,
        pagination=PaginationMeta.create(limit, offset, total).model_dump(),
    )


@router.get("/{employee_id}/quiz-attempts", response_model=EmployeeQuizAttemptsResponse)
def get_employee_quiz_attempts(
    employee_id: str,
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    search: str | None = Query(default=None),
    db: Session = Depends(get_db),
    pagination: dict = Depends(validate_pagination_params),
):
    """
    Get cross-quiz attempt history for an employee.
    
    Returns attempt history spanning all quizzes for the specified employee.
    Supports pagination and search by course name or skill name.
    
    **Path Parameters:**
    - `employee_id`: Unique identifier of the employee
    
    **Query Parameters:**
    - `limit`: Maximum items per page (default: 20, max: 100)
    - `offset`: Number of items to skip (default: 0)
    - `search`: Filter by course name or skill name (case-insensitive)
    
    **Returns:**
    - Employee ID
    - List of attempts across all quizzes (most recent first)
    - Pagination metadata
    
    **Status Codes:**
    - 200: Success
    - 401: Unauthorized (invalid or expired token)
    - 403: Forbidden (user lacks permission)
    - 404: Not Found (employee not found)
    
    **Used By:**
    - Team 5 for recent activity dashboard view
    """
    # Verify employee exists
    employee = db.query(Employee).filter(Employee.employee_id == employee_id).first()
    if not employee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Employee with id '{employee_id}' not found",
        )
    
    # Build base query with quiz information
    query = (
        db.query(Attempt)
        .join(Quiz, Attempt.quiz_id == Quiz.quiz_id)
        .filter(Attempt.employee_id == employee_id)
    )
    
    # Apply search filter (search in course name or skill_id)
    if search:
        query = query.filter(
            or_(
                Quiz.course.ilike(f"%{search}%"),
                Quiz.skill_id.ilike(f"%{search}%")
            )
        )
    
    # Get total count
    total = query.count()
    
    # Get attempts with pagination (most recent first)
    attempts = (
        query
        .options(joinedload(Attempt.quiz))
        .order_by(Attempt.attempted_on.desc())
        .limit(limit)
        .offset(offset)
        .all()
    )
    
    # Format attempts with quiz information
    attempt_list = [
        AttemptWithQuizInfo(
            quiz_id=attempt.quiz_id,
            skill_id=attempt.quiz.skill_id,
            course=attempt.quiz.course,
            score=attempt.score,
            status=attempt.status.value,
            attempted_on=attempt.attempted_on,
            feedback=attempt.feedback or "",
        )
        for attempt in attempts
    ]
    
    return EmployeeQuizAttemptsResponse(
        employee_id=employee_id,
        attempts=attempt_list,
        pagination=PaginationMeta.create(limit, offset, total).model_dump(),
    )
