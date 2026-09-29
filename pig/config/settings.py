import os

class Settings:
    PIG_HDFS_INPUT = os.getenv("PIG_HDFS_INPUT", "/smartcity/traffic/raw")
    PIG_HDFS_OUTPUT = os.getenv("PIG_HDFS_OUTPUT", "/smartcity/traffic/pig_output")
    PIG_DATABASE = os.getenv("PIG_DATABASE", "smart_city")

settings = Settings()
