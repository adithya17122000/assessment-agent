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
    return f"""
            Generate {question_count} {difficulty.lower()} level multiple-choice questions on {course_name}, covering the topics: {topics_str}.

            Return ONLY a JSON array, no other text, in this exact format.

            You can include:
            - Multiple-choice questions with options.
            - Boolean questions with True/False.
            - Question which can have multiple correct answers. In this case, the "correct_answer" field should contain all correct answers.
            - The "options" field must be a dictionary with keys a, b, c, d. if its boolean, then the options keys should be a,b
            - The "correct_answer" field must be a list containing all correct answers.
            - Do not deviate from the provided topics.
            - Do not include any code snippets in the questions or answers.
            - Do not include explanations, markdown, code snippets, or special characters such as `, *, or \\n.
            - Make sure the JSON is valid and parsable.

            [
            {{
                "question": "...",
                "options": {{
                "a": "...",
                "b": "...",
                "c": "...",
                "d": "..."
                }},
                "correct_answer": ["..."]
            }}
            ]
            """

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
        if not all(k in q for k in ("question", "options", "correct_answer")):
            raise QuestionParseError(f"Question at index {i} missing required fields.")
        if not isinstance(q["options"], dict):
            raise QuestionParseError(f"Question at index {i}: options must be a dict, got {type(q['options'])}")
        if not isinstance(q["correct_answer"], list):
            raise QuestionParseError(f"Question at index {i}: correct_answer must be a list, got {type(q['correct_answer'])}")

    return parsed

if __name__ == "__main__":
    # Example usage
    prompt = build_question_prompt("Python Programming", "Intermediate", ["Functions", "Loops"], 10)
    # print(prompt)
    # print("*"*40)
    from app.question_generation.helper import parse_llm_response
    from app.question_generation.llm_client import call_llm
    raw_response = call_llm(prompt)
    print(raw_response)
    try:
        parsed_questions = parse_llm_response(raw_response)
        for q in parsed_questions:
            print(q.get("question"))
            print(q.get("options"))
            print(q.get("correct_answer"))
            print("-"*20)
    except Exception as e:
        import ipdb; ipdb.set_trace()
        parsed_questions = parse_llm_response(raw_response)

        print(f"Error parsing LLM response: {e}")