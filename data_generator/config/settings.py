import os

class Settings:
    NUM_SENSORS = int(os.getenv("NUM_SENSORS", 30))
    NUM_JUNCTIONS = int(os.getenv("NUM_JUNCTIONS", 10))

    VEHICLE_PROBABILITIES = {
        "car": 0.50,
        "motorcycle": 0.25,
        "auto_rickshaw": 0.10,
        "bus": 0.05,
        "truck": 0.05,
        "van": 0.05
    }

    WEATHER_PROBABILITIES = {
        "clear": 0.60,
        "cloudy": 0.20,
        "rain": 0.15,
        "fog": 0.05
    }

    DENSITY_STATES = ["LOW", "MEDIUM", "HIGH", "SEVERE"]

    INCIDENT_PROBABILITIES = {
        "normal": 0.95,
        "minor_incident": 0.04,
        "major_incident": 0.01
    }

    BASE_LAT = 28.6139  # Simulated center latitude
    BASE_LON = 77.2090  # Simulated center longitude

settings = Settings()
