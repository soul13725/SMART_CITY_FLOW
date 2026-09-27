USE smart_city;

SELECT weather_condition,
       COUNT(*) AS event_count,
       SUM(vehicle_count) AS total_vehicles,
       AVG(average_speed) AS average_speed,
       AVG(occupancy_rate) AS average_occupancy
FROM traffic_events
GROUP BY weather_condition
ORDER BY event_count DESC;
