# Smart City Big Data Traffic Analytics Platform - Backend

## Overview
This is the FastAPI backend foundation for the Smart City platform. Currently in Phase 1, it provides the core architecture, centralized configuration, basic health APIs, and CORS middleware for frontend communication. It is designed to act as the intermediary between the React dashboard and the future Big Data analytics layer.

## Quick Start
```powershell
uv venv --python 3.12 .venv
.\.venv\Scripts\activate
uv pip install -r requirements.txt
uvicorn app.main:app --reload
```
The server will run on `http://127.0.0.1:8000`.

## Configuration
Configuration is managed via environment variables and Pydantic Settings.
- `APP_NAME`
- `APP_VERSION`
- `ENVIRONMENT`
- `BACKEND_HOST`
- `BACKEND_PORT`
- `FRONTEND_URL` (Used for CORS)
- `LOG_LEVEL`

## Endpoints
- `GET /api/health` - Check backend health status
- `GET /api/system/info` - Get system version and environment info
- `GET /docs` - Swagger UI documentation
- `GET /redoc` - ReDoc API documentation

## Future Phases
Subsequent phases will introduce Kafka consumers, Spark streaming interfaces, MongoDB adapters, and analytical endpoints to feed live and historical traffic data to the frontend.
