USE smart_city;

SELECT COUNT(*) AS total_events,
       SUM(vehicle_count) AS total_vehicle_count,
       AVG(average_speed) AS average_speed,
       AVG(occupancy_rate) AS average_occupancy,
       COUNT(DISTINCT sensor_id) AS distinct_sensors,
       COUNT(DISTINCT junction_id) AS distinct_junctions,
       SUM(CASE WHEN incident_status != 'normal' THEN 1 ELSE 0 END) AS incident_events
FROM traffic_events;
