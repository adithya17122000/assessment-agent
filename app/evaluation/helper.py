# app/evaluation/repository.py — updated to match
import uuid
from sqlalchemy.orm import Session
from app.evaluation.models import Response


def bulk_insert_responses(db: Session, assessment_id: str, answers: list) -> list[Response]:
    response_rows = []
    for answer in answers:
        row = Response(
            id=f"resp-{uuid.uuid4().hex[:8]}",
            question_id=answer.question_id,
            assessment_id=assessment_id,
            submitted_answer=answer.submitted_answer,
        )
        db.add(row)
        response_rows.append(row)
    db.commit()
    return response_rows

def is_answer_correct(submitted_answer: list[str], correct_answer: list[str]) -> bool:
    """
    Exact-set match: submitted answer counts as correct only if the set of
    selected options exactly matches the set of correct options - no partial
    credit for multi-select questions.
    """
    return set(submitted_answer) == set(correct_answer)