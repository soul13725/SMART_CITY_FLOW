import os

class HiveSettings:
    HIVE_DATABASE = os.getenv("HIVE_DATABASE", "smart_city")
    HIVE_RAW_TABLE = os.getenv("HIVE_RAW_TABLE", "traffic_events_raw")
    HIVE_TRAFFIC_TABLE = os.getenv("HIVE_TRAFFIC_TABLE", "traffic_events")
    HIVE_HDFS_RAW_PATH = os.getenv("HIVE_HDFS_RAW_PATH", "/smartcity/traffic/raw")
    HIVE_HDFS_PROCESSED_PATH = os.getenv("HIVE_HDFS_PROCESSED_PATH", "/smartcity/traffic/processed")
    HIVE_OUTPUT_PATH = os.getenv("HIVE_OUTPUT_PATH", "/smartcity/traffic/hive_output")

settings = HiveSettings()
