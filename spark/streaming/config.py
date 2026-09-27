import os

class SparkConfig:
    KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
    KAFKA_TRAFFIC_TOPIC = os.getenv("KAFKA_TRAFFIC_TOPIC", "traffic-events")
    SPARK_CHECKPOINT_LOCATION = os.getenv("SPARK_CHECKPOINT_LOCATION", "spark/checkpoints")
    SPARK_OUTPUT_LOCATION = os.getenv("SPARK_OUTPUT_LOCATION", "spark/output")
    SPARK_TRIGGER_INTERVAL = os.getenv("SPARK_TRIGGER_INTERVAL", "10 seconds")

config = SparkConfig()
