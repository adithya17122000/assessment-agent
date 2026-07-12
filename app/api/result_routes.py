from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.config.database import get_db
from app.result_management.schemas import AssessmentResultSummary
from app.result_management.service import get_user_results

router = APIRouter(prefix="/results", tags=["Result Management"])


@router.get("/{user_id}", response_model=List[AssessmentResultSummary])
def get_results(user_id: str, db: Session = Depends(get_db)):
    return get_user_results(db, user_id)