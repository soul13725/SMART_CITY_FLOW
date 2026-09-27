import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

import pytest
from datetime import datetime, timezone
from data_generator.schemas.traffic_event import TrafficEvent
from data_generator.generators.location_generator import generate_junctions
from data_generator.generators.sensor_generator import generate_sensors
from data_generator.generators.traffic_generator import generate_event
from data_generator.config.settings import settings

def test_traffic_event_schema():
    event = TrafficEvent(
        timestamp="2026-09-27T08:42:15Z",
        sensor_id="S001",
        junction_id="J001",
        lane_id="L1",
        vehicle_type="car",
        vehicle_count=10,
        average_speed=45.5,
        traffic_density="LOW",
        weather_condition="clear",
        latitude=28.6,
        longitude=77.2
    )
    assert event.event_id.startswith("evt_")
    assert event.vehicle_count == 10

def test_unique_event_ids():
    event1 = TrafficEvent(
        timestamp="T1", sensor_id="S1", junction_id="J1", lane_id="L1",
        vehicle_type="car", vehicle_count=1, average_speed=1.0,
        traffic_density="LOW", weather_condition="clear", latitude=1.0, longitude=1.0
    )
    event2 = TrafficEvent(
        timestamp="T2", sensor_id="S1", junction_id="J1", lane_id="L1",
        vehicle_type="car", vehicle_count=1, average_speed=1.0,
        traffic_density="LOW", weather_condition="clear", latitude=1.0, longitude=1.0
    )
    assert event1.event_id != event2.event_id

def test_seeded_generation():
    junctions = generate_junctions(5, seed=42)
    assert junctions[0]['junction_id'] == 'J001'
    
    sensors = generate_sensors(10, junctions, seed=42)
    assert len(sensors) == 10
    
    # Two identical runs should produce the same first event
    import random
    random.seed(42)
    e1 = generate_event(sensors[0], datetime(2026, 1, 1, 12, 0, tzinfo=timezone.utc))
    
    random.seed(42)
    e2 = generate_event(sensors[0], datetime(2026, 1, 1, 12, 0, tzinfo=timezone.utc))
    
    assert e1.vehicle_type == e2.vehicle_type
    assert e1.average_speed == e2.average_speed

def test_valid_ranges():
    junctions = generate_junctions(2)
    sensors = generate_sensors(2, junctions)
    event = generate_event(sensors[0], datetime.now(timezone.utc))
    
    assert event.vehicle_count >= 0
    assert event.average_speed >= 0.0
    assert event.traffic_density in settings.DENSITY_STATES
    assert event.vehicle_type in settings.VEHICLE_PROBABILITIES.keys()
