import streamlit as st
import httpx
import plotly.express as px
import gpxpy

# Pointing to our FastAPI Backend
API_URL = "http://127.0.0.1:8000/api/v1/pacing/generate-strategy"

st.set_page_config(
    page_title="Race Intelligence Engine",
    page_icon="🏃‍♂️",
    layout="wide"
)

st.title("🏃‍♂️ Race Intelligence Engine")
st.markdown("Upload your race GPX track, set your target finish time, and get an AI-synthesized spatial pacing strategy.")

# Sidebar Configuration
st.sidebar.header("Race Settings")
uploaded_file = st.sidebar.file_uploader("Upload GPX Route File", type=["gpx"])
target_time_mins = st.sidebar.number_input("Target Finish Time (minutes)", min_value=1.0, value=60.0, step=1.0)

submit_button = st.sidebar.button("Generate Strategy", type="primary")

if submit_button:
    if not uploaded_file:
        st.error("Please upload a .gpx file first!")
    else:
        with st.spinner("Analyzing spatial geometry and synthesizing AI pacing strategy..."):
            try:
                # 1. Prepare file and payload for FastAPI request
                files = {"file": (uploaded_file.name, uploaded_file.getvalue(), "application/gpx+xml")}
                data = {"target_time_mins": target_time_mins}
                
                # 2. Call FastAPI Backend
                response = httpx.post(API_URL, data=data, files=files, timeout=60.0)
                
                if response.status_code == 200:
                    result = response.json()
                    
                    # 3. Top Metrics Row
                    col1, col2, col3, col4 = st.columns(4)
                    col1.metric("Route Name", result["route_name"])
                    col2.metric("Distance", f"{result['distance_km']} km")
                    col3.metric("Elevation Gain", f"{result['elevation_gain_m']} m")
                    col4.metric("Elevation Loss", f"{result['elevation_loss_m']} m")
                    
                    st.divider()

                    # 4. Render Local Elevation Profile Chart
                    uploaded_file.seek(0)
                    gpx = gpxpy.parse(uploaded_file.getvalue().decode("utf-8"))
                    
                    elevations = []
                    distances = []
                    cum_dist = 0.0
                    
                    points = [pt for track in gpx.tracks for segment in track.segments for pt in segment.points]
                    for i in range(len(points)):
                        if i > 0:
                            cum_dist += points[i].distance_2d(points[i-1]) / 1000.0
                        distances.append(cum_dist)
                        elevations.append(points[i].elevation)

                    st.subheader("📊 Elevation Profile")
                    fig = px.line(x=distances, y=elevations, labels={'x': 'Distance (km)', 'y': 'Elevation (m)'})
                    fig.update_traces(line_color='#FF4B4B')
                    st.plotly_chart(fig, use_container_width=True)

                    st.divider()

                    # 5. Render AI Strategy Output
                    st.subheader("🤖 AI Pacing Briefing")
                    if result.get("source") == "cache":
                        st.caption("⚡ Retrieved from database cache")
                    st.markdown(result["strategy_briefing"])

                else:
                    st.error(f"API Error ({response.status_code}): {response.text}")

            except Exception as e:
                st.error(f"Could not connect to FastAPI server. Ensure Uvicorn is running on port 8000! Error: {e}")