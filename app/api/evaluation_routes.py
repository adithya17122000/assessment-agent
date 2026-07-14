from fastapi import APIRouter, Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.config.database import get_db
from app.evaluation.service import submit_and_evaluate, get_assessment_review
from app.evaluation.schemas import BulkResponseSubmission, EvaluationResponse, AssessmentReview


router = APIRouter(prefix="/submit-assessment", tags=["Evaluation"])

@router.post("/", response_model=EvaluationResponse)
def submit_assessment(payload: BulkResponseSubmission, db: Session = Depends(get_db)):
    return submit_and_evaluate(db, payload)


@router.get("/{assessment_id}/review", response_model=AssessmentReview)
def get_review(assessment_id: str, db: Session = Depends(get_db)):
    try:
        return get_assessment_review(db, assessment_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))