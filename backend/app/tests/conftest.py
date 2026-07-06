"""
Pytest configuration and fixtures for testing.
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.db.base import Base
from app.core.dependencies import get_db
from app.main import app

# Use in-memory SQLite database for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db_session():
    """Create a fresh database session for each test."""
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db_session):
    """Create a test client with database session override."""
    
    def override_get_db():
        try:
            yield db_session
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture
def sample_quiz(db_session):
    """Create a sample quiz for testing."""
    from app.models.quiz import Quiz
    
    quiz = Quiz(
        quiz_id="Q101",
        skill_id="108",
        course="Learning FastAPI Fundamentals",
        pass_threshold=60,
    )
    db_session.add(quiz)
    db_session.commit()
    db_session.refresh(quiz)
    return quiz


@pytest.fixture
def sample_employee(db_session):
    """Create a sample employee for testing."""
    from app.models.employee import Employee
    
    employee = Employee(
        employee_id="usr_9823471",
        employee_name="Test User",
        email="test@example.com",
    )
    db_session.add(employee)
    db_session.commit()
    db_session.refresh(employee)
    return employee


@pytest.fixture
def sample_attempt(db_session, sample_employee, sample_quiz):
    """Create a sample attempt for testing."""
    from app.models.attempt import Attempt, AttemptStatus
    from datetime import datetime
    
    attempt = Attempt(
        employee_id=sample_employee.employee_id,
        quiz_id=sample_quiz.quiz_id,
        score=82,
        status=AttemptStatus.PASSED,
        feedback="Great job!",
        attempted_on=datetime.utcnow(),
    )
    db_session.add(attempt)
    db_session.commit()
    db_session.refresh(attempt)
    return attempt
