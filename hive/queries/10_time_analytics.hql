USE smart_city;

-- Hourly traffic
SELECT HOUR(`timestamp`) AS traffic_hour,
       COUNT(*) AS event_count,
       SUM(vehicle_count) AS vehicle_volume,
       AVG(average_speed) AS average_speed
FROM traffic_events
GROUP BY HOUR(`timestamp`)
ORDER BY traffic_hour;

-- Daily traffic
SELECT TO_DATE(`timestamp`) AS traffic_date,
       COUNT(*) AS event_count,
       SUM(vehicle_count) AS vehicle_volume
FROM traffic_events
GROUP BY TO_DATE(`timestamp`)
ORDER BY traffic_date;
