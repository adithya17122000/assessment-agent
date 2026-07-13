from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.config.database import get_db
from app.evaluation.service import submit_and_evaluate
from app.evaluation.schemas import BulkResponseSubmission, EvaluationResponse

router = APIRouter(prefix="/submit-assessment", tags=["Evaluation"])

@router.post("/", response_model=EvaluationResponse)
def submit_assessment(payload: BulkResponseSubmission, db: Session = Depends(get_db)):
    return submit_and_evaluate(db, payload)


'''
{
  "assessment_id": "asmt-a08f7ed6",
  "answers": [
    {"question_id": "q-2606e5a9", "submitted_answer": ["b"]},
    {"question_id": "q-7e61da34", "submitted_answer": ["b"]},
    {"question_id": "q-5107e458", "submitted_answer": ["a", "c"]},
    {"question_id": "q-ff842389", "submitted_answer": ["c"]},
    {"question_id": "q-502075d9", "submitted_answer": ["a"]},
    {"question_id": "q-17127db8", "submitted_answer": ["b"]},
    {"question_id": "q-31e312d0", "submitted_answer": ["b", "d"]},
    {"question_id": "q-1aec130a", "submitted_answer": ["a"]},
    {"question_id": "q-6a5aa6d1", "submitted_answer": ["a"]},
    {"question_id": "q-a1176c9e", "submitted_answer": ["a"]}
  ]
}
'''