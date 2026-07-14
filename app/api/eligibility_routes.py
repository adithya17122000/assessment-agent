from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.config.database import get_db
from app.eligibility.schemas import AssessmentEligibilityCreate, AssessmentEligibilityResponse, EligibilityCreateResponse, MockTakeAssessmentPayload
from app.eligibility import service
from app.eligibility.schemas import CourseEligibilitySummary
from app.eligibility.service import get_dropdown_summary
from app.eligibility.schemas import MockTakeAssessmentPayload
from app.eligibility.service import build_mock_take_assessment_payload

router = APIRouter(prefix="/eligibility", tags=["Eligibility"])


@router.post("/", response_model=EligibilityCreateResponse)
def create_eligibility(payload: AssessmentEligibilityCreate, db: Session = Depends(get_db)):
    return service.record_eligibility(db, payload)

# @router.get("/{user_id}", response_model=List[AssessmentEligibilityResponse])
def get_eligibility_dropdown(user_id: str, db: Session = Depends(get_db)):
    return service.get_dropdown_options(db, user_id)

@router.get("/{user_id}/summary", response_model=List[CourseEligibilitySummary])
def get_eligibility_summary(user_id: str, db: Session = Depends(get_db)):
    return get_dropdown_summary(db, user_id)

@router.get("/{user_id}/mock-take-assessment", response_model=MockTakeAssessmentPayload)
def get_mock_take_assessment(user_id: str, db: Session = Depends(get_db)):
    return build_mock_take_assessment_payload(db, user_id)