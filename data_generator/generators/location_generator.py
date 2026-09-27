import random
from data_generator.config.settings import settings

def generate_junctions(num_junctions, seed=None):
    if seed is not None:
        random.seed(seed)
    junctions = []
    for i in range(1, num_junctions + 1):
        junctions.append({
            "junction_id": f"J{i:03d}",
            "junction_name": f"Simulated_Junction_{i}",
            "latitude": round(settings.BASE_LAT + random.uniform(-0.05, 0.05), 6),
            "longitude": round(settings.BASE_LON + random.uniform(-0.05, 0.05), 6),
            "number_of_lanes": random.choice([2, 3, 4, 6]),
            "road_type": random.choice(["arterial", "collector", "highway", "local"])
        })
    return junctions
