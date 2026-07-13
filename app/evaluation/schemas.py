# app/evaluation/schemas.py — complete file, all three classes
from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel


class AnswerSubmission(BaseModel):
    question_id: str
    submitted_answer: List[str]


class BulkResponseSubmission(BaseModel):
    assessment_id: str
    answers: List[AnswerSubmission]


class EvaluationResponse(BaseModel):
    assessment_id: str
    score: int
    total_questions: int
    pass_fail_status: Optional[str]
    evaluated_at: datetime

    class Config:
        from_attributes = True


class AnswerReview(BaseModel):
    question_id: str
    question_text: str
    options: dict
    submitted_answer: List[str]
    correct_answer: List[str]
    is_correct: bool


class AssessmentReview(BaseModel):
    assessment_id: str
    score: int
    total_questions: int
    pass_fail_status: str
    answers: List[AnswerReview]