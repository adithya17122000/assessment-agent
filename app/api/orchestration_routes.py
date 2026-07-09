from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.config.database import get_db
from app.assessment_management.schemas import TakeAssessmentRequest, TakeAssessmentAndQuestionsResponse
from app.assessment_management import service as assessment_service
from app.question_generation.service import generate_questions_for_assessment
from app.question_generation.helper import QuestionParseError

router = APIRouter(prefix="/take-assessment", tags=["Take Assessment (Orchestration)"])


@router.post("/", response_model=TakeAssessmentAndQuestionsResponse)
def take_assessment_and_generate(payload: TakeAssessmentRequest, db: Session = Depends(get_db)):
    assessment_request, assessment = assessment_service.take_assessment(db, payload)

    try:
        questions = generate_questions_for_assessment(db, assessment_id=assessment.id)
    except QuestionParseError as e:
        raise HTTPException(
            status_code=502,
            detail={"message": "Question generation failed. Please retry.", "assessment_id": assessment.id, "retryable": True}
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={"message": "Unexpected error during question generation.", "assessment_id": assessment.id, "retryable": True}
        )

    return TakeAssessmentAndQuestionsResponse(assessment_id=assessment.id, questions=questions)