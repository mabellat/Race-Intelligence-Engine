from sqlalchemy.orm import Session
from geoalchemy2.shape import from_shape
from shapely.geometry import LineString
from app.db.models import RouteModel

class RouteRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_route(
        self, 
        name: str, 
        distance_km: float, 
        elevation_gain_m: float, 
        elevation_loss_m: float, 
        coordinates: list[tuple[float, float, float]]
    ) -> RouteModel:
        """
        Converts 3D coordinates (lon, lat, ele) into a PostGIS LineStringZ geometry
        and saves the route record in PostgreSQL.
        """
        # Convert coordinate tuples to a Shapely 3D LineString
        shapely_line = LineString(coordinates)
        
        # Convert Shapely shape to PostGIS geometry (SRID 4326 = standard GPS coordinates)
        postgis_geom = from_shape(shapely_line, srid=4326)

        db_route = RouteModel(
            name=name,
            distance_km=distance_km,
            elevation_gain_m=elevation_gain_m,
            elevation_loss_m=elevation_loss_m,
            geom=postgis_geom
        )

        self.db.add(db_route)
        self.db.commit()
        self.db.refresh(db_route)
        return db_route

    def get_by_id(self, route_id: int) -> RouteModel | None:
        """Retrieves a route by its primary key ID."""
        return self.db.query(RouteModel).filter(RouteModel.id == route_id).first()