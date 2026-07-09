# app/api/question_generation_routes.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.config.database import get_db
from app.question_generation.schemas import QuestionGenerationRequest, QuestionResponse
from app.question_generation.service import generate_questions_for_assessment
from app.question_generation.helper import QuestionParseError
from app.question_generation.schemas import QuestionForFrontend
from app.question_generation.service import get_questions_for_frontend


router = APIRouter(prefix="/question-generation", tags=["Question Generation"])


@router.post("/", response_model=List[QuestionResponse])
def generate_questions(payload: QuestionGenerationRequest, db: Session = Depends(get_db)):
    try:
        return generate_questions_for_assessment(
            db=db,
            assessment_id=payload.assessment_id,
        )
    except QuestionParseError as e:
        raise HTTPException(status_code=502, detail=f"LLM response could not be parsed: {e}")
    
@router.get("/{assessment_id}", response_model=List[QuestionForFrontend])
def get_questions(assessment_id: str, db: Session = Depends(get_db)):
    questions = get_questions_for_frontend(db, assessment_id)
    if not questions:
        raise HTTPException(status_code=404, detail=f"No questions found for assessment_id={assessment_id}")
    return questions