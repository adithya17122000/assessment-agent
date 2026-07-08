# app/eligibility/models.py
from sqlalchemy import Column, String, Date, DateTime
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.sql import func

from app.config.database import Base


class AssessmentEligibility(Base):
    __tablename__ = "assessment_eligibility"

    id = Column(String, primary_key=True)
    employee_id = Column(String, nullable=False, index=True)
    employee_name = Column(String, nullable=True)
    course_id = Column(String, nullable=False, index=True)
    course_name = Column(String, nullable=False)
    module_name = Column(String, nullable=True)
    topics = Column(JSONB, nullable=False)
    difficulty = Column(String, nullable=False)
    completion_date = Column(Date, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())