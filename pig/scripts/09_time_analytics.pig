raw_data = LOAD '/smartcity/traffic/raw/traffic_events.csv' USING PigStorage(',') 
AS (event_id:chararray, timestamp:chararray, sensor_id:chararray, junction_id:chararray, 
    lane_id:chararray, vehicle_type:chararray, vehicle_count:int, average_speed:double, 
    traffic_density:chararray, weather_condition:chararray, latitude:double, 
    longitude:double, occupancy_rate:double, road_type:chararray, direction:chararray, 
    incident_status:chararray);

traffic_data = FILTER raw_data BY event_id != 'event_id';

-- Timestamp format assumed ISO 8601: 2023-10-25T14:30:00Z or similar
-- We can extract substring for date and hour.
-- Date is first 10 characters (0 to 10), hour is 11 to 13

time_data = FOREACH traffic_data GENERATE 
    SUBSTRING(timestamp, 0, 10) AS event_date,
    SUBSTRING(timestamp, 11, 13) AS event_hour,
    vehicle_count,
    average_speed;

-- Hourly traffic
by_hour = GROUP time_data BY event_hour;
hourly_stats = FOREACH by_hour GENERATE
    group AS event_hour,
    COUNT(time_data) AS event_count,
    SUM(time_data.vehicle_count) AS vehicle_volume,
    AVG(time_data.average_speed) AS average_speed;

STORE hourly_stats INTO '/smartcity/traffic/pig_output/time/hourly';

-- Daily traffic
by_date = GROUP time_data BY event_date;
daily_stats = FOREACH by_date GENERATE
    group AS event_date,
    COUNT(time_data) AS event_count,
    SUM(time_data.vehicle_count) AS vehicle_volume,
    AVG(time_data.average_speed) AS average_speed;

STORE daily_stats INTO '/smartcity/traffic/pig_output/time/daily';
