import random

def generate_sensors(num_sensors, junctions, seed=None):
    if seed is not None:
        random.seed(seed)
    sensors = []
    for i in range(1, num_sensors + 1):
        junction = random.choice(junctions)
        lane = random.randint(1, junction["number_of_lanes"])
        sensors.append({
            "sensor_id": f"S{i:03d}",
            "junction_id": junction["junction_id"],
            "lane_id": f"L{lane}",
            "latitude": round(junction["latitude"] + random.uniform(-0.0001, 0.0001), 6),
            "longitude": round(junction["longitude"] + random.uniform(-0.0001, 0.0001), 6),
            "road_type": junction["road_type"],
            "direction": random.choice(["N", "S", "E", "W", "NE", "NW", "SE", "SW"])
        })
    return sensors
