USE smart_city;

SELECT junction_id,
       COUNT(*) AS events_per_junction,
       SUM(vehicle_count) AS total_vehicle_count,
       AVG(average_speed) AS average_speed,
       AVG(occupancy_rate) AS average_occupancy
FROM traffic_events
GROUP BY junction_id
ORDER BY total_vehicle_count DESC
LIMIT 10;
