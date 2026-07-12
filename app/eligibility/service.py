from sqlalchemy.orm import Session

from app.eligibility import helper
from app.eligibility.schemas import AssessmentEligibilityCreate


def record_eligibility(db: Session, payload: AssessmentEligibilityCreate):
    return helper.create_eligibility(db, payload)


def get_dropdown_options(db: Session, user_id: str):
    return helper.get_eligibility_by_user(db, user_id)


def get_dropdown_summary(db: Session, user_id: str):
    return helper.get_eligibility_summary_by_user(db, user_id)