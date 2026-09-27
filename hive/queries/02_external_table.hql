USE smart_city;

CREATE EXTERNAL TABLE IF NOT EXISTS traffic_events_raw (
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
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
STORED AS TEXTFILE
LOCATION '/smartcity/traffic/raw'
TBLPROPERTIES ("skip.header.line.count"="1");
