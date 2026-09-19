import os
import psycopg2
from dotenv import load_dotenv

# Load variables from .env
load_dotenv()

db_url = os.getenv("DATABASE_URL")
api_key = os.getenv("GEMINI_API_KEY")

print("Checking environment variables...")
print(f"DATABASE_URL loaded: {'Yes' if db_url else 'No'}")
print(f"GEMINI_API_KEY loaded: {'Yes' if api_key else 'No'}")

# Test Neon Database Connection
try:
    conn = psycopg2.connect(db_url)
    cursor = conn.cursor()
    cursor.execute("SELECT PostGIS_Version();")
    version = cursor.fetchone()
    print(f"Neon Database Connected Successfully!")
    print(f"PostGIS Version: {version[0]}")
    cursor.close()
    conn.close()
except Exception as e:
    print(f"Database connection failed: {e}")