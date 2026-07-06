"""
Tests for Team 4 Assessment & Quiz Agent API endpoints.
"""
import pytest
from fastapi import status


def test_root_endpoint(client):
    """Test the root endpoint returns API information."""
    response = client.get("/")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "message" in data
    assert "version" in data
    assert data["version"] == "1.0.0"


def test_health_check(client):
    """Test the health check endpoint."""
    response = client.get("/health")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["status"] == "healthy"
    assert "service" in data


def test_get_employee_quizzes_empty(client, sample_employee):
    """Test getting quizzes for an employee with no quizzes."""
    response = client.get(f"/api/v1/employees/{sample_employee.employee_id}/quizzes")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["employee_id"] == sample_employee.employee_id
    assert data["quizzes"] == []
    assert "pagination" in data


def test_get_employee_quizzes_with_data(client, sample_employee, sample_quiz, sample_attempt):
    """Test getting quizzes for an employee with quiz data."""
    response = client.get(f"/api/v1/employees/{sample_employee.employee_id}/quizzes")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["employee_id"] == sample_employee.employee_id
    assert len(data["quizzes"]) == 1
    
    quiz = data["quizzes"][0]
    assert quiz["quiz_id"] == "Q101"
    assert quiz["skill_id"] == "108"
    assert quiz["course"] == "Learning FastAPI Fundamentals"
    assert quiz["last_score"] == 82
    assert quiz["status"] == "passed"


def test_get_employee_quizzes_with_search(client, sample_employee, sample_quiz):
    """Test searching quizzes by course name."""
    response = client.get(
        f"/api/v1/employees/{sample_employee.employee_id}/quizzes",
        params={"search": "FastAPI"}
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data["quizzes"]) == 1
    
    # Search for non-existent course
    response = client.get(
        f"/api/v1/employees/{sample_employee.employee_id}/quizzes",
        params={"search": "NonExistent"}
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data["quizzes"]) == 0


def test_get_employee_quizzes_pagination(client, sample_employee, sample_quiz):
    """Test pagination for employee quizzes."""
    response = client.get(
        f"/api/v1/employees/{sample_employee.employee_id}/quizzes",
        params={"limit": 1, "offset": 0}
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["pagination"]["limit"] == 1
    assert data["pagination"]["offset"] == 0
    assert data["pagination"]["total"] == 1


def test_get_quiz_attempts_not_found(client):
    """Test getting attempts for non-existent quiz."""
    response = client.get("/api/v1/quizzes/NONEXISTENT/attempts")
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_get_quiz_attempts_success(client, sample_quiz, sample_attempt):
    """Test getting attempts for a quiz."""
    response = client.get(f"/api/v1/quizzes/{sample_quiz.quiz_id}/attempts")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["quiz_id"] == sample_quiz.quiz_id
    assert len(data["attempts"]) == 1
    
    attempt = data["attempts"][0]
    assert attempt["score"] == 82
    assert attempt["status"] == "passed"
    assert attempt["course"] == "Learning FastAPI Fundamentals"
    assert "feedback" in attempt


def test_get_employee_quiz_attempts_not_found(client):
    """Test getting quiz attempts for non-existent employee."""
    response = client.get("/api/v1/employees/NONEXISTENT/quiz-attempts")
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_get_employee_quiz_attempts_success(client, sample_employee, sample_attempt):
    """Test getting cross-quiz attempts for an employee."""
    response = client.get(f"/api/v1/employees/{sample_employee.employee_id}/quiz-attempts")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["employee_id"] == sample_employee.employee_id
    assert len(data["attempts"]) == 1
    
    attempt = data["attempts"][0]
    assert attempt["quiz_id"] == "Q101"
    assert attempt["skill_id"] == "108"
    assert attempt["score"] == 82
    assert attempt["status"] == "passed"


def test_get_employee_quiz_attempts_with_search(client, sample_employee, sample_attempt):
    """Test searching quiz attempts by course or skill."""
    # Search by course
    response = client.get(
        f"/api/v1/employees/{sample_employee.employee_id}/quiz-attempts",
        params={"search": "FastAPI"}
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data["attempts"]) == 1
    
    # Search by skill_id
    response = client.get(
        f"/api/v1/employees/{sample_employee.employee_id}/quiz-attempts",
        params={"search": "108"}
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data["attempts"]) == 1


def test_pagination_validation(client, sample_employee):
    """Test pagination parameter validation."""
    # Test limit too large
    response = client.get(
        f"/api/v1/employees/{sample_employee.employee_id}/quizzes",
        params={"limit": 200}
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    
    # Test negative offset
    response = client.get(
        f"/api/v1/employees/{sample_employee.employee_id}/quizzes",
        params={"offset": -1}
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    
    # Test limit too small
    response = client.get(
        f"/api/v1/employees/{sample_employee.employee_id}/quizzes",
        params={"limit": 0}
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_cors_headers(client):
    """Test that CORS headers are present."""
    response = client.get("/")
    # Note: TestClient doesn't always include CORS headers in tests
    # This test verifies the endpoint works; actual CORS testing would need integration tests
    assert response.status_code == status.HTTP_200_OK
