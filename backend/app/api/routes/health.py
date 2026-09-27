from fastapi import APIRouter
from app.config.settings import settings

router = APIRouter()

@router.get("/health")
def health_check():
    return {
        "status": "ok",
        "service": "smart-city-big-data-backend",
        "version": settings.APP_VERSION
    }
