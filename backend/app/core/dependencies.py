"""
Dependency injection for FastAPI routes.
"""
from typing import Generator

from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.config import Settings, get_settings
from app.db.database import SessionLocal


def get_db() -> Generator[Session, None, None]:
    """
    Database session dependency.
    Yields a database session and ensures it's closed after use.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_settings() -> Settings:
    """
    Get current application settings.
    """
    return get_settings()


# Placeholder for future authentication
async def get_current_user():
    """
    Get current authenticated user from JWT token.
    TODO: Implement Supabase JWT validation.
    
    For now, this is a placeholder that can be implemented later.
    """
    # This will be implemented when Supabase auth is added
    pass


def validate_pagination_params(
    limit: int = 20,
    offset: int = 0,
    settings: Settings = Depends(get_current_settings),
) -> dict:
    """
    Validate and return pagination parameters.
    
    Args:
        limit: Maximum number of items to return
        offset: Number of items to skip
        settings: Application settings
        
    Returns:
        Dictionary with validated limit and offset
        
    Raises:
        HTTPException: If parameters are invalid
    """
    if limit < 1:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Limit must be greater than 0",
        )
    
    if limit > settings.MAX_PAGE_SIZE:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Limit cannot exceed {settings.MAX_PAGE_SIZE}",
        )
    
    if offset < 0:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Offset must be greater than or equal to 0",
        )
    
    return {"limit": limit, "offset": offset}
