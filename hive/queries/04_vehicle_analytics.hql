USE smart_city;

SELECT vehicle_type, 
       SUM(vehicle_count) AS total_vehicles,
       COUNT(*) AS event_count,
       AVG(average_speed) AS avg_speed,
       AVG(occupancy_rate) AS avg_occupancy
FROM traffic_events
GROUP BY vehicle_type
ORDER BY total_vehicles DESC;
