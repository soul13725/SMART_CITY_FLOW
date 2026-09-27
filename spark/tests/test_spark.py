import sys
import os
import pytest
from datetime import datetime
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, DoubleType, TimestampType

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from spark.streaming.schemas import traffic_event_schema
from spark.streaming.transformations import parse_and_validate, with_traffic_intensity, with_congestion_indicator, with_speed_category, with_vehicle_volume_category
from spark.streaming.aggregations import junction_metrics, sensor_metrics, vehicle_type_metrics

@pytest.fixture(scope="session")
def spark():
    # Set Python executable explicitly for Windows compatibility
    import os
    os.environ['PYSPARK_PYTHON'] = sys.executable
    os.environ['PYSPARK_DRIVER_PYTHON'] = sys.executable
    
    spark = SparkSession.builder \
        .appName("pytest-spark") \
        .master("local[2]") \
        .getOrCreate()
    yield spark
    spark.stop()

def test_schema_valid():
    # Verify canonical fields exist
    fields = [f.name for f in traffic_event_schema.fields]
    assert "event_id" in fields
    assert "timestamp" in fields
    assert "vehicle_count" in fields
    assert "average_speed" in fields

def test_transformations(spark):
    data = [
        {"event_id": "e1", "average_speed": 10.0, "traffic_density": "SEVERE", "vehicle_count": 50},
        {"event_id": "e2", "average_speed": 50.0, "traffic_density": "LOW", "vehicle_count": 5},
        {"event_id": "e3", "average_speed": 70.0, "traffic_density": "MEDIUM", "vehicle_count": 25},
    ]
    
    df = spark.createDataFrame(data)
    
    df = with_traffic_intensity(df)
    df = with_congestion_indicator(df)
    df = with_speed_category(df)
    df = with_vehicle_volume_category(df)
    
    results = df.collect()
    
    for r in results:
        if r.event_id == "e1":
            assert r.congestion_indicator == "CONGESTED"
            assert r.speed_category == "LOW_SPEED"
            assert r.volume_category == "HEAVY"
        elif r.event_id == "e2":
            assert r.congestion_indicator == "NORMAL"
            assert r.volume_category == "LIGHT"

def test_aggregations(spark):
    schema = StructType([
        StructField("kafka_timestamp", TimestampType(), True),
        StructField("event_id", StringType(), True),
        StructField("junction_id", StringType(), True),
        StructField("vehicle_count", IntegerType(), True),
        StructField("average_speed", DoubleType(), True),
        StructField("occupancy_rate", DoubleType(), True)
    ])
    
    dt = datetime.now()
    data = [
        (dt, "e1", "j1", 10, 40.0, 0.5),
        (dt, "e2", "j1", 20, 50.0, 0.6),
        (dt, "e3", "j2", 5, 60.0, 0.2),
    ]
    
    df = spark.createDataFrame(data, schema=schema)
    
    j_metrics = junction_metrics(df).collect()
    
    assert len(j_metrics) == 2
    for m in j_metrics:
        if m.junction_id == "j1":
            assert m.total_vehicles == 30
            assert m.event_count == 2
        elif m.junction_id == "j2":
            assert m.total_vehicles == 5
            assert m.event_count == 1
