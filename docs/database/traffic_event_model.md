# Traffic Data Model Documentation

This document describes the schema for the future traffic event data that will be ingested and processed by the Smart City Big Data Traffic Analytics Platform.

## Traffic Event Schema

| Field | Type | Description |
|---|---|---|
| `event_id` | String | Unique identifier for the traffic event |
| `timestamp` | Timestamp | Date and time when the event occurred |
| `sensor_id` | String | Identifier for the sensor that recorded the event |
| `junction_id` | String | Identifier for the junction where the sensor is located |
| `vehicle_type` | String | Type of vehicle (e.g., Car, Truck, Bus, Motorcycle) |
| `vehicle_count` | Integer | Number of vehicles detected in this event |
| `average_speed` | Float | Average speed of the vehicle(s) in km/h |
| `traffic_density` | Float | Measured traffic density at the location (0.0 to 1.0) |
| `lane_id` | String | Identifier for the specific lane |
| `weather_condition` | String | Current weather conditions (e.g., Clear, Rain, Snow, Fog) |
| `latitude` | Float | GPS latitude coordinate of the sensor |
| `longitude` | Float | GPS longitude coordinate of the sensor |

*Note: This is documentation only for Phase 0. The actual data generator and ingestion mechanisms will be implemented in later phases.*
