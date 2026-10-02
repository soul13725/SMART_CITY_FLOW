from fastapi import APIRouter
from app.api.routes import health, system, traffic, analytics, bigdata

api_router = APIRouter()

# Phase 1 — existing routes
api_router.include_router(health.router, tags=["health"])
api_router.include_router(system.router, tags=["system"])

# Phase 11 — new routes
api_router.include_router(traffic.router, tags=["traffic"])
api_router.include_router(analytics.router, tags=["analytics"])
api_router.include_router(bigdata.router, tags=["bigdata"])
