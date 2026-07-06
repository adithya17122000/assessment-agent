"""
Employee schemas for request/response validation.
"""
from pydantic import BaseModel, Field


class EmployeeBase(BaseModel):
    """Base employee schema with common attributes."""

    employee_id: str = Field(description="Unique identifier of the employee")


class Employee(EmployeeBase):
    """Employee schema."""

    employee_name: str | None = Field(default=None, description="Employee name")
    email: str | None = Field(default=None, description="Employee email")

    class Config:
        """Pydantic configuration."""

        from_attributes = True


class EmployeeCreate(BaseModel):
    """Schema for creating a new employee."""

    employee_id: str
    employee_name: str | None = None
    email: str | None = None
