#!/usr/bin/env python
import sys
import csv

def main():
    reader = csv.reader(sys.stdin)
    for row in reader:
        # Phase 2 Schema:
        # event_id(0), timestamp(1), sensor_id(2), junction_id(3), lane_id(4), vehicle_type(5),
        # vehicle_count(6), average_speed(7), traffic_density(8), weather_condition(9),
        # latitude(10), longitude(11), occupancy_rate(12), road_type(13), direction(14), incident_status(15)
        if not row or row[0] == "event_id":  # Skip empty or header
            continue
            
        try:
            junction_id = row[3]
            vehicle_count = int(row[6])
            if vehicle_count >= 0:
                print(f"{junction_id}\t{vehicle_count}")
        except (IndexError, ValueError):
            pass  # Silently discard invalid records in mapper

if __name__ == "__main__":
    main()
