import uuid
from sqlalchemy.orm import Session

from app.config.settings import PASS_THRESHOLD_PERCENT
from app.result_management.schemas import (
    EmployeeAssessmentSummary, EmployeeAssessmentsResponse,
    AssessmentAttemptEntry, EmployeeAssessmentAttemptsResponse,
    CourseAssessmentAttemptEntry, CourseAssessmentAttemptsResponse,
)
from app.result_management import helper

def get_employee_assessments_response(db: Session, user_id: str, limit: int, offset: int, search: str = None):
    rows, total = helper.get_employee_assessments(db, user_id, limit, offset, search)
    assessments = [
        EmployeeAssessmentSummary(
            assessment_id=assessment.id,
            course_id=request.course_id,
            course=request.course_name,
            last_score=evaluation.score if evaluation else None,
            pass_threshold=int(PASS_THRESHOLD_PERCENT),
            status=(evaluation.pass_fail_status.lower() if evaluation else "pending"),
        )
        for assessment, request, evaluation in rows
    ]
    return EmployeeAssessmentsResponse(
        user_id=user_id,
        assessments=assessments,
        pagination={"limit": limit, "offset": offset, "total": total, "has_more": offset + limit < total},
    )


def get_employee_assessment_attempts_response(db: Session, user_id: str, limit: int, offset: int, search: str = None):
    rows, total = helper.get_employee_assessment_attempts(db, user_id, limit, offset, search)
    attempts = [
        AssessmentAttemptEntry(
            assessment_id=assessment.id,
            course_id=request.course_id,
            course=request.course_name,
            score=evaluation.score if evaluation else None,
            status=(evaluation.pass_fail_status.lower() if evaluation else "pending"),
            attempted_on=assessment.submitted_at,
            feedback=evaluation.feedback if evaluation else None,
        )
        for assessment, request, evaluation in rows
    ]
    return EmployeeAssessmentAttemptsResponse(
        user_id=user_id,
        attempts=attempts,
        pagination={"limit": limit, "offset": offset, "total": total, "has_more": offset + limit < total},
    )


def get_course_assessment_attempts_response(db: Session, course_id: str, limit: int, offset: int):
    rows, total = helper.get_course_assessment_attempts(db, course_id, limit, offset)
    attempts = [
        CourseAssessmentAttemptEntry(
            user_id=request.user_id,
            assessment_id=assessment.id,
            score=evaluation.score if evaluation else None,
            status=(evaluation.pass_fail_status.lower() if evaluation else "pending"),
            attempted_on=assessment.submitted_at,
        )
        for assessment, request, evaluation in rows
    ]
    return CourseAssessmentAttemptsResponse(
        course_id=course_id,
        attempts=attempts,
        pagination={"limit": limit, "offset": offset, "total": total, "has_more": offset + limit < total},
    )