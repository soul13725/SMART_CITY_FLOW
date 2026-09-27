USE smart_city;

SELECT sensor_id,
       COUNT(*) AS event_count,
       SUM(vehicle_count) AS total_vehicles,
       AVG(average_speed) AS average_speed,
       AVG(occupancy_rate) AS average_occupancy
FROM traffic_events
GROUP BY sensor_id
ORDER BY total_vehicles DESC;

-- Sensors reporting incidents
SELECT sensor_id, COUNT(*) as incident_events
FROM traffic_events
WHERE incident_status != 'normal'
GROUP BY sensor_id
ORDER BY incident_events DESC;
