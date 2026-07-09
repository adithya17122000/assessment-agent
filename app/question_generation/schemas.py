from typing import List, Dict
from pydantic import BaseModel


class QuestionGenerationRequest(BaseModel):
    assessment_id: str
    question_count: int = 10


class QuestionResponse(BaseModel):
    id: str
    assessment_id: str
    sequence_number: int
    question_text: str
    question_type: str
    options: dict
    correct_answer: List[str]

    class Config:
        from_attributes = True


class QuestionForFrontend(BaseModel):
    id: str
    sequence_number: int
    question_text: str
    question_type: str
    options: Dict[str, str]

    class Config:
        from_attributes = True