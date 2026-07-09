from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.config.database import get_db
from app.evaluation.service import submit_and_evaluate
from app.evaluation.schemas import BulkResponseSubmission, EvaluationResponse

router = APIRouter(prefix="/submit-assessment", tags=["Evaluation"])

@router.post("/", response_model=EvaluationResponse)
def submit_assessment(payload: BulkResponseSubmission, db: Session = Depends(get_db)):
    return submit_and_evaluate(db, payload)