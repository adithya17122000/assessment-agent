from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.config.database import get_db
from app.eligibility.schemas import AssessmentEligibilityCreate, AssessmentEligibilityResponse
from app.eligibility import service

router = APIRouter(prefix="/eligibility", tags=["Eligibility"])


@router.post("/", response_model=AssessmentEligibilityResponse)
def create_eligibility(payload: AssessmentEligibilityCreate, db: Session = Depends(get_db)):
    return service.record_eligibility(db, payload)


@router.get("/{employee_id}", response_model=List[AssessmentEligibilityResponse])
def get_eligibility_dropdown(employee_id: str, db: Session = Depends(get_db)):
    return service.get_dropdown_options(db, employee_id)