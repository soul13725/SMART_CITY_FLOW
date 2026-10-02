import sys
from fastapi import APIRouter
from app.config.settings import settings
from app.services import bigdata_service

router = APIRouter()


@router.get(
    "/system/info",
    summary="System Information",
    description=(
        "Returns general system information including Python version, app version, "
        "environment, and a summary of Big Data component availability."
    ),
    tags=["system"],
)
def system_info():
    """Return system info and Big Data component availability summary."""
    component_raw = bigdata_service.get_component_status()
    components_summary = {
        name: (
            "runtime_ready"
            if info.get("runtime_available")
            else ("implemented" if info.get("implemented") else "unavailable")
        )
        for name, info in component_raw.items()
    }

    return {
        "service": "smart-city-big-data-backend",
        "version": settings.APP_VERSION,
        "environment": settings.ENVIRONMENT,
        "python_version": f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
        "backend": "available",
        "components": components_summary,
    }
