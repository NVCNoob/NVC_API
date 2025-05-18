import os
from sqlmodel import SQLModel, create_engine, Session
from typing import Generator

# Default to SQLite if DATABASE_URL is not set
SQLMODEL_DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./test.db")

# Conditional connect_args for SQLite
connect_args = {"check_same_thread": False} if SQLMODEL_DATABASE_URL.startswith("sqlite") else {}

try:
    engine = create_engine(SQLMODEL_DATABASE_URL, connect_args=connect_args)
except Exception as e:
    raise Exception(f"Failed to create database engine: {str(e)}")

def create_db_and_tables():
    """Initialize database and create tables."""
    try:
        SQLModel.metadata.create_all(engine)
    except Exception as e:
        raise Exception(f"Failed to create database tables: {str(e)}")

def get_db() -> Generator[Session, None, None]:
    """Dependency to provide a database session."""
    with Session(engine) as session:
        yield session

