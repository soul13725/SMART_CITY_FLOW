raw_data = LOAD '/smartcity/traffic/raw/traffic_events.csv' USING PigStorage(',') 
AS (event_id:chararray, timestamp:chararray, sensor_id:chararray, junction_id:chararray, 
    lane_id:chararray, vehicle_type:chararray, vehicle_count:int, average_speed:double, 
    traffic_density:chararray, weather_condition:chararray, latitude:double, 
    longitude:double, occupancy_rate:double, road_type:chararray, direction:chararray, 
    incident_status:chararray);

traffic_data = FILTER raw_data BY event_id != 'event_id';

-- Junctions by traffic volume
by_junction = GROUP traffic_data BY junction_id;
junction_stats = FOREACH by_junction GENERATE 
    group AS junction_id, 
    SUM(traffic_data.vehicle_count) AS total_vehicle_count,
    AVG(traffic_data.average_speed) AS avg_speed;

junctions_by_volume = ORDER junction_stats BY total_vehicle_count DESC;
lowest_speed_junctions = ORDER junction_stats BY avg_speed ASC;

STORE junctions_by_volume INTO '/smartcity/traffic/pig_output/sorted/junctions_by_volume';
STORE lowest_speed_junctions INTO '/smartcity/traffic/pig_output/sorted/lowest_speed_junctions';

-- Sensors by event count
by_sensor = GROUP traffic_data BY sensor_id;
sensor_stats = FOREACH by_sensor GENERATE group AS sensor_id, COUNT(traffic_data) AS event_count;
sensors_by_events = ORDER sensor_stats BY event_count DESC;

STORE sensors_by_events INTO '/smartcity/traffic/pig_output/sorted/sensors_by_events';

-- Vehicle types by volume
by_vehicle = GROUP traffic_data BY vehicle_type;
vehicle_stats = FOREACH by_vehicle GENERATE group AS vehicle_type, SUM(traffic_data.vehicle_count) AS volume;
vehicles_by_volume = ORDER vehicle_stats BY volume DESC;

STORE vehicles_by_volume INTO '/smartcity/traffic/pig_output/sorted/vehicles_by_volume';
