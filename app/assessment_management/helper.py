# app/assessment_management/helper.py
import uuid
from sqlalchemy.orm import Session

from app.assessment_management.models import Assessment, AssessmentRequest
from app.assessment_management.schemas import TakeAssessmentRequest


def create_assessment_request(db: Session, payload: TakeAssessmentRequest) -> AssessmentRequest:
    record = AssessmentRequest(
        id=f"req-{uuid.uuid4().hex[:8]}",
        user_id=payload.user_id,
        course_id=payload.course_id,
        course_name=payload.course_name,
        module_id=payload.module_id,
        module_name=payload.module_name,
        topics=payload.topics,
        difficulty=payload.difficulty,
    )
    db.add(record)
    db.flush()  # persist to get id before creating assessment
    return record


def create_assessment(db: Session, request_id: str) -> Assessment:
    record = Assessment(
        id=f"asmt-{uuid.uuid4().hex[:8]}",
        request_id=request_id,
        status="In Progress",
        question_count=10,
        submitted_at=None,
    )
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


def get_assessment_by_id(db: Session, assessment_id: str) -> Assessment:
    return db.query(Assessment).filter(Assessment.id == assessment_id).first()
