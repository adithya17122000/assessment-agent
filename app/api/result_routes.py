from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from typing import Optional

from app.config.database import get_db
from app.result_management.schemas import (
    EmployeeAssessmentsResponse, EmployeeAssessmentAttemptsResponse, CourseAssessmentAttemptsResponse
)
from app.result_management.service import (
    get_employee_assessments_response, get_employee_assessment_attempts_response, get_course_assessment_attempts_response
)
from app.config.auth import verify_service_token

router = APIRouter(prefix="/results", tags=["Result Management"])


@router.get("/employees/{user_id}/assessments", response_model=EmployeeAssessmentsResponse, dependencies=[Depends(verify_service_token)])
def get_employee_assessments(user_id: str, limit: int = 20, offset: int = 0, search: Optional[str] = None, db: Session = Depends(get_db)):
    return get_employee_assessments_response(db, user_id, limit, offset, search)


@router.get("/employees/{user_id}/assessment-attempts", response_model=EmployeeAssessmentAttemptsResponse, dependencies=[Depends(verify_service_token)])
def get_employee_assessment_attempts(user_id: str, limit: int = 20, offset: int = 0, search: Optional[str] = None, db: Session = Depends(get_db)):
    return get_employee_assessment_attempts_response(db, user_id, limit, offset, search)


@router.get("/courses/{course_id}/assessment-attempts", response_model=CourseAssessmentAttemptsResponse, dependencies=[Depends(verify_service_token)])
def get_course_assessment_attempts(course_id: str, limit: int = 20, offset: int = 0, db: Session = Depends(get_db)):
    return get_course_assessment_attempts_response(db, course_id, limit, offset)