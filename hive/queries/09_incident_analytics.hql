USE smart_city;

SELECT incident_status,
       COUNT(*) AS incident_event_count,
       COUNT(DISTINCT junction_id) AS affected_junctions,
       COUNT(DISTINCT sensor_id) AS affected_sensors,
       AVG(average_speed) AS average_speed_during_incidents,
       SUM(vehicle_count) AS vehicle_volume_during_incidents
FROM traffic_events
WHERE incident_status != 'normal'
GROUP BY incident_status;
