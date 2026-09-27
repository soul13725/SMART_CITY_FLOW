from pydantic import BaseModel, Field
from typing import Optional
import uuid

class TrafficEvent(BaseModel):
    event_id: str = Field(default_factory=lambda: f"evt_{uuid.uuid4().hex}")
    timestamp: str
    sensor_id: str
    junction_id: str
    lane_id: str
    vehicle_type: str
    vehicle_count: int
    average_speed: float
    traffic_density: str
    weather_condition: str
    latitude: float
    longitude: float
    occupancy_rate: Optional[float] = None
    road_type: Optional[str] = None
    direction: Optional[str] = None
    incident_status: Optional[str] = None
