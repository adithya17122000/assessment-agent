# app/assessment_management/schemas.py
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel
from app.question_generation.schemas import QuestionForFrontend


class TakeAssessmentRequest(BaseModel):
    employee_id: str
    course_id: str
    course_name: str
    module_id: Optional[str] = None
    module_name: Optional[str] = None
    topics: List[str]
    difficulty: str


class AssessmentRequestResponse(BaseModel):
    id: str
    employee_id: str
    course_id: str
    course_name: str
    module_id: Optional[str]
    module_name: Optional[str]
    topics: List[str]
    difficulty: str
    request_timestamp: datetime

    class Config:
        from_attributes = True


class AssessmentResponse(BaseModel):
    id: str
    request_id: str
    status: str
    question_count: int
    started_at: datetime
    submitted_at: Optional[datetime]

    class Config:
        from_attributes = True


class TakeAssessmentResponse(BaseModel):
    assessment_request: AssessmentRequestResponse
    assessment: AssessmentResponse


class TakeAssessmentAndQuestionsResponse(BaseModel):
    assessment_id: str
    questions: List[QuestionForFrontend]