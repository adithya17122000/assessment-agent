from sqlalchemy.orm import Session

from app.assessment_management import helper
from app.assessment_management.schemas import TakeAssessmentRequest


def take_assessment(db: Session, payload: TakeAssessmentRequest):
    assessment_request = helper.create_assessment_request(db, payload)
    assessment = helper.create_assessment(db, assessment_request.id)
    return assessment_request, assessment


def get_assessment(db: Session, assessment_id: str):
    return helper.get_assessment_by_id(db, assessment_id)
