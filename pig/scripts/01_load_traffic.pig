raw_data = LOAD '/smartcity/traffic/raw/traffic_events.csv' USING PigStorage(',') 
AS (
    event_id:chararray,
    timestamp:chararray,
    sensor_id:chararray,
    junction_id:chararray,
    lane_id:chararray,
    vehicle_type:chararray,
    vehicle_count:int,
    average_speed:double,
    traffic_density:chararray,
    weather_condition:chararray,
    latitude:double,
    longitude:double,
    occupancy_rate:double,
    road_type:chararray,
    direction:chararray,
    incident_status:chararray
);

-- Filter out the header if it exists
traffic_data = FILTER raw_data BY event_id != 'event_id';

STORE traffic_data INTO '/smartcity/traffic/pig_output/loaded';
