"""
SQLAlchemy declarative base and common model mixins.
"""
from datetime import datetime
from typing import Any

from sqlalchemy import Column, DateTime
from sqlalchemy.orm import DeclarativeBase, declared_attr


class Base(DeclarativeBase):
    """
    Base class for all database models.
    """

    # Generate __tablename__ automatically from class name
    @declared_attr.directive
    def __tablename__(cls) -> str:
        return cls.__name__.lower()


class TimestampMixin:
    """
    Mixin to add created_at and updated_at timestamps to models.
    """

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )


# Import all models here so Alembic can detect them
from app.models.employee import Employee  # noqa: E402, F401
from app.models.quiz import Quiz  # noqa: E402, F401
from app.models.attempt import Attempt  # noqa: E402, F401
