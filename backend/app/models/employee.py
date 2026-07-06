"""
Employee model for database.
"""
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from app.db.base import Base, TimestampMixin


class Employee(Base, TimestampMixin):
    """
    Employee model representing users in the system.
    
    Note: This is a simplified model. In production, this might be synced
    with Team 1's employee data or use a shared authentication service.
    """

    __tablename__ = "employees"

    employee_id = Column(String, primary_key=True, index=True)
    employee_name = Column(String, nullable=True)
    email = Column(String, nullable=True)
    
    # Relationships
    quiz_attempts = relationship("Attempt", back_populates="employee", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"<Employee(employee_id={self.employee_id}, employee_name={self.employee_name})>"
