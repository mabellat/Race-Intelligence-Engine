from sqlalchemy.orm import Session
from app.db.models import RaceStrategyModel

class StrategyRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_strategy(
        self, 
        route_id: int, 
        target_time_mins: float, 
        strategy_summary: str
    ) -> RaceStrategyModel:
        """Saves a synthesized AI pacing strategy to PostgreSQL."""
        db_strategy = RaceStrategyModel(
            route_id=route_id,
            target_time_mins=target_time_mins,
            strategy_summary=strategy_summary
        )
        self.db.add(db_strategy)
        self.db.commit()
        self.db.refresh(db_strategy)
        return db_strategy

    def get_cached_strategy(self, route_id: int, target_time_mins: float) -> RaceStrategyModel | None:
        """
        Checks if a strategy already exists for the given route and target finish time.
        Prevents redundant Gemini API calls.
        """
        return self.db.query(RaceStrategyModel).filter(
            RaceStrategyModel.route_id == route_id,
            RaceStrategyModel.target_time_mins == target_time_mins
        ).first()