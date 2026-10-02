"""
Big Data component routes.

GET /api/bigdata/status
GET /api/bigdata/bloom-filter
GET /api/bigdata/r-status
"""
from fastapi import APIRouter, HTTPException
from app.schemas.system import BigDataStatusResponse, BloomFilterStatistics, RStatusResponse, ComponentStatus
from app.services import bigdata_service, bloom_service
from app.utils.logger import logger

router = APIRouter()


@router.get(
    "/bigdata/status",
    response_model=BigDataStatusResponse,
    summary="Big Data Component Status",
    description=(
        "Reports the current implementation and runtime availability of all Big Data "
        "components: Kafka, Spark, Hadoop, MongoDB, Hive, Pig, Bloom Filter, and R Analytics."
    ),
    tags=["bigdata"],
)
def bigdata_status():
    """
    Probe each Big Data component and report its implementation and runtime status.
    This endpoint never returns 503 — it always returns 200 with the status of each component.
    """
    raw = bigdata_service.get_component_status()

    # Convert raw dicts to ComponentStatus Pydantic models
    components = {}
    for name, info in raw.items():
        components[name] = ComponentStatus(
            implemented=info.get("implemented", False),
            runtime_available=info.get("runtime_available", False),
            reason=info.get("reason"),
        )

    return BigDataStatusResponse(components=components)


@router.get(
    "/bigdata/bloom-filter",
    response_model=BloomFilterStatistics,
    summary="Bloom Filter Statistics",
    description=(
        "Runs the Phase 9 Bloom Filter duplicate detector against all event_ids in the "
        "local traffic dataset and returns usage statistics. "
        "This is a read-only adapter and does not modify the Bloom Filter implementation."
    ),
    tags=["bigdata"],
)
def bloom_filter_stats():
    """Return Bloom Filter statistics computed from the local dataset."""
    stats = bloom_service.get_bloom_filter_statistics()
    if stats is None:
        raise HTTPException(
            status_code=503,
            detail={
                "status": "unavailable",
                "service": "bloom_filter",
                "reason": (
                    "Bloom Filter statistics unavailable. "
                    "Either the dataset CSV is missing or the bloom_filter module could not be imported."
                ),
            },
        )
    return stats


@router.get(
    "/bigdata/r-status",
    response_model=RStatusResponse,
    summary="R Analytics Status",
    description=(
        "Reports whether the R Analytics runtime is available. "
        "R scripts are implemented (Phase 10) but R.exe / Rscript.exe may not be installed."
    ),
    tags=["bigdata"],
)
def r_status():
    """Report R Analytics runtime availability without attempting to execute R."""
    info = bigdata_service.get_r_status()
    return RStatusResponse(
        implemented=info["implemented"],
        runtime_available=info["runtime_available"],
        reason=info["reason"],
    )
