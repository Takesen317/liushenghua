"""
Database connection and session management
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.pool import NullPool

from app.core.config import settings

# Create Base for model inheritance
Base = declarative_base()

# Handle SQLite for local development (no PostgreSQL needed yet)
if "sqlite" in settings.DATABASE_URL or "postgresql" not in settings.DATABASE_URL:
    engine = create_engine(
        "sqlite:///./liushenghua.db",
        connect_args={"check_same_thread": False},
        poolclass=NullPool,  # NullPool is safer for SQLite with threading
    )
else:
    engine = create_engine(
        settings.DATABASE_URL,
        pool_pre_ping=True,
        pool_size=5,
        max_overflow=10
    )

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    """Dependency for getting database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
