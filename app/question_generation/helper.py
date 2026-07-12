import json
from typing import List
from sqlalchemy.orm import Session
from app.question_generation.models import Question



class QuestionParseError(Exception):
    pass

def get_questions_by_assessment(db: Session, assessment_id: str):
    return (
        db.query(Question)
        .filter(Question.assessment_id == assessment_id)
        .order_by(Question.sequence_number.asc())
        .all()
    )

def build_question_prompt(course_name: str, difficulty: str, topics: list[str], question_count: int = 10) -> str:
    topics_str = ", ".join(topics)
    return (
        f"Generate {question_count} {difficulty.lower()} level questions "
        f"on {course_name}, covering the topics: {topics_str}.\n\n"
        f"You can include:\n"
        f"- Multiple-choice questions with 4 options.\n"
        f"- Boolean questions with True/False (2 options).\n"
        f"- Questions with multiple correct answers, where 'correct_answer' contains all correct values.\n\n"
        f"Return ONLY a JSON array, no other text, in this exact format:\n"
        f'[\n'
        f'  {{"question": "...", "topic": "...", "options": {{"a": "...", "b": "...", "c": "...", "d": "..."}}, "correct_answer": ["..."]}},\n'
        f'  {{"question": "...", "topic": "...", "options": {{"a": "True", "b": "False"}}, "correct_answer": ["..."]}}\n'
        f']\n\n'
        f"Rules:\n"
        f"- The 'topic' field must be exactly one of the provided topics: {topics_str}.\n"
        f"- The 'options' field must be a dictionary with keys a, b, c, d for MCQ, or a, b for boolean.\n"
        f"- The 'correct_answer' field must always be a list, even for single-answer questions.\n"
        f"- Do not deviate from the provided topics.\n"
        f"- Do not include code snippets, markdown, explanations, or special characters such as `, *, or \\n.\n"
        f"- Do not include any text outside the JSON array.\n"
        f"- Ensure the JSON is valid and parsable."
    )

def parse_llm_response(raw_response: str) -> List[dict]:
    cleaned = raw_response.strip()
    if cleaned.startswith("```"):
        cleaned = cleaned.strip("`")
        cleaned = cleaned.replace("json", "", 1).strip()

    try:
        parsed = json.loads(cleaned)
    except json.JSONDecodeError as e:
        raise QuestionParseError(f"LLM response was not valid JSON: {e}")

    if not isinstance(parsed, list):
        raise QuestionParseError("Expected a JSON array of questions.")

    for i, q in enumerate(parsed):
        if not all(k in q for k in ("question", "topic", "options", "correct_answer")):
            raise QuestionParseError(f"Question at index {i} missing required fields.")
        if not isinstance(q["options"], dict):
            raise QuestionParseError(f"Question at index {i}: options must be a dict, got {type(q['options'])}")
        if not isinstance(q["correct_answer"], list):
            raise QuestionParseError(f"Question at index {i}: correct_answer must be a list, got {type(q['correct_answer'])}")

    return parsed

if __name__ == "__main__":
    prompt = build_question_prompt("Python Programming", "Intermediate", ["Functions", "Loops"], 10)
    from app.question_generation.helper import parse_llm_response
    from app.question_generation.llm_client import call_llm
    import ipdb;ipdb.set_trace(context=15)
    raw_response = call_llm(prompt)
    print(raw_response)

    try:
        parsed_questions = parse_llm_response(raw_response)
        for q in parsed_questions:
            print(q.get("question"))
            print(q.get("topic"))
            print(q.get("options"))
            print(q.get("correct_answer"))
            print("-" * 20)
    except Exception as e:
        print(f"Error parsing LLM response: {e}")