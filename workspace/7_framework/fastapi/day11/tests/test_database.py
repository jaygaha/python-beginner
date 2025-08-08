import pytest
from src.models.user import Base
from tests.conftest import engine

def test_database_tables_created():
    """Test that database tables are created properly"""
    Base.metadata.create_all(bind=engine)

    # Check if tables exist
    from sqlalchemy import inspect
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    assert "users" in tables
