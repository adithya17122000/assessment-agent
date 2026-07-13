from sqlalchemy import func
from sqlalchemy.orm import Session

from app.assessment_management.models import Assessment, AssessmentRequest
from app.evaluation.models import Evaluation


def get_results_by_user(db: Session, user_id: str):
    return (
        db.query(Assessment, AssessmentRequest, Evaluation)
        .join(AssessmentRequest, Assessment.request_id == AssessmentRequest.id)
        .outerjoin(Evaluation, Evaluation.assessment_id == Assessment.id)
        .filter(AssessmentRequest.user_id == user_id)
        .order_by(Assessment.started_at.desc())
        .all()
    )


def get_course_status_counts(db: Session, user_id: str):
    return (
        db.query(
            AssessmentRequest.course_id,
            AssessmentRequest.course_name,
            Assessment.status,
            Evaluation.pass_fail_status,
            func.count(Assessment.id).label("attempt_count"),
        )
        .join(Assessment, Assessment.request_id == AssessmentRequest.id)
        .outerjoin(Evaluation, Evaluation.assessment_id == Assessment.id)
        .filter(AssessmentRequest.user_id == user_id)
        .group_by(
            AssessmentRequest.course_id,
            AssessmentRequest.course_name,
            Assessment.status,
            Evaluation.pass_fail_status,
        )
        .all()
    )