USE smart_city;

CREATE TABLE IF NOT EXISTS traffic_events (
    event_id STRING,
    `timestamp` TIMESTAMP,
    sensor_id STRING,
    junction_id STRING,
    lane_id STRING,
    vehicle_type STRING,
    vehicle_count INT,
    average_speed DOUBLE,
    traffic_density STRING,
    weather_condition STRING,
    latitude DOUBLE,
    longitude DOUBLE,
    occupancy_rate DOUBLE,
    road_type STRING,
    direction STRING,
    incident_status STRING
)
STORED AS ORC;

INSERT OVERWRITE TABLE traffic_events
SELECT * FROM traffic_events_raw;
