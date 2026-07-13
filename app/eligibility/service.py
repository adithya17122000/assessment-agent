from sqlalchemy.orm import Session

from app.eligibility import helper
from app.eligibility.schemas import AssessmentEligibilityCreate


def record_eligibility(db: Session, payload: AssessmentEligibilityCreate):
    return helper.create_eligibility(db, payload)


def get_dropdown_options(db: Session, user_id: str):
    return helper.get_eligibility_by_user(db, user_id)


def get_dropdown_summary(db: Session, user_id: str):
    return helper.get_eligibility_summary_by_user(db, user_id)

def build_mock_take_assessment_payload(db: Session, user_id: str) -> dict:
    rows = helper.get_eligibility_by_user(db, user_id)
    if not rows:
        raise ValueError(f"No eligibility records found for user_id={user_id}")

    latest = sorted(rows, key=lambda r: r.created_at, reverse=True)[0]

    return {
        "user_id": user_id,
        "course_id": latest.course_id,
        "course_name": latest.course_name,
        "module_id": latest.module_id,
        "module_name": latest.module_name,
        "topics": latest.topics,
        "difficulty": latest.difficulty,
    }