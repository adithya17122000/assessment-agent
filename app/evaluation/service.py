# app/evaluation/service.py — final combined version
import uuid
from sqlalchemy.orm import Session
from sqlalchemy.sql import func

from app.evaluation import helper
from app.evaluation.models import Evaluation, Response
from app.evaluation.helper import is_answer_correct
from app.evaluation.schemas import AssessmentReview, BulkResponseSubmission, AnswerReview
from app.question_generation.models import Question
from app.question_generation.llm_client import call_llm
from app.config.settings import PASS_THRESHOLD_PERCENT
from app.assessment_management.models import Assessment


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
    weak_topics = set()

    for response in responses:
        question = question_lookup.get(response.question_id)
        if not question:
            continue
        if is_answer_correct(response.submitted_answer, question.correct_answer):
            correct_count += 1
        else:
            weak_topics.add(question.topic)

    score_percent = (correct_count / total_questions) * 100 if total_questions else 0
    pass_fail_status = "Pass" if score_percent >= PASS_THRESHOLD_PERCENT else "Fail"
    weak_topics_list = sorted(weak_topics)

    feedback = generate_feedback(score_percent, weak_topics_list, pass_fail_status)

    evaluation = Evaluation(
        id=f"eval-{uuid.uuid4().hex[:8]}",
        assessment_id=assessment_id,
        score=correct_count,
        total_questions=total_questions,
        pass_fail_status=pass_fail_status,
        weak_topics=weak_topics_list,
        feedback=feedback,
    )
    db.add(evaluation)

    assessment = db.query(Assessment).filter(Assessment.id == assessment_id).first()
    if assessment:
        assessment.status = "Completed"
        assessment.submitted_at = func.now()

    db.commit()
    db.refresh(evaluation)
    return evaluation

def build_feedback_prompt(score_percent: float, weak_topics: list[str], pass_fail_status: str) -> str:
    if not weak_topics:
        return (
            "Write a short, encouraging feedback message (max 150 characters) "
            "for an employee who answered all quiz questions correctly."
        )
    topics_str = ", ".join(weak_topics)
    return (
        f"Write a short feedback message (max 150 characters) for an employee "
        f"who scored {round(score_percent)}% and struggled with these topics: {topics_str}. "
        f"Be constructive, not harsh. Return ONLY the feedback sentence, no extra text."
    )


def generate_feedback(score_percent: float, weak_topics: list[str], pass_fail_status: str) -> str:
    prompt = build_feedback_prompt(score_percent, weak_topics, pass_fail_status)
    try:
        raw = call_llm(prompt)
        return raw.strip()[:150]  # defensive truncation regardless of what LLM actually returns
    except Exception:
        return None 
    
def get_assessment_review(db: Session, assessment_id: str) -> AssessmentReview:
    evaluation = db.query(Evaluation).filter(Evaluation.assessment_id == assessment_id).first()
    if not evaluation:
        raise ValueError(f"No evaluation found for assessment_id={assessment_id} — assessment not yet submitted.")

    responses = db.query(Response).filter(Response.assessment_id == assessment_id).all()
    questions = db.query(Question).filter(Question.assessment_id == assessment_id).all()
    evaluation = db.query(Evaluation).filter(Evaluation.assessment_id == assessment_id).first()

    question_lookup = {q.id: q for q in questions}

    answer_reviews = []
    for response in responses:
        question = question_lookup.get(response.question_id)
        if not question:
            continue
        answer_reviews.append(AnswerReview(
            question_id=question.id,
            question_text=question.question_text,
            options=question.options,
            submitted_answer=response.submitted_answer,
            correct_answer=question.correct_answer,
            is_correct=is_answer_correct(response.submitted_answer, question.correct_answer),
        ))

    return AssessmentReview(
        assessment_id=assessment_id,
        score=evaluation.score,
        total_questions=evaluation.total_questions,
        pass_fail_status=evaluation.pass_fail_status,
        answers=answer_reviews,
    )