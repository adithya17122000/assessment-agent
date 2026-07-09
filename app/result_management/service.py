from sqlalchemy.orm import Session
from app.result_management import helper
from app.result_management.schemas import AssessmentResultSummary


def get_employee_results(db: Session, employee_id: str) -> list[AssessmentResultSummary]:
    rows = helper.get_results_by_employee(db, employee_id)

    results = []
    for assessment, request, evaluation in rows:
        results.append(AssessmentResultSummary(
            assessment_id=assessment.id,
            employee_id=request.employee_id,
            course_id=request.course_id,
            course_name=request.course_name,
            status=assessment.status,
            score=evaluation.score if evaluation else None,
            total_questions=evaluation.total_questions if evaluation else None,
            pass_fail_status=evaluation.pass_fail_status if evaluation else None,
            submitted_at=assessment.submitted_at,
        ))
    return results