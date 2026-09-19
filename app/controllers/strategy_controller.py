from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.db.connection import get_db
from app.repositories.route_repository import RouteRepository
from app.repositories.strategy_repository import StrategyRepository
from app.services.ai_strategy_service import AIStrategyService
from app.services.gpx_service import GPXService

router = APIRouter(prefix="/api/v1/pacing", tags=["Pacing Strategy"])

# Instantiate service instances
ai_service = AIStrategyService()


@router.post("/generate-strategy")
async def generate_strategy(
    target_time_mins: float = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    """
    Uploads a GPX file, extracts 3D telemetry, saves spatial route geometry to PostGIS,
    and returns a Gemini-synthesized race pacing strategy.
    """
    if not file.filename.endswith(".gpx"):
        raise HTTPException(
            status_code=400, detail="Invalid file type. Only .gpx files are allowed."
        )

    # 1. Read uploaded file content
    content = await file.read()
    gpx_str = content.decode("utf-8")

    # 2. Parse GPX content using GPXService
    parsed_telemetry = GPXService.parse_gpx_content(gpx_str)

    # Initialize Repositories with DB Session
    route_repo = RouteRepository(db)
    strategy_repo = StrategyRepository(db)

    # 3. Save parsed spatial route into Neon PostgreSQL via RouteRepository
    route = route_repo.create_route(
        name=parsed_telemetry["name"],
        distance_km=parsed_telemetry["distance_km"],
        elevation_gain_m=parsed_telemetry["elevation_gain_m"],
        elevation_loss_m=parsed_telemetry["elevation_loss_m"],
        coordinates=parsed_telemetry["coordinates"],
    )

    # 4. Check repository cache to avoid duplicate Gemini LLM calls
    cached_strategy = strategy_repo.get_cached_strategy(
        route_id=route.id, target_time_mins=target_time_mins
    )
    if cached_strategy:
        return {
            "source": "cache",
            "route_id": route.id,
            "route_name": route.name,
            "distance_km": route.distance_km,
            "elevation_gain_m": route.elevation_gain_m,
            "elevation_loss_m": route.elevation_loss_m,
            "target_time_mins": cached_strategy.target_time_mins,
            "strategy_briefing": cached_strategy.strategy_summary,
        }

    # 5. Synthesize Strategy using Gemini AI Service
    strategy_text = ai_service.generate_race_strategy(
        route_name=route.name,
        distance_km=route.distance_km,
        elevation_gain_m=route.elevation_gain_m,
        elevation_loss_m=route.elevation_loss_m,
        target_time_mins=target_time_mins,
    )

    # 6. Save newly generated strategy to Database
    new_strategy = strategy_repo.create_strategy(
        route_id=route.id,
        target_time_mins=target_time_mins,
        strategy_summary=strategy_text,
    )

    return {
        "source": "generated",
        "route_id": route.id,
        "route_name": route.name,
        "distance_km": route.distance_km,
        "elevation_gain_m": route.elevation_gain_m,
        "elevation_loss_m": route.elevation_loss_m,
        "target_time_mins": new_strategy.target_time_mins,
        "strategy_briefing": new_strategy.strategy_summary,
    }