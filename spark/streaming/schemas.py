from pyspark.sql.types import StructType, StructField, StringType, IntegerType, DoubleType

# Phase 2 canonical schema
traffic_event_schema = StructType([
    StructField("event_id", StringType(), False),
    StructField("timestamp", StringType(), False),
    StructField("sensor_id", StringType(), False),
    StructField("junction_id", StringType(), False),
    StructField("lane_id", StringType(), False),
    StructField("vehicle_type", StringType(), False),
    StructField("vehicle_count", IntegerType(), False),
    StructField("average_speed", DoubleType(), False),
    StructField("traffic_density", StringType(), False),
    StructField("weather_condition", StringType(), False),
    StructField("latitude", DoubleType(), False),
    StructField("longitude", DoubleType(), False),
    StructField("occupancy_rate", DoubleType(), True),
    StructField("road_type", StringType(), True),
    StructField("direction", StringType(), True),
    StructField("incident_status", StringType(), True)
])
