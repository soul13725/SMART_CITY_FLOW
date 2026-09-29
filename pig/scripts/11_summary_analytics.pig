raw_data = LOAD '/smartcity/traffic/raw/traffic_events.csv' USING PigStorage(',') 
AS (event_id:chararray, timestamp:chararray, sensor_id:chararray, junction_id:chararray, 
    lane_id:chararray, vehicle_type:chararray, vehicle_count:int, average_speed:double, 
    traffic_density:chararray, weather_condition:chararray, latitude:double, 
    longitude:double, occupancy_rate:double, road_type:chararray, direction:chararray, 
    incident_status:chararray);

traffic_data = FILTER raw_data BY event_id != 'event_id';

-- Group all into a single group using 'all'
group_all = GROUP traffic_data ALL;

summary_stats = FOREACH group_all {
    unique_junctions = DISTINCT traffic_data.junction_id;
    unique_sensors = DISTINCT traffic_data.sensor_id;
    incidents = FILTER traffic_data BY incident_status != 'normal' AND incident_status IS NOT NULL;
    
    GENERATE 
        COUNT(traffic_data) AS total_events,
        SUM(traffic_data.vehicle_count) AS total_vehicle_volume,
        AVG(traffic_data.average_speed) AS average_speed,
        AVG(traffic_data.occupancy_rate) AS average_occupancy,
        COUNT(unique_junctions) AS distinct_junctions,
        COUNT(unique_sensors) AS distinct_sensors,
        COUNT(incidents) AS incident_events;
};

STORE summary_stats INTO '/smartcity/traffic/pig_output/summary';
