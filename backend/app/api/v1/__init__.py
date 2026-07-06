"""API v1 routes."""

from fastapi import APIRouter

from . import employees, quizzes

api_router = APIRouter()

# Include routers
api_router.include_router(employees.router)
api_router.include_router(quizzes.router)
