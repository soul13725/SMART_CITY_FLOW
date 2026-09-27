import os

class HadoopSettings:
    HADOOP_HOME = os.getenv("HADOOP_HOME", "C:\\hadoop")
    HDFS_NAMENODE = os.getenv("HDFS_NAMENODE", "hdfs://localhost:9000")
    HDFS_USER = os.getenv("HDFS_USER", "smartcity")
    HDFS_RAW_PATH = "/smartcity/traffic/raw"
    HDFS_PROCESSED_PATH = "/smartcity/traffic/processed"
    HDFS_OUTPUT_PATH = "/smartcity/traffic/output"

settings = HadoopSettings()
