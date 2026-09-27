from pyspark.sql.functions import col, when

def parse_and_validate(df, schema):
    from pyspark.sql.functions import from_json
    # Value is binary from Kafka, cast to string
    parsed = df.selectExpr("CAST(value AS STRING)", "timestamp as kafka_timestamp") \
               .select(from_json("value", schema).alias("data"), "kafka_timestamp") \
               .select("data.*", "kafka_timestamp")
    
    # Validation
    valid_df = parsed.filter(col("event_id").isNotNull() & (col("vehicle_count") >= 0))
    invalid_df = parsed.filter(col("event_id").isNull() | (col("vehicle_count") < 0))
    return valid_df, invalid_df

def with_traffic_intensity(df):
    return df.withColumn("intensity", col("traffic_density"))

def with_congestion_indicator(df):
    return df.withColumn(
        "congestion_indicator",
        when((col("traffic_density") == "SEVERE") | (col("average_speed") < 15.0), "CONGESTED")
        .when((col("traffic_density") == "HIGH"), "HEAVY")
        .otherwise("NORMAL")
    )

def with_speed_category(df):
    return df.withColumn(
        "speed_category",
        when(col("average_speed") < 20.0, "LOW_SPEED")
        .when(col("average_speed") > 60.0, "HIGH_SPEED")
        .otherwise("NORMAL_SPEED")
    )

def with_vehicle_volume_category(df):
    return df.withColumn(
        "volume_category",
        when(col("vehicle_count") < 10, "LIGHT")
        .when(col("vehicle_count") < 50, "MODERATE")
        .otherwise("HEAVY")
    )
