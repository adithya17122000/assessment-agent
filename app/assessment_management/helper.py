import uuid
from sqlalchemy.orm import Session
from sqlalchemy import func, and_

from app.assessment_management.models import Assessment, AssessmentRequest
from app.assessment_management.schemas import TakeAssessmentRequest
from app.evaluation.models import Evaluation

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

def assessment_history(db: Session, user_id: str):
    query = (
        db.query(
            AssessmentRequest.course_id.label("course_id"),
            AssessmentRequest.course_name.label("course_name"),
            AssessmentRequest.user_id.label("user_id"),
            Assessment.status.label("status"),
            Assessment.started_at.label("started_at"),
            Assessment.id.label("assessment_id"),
            Evaluation.score.label("latest_score"),
        )
        .join(
            Assessment,
            Assessment.request_id == AssessmentRequest.id,
        )
        .outerjoin(
            Evaluation,
            Evaluation.assessment_id == Assessment.id,
        )
        .filter(
            AssessmentRequest.user_id == user_id
        )
    )

    
    rows = query.order_by(Assessment.started_at.desc()).all()
    aggregated = {}
    for row in rows:
        key = (row.course_id, row.status)

        if key not in aggregated:
            aggregated[key] = {
                "course_id": row.course_id,
                "course": row.course_name,
                "status": row.status,
                "attempts": 1,
                "latest_assessment_id": row.assessment_id,
                "last_score": row.latest_score,
            }
        else:
            aggregated[key]["attempts"] += 1

    return list(aggregated.values())
    
