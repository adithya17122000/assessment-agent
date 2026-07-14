import os
import requests
from dotenv import load_dotenv

load_dotenv()

TEAM3_WEBHOOK_URL = os.getenv("TEAM3_WEBHOOK_URL")
TEAM3_SERVICE_TOKEN = os.getenv("TEAM3_SERVICE_TOKEN")


def notify_team3_quiz_result(
    user_id: str,
    course_id: str,
    course_name: str,
    assessment_id: str,
    score: int,
    pass_threshold: int,
    pass_fail_status: str,
    feedback: str,
    weak_topics: list[str],
    attempted_on: str,
) -> dict:
    payload = {
        "user_id": user_id,
        "skill_id": course_id,
        "quiz_id": assessment_id,
        "course": course_name,
        "score": score,
        "pass_threshold": pass_threshold,
        "status": "passed" if pass_fail_status == "Pass" else "failed",
        "feedback": feedback or "",
        "weak_topics": weak_topics or [],
        "attempted_on": attempted_on,
    }

    headers = {
        "Authorization": f"Bearer {TEAM3_SERVICE_TOKEN}",
        "Content-Type": "application/json",
    }

    try:
        response = requests.post(TEAM3_WEBHOOK_URL, json=payload, headers=headers, timeout=5)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Team 3 webhook failed: {e}")
        return None