from sqlalchemy.orm import Session
from app.result_management import helper
from app.result_management.schemas import AssessmentResultSummary
from app.result_management.schemas import CourseStatusSummary, UserAssessmentStats


def get_user_results(db: Session, user_id: str) -> list[AssessmentResultSummary]:
    rows = helper.get_results_by_user(db, user_id)

    results = []
    for assessment, request, evaluation in rows:
        results.append(
            AssessmentResultSummary(
                assessment_id=assessment.id,
                user_id=request.user_id,
                course_id=request.course_id,
                course_name=request.course_name,
                status=assessment.status,
                score=evaluation.score if evaluation else None,
                total_questions=evaluation.total_questions if evaluation else None,
                pass_fail_status=evaluation.pass_fail_status if evaluation else None,
                submitted_at=assessment.submitted_at,
            )
        )
    return results

def get_user_stats(db: Session, user_id: str) -> UserAssessmentStats:
    rows = helper.get_course_status_counts(db, user_id)

    courses = [
        CourseStatusSummary(
            course_id=row.course_id,
            course_name=row.course_name,
            status=row.status,
            pass_fail_status=row.pass_fail_status,
            attempt_count=row.attempt_count,
        )
        for row in rows
    ]

    return UserAssessmentStats(user_id=user_id, courses=courses)