# Smart City Big Data Traffic Generator

## Purpose
This module generates realistic, simulated smart-city traffic events. It serves as the foundational data source for the Big Data pipeline (Kafka, Spark, Hadoop, Hive, etc.) to be developed in subsequent phases. 

**IMPORTANT: THIS DATA IS SIMULATED. It is not collected from real traffic sensors.**

## Architecture
- `schemas/` - Defines the canonical `TrafficEvent` data model using Pydantic.
- `generators/` - Contains the logic for simulating junctions, sensors, and the event stream itself.
- `config/` - Centralized settings for generation parameters.

## Event Schema
The core schema includes:
`event_id`, `timestamp`, `sensor_id`, `junction_id`, `lane_id`, `vehicle_type`, `vehicle_count`, `average_speed`, `traffic_density`, `weather_condition`, `latitude`, `longitude`, `occupancy_rate`, `road_type`, `direction`, `incident_status`.

## CLI Usage
Generate a batch of 1,000 events to a CSV file:
```bash
python -m data_generator.generators.traffic_generator --events 1000 --output ../data/generated/traffic_events.csv --seed 42
```
Generate events in a JSONL stream (useful for piping or Kafka):
```bash
python -m data_generator.generators.traffic_generator --mode stream --interval 1.0
```

## Testing
To run the automated tests for schema validation and generation logic:
```bash
pytest tests/
```
