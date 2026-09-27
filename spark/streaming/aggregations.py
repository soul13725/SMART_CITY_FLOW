from pyspark.sql.functions import window, avg, sum as _sum, count

def junction_metrics(df):
    return df.withWatermark("kafka_timestamp", "1 minute") \
        .groupBy(window("kafka_timestamp", "1 minute"), "junction_id") \
        .agg(
            _sum("vehicle_count").alias("total_vehicles"),
            avg("average_speed").alias("avg_speed"),
            avg("occupancy_rate").alias("avg_occupancy"),
            count("event_id").alias("event_count")
        )

def sensor_metrics(df):
    return df.withWatermark("kafka_timestamp", "1 minute") \
        .groupBy(window("kafka_timestamp", "1 minute"), "sensor_id") \
        .agg(
            _sum("vehicle_count").alias("total_vehicles"),
            avg("average_speed").alias("avg_speed"),
            avg("occupancy_rate").alias("avg_occupancy"),
            count("event_id").alias("event_count")
        )

def vehicle_type_metrics(df):
    return df.withWatermark("kafka_timestamp", "1 minute") \
        .groupBy(window("kafka_timestamp", "1 minute"), "vehicle_type") \
        .agg(
            _sum("vehicle_count").alias("total_vehicles"),
            count("event_id").alias("event_count"),
            avg("average_speed").alias("avg_speed")
        )

def weather_metrics(df):
    return df.withWatermark("kafka_timestamp", "1 minute") \
        .groupBy(window("kafka_timestamp", "1 minute"), "weather_condition") \
        .agg(
            avg("average_speed").alias("avg_speed"),
            avg("vehicle_count").alias("avg_volume"),
            avg("occupancy_rate").alias("avg_occupancy")
        )

def incident_metrics(df):
    return df.withWatermark("kafka_timestamp", "1 minute") \
        .filter(df.incident_status != "normal") \
        .groupBy(window("kafka_timestamp", "1 minute"), "incident_status") \
        .agg(
            count("event_id").alias("incident_event_count"),
            count("junction_id").alias("affected_junctions"),
            count("sensor_id").alias("affected_sensors"),
            avg("average_speed").alias("avg_speed_during_incident")
        )
