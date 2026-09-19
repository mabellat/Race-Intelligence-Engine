from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.controllers.strategy_controller import router as strategy_router
from app.db.init_db import init_db

# Initialize database schema on server startup
init_db()

app = FastAPI(
    title="Personal Race Intelligence API",
    version="1.0.0",
    description="Engineered backend for GPX telemetry processing, PostGIS spatial tracking, and AI race pacing strategies.",
)

# Enable CORS (Allows cross-origin requests from frontends like Streamlit or React)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Controller Routers
app.include_router(strategy_router)


@app.get("/health")
def health_check():
    return {"status": "active", "service": "race-intelligence-engine"}