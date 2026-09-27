import os
import sys
import datetime
from dateutil.parser import parse as parse_date

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from mongodb.schemas.traffic_document import validate_and_parse

def test_schema_valid_row():
    row = {
        "event_id": "e1",
        "timestamp": "2026-09-27T08:42:15Z",
        "sensor_id": "S1",
        "junction_id": "J1",
        "lane_id": "L1",
        "vehicle_type": "car",
        "vehicle_count": "10",
        "average_speed": "40.5",
        "traffic_density": "LOW",
        "weather_condition": "clear",
        "latitude": "28.6",
        "longitude": "77.2",
        "occupancy_rate": "0.4",
        "road_type": "arterial",
        "direction": "N",
        "incident_status": "normal"
    }
    doc, err = validate_and_parse(row)
    assert err is None
    assert doc["event_id"] == "e1"
    assert isinstance(doc["timestamp"], datetime.datetime)
    assert doc["vehicle_count"] == 10
    assert doc["average_speed"] == 40.5

def test_schema_negative_values():
    row = {
        "event_id": "e2",
        "timestamp": "2026-09-27T08:42:15Z",
        "sensor_id": "S1",
        "junction_id": "J1",
        "lane_id": "L1",
        "vehicle_type": "car",
        "vehicle_count": "-5",
        "average_speed": "40.5",
        "traffic_density": "LOW",
        "weather_condition": "clear",
        "latitude": "28.6",
        "longitude": "77.2",
        "occupancy_rate": "0.4",
        "road_type": "arterial",
        "direction": "N",
        "incident_status": "normal"
    }
    doc, err = validate_and_parse(row)
    assert doc is None
    assert err == "Negative numeric value"
