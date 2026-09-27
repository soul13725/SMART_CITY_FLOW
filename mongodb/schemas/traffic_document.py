import datetime
from dateutil.parser import parse as parse_date

def validate_and_parse(row):
    """
    Parses a dictionary (from CSV or JSON) into a strictly typed MongoDB document.
    Preserves Phase 2 canonical schema exactly.
    """
    try:
        doc = {
            "event_id": str(row["event_id"]),
            "timestamp": parse_date(str(row["timestamp"])),
            "sensor_id": str(row["sensor_id"]),
            "junction_id": str(row["junction_id"]),
            "lane_id": str(row["lane_id"]),
            "vehicle_type": str(row["vehicle_type"]),
            "vehicle_count": int(row["vehicle_count"]),
            "average_speed": float(row["average_speed"]),
            "traffic_density": str(row["traffic_density"]),
            "weather_condition": str(row["weather_condition"]),
            "latitude": float(row["latitude"]),
            "longitude": float(row["longitude"]),
            "occupancy_rate": float(row["occupancy_rate"]) if row.get("occupancy_rate") else 0.0,
            "road_type": str(row.get("road_type", "unknown")),
            "direction": str(row.get("direction", "unknown")),
            "incident_status": str(row.get("incident_status", "normal"))
        }
        
        if doc["vehicle_count"] < 0 or doc["average_speed"] < 0:
            return None, "Negative numeric value"
            
        return doc, None
    except Exception as e:
        return None, str(e)
