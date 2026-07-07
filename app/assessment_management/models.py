# app/assessment_management/models.py
from sqlalchemy import Column, String, DateTime, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.sql import func

from app.config.database import Base


class AssessmentRequest(Base):
    __tablename__ = "assessment_request"

    id = Column(String, primary_key=True)
    employee_id = Column(String, nullable=False, index=True)
    course_id = Column(String, nullable=False, index=True)
    course_name = Column(String, nullable=False)
    module_id = Column(String, nullable=True)
    module_name = Column(String, nullable=True)
    topics = Column(JSONB, nullable=False)
    difficulty = Column(String, nullable=False)
    request_timestamp = Column(DateTime(timezone=True), server_default=func.now())


class Assessment(Base):
    __tablename__ = "assessment"

    id = Column(String, primary_key=True)
    request_id = Column(String, ForeignKey("assessment_request.id"), nullable=False, index=True)
    status = Column(String, nullable=False, default="In Progress")  # unconfirmed enum, revisit later
    question_count = Column(Integer, nullable=False, default=10)
    started_at = Column(DateTime(timezone=True), server_default=func.now())
    submitted_at = Column(DateTime(timezone=True), nullable=True)