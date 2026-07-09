from datetime import date, datetime
from typing import List, Optional
from pydantic import BaseModel


class AssessmentEligibilityCreate(BaseModel):
    employee_id: str
    employee_name: Optional[str] = None
    course_id: str
    course_name: str
    module_name: Optional[str] = None
    topics: List[str]
    difficulty: str
    completion_date: date

class CourseEligibilitySummary(BaseModel):
    course_id: str
    course_name: str
    union_topics: List[str]
    latest_topics: List[str]
    latest_completion_date: str

class AssessmentEligibilityResponse(BaseModel):
    id: str
    employee_id: str
    course_id: str
    course_name: str
    module_name: Optional[str]
    topics: List[str]
    difficulty: str
    completion_date: date
    created_at: datetime

    class Config:
        from_attributes = True  # Pydantic v2; use orm_mode = True if you're on v1