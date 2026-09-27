# Smart City Spark Structured Streaming

## Overview
This module processes continuous JSON traffic event streams from Apache Kafka in real-time using Apache Spark Structured Streaming. It parses the events based on the Phase 2 schema, validates records, performs analytical transformations, calculates windowed aggregations, and writes the results to durable outputs.

## Architecture
- `schemas.py`: Explicit definition of the PySpark `StructType` mirroring the canonical `TrafficEvent` from Phase 2.
- `transformations.py`: Functions to parse Kafka values, handle validation branching, and compute rule-based classifications (intensity, speed, congestion, volume).
- `aggregations.py`: 1-minute tumbling window metrics grouping by junction, sensor, weather, vehicle type, and incident status.
- `traffic_stream.py`: The core application that bridges Kafka -> Spark -> Output.
- `output/`: Processed parquets / JSON outputs.
- `checkpoints/`: Spark streaming durability checkpoints.

## Setup & Execution
If Kafka is running locally on port 9092:

```bash
# If using python virtual environments
python -m spark.streaming.traffic_stream

# If using spark-submit (recommended for actual clusters)
spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0 spark/streaming/traffic_stream.py
```

## Features
- **Validation Branching**: Invalid JSON or negative vehicle counts are separated into an `invalid_events` stream, avoiding application crashes.
- **Micro-batch Outputs**: Outputs multiple independent Parquet tables per window (e.g. `junction_metrics`, `sensor_metrics`) and checkpointing ensures exactly-once semantics.
- **Local Testing**: The transformation and aggregation logic is isolated to easily allow pure DataFrame unit testing without a live Kafka broker.
