raw_data = LOAD '/smartcity/traffic/raw/traffic_events.csv' USING PigStorage(',') 
AS (event_id:chararray, timestamp:chararray, sensor_id:chararray, junction_id:chararray, 
    lane_id:chararray, vehicle_type:chararray, vehicle_count:int, average_speed:double, 
    traffic_density:chararray, weather_condition:chararray, latitude:double, 
    longitude:double, occupancy_rate:double, road_type:chararray, direction:chararray, 
    incident_status:chararray);

traffic_data = FILTER raw_data BY event_id != 'event_id';

by_weather = GROUP traffic_data BY weather_condition;

weather_stats = FOREACH by_weather GENERATE 
    group AS weather_condition,
    COUNT(traffic_data) AS event_count,
    SUM(traffic_data.vehicle_count) AS total_vehicle_count,
    AVG(traffic_data.average_speed) AS average_speed,
    AVG(traffic_data.occupancy_rate) AS average_occupancy;

STORE weather_stats INTO '/smartcity/traffic/pig_output/weather';
