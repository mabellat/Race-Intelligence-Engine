import os
from google import genai
from dotenv import load_dotenv

load_dotenv()

class AIStrategyService:
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY environment variable is missing!")
        # Initialize Google GenAI client
        self.client = genai.Client(api_key=api_key)

    def generate_race_strategy(
        self, 
        route_name: str,
        distance_km: float, 
        elevation_gain_m: float, 
        elevation_loss_m: float, 
        target_time_mins: float
    ) -> str:
        """
        Synthesizes an adaptive pacing briefing using Gemini 2.5 Flash based on 
        route geometry metrics and runner targets.
        """
        avg_pace_min_km = target_time_mins / distance_km if distance_km > 0 else 0

        prompt = f"""
        Act as an elite endurance race pacing strategist. Synthesize an adaptive race execution strategy for a runner based on the following route telemetry:

        Route Details:
        - Route Name: {route_name}
        - Total Distance: {distance_km} km
        - Total Elevation Gain: {elevation_gain_m} meters
        - Total Elevation Loss: {elevation_loss_m} meters
        - Runner's Target Finish Time: {target_time_mins} minutes
        - Required Average Pace: {avg_pace_min_km:.2f} min/km

        Please construct a structured race execution plan containing:
        1. **Executive Strategy Summary**: Key approach (e.g., negative split, effort-based pacing on hills).
        2. **Pacing Strategy Breakdown**: Advice tailored to distance splits and elevation dynamics (uphill vs downhill effort management).
        3. **Tactical Race Tips**: 3 actionable instructions on pacing discipline, fueling, and mental control tailored to this specific elevation profile.

        Keep the tone encouraging, professional, and practical for race day execution.
        """

        response = self.client.models.generate_content(
            model="gemini-3.6-flash",
            contents=prompt,
        )

        return response.text