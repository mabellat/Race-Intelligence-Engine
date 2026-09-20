


# 🏃‍♂️ Race Intelligence Engine

[![Live App](https://img.shields.io/badge/Streamlit-Live%20App-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://race-intelligence-engine-mabellat.streamlit.app/)
[![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-PostGIS-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)](https://postgis.net/)
[![Gemini 2.0](https://img.shields.io/badge/Google_Gemini-3.6_Flash-8E44AD?style=for-the-badge&logo=google&logoColor=white)](https://ai.google.dev/)

> A production-ready, full-stack spatial engineering platform that parses raw 3D GPX track telemetry, computes terrain profiles via PostGIS spatial primitives, and synthesizes LLM-driven race execution plans.

---
## Demonstration

https://github.com/mabellat/Race-Intelligence-Engine/issues/1#issue-5516174096

## 💡 System Context & Motivation

As an aspiring endurance athlete, I encountered a major gap when preparing for structured race events: while running jargon like **min/km pacing**, **negative splits**, **elevation gain/loss profiles**, and **effort management** are critical to avoiding early race fatigue, obtaining route-aware pacing strategies usually requires expensive subscriptions (e.g., Runna) or private coaching.

I built the **Race Intelligence Engine** to make advanced spatial race planning accessible. The system processes raw 3D spatial geometry, persists route data in a geospatial database, and leverages Google Gemini 3.6 Flash to output terrain-aware pacing, fueling, and tactical race-day execution plans.

---
## Architecture Breakdown

1. **Frontend Presentation Layer:** Lightweight Streamlit dashboard handling file parsing feedback, Plotly elevation charts, and responsive UI layout.
2. **Backend API Layer:** FastAPI framework built using Controller-Repository software design patterns to maintain strict separation of concerns.
3. **Geospatial Engine:** `gpxpy` and `Shapely` transform raw XML route files into high-dimensional geometric representations (`LINESTRING Z`), calculating 2D distances and cumulative 3D elevation gains.
4. **Data Persistence Layer:** Managed Neon PostgreSQL database running PostGIS spatial extensions. Stores 3D spatial coordinates using spatial query primitives (`ST_GeomFromEWKT`) with spatial index optimizations.
5. **AI Synthesis Engine:** Integrates the `google-genai` SDK using `gemini-2.0-flash` to generate contextually aware pacing tactics conditioned on runner targets and elevation constraints.

---

### 🛠️ Tech Stack & Engineering Highlights

| Component | Technology | Technical Purpose |
| :--- | :--- | :--- |
| **API Framework** | FastAPI / Uvicorn | Asynchronous processing, auto-generated OpenAPI specs, strict payload validation via Pydantic |
| **Geospatial Processing** | PostGIS / Shapely / gpxpy | 3D coordinate vector calculations, EWKT spatial modeling (`SRID 4326`) |
| **Data Layer** | SQLAlchemy 2.0 / GeoAlchemy2 | Object-Relational Mapping (ORM) for PostGIS geometries with connection pool recycling |
| **LLM Engine** | Google Gemini 2.0 Flash | Ultra-low latency reasoning engine for domain-specific strategy synthesis |
| **Frontend** | Streamlit / Plotly | Declarative UI rendering interactive elevation line profiles and metric cards |

---

### ☁️ Production Deployment

* **Backend API:** Hosted on **Render** (Python Web Service running Uvicorn).
* **Frontend App:** Hosted on **Streamlit Community Cloud** (Auto-syncs on Git push).
* **Geospatial Database:** Hosted on **Neon PostgreSQL** with active PostGIS extension.

## 🏗️ System Architecture

```text
                                  +-----------------------+
                                  | Streamlit Dashboard   |
                                  | (Interactive UI/UX)   |
                                  +-----------+-----------+
                                              |
                                              | HTTP POST (Multipart GPX + Payload)
                                              v
                                  +-----------------------+
                                  | FastAPI REST Engine   |
                                  | (Pydantic / Uvicorn)  |
                                  +-----------+-----------+
                                              |
                 +----------------------------+----------------------------+
                 |                                                         |
                 v                                                         v
    +-------------------------+                               +-------------------------+
    | Telemetry & GIS Engine  |                               | AI Synthesis Pipeline   |
    | - gpxpy (3D Parsing)    |                               | - Google GenAI SDK      |
    | - Shapely (Linestring)  |                               | - Gemini 2.0 Flash Model|
    +------------+------------+                               +------------+------------+
                 |                                                         |
                 v                                                         |
    +-------------------------+                                            |
    | PostGIS PostgreSQL DB   |                                            |
    | - ST_GeomFromEWKT       |                                            |
    | - 3D Coordinates (Z)    |                                            |
    +------------+------------+                                            |
                 |                                                         |
                 +----------------------------+----------------------------+
                                              |
                                              v
                                  +-----------------------+
                                  | Adaptive Pacing Plan  |
                                  | (Structured Briefing) |
                                  +-----------------------+
