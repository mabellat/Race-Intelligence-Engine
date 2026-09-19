from sqlalchemy import Column, Integer, String, Float, Text, ForeignKey, DateTime
from sqlalchemy.sql import func
from geoalchemy2 import Geometry
from app.db.connection import Base

class RouteModel(Base):
    __tablename__ = "routes"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    distance_km = Column(Float, nullable=False)
    elevation_gain_m = Column(Float, nullable=False)
    elevation_loss_m = Column(Float, nullable=False)
    
    # 3D LineString geometry for PostGIS (SRID 4326 = standard GPS lat/lon)
    geom = Column(Geometry(geometry_type='LINESTRINGZ', srid=4326))
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class RaceStrategyModel(Base):
    __tablename__ = "race_strategies"

    id = Column(Integer, primary_key=True, index=True)
    route_id = Column(Integer, ForeignKey("routes.id", ondelete="CASCADE"), nullable=False)
    target_time_mins = Column(Float, nullable=False)
    strategy_summary = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())