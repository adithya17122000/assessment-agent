"""
Pagination schemas for API responses.
"""
from typing import Generic, List, TypeVar

from pydantic import BaseModel, Field

T = TypeVar("T")


class PaginationParams(BaseModel):
    """
    Pagination query parameters.
    """

    limit: int = Field(default=20, ge=1, le=100, description="Maximum items per page")
    offset: int = Field(default=0, ge=0, description="Number of items to skip")
    search: str | None = Field(default=None, description="Search query string")


class PaginationMeta(BaseModel):
    """
    Pagination metadata included in responses.
    """

    limit: int = Field(description="Items per page")
    offset: int = Field(description="Items skipped")
    total: int = Field(description="Total items available")
    has_more: bool = Field(description="Whether more items exist")

    @classmethod
    def create(cls, limit: int, offset: int, total: int) -> "PaginationMeta":
        """Create pagination metadata."""
        return cls(
            limit=limit,
            offset=offset,
            total=total,
            has_more=(offset + limit) < total,
        )


class PaginatedResponse(BaseModel, Generic[T]):
    """
    Generic paginated response wrapper.
    """

    items: List[T]
    pagination: PaginationMeta

    class Config:
        """Pydantic configuration."""

        from_attributes = True
