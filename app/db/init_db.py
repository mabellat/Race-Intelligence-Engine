import sys
from pathlib import Path
# Add project root directory to sys.path
sys.path.append(str(Path(__file__).resolve().parent.parent.parent))

from sqlalchemy import text
from app.db.connection import engine, Base
from app.db.models import RouteModel, RaceStrategyModel  # Ensures models are registered

def init_db():
    # 1. Enable PostGIS Extension on Neon
    with engine.connect() as conn:
        conn.execute(text("CREATE EXTENSION IF NOT EXISTS postgis;"))
        conn.commit()

    # 2. Automatically create all ORM tables
    Base.metadata.create_all(bind=engine)
    print("Database tables and PostGIS spatial extensions initialized successfully via SQLAlchemy!")

if __name__ == "__main__":
    init_db()