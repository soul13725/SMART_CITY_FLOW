import argparse
import sys
import os

from pyspark.sql import SparkSession

# Adjust path for direct execution
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from spark.streaming.config import config
from spark.streaming.schemas import traffic_event_schema
from spark.streaming.transformations import parse_and_validate, with_traffic_intensity, with_congestion_indicator, with_speed_category, with_vehicle_volume_category
from spark.streaming.aggregations import junction_metrics, sensor_metrics, vehicle_type_metrics, weather_metrics, incident_metrics

def main():
    parser = argparse.ArgumentParser(description="Spark Structured Streaming - Traffic Events")
    parser.add_argument("--bootstrap-server", default=config.KAFKA_BOOTSTRAP_SERVERS)
    parser.add_argument("--topic", default=config.KAFKA_TRAFFIC_TOPIC)
    parser.add_argument("--starting-offsets", default="latest")
    parser.add_argument("--trigger", default=config.SPARK_TRIGGER_INTERVAL)
    args = parser.parse_args()

    # Ensure output and checkpoint directories exist
    os.makedirs(config.SPARK_CHECKPOINT_LOCATION, exist_ok=True)
    os.makedirs(config.SPARK_OUTPUT_LOCATION, exist_ok=True)

    spark = SparkSession.builder \
        .appName("SmartCityTrafficStreaming") \
        .config("spark.sql.streaming.checkpointLocation", config.SPARK_CHECKPOINT_LOCATION) \
        .getOrCreate()
        
    spark.sparkContext.setLogLevel("WARN")

    print(f"Connecting to Kafka: {args.bootstrap_server}, Topic: {args.topic}")

    try:
        # Source
        raw_stream = spark.readStream \
            .format("kafka") \
            .option("kafka.bootstrap.servers", args.bootstrap_server) \
            .option("subscribe", args.topic) \
            .option("startingOffsets", args.starting_offsets) \
            .option("failOnDataLoss", "false") \
            .load()

        # Parse & Validate
        valid_df, invalid_df = parse_and_validate(raw_stream, traffic_event_schema)

        # Transforms
        enriched_df = with_traffic_intensity(valid_df)
        enriched_df = with_congestion_indicator(enriched_df)
        enriched_df = with_speed_category(enriched_df)
        enriched_df = with_vehicle_volume_category(enriched_df)

        # Aggregations
        j_metrics = junction_metrics(enriched_df)
        s_metrics = sensor_metrics(enriched_df)
        v_metrics = vehicle_type_metrics(enriched_df)
        w_metrics = weather_metrics(enriched_df)
        i_metrics = incident_metrics(enriched_df)

        # Outputs
        queries = []
        
        def write_query(df, name):
            out_path = os.path.join(config.SPARK_OUTPUT_LOCATION, name)
            chk_path = os.path.join(config.SPARK_CHECKPOINT_LOCATION, name)
            return df.writeStream \
                .queryName(name) \
                .format("parquet") \
                .option("path", out_path) \
                .option("checkpointLocation", chk_path) \
                .trigger(processingTime=args.trigger) \
                .start()
                
        def write_console(df, name):
            return df.writeStream \
                .queryName(name) \
                .format("console") \
                .option("truncate", "false") \
                .trigger(processingTime=args.trigger) \
                .start()

        queries.append(write_query(j_metrics, "junction_metrics"))
        queries.append(write_query(s_metrics, "sensor_metrics"))
        queries.append(write_query(v_metrics, "vehicle_type_metrics"))
        queries.append(write_query(w_metrics, "weather_metrics"))
        queries.append(write_query(i_metrics, "incident_metrics"))
        
        # Invalid events dumped to JSON
        queries.append(invalid_df.writeStream \
            .queryName("invalid_events") \
            .format("json") \
            .option("path", os.path.join(config.SPARK_OUTPUT_LOCATION, "invalid_events")) \
            .option("checkpointLocation", os.path.join(config.SPARK_CHECKPOINT_LOCATION, "invalid_events")) \
            .trigger(processingTime=args.trigger) \
            .start())
            
        # Console debug
        queries.append(write_console(j_metrics, "console_junction_metrics"))

        print("Streaming queries started. Awaiting termination...")
        for q in queries:
            print(f" - {q.name}")
            
        spark.streams.awaitAnyTermination()
        
    except Exception as e:
        print(f"Streaming application failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
