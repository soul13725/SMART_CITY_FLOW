raw_data = LOAD '/smartcity/traffic/raw/traffic_events.csv' USING PigStorage(',') 
AS (event_id:chararray, timestamp:chararray, sensor_id:chararray, junction_id:chararray, 
    lane_id:chararray, vehicle_type:chararray, vehicle_count:int, average_speed:double, 
    traffic_density:chararray, weather_condition:chararray, latitude:double, 
    longitude:double, occupancy_rate:double, road_type:chararray, direction:chararray, 
    incident_status:chararray);

traffic_data = FILTER raw_data BY event_id != 'event_id';
incidents_only = FILTER traffic_data BY incident_status != 'normal' AND incident_status IS NOT NULL;

by_incident = GROUP incidents_only BY incident_status;

incident_stats = FOREACH by_incident {
    -- Distinct junctions count workaround if distinct is fully supported, else just count events
    unique_junctions = DISTINCT incidents_only.junction_id;
    GENERATE 
        group AS incident_status,
        COUNT(incidents_only) AS event_count,
        SUM(incidents_only.vehicle_count) AS total_vehicle_count,
        AVG(incidents_only.average_speed) AS average_speed,
        AVG(incidents_only.occupancy_rate) AS average_occupancy,
        COUNT(unique_junctions) AS affected_junctions;
};

STORE incident_stats INTO '/smartcity/traffic/pig_output/incident';
