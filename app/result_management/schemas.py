# app/result_management/schemas.py — add these
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel


class EmployeeAssessmentSummary(BaseModel):
    assessment_id: str
    course_id: str
    course: str
    last_score: Optional[int]
    pass_threshold: int
    status: str


class EmployeeAssessmentsResponse(BaseModel):
    user_id: str
    assessments: List[EmployeeAssessmentSummary]
    pagination: dict


class AssessmentAttemptEntry(BaseModel):
    assessment_id: str
    course_id: str
    course: str
    score: Optional[int]
    status: str
    attempted_on: Optional[datetime]
    feedback: Optional[str]


class EmployeeAssessmentAttemptsResponse(BaseModel):
    user_id: str
    attempts: List[AssessmentAttemptEntry]
    pagination: dict


class CourseAssessmentAttemptEntry(BaseModel):
    user_id: str
    assessment_id: str
    score: Optional[int]
    status: str
    attempted_on: Optional[datetime]


class CourseAssessmentAttemptsResponse(BaseModel):
    course_id: str
    attempts: List[CourseAssessmentAttemptEntry]
    pagination: dict