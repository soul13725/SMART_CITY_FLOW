"""
Pydantic response schemas for traffic analytics endpoints.
"""
from pydantic import BaseModel
from typing import Optional


class TrafficSummary(BaseModel):
    """High-level summary of all traffic events in the dataset."""
    total_events: int
    total_vehicle_count: int
    average_speed: float
    average_occupancy: float
    junction_count: int
    sensor_count: int


class VehicleAnalyticsItem(BaseModel):
    """Analytics for a single vehicle type."""
    vehicle_type: str
    event_count: int
    total_vehicle_count: int
    average_speed: float


class VehicleAnalyticsResponse(BaseModel):
    """Response wrapper for vehicle analytics."""
    data: list[VehicleAnalyticsItem]


class JunctionAnalyticsItem(BaseModel):
    """Analytics for a single junction."""
    junction_id: str
    event_count: int
    total_vehicle_count: int
    average_speed: float
    average_occupancy: float


class JunctionAnalyticsResponse(BaseModel):
    """Response wrapper for junction analytics."""
    data: list[JunctionAnalyticsItem]


class SensorAnalyticsItem(BaseModel):
    """Analytics for a single sensor."""
    sensor_id: str
    event_count: int
    total_vehicle_count: int
    average_speed: float
    average_occupancy: float


class SensorAnalyticsResponse(BaseModel):
    """Response wrapper for sensor analytics."""
    data: list[SensorAnalyticsItem]


class DensityAnalyticsItem(BaseModel):
    """Analytics for a single traffic density level."""
    traffic_density: str
    event_count: int
    percentage: float
    average_vehicle_count: float
    average_speed: float


class DensityAnalyticsResponse(BaseModel):
    """Response wrapper for density analytics."""
    data: list[DensityAnalyticsItem]


class WeatherAnalyticsItem(BaseModel):
    """Analytics for a single weather condition."""
    weather_condition: str
    event_count: int
    percentage: float
    average_speed: float
    average_vehicle_count: float


class WeatherAnalyticsResponse(BaseModel):
    """Response wrapper for weather analytics."""
    data: list[WeatherAnalyticsItem]


class IncidentAnalyticsItem(BaseModel):
    """Analytics for a single incident status category."""
    incident_status: str
    event_count: int
    percentage: float


class IncidentAnalyticsResponse(BaseModel):
    """Response wrapper for incident analytics."""
    data: list[IncidentAnalyticsItem]


class HourlyAnalyticsItem(BaseModel):
    """Traffic analytics aggregated by hour."""
    hour: int
    event_count: int
    total_vehicle_count: int
    average_speed: float


class HourlyAnalyticsResponse(BaseModel):
    """Response wrapper for hourly analytics."""
    data: list[HourlyAnalyticsItem]


class DailyAnalyticsItem(BaseModel):
    """Traffic analytics aggregated by calendar date."""
    date: str
    event_count: int
    total_vehicle_count: int
    average_speed: float


class DailyAnalyticsResponse(BaseModel):
    """Response wrapper for daily analytics."""
    data: list[DailyAnalyticsItem]
