import uuid
from sqlalchemy.orm import Session

from app.question_generation.models import Question
from app.question_generation.helper import build_question_prompt, get_questions_by_assessment, parse_llm_response
from app.question_generation.llm_client import call_llm
from app.assessment_management.models import Assessment, AssessmentRequest


def get_generation_context(db: Session, assessment_id: str) -> AssessmentRequest:
    """
    Looks up the AssessmentRequest tied to this Assessment, so callers
    never need to supply course_name/difficulty/topics manually — those
    values are read from the system's own records, not trusted from input.
    """
    assessment = db.query(Assessment).filter(Assessment.id == assessment_id).first()
    if not assessment:
        raise ValueError(f"No Assessment found for id={assessment_id}")

    request = db.query(AssessmentRequest).filter(AssessmentRequest.id == assessment.request_id).first()
    if not request:
        raise ValueError(f"No AssessmentRequest found for assessment_id={assessment_id}")

    return request


def generate_questions_for_assessment(db: Session, assessment_id: str, question_count: int = 10) -> list[Question]:
    
    existing = db.query(Question).filter(Question.assessment_id == assessment_id).all()
    if existing:
        return existing
    
    request = get_generation_context(db, assessment_id)

    prompt = build_question_prompt(
        course_name=request.course_name,
        difficulty=request.difficulty,
        topics=request.topics,
        question_count=question_count,
    )

    raw_response = call_llm(prompt)
    parsed_questions = parse_llm_response(raw_response)

    question_rows = []
    for i, q in enumerate(parsed_questions, start=1):
        row = Question(
            id=f"q-{uuid.uuid4().hex[:8]}",
            assessment_id=assessment_id,
            sequence_number=i,
            question_text=q["question"],
            question_type="MCQ",
            options=q["options"],
            correct_answer=q["correct_answer"],
        )
        db.add(row)
        question_rows.append(row)

    db.commit()
    return question_rows

def get_questions_for_frontend(db: Session, assessment_id: str):
    return get_questions_by_assessment(db, assessment_id)