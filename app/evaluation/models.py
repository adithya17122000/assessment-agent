# app/evaluation/models.py
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from sqlalchemy.sql import func

from app.config.database import Base


class Response(Base):
    __tablename__ = "response"

    id = Column(String, primary_key=True)
    question_id = Column(String, ForeignKey("question.id"), nullable=False, index=True)
    assessment_id = Column(String, ForeignKey("assessment.id"), nullable=False, index=True)
    submitted_answer = Column(String, nullable=False)
    answered_at = Column(DateTime(timezone=True), server_default=func.now())


class Evaluation(Base):
    __tablename__ = "evaluation"

    id = Column(String, primary_key=True)
    assessment_id = Column(String, ForeignKey("assessment.id"), nullable=False, index=True)
    score = Column(Integer, nullable=True)
    total_questions = Column(Integer, nullable=False)
    pass_fail_status = Column(String, nullable=True)
    evaluated_at = Column(DateTime(timezone=True), nullable=True)