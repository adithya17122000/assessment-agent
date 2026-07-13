from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from typing import List


class AssessmentResultSummary(BaseModel):
    assessment_id: str
    user_id: str
    course_id: str
    course_name: str
    status: str
    score: Optional[int]
    total_questions: Optional[int]
    pass_fail_status: Optional[str]
    submitted_at: Optional[datetime]


class CourseStatusSummary(BaseModel):
    course_id: str
    course_name: str
    status: str
    pass_fail_status: Optional[str]
    attempt_count: int


class UserAssessmentStats(BaseModel):
    user_id: str
    courses: List[CourseStatusSummary]