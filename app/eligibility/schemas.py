from datetime import date, datetime
from typing import List, Optional
from pydantic import BaseModel


class AssessmentEligibilityCreate(BaseModel):
    user_id: str
    user_name: Optional[str] = None
    course_id: str
    course_name: str
    module_name: Optional[str] = None
    module_id: Optional[str] = None
    topics: List[str]
    difficulty: str
    completion_date: date

class CourseEligibilitySummary(BaseModel):
    course_id: str
    course_name: str
    topics: List[str]
    # latest_topics: List[str]
    latest_completion_date: str
    difficulty: Optional[str] = None
    module_id: Optional[str] = None
    module_name: Optional[str] = None

class AssessmentEligibilityResponse(BaseModel):
    id: str
    user_id: str
    course_id: str
    course_name: str
    module_id: Optional[str] = None
    module_name: Optional[str] = None
    topics: List[str]
    difficulty: str
    completion_date: date
    created_at: datetime

    class Config:
        from_attributes = True  # Pydantic v2; use orm_mode = True if you're on v1

class EligibilityCreateResponse(BaseModel):
    message: str
    eligibility_id: str

class MockTakeAssessmentPayload(BaseModel):
    user_id: str
    course_id: str
    course_name: str
    module_id: Optional[str] = None
    module_name: Optional[str] = None
    topics: List[str]
    difficulty: str


class EligibilitySummaryResponse(BaseModel):
    courses: List[CourseEligibilitySummary]
    message: Optional[str] = None