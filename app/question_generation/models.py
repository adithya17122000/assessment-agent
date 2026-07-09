from sqlalchemy import Column, String, Integer
from sqlalchemy.dialects.postgresql import JSONB

from app.config.database import Base


class Question(Base):
    __tablename__ = "question"

    id = Column(String, primary_key=True)
    assessment_id = Column(String, nullable=False, index=True)
    sequence_number = Column(Integer, nullable=False)  
    question_text = Column(String, nullable=False)
    question_type = Column(String, nullable=False, default="MCQ")
    options = Column(JSONB, nullable=False)         
    correct_answer = Column(JSONB, nullable=False)  