from sqlalchemy.orm import Session

from app.assessment_management.models import Assessment, AssessmentRequest
from app.evaluation.models import Evaluation


def get_employee_assessments(db: Session, user_id: str, limit: int, offset: int, search: str = None):
    query = (
        db.query(Assessment, AssessmentRequest, Evaluation)
        .join(AssessmentRequest, Assessment.request_id == AssessmentRequest.id)
        .outerjoin(Evaluation, Evaluation.assessment_id == Assessment.id)
        .filter(AssessmentRequest.user_id == user_id)
    )
    if search:
        query = query.filter(AssessmentRequest.course_name.ilike(f"%{search}%"))

    total = query.count()
    rows = query.order_by(Assessment.started_at.desc()).offset(offset).limit(limit).all()
    return rows, total


def get_employee_assessment_attempts(db: Session, user_id: str, limit: int, offset: int, search: str = None):
    # Same underlying data as get_employee_assessments — response shape differs, not the query.
    return get_employee_assessments(db, user_id, limit, offset, search)


def get_course_assessment_attempts(db: Session, course_id: str, limit: int, offset: int):
    query = (
        db.query(Assessment, AssessmentRequest, Evaluation)
        .join(AssessmentRequest, Assessment.request_id == AssessmentRequest.id)
        .outerjoin(Evaluation, Evaluation.assessment_id == Assessment.id)
        .filter(AssessmentRequest.course_id == course_id)
    )
    total = query.count()
    rows = query.order_by(Assessment.started_at.desc()).offset(offset).limit(limit).all()
    return rows, total