import uuid
from sqlalchemy.orm import Session

from app.eligibility.models import AssessmentEligibility
from app.eligibility.schemas import AssessmentEligibilityCreate


def create_eligibility(db: Session, payload: AssessmentEligibilityCreate):
    record = AssessmentEligibility(
        id=f"elig-{uuid.uuid4().hex[:8]}",
        employee_id=payload.employee_id,
        employee_name=payload.employee_name,
        course_id=payload.course_id,
        course_name=payload.course_name,
        module_name=payload.module_name,
        topics=payload.topics,
        difficulty=payload.difficulty,
        completion_date=payload.completion_date,
    )
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


def get_eligibility_by_employee(db: Session, employee_id: str):
    return (
        db.query(AssessmentEligibility)
        .filter(AssessmentEligibility.employee_id == employee_id)
        .order_by(AssessmentEligibility.created_at.desc())
        .all()
    )