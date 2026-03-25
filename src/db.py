"""
Database connection and initialization module.
Supports Postgres (production/Docker).
"""

import os
from sqlalchemy import create_engine, pool
from sqlalchemy.orm import sessionmaker, Session
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Postgres is the only supported database for this deployment
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:postgres@localhost:5432/pokedex"
)

# Educational Setting: echo=True shows all generated SQL
SQL_ECHO = os.getenv("SQL_ECHO", "False").lower() == "true"

engine = create_engine(
    DATABASE_URL,
    poolclass=pool.NullPool,
    echo=SQL_ECHO
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_session() -> Session:
    """Get a new database session."""
    return SessionLocal()

def init_db():
    """Initialize the database schema."""
    from src.models import Base
    Base.metadata.create_all(bind=engine)
    print("✓ Pokedex schema initialized successfully (Postgres)")

def close_db():
    """Close the database connection."""
    engine.dispose()
