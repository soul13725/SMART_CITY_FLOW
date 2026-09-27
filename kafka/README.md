# Smart City Kafka Real-Time Ingestion

## Overview
This module handles real-time ingestion and transportation of traffic events using Apache Kafka. It acts as the intermediary between the Python Data Generator (Phase 2) and future real-time analytics engines (like Apache Spark in Phase 4).

## Architecture
- `Traffic Generator (Phase 2)` → `Kafka Producer` → `Kafka Broker (Topic: traffic-events)` → `Kafka Consumer`

## Configuration
- **Kafka Version**: Currently expects a standard Apache Kafka (KRaft or ZooKeeper) installation.
- **Topic**: `traffic-events`
- **Partitions**: Recommended 3 (for local development).
- **Replication Factor**: 1 (Single broker local setup).
- **Message Key**: `sensor_id` (Ensures events from the same sensor stay in the same partition, critical for future stateful processing).
- **Serialization**: UTF-8 encoded JSON matching the Phase 2 `TrafficEvent` schema.
- **Consumer Group**: `traffic-analytics-consumer`

## Setup & Execution
If you have Kafka installed, follow your distribution's instructions to start the broker (e.g., using `kafka-server-start.sh` or KRaft equivalents).

### Install Dependencies
```bash
uv pip install -r requirements.txt
```

### Producer Usage
Publish events from an existing JSONL file:
```bash
python -m kafka.producers.traffic_producer --mode file --input ../data/generated/traffic_events.jsonl
```

Publish events in live continuous stream mode (1 event per second):
```bash
python -m kafka.producers.traffic_producer --mode live --interval 1.0
```

### Consumer Usage
Consume events from the topic (reads from the earliest offset if it's a new consumer group):
```bash
python -m kafka.consumers.traffic_consumer --from-beginning
```

## Status
*Implementation complete. Runtime validation is currently blocked pending a local Kafka broker installation on the host machine.*
