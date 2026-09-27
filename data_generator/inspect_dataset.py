import argparse
import csv
import json
import statistics
from collections import Counter

def inspect_csv(file_path):
    events = []
    with open(file_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            events.append(row)
            
    if not events:
        print("Dataset is empty.")
        return

    print(f"--- Dataset Inspection: {file_path} ---")
    print(f"Total events: {len(events)}")
    
    sensors = set(e['sensor_id'] for e in events)
    junctions = set(e['junction_id'] for e in events)
    print(f"Unique sensors: {len(sensors)}")
    print(f"Unique junctions: {len(junctions)}")
    
    vehicle_types = Counter(e['vehicle_type'] for e in events)
    print("\nVehicle Type Distribution:")
    for v_type, count in vehicle_types.most_common():
        print(f"  {v_type}: {count} ({(count/len(events))*100:.1f}%)")
        
    densities = Counter(e['traffic_density'] for e in events)
    print("\nDensity Distribution:")
    for d_type, count in densities.most_common():
        print(f"  {d_type}: {count} ({(count/len(events))*100:.1f}%)")

    weather = Counter(e['weather_condition'] for e in events)
    print("\nWeather Distribution:")
    for w_type, count in weather.most_common():
        print(f"  {w_type}: {count} ({(count/len(events))*100:.1f}%)")

    speeds = [float(e['average_speed']) for e in events]
    counts = [int(e['vehicle_count']) for e in events]
    print(f"\nAverage Speed: {statistics.mean(speeds):.2f} km/h")
    print(f"Average Vehicle Count: {statistics.mean(counts):.2f}")
    
    timestamps = sorted([e['timestamp'] for e in events])
    print(f"\nTime Range:")
    print(f"  Start: {timestamps[0]}")
    print(f"  End:   {timestamps[-1]}")

def main():
    parser = argparse.ArgumentParser(description="Inspect generated traffic dataset")
    parser.add_argument("file", type=str, help="Path to the generated dataset (.csv)")
    args = parser.parse_args()
    
    if args.file.endswith('.csv'):
        inspect_csv(args.file)
    else:
        print("Currently only .csv inspection is supported by this simple utility.")

if __name__ == "__main__":
    main()
