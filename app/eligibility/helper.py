import uuid
from collections import defaultdict
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.eligibility.models import AssessmentEligibility
from app.eligibility.schemas import AssessmentEligibilityCreate, CourseEligibilitySummary


def create_eligibility(db: Session, payload: AssessmentEligibilityCreate):
    try:
        record = AssessmentEligibility(
            id=f"elig-{uuid.uuid4().hex[:8]}",
            user_id=payload.user_id,
            user_name=payload.user_name,
            course_id=payload.course_id,
            course_name=payload.course_name,
            module_name=payload.module_name,
            module_id=payload.module_id,
            topics=payload.topics,
            difficulty=payload.difficulty,
            completion_date=payload.completion_date,
        )
        db.add(record)
        db.commit()
        db.refresh(record)
        return {
            "message": f"Eligibility record created for user_id={payload.user_id}, course_id={payload.course_id}",
            "eligibility_id": record.id,
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to create eligibility record: {str(e)}")

def get_eligibility_by_user(db: Session, user_id: str):
    return (
        db.query(AssessmentEligibility)
        .filter(AssessmentEligibility.user_id == user_id)
        .order_by(AssessmentEligibility.created_at.desc())
        .all()
    )


def get_eligibility_summary_by_user(db: Session, user_id: str):
    all_rows = get_eligibility_by_user(db, user_id)

    grouped = defaultdict(list)
    for row in all_rows:
        grouped[row.course_id].append(row)

    summaries = []
    for course_id, rows in grouped.items():
        rows_sorted = sorted(rows, key=lambda r: r.created_at, reverse=True)
        latest_row = rows_sorted[0]

        union_set = set()
        for row in rows:
            union_set.update(row.topics)

        summaries.append(
            CourseEligibilitySummary(
                course_id=course_id,
                course_name=latest_row.course_name,
                topics=sorted(union_set),
                # latest_topics=latest_row.topics,
                latest_completion_date=str(latest_row.completion_date),
                difficulty=latest_row.difficulty,

            )
        )

    return summaries