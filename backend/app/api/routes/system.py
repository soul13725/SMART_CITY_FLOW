from fastapi import APIRouter
from app.config.settings import settings

router = APIRouter()

@router.get("/system/info")
def system_info():
    return {
        "service": "smart-city-big-data-backend",
        "version": settings.APP_VERSION,
        "environment": settings.ENVIRONMENT
    }
