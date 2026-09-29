raw_data = LOAD '/smartcity/traffic/raw/traffic_events.csv' USING PigStorage(',') 
AS (event_id:chararray, timestamp:chararray, sensor_id:chararray, junction_id:chararray, 
    lane_id:chararray, vehicle_type:chararray, vehicle_count:int, average_speed:double, 
    traffic_density:chararray, weather_condition:chararray, latitude:double, 
    longitude:double, occupancy_rate:double, road_type:chararray, direction:chararray, 
    incident_status:chararray);

traffic_data = FILTER raw_data BY event_id != 'event_id';

by_sensor = GROUP traffic_data BY sensor_id;

sensor_stats = FOREACH by_sensor {
    incidents = FILTER traffic_data BY incident_status == 'minor_incident' OR incident_status == 'major_incident';
    high_density = FILTER traffic_data BY traffic_density == 'HIGH';
    GENERATE 
        group AS sensor_id,
        COUNT(traffic_data) AS event_count,
        SUM(traffic_data.vehicle_count) AS total_vehicle_count,
        AVG(traffic_data.average_speed) AS average_speed,
        COUNT(incidents) AS incident_count,
        COUNT(high_density) AS high_density_count;
};

STORE sensor_stats INTO '/smartcity/traffic/pig_output/sensor';
