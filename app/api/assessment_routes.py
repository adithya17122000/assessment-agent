# app/api/assessment_routes.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.config.database import get_db
from app.assessment_management.schemas import TakeAssessmentRequest, TakeAssessmentResponse, AssessmentResponse
from app.assessment_management import service

router = APIRouter(prefix="/assessments", tags=["Assessment Management"])


# @router.post("/", response_model=TakeAssessmentResponse)
def take_assessment(payload: TakeAssessmentRequest, db: Session = Depends(get_db)):
    assessment_request, assessment = service.take_assessment(db, payload)
    return TakeAssessmentResponse(
        assessment_request=assessment_request,
        assessment=assessment,
    )


# @router.get("/{assessment_id}", response_model=AssessmentResponse)
def get_assessment(assessment_id: str, db: Session = Depends(get_db)):
    assessment = service.get_assessment(db, assessment_id)
    if not assessment:
        raise HTTPException(status_code=404, detail="Assessment not found")
    return assessment
