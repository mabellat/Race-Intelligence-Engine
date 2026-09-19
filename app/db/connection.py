import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL is not set in environment variables!")

# Enhanced engine configuration for Neon PostgreSQL / Cloud DBs
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,  # Checks connection liveness before every query execution
    pool_recycle=300,  # Recycles connections every 5 minutes to prevent stale timeouts
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()