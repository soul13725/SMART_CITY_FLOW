raw_data = LOAD '/smartcity/traffic/raw/traffic_events.csv' USING PigStorage(',') 
AS (event_id:chararray, timestamp:chararray, sensor_id:chararray, junction_id:chararray, 
    lane_id:chararray, vehicle_type:chararray, vehicle_count:int, average_speed:double, 
    traffic_density:chararray, weather_condition:chararray, latitude:double, 
    longitude:double, occupancy_rate:double, road_type:chararray, direction:chararray, 
    incident_status:chararray);

traffic_data = FILTER raw_data BY event_id != 'event_id';

by_density = GROUP traffic_data BY traffic_density;

density_stats = FOREACH by_density GENERATE 
    group AS traffic_density,
    COUNT(traffic_data) AS event_count,
    SUM(traffic_data.vehicle_count) AS total_vehicle_count,
    AVG(traffic_data.average_speed) AS average_speed,
    AVG(traffic_data.occupancy_rate) AS average_occupancy;

STORE density_stats INTO '/smartcity/traffic/pig_output/density/overall';

-- Junction-density analysis
by_junction_density = GROUP traffic_data BY (junction_id, traffic_density);

junction_density_stats = FOREACH by_junction_density GENERATE 
    group.junction_id AS junction_id,
    group.traffic_density AS traffic_density,
    COUNT(traffic_data) AS event_count,
    SUM(traffic_data.vehicle_count) AS total_vehicle_count;

STORE junction_density_stats INTO '/smartcity/traffic/pig_output/density/by_junction';
