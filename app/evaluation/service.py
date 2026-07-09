# app/evaluation/service.py — final combined version
import uuid
from sqlalchemy.orm import Session

from app.evaluation import helper
from app.evaluation.models import Evaluation, Response
from app.evaluation.helper import is_answer_correct
from app.evaluation.schemas import BulkResponseSubmission
from app.question_generation.models import Question
from app.config.settings import PASS_THRESHOLD_PERCENT


def submit_and_evaluate(db: Session, payload: BulkResponseSubmission) -> Evaluation:
    # Step 1: bulk insert raw responses
    helper.bulk_insert_responses(db, payload.assessment_id, payload.answers)

    # Step 2: score immediately, same request
    return evaluate_assessment(db, payload.assessment_id)


def evaluate_assessment(db: Session, assessment_id: str) -> Evaluation:
    responses = db.query(Response).filter(Response.assessment_id == assessment_id).all()
    questions = db.query(Question).filter(Question.assessment_id == assessment_id).all()

    question_lookup = {q.id: q for q in questions}

    total_questions = len(questions)
    correct_count = 0

    for response in responses:
        question = question_lookup.get(response.question_id)
        if not question:
            continue
        if is_answer_correct(response.submitted_answer, question.correct_answer):
            correct_count += 1

    score_percent = (correct_count / total_questions) * 100 if total_questions else 0
    pass_fail_status = "Pass" if score_percent >= PASS_THRESHOLD_PERCENT else "Fail"

    evaluation = Evaluation(
        id=f"eval-{uuid.uuid4().hex[:8]}",
        assessment_id=assessment_id,
        score=correct_count,
        total_questions=total_questions,
        pass_fail_status=pass_fail_status,
    )
    db.add(evaluation)
    db.commit()
    db.refresh(evaluation)
    return evaluation