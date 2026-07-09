from sqlalchemy.orm import Session

from app.assessment_management.models import Assessment, AssessmentRequest
from app.evaluation.models import Evaluation


def get_results_by_employee(db: Session, employee_id: str):
    return (
        db.query(Assessment, AssessmentRequest, Evaluation)
        .join(AssessmentRequest, Assessment.request_id == AssessmentRequest.id)
        .outerjoin(Evaluation, Evaluation.assessment_id == Assessment.id)
        .filter(AssessmentRequest.employee_id == employee_id)
        .order_by(Assessment.started_at.desc())
        .all()
    )