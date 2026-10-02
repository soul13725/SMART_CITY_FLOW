"""
Analytics routes.

GET /api/analytics/vehicles
GET /api/analytics/junctions
GET /api/analytics/sensors
GET /api/analytics/density
GET /api/analytics/weather
GET /api/analytics/incidents
GET /api/analytics/time/hourly
GET /api/analytics/time/daily
"""
from typing import Optional
from fastapi import APIRouter, HTTPException, Query
from app.schemas.traffic import (
    VehicleAnalyticsResponse,
    JunctionAnalyticsResponse,
    SensorAnalyticsResponse,
    DensityAnalyticsResponse,
    WeatherAnalyticsResponse,
    IncidentAnalyticsResponse,
    HourlyAnalyticsResponse,
    DailyAnalyticsResponse,
)
from app.services import traffic_service
from app.utils.logger import logger

router = APIRouter()


def _dataset_unavailable():
    raise HTTPException(
        status_code=503,
        detail={
            "status": "unavailable",
            "service": "traffic_dataset",
            "reason": "Traffic dataset CSV not found or could not be loaded.",
        },
    )


@router.get(
    "/analytics/vehicles",
    response_model=VehicleAnalyticsResponse,
    summary="Vehicle Analytics",
    description="Returns traffic event counts, vehicle counts, and average speed grouped by vehicle type.",
    tags=["analytics"],
)
def vehicle_analytics(
    vehicle_type: Optional[str] = Query(
        None,
        description="Filter results to a specific vehicle type (e.g. car, bus, truck).",
    )
):
    data = traffic_service.get_vehicle_analytics(vehicle_type=vehicle_type)
    if data is None:
        _dataset_unavailable()
    return {"data": data}


@router.get(
    "/analytics/junctions",
    response_model=JunctionAnalyticsResponse,
    summary="Junction Analytics",
    description="Returns per-junction traffic statistics including event count, vehicle count, speed, and occupancy.",
    tags=["analytics"],
)
def junction_analytics(
    junction_id: Optional[str] = Query(
        None,
        description="Filter results to a specific junction ID (e.g. J001).",
    )
):
    data = traffic_service.get_junction_analytics(junction_id=junction_id)
    if data is None:
        _dataset_unavailable()
    return {"data": data}


@router.get(
    "/analytics/sensors",
    response_model=SensorAnalyticsResponse,
    summary="Sensor Analytics",
    description="Returns per-sensor traffic statistics including event count, vehicle count, speed, and occupancy.",
    tags=["analytics"],
)
def sensor_analytics(
    sensor_id: Optional[str] = Query(
        None,
        description="Filter results to a specific sensor ID (e.g. S001).",
    )
):
    data = traffic_service.get_sensor_analytics(sensor_id=sensor_id)
    if data is None:
        _dataset_unavailable()
    return {"data": data}


@router.get(
    "/analytics/density",
    response_model=DensityAnalyticsResponse,
    summary="Density Analytics",
    description=(
        "Returns traffic statistics grouped by density level "
        "(LOW, MEDIUM, HIGH, SEVERE — detected from actual dataset values)."
    ),
    tags=["analytics"],
)
def density_analytics(
    traffic_density: Optional[str] = Query(
        None,
        description="Filter results to a specific density level (e.g. HIGH).",
    )
):
    data = traffic_service.get_density_analytics(traffic_density=traffic_density)
    if data is None:
        _dataset_unavailable()
    return {"data": data}


@router.get(
    "/analytics/weather",
    response_model=WeatherAnalyticsResponse,
    summary="Weather Analytics",
    description="Returns traffic statistics grouped by weather condition (e.g. clear, rain, fog, cloudy).",
    tags=["analytics"],
)
def weather_analytics(
    weather_condition: Optional[str] = Query(
        None,
        description="Filter results to a specific weather condition (e.g. rain).",
    )
):
    data = traffic_service.get_weather_analytics(weather_condition=weather_condition)
    if data is None:
        _dataset_unavailable()
    return {"data": data}


@router.get(
    "/analytics/incidents",
    response_model=IncidentAnalyticsResponse,
    summary="Incident Analytics",
    description="Returns traffic event counts grouped by incident status (normal, minor_incident, major_incident).",
    tags=["analytics"],
)
def incident_analytics():
    data = traffic_service.get_incident_analytics()
    if data is None:
        _dataset_unavailable()
    return {"data": data}


@router.get(
    "/analytics/time/hourly",
    response_model=HourlyAnalyticsResponse,
    summary="Hourly Time Analytics",
    description="Returns traffic statistics aggregated by hour-of-day (0–23).",
    tags=["analytics"],
)
def hourly_analytics():
    data = traffic_service.get_hourly_analytics()
    if data is None:
        _dataset_unavailable()
    return {"data": data}


@router.get(
    "/analytics/time/daily",
    response_model=DailyAnalyticsResponse,
    summary="Daily Time Analytics",
    description="Returns traffic statistics aggregated by calendar date.",
    tags=["analytics"],
)
def daily_analytics():
    data = traffic_service.get_daily_analytics()
    if data is None:
        _dataset_unavailable()
    return {"data": data}
