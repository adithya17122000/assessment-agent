#!/usr/bin/env python3
"""
Database initialization script.
Creates all tables defined in SQLAlchemy models.
"""
import sys
from pathlib import Path

# Add the parent directory to the path so we can import app modules
sys.path.insert(0, str(Path(__file__).parent))

from app.db.database import engine
from app.db.base import Base
from app.core.config import get_settings

# Import all models to ensure they are registered with SQLAlchemy
from app.models.employee import Employee
from app.models.quiz import Quiz
from app.models.attempt import Attempt


def init_db():
    """Initialize the database by creating all tables."""
    settings = get_settings()
    
    print("=" * 60)
    print("Database Initialization")
    print("=" * 60)
    print(f"\nDatabase URL: {settings.DATABASE_URL.split('@')[1] if '@' in settings.DATABASE_URL else 'configured'}")
    print(f"Project: {settings.PROJECT_NAME}")
    print(f"Version: {settings.VERSION}")
    print("\nCreating database tables...")
    print("-" * 60)
    
    try:
        # Create all tables
        Base.metadata.create_all(bind=engine)
        
        print("\n✅ Database tables created successfully!")
        print("\nCreated tables:")
        for table_name in Base.metadata.tables.keys():
            print(f"  - {table_name}")
        
        print("\n" + "=" * 60)
        print("🎉 Database initialization complete!")
        print("=" * 60)
        print("\nNext steps:")
        print("  1. Start the server: uvicorn app.main:app --reload")
        print("  2. Visit API docs: http://localhost:8000/docs")
        print("  3. Check health: http://localhost:8000/health")
        print()
        
    except Exception as e:
        print(f"\n❌ Error creating database tables: {e}")
        print("\nTroubleshooting:")
        print("  1. Check that PostgreSQL is running")
        print("  2. Verify DATABASE_URL in .env file")
        print("  3. Ensure the database exists: createdb team4_assessment_db")
        sys.exit(1)


if __name__ == "__main__":
    init_db()
