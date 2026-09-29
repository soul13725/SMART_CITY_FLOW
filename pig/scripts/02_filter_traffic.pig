raw_data = LOAD '/smartcity/traffic/raw/traffic_events.csv' USING PigStorage(',') 
AS (event_id:chararray, timestamp:chararray, sensor_id:chararray, junction_id:chararray, 
    lane_id:chararray, vehicle_type:chararray, vehicle_count:int, average_speed:double, 
    traffic_density:chararray, weather_condition:chararray, latitude:double, 
    longitude:double, occupancy_rate:double, road_type:chararray, direction:chararray, 
    incident_status:chararray);

traffic_data = FILTER raw_data BY event_id != 'event_id';

-- Projection
projected_data = FOREACH traffic_data GENERATE event_id, timestamp, sensor_id, junction_id, vehicle_type, vehicle_count, average_speed, traffic_density;

-- Filtering
high_density = FILTER traffic_data BY traffic_density == 'HIGH' OR traffic_density == 'SEVERE';
low_speed = FILTER traffic_data BY average_speed < 15.0;
incidents = FILTER traffic_data BY incident_status == 'minor_incident' OR incident_status == 'major_incident';
trucks = FILTER traffic_data BY vehicle_type == 'truck';

STORE projected_data INTO '/smartcity/traffic/pig_output/filtered/projected';
STORE high_density INTO '/smartcity/traffic/pig_output/filtered/high_density';
STORE low_speed INTO '/smartcity/traffic/pig_output/filtered/low_speed';
STORE incidents INTO '/smartcity/traffic/pig_output/filtered/incidents';
STORE trucks INTO '/smartcity/traffic/pig_output/filtered/trucks';
