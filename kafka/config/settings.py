import os

class Settings:
    KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
    KAFKA_TRAFFIC_TOPIC = os.getenv("KAFKA_TRAFFIC_TOPIC", "traffic-events")
    KAFKA_CONSUMER_GROUP = os.getenv("KAFKA_CONSUMER_GROUP", "traffic-analytics-consumer")

settings = Settings()
