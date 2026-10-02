"""
Traffic summary route.

GET /api/traffic/summary
"""
from fastapi import APIRouter, HTTPException
from app.schemas.traffic import TrafficSummary
from app.services import traffic_service
from app.utils.logger import logger

router = APIRouter()


@router.get(
    "/traffic/summary",
    response_model=TrafficSummary,
    summary="Traffic Summary",
    description=(
        "Returns a high-level summary of all traffic events in the Phase 2 dataset: "
        "total events, total vehicle count, average speed, average occupancy, "
        "junction count, and sensor count."
    ),
    tags=["traffic"],
)
def traffic_summary():
    """Compute and return a summary of the traffic dataset."""
    result = traffic_service.get_traffic_summary()
    if result is None:
        raise HTTPException(
            status_code=503,
            detail={
                "status": "unavailable",
                "service": "traffic_dataset",
                "reason": "Traffic dataset CSV not found or could not be loaded.",
            },
        )
    return result
