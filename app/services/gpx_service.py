import gpxpy
import gpxpy.gpx

class GPXService:
    @staticmethod
    def parse_gpx_content(gpx_content: str) -> dict:
        """
        Parses raw GPX XML string content and returns structured telemetry metrics
        along with a list of 3D coordinates (lon, lat, ele) for PostGIS ingestion.
        """
        gpx = gpxpy.parse(gpx_content)

        total_distance_m = 0.0
        total_elevation_gain_m = 0.0
        total_elevation_loss_m = 0.0
        
        coordinates: list[tuple[float, float, float]] = []
        previous_point = None

        for track in gpx.tracks:
            for segment in track.segments:
                for point in segment.points:
                    # Extract 3D spatial coordinate (Longitude, Latitude, Elevation)
                    # Note: PostGIS expects (Longitude, Latitude) order!
                    lon = point.longitude
                    lat = point.latitude
                    ele = point.elevation if point.elevation is not None else 0.0

                    coordinates.append((lon, lat, ele))

                    # Calculate distance and elevation changes relative to previous point
                    if previous_point:
                        # Distance calculation (2D surface distance)
                        dist = point.distance_2d(previous_point)
                        if dist:
                            total_distance_m += dist

                        # Elevation changes
                        if point.elevation is not None and previous_point.elevation is not None:
                            ele_diff = point.elevation - previous_point.elevation
                            if ele_diff > 0:
                                total_elevation_gain_m += ele_diff
                            else:
                                total_elevation_loss_m += abs(ele_diff)

                    previous_point = point

        # Fallback to route name or default
        route_name = gpx.tracks[0].name if gpx.tracks and gpx.tracks[0].name else "Untitled GPX Route"

        return {
            "name": route_name,
            "distance_km": round(total_distance_m / 1000.0, 2),
            "elevation_gain_m": round(total_elevation_gain_m, 2),
            "elevation_loss_m": round(total_elevation_loss_m, 2),
            "coordinates": coordinates
        }