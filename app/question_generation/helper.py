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
        f"Generate exactly {question_count} {difficulty.lower()} level questions "
        f"on {course_name}, covering the topics: {topics_str}.\n\n"
        f"The {question_count} questions must follow this exact distribution:\n"
        f"- 6 single-answer multiple-choice questions, with 4 options (keys a, b, c, d) and exactly ONE correct answer.\n"
        f"- 2 boolean questions, with exactly 2 options (keys a, b representing True/False) and exactly ONE correct answer.\n"
        f"- 2 multi-select questions, with 4 options (keys a, b, c, d) where MORE THAN ONE option is correct "
        f"(e.g. correct_answer could be [\"a\", \"c\"] or [\"b\", \"c\", \"d\"]).\n\n"
        f"For multi-select questions ONLY: the 'question' field must begin with 'Select all that are true: ' "
        f"followed by the actual question text. Single-answer and boolean questions must NOT have this prefix.\n\n"
        f"Return ONLY a JSON array, no other text, in this exact format:\n"
        f'[\n'
        f'  {{"question": "...", "topic": "...", "options": {{"a": "...", "b": "...", "c": "...", "d": "..."}}, "correct_answer": ["a"]}},\n'
        f'  {{"question": "...", "topic": "...", "options": {{"a": "True", "b": "False"}}, "correct_answer": ["a"]}},\n'
        f'  {{"question": "Select all that are true: ...", "topic": "...", "options": {{"a": "...", "b": "...", "c": "...", "d": "..."}}, "correct_answer": ["a", "c"]}}\n'
        f']\n\n'
        f"Rules:\n"
        f"- The 'topic' field must be exactly one of the provided topics: {topics_str}.\n"
        f"- The 'options' field must be a dictionary with keys a, b, c, d for MCQ/multi-select, or a, b for boolean.\n"
        f"- The 'correct_answer' field must contain ONLY the option keys (e.g. 'a', 'b'), never the option text itself.\n"
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
        
        valid_keys = set(q["options"].keys())
        invalid_answers = [a for a in q["correct_answer"] if a not in valid_keys]
        if invalid_answers:
            raise QuestionParseError(f"Question at index {i}: correct_answer contains values not in options keys: {invalid_answers}")

    return parsed

if __name__ == "__main__":
    prompt = build_question_prompt("Python Programming", "Intermediate", ["Functions", "Loops"], 10)
    from app.question_generation.helper import parse_llm_response
    from app.question_generation.llm_client import call_llm
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