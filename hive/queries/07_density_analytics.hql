USE smart_city;

-- Global Density Distribution
SELECT traffic_density,
       COUNT(*) AS event_count,
       SUM(vehicle_count) AS total_vehicle_count,
       AVG(average_speed) AS average_speed,
       AVG(occupancy_rate) AS average_occupancy
FROM traffic_events
GROUP BY traffic_density
ORDER BY total_vehicle_count DESC;

-- Density by Junction
SELECT junction_id, traffic_density, COUNT(*) AS density_events
FROM traffic_events
GROUP BY junction_id, traffic_density;
