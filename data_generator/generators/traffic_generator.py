import argparse
import csv
import json
import random
import time
import uuid
import sys
import os
from datetime import datetime, timezone, timedelta

# Adjust path for direct execution
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from data_generator.config.settings import settings
from data_generator.schemas.traffic_event import TrafficEvent
from data_generator.generators.location_generator import generate_junctions
from data_generator.generators.sensor_generator import generate_sensors

def weighted_choice(choices_dict):
    choices = list(choices_dict.keys())
    weights = list(choices_dict.values())
    return random.choices(choices, weights=weights, k=1)[0]

def generate_event(sensor: dict, current_time: datetime) -> TrafficEvent:
    # 1. Weather and Incident
    weather = weighted_choice(settings.WEATHER_PROBABILITIES)
    incident = weighted_choice(settings.INCIDENT_PROBABILITIES)
    
    # 2. Base traffic on time of day (naive simulation)
    hour = current_time.hour
    if 7 <= hour <= 10 or 17 <= hour <= 21:
        base_density = random.choices(["MEDIUM", "HIGH", "SEVERE"], weights=[0.2, 0.6, 0.2])[0]
    elif 10 < hour < 17:
        base_density = random.choices(["LOW", "MEDIUM", "HIGH"], weights=[0.3, 0.5, 0.2])[0]
    else:
        base_density = random.choices(["LOW", "MEDIUM"], weights=[0.8, 0.2])[0]

    # Incidents increase density
    if incident == "major_incident":
        base_density = "SEVERE"
    elif incident == "minor_incident" and base_density == "LOW":
        base_density = "MEDIUM"
        
    # Weather affects density
    if weather in ["rain", "fog"] and base_density in ["MEDIUM", "HIGH"]:
        base_density = "HIGH" if base_density == "MEDIUM" else "SEVERE"

    # 3. Vehicle Count based on density
    if base_density == "LOW":
        count = random.randint(1, 10)
    elif base_density == "MEDIUM":
        count = random.randint(11, 30)
    elif base_density == "HIGH":
        count = random.randint(31, 70)
    else: # SEVERE
        count = random.randint(71, 150)
        
    # 4. Average Speed based on density (km/h)
    if base_density == "LOW":
        speed = random.uniform(40.0, 80.0)
    elif base_density == "MEDIUM":
        speed = random.uniform(25.0, 50.0)
    elif base_density == "HIGH":
        speed = random.uniform(10.0, 30.0)
    else:
        speed = random.uniform(0.0, 15.0)

    # Weather reduces speed
    if weather in ["rain", "fog"]:
        speed *= random.uniform(0.7, 0.9)

    vehicle_type = weighted_choice(settings.VEHICLE_PROBABILITIES)
    
    occupancy = min(1.0, count / 150.0)

    event = TrafficEvent(
        event_id=f"evt_{uuid.uuid4().hex}",
        timestamp=current_time.isoformat(timespec='seconds'),
        sensor_id=sensor["sensor_id"],
        junction_id=sensor["junction_id"],
        lane_id=sensor["lane_id"],
        vehicle_type=vehicle_type,
        vehicle_count=count,
        average_speed=round(speed, 2),
        traffic_density=base_density,
        weather_condition=weather,
        latitude=sensor["latitude"],
        longitude=sensor["longitude"],
        occupancy_rate=round(occupancy, 2),
        road_type=sensor["road_type"],
        direction=sensor["direction"],
        incident_status=incident
    )
    return event

def main():
    parser = argparse.ArgumentParser(description="Smart City Traffic Data Generator")
    parser.add_argument("--events", type=int, default=1000, help="Number of events to generate")
    parser.add_argument("--interval", type=float, default=0.0, help="Interval between events (for streaming mode)")
    parser.add_argument("--output", type=str, help="Output file path (.csv or .jsonl)")
    parser.add_argument("--mode", type=str, choices=["batch", "stream"], default="batch", help="Generation mode")
    parser.add_argument("--seed", type=int, help="Random seed for reproducibility")
    
    args = parser.parse_args()

    if args.seed is not None:
        random.seed(args.seed)

    junctions = generate_junctions(settings.NUM_JUNCTIONS, args.seed)
    sensors = generate_sensors(settings.NUM_SENSORS, junctions, args.seed)

    output_path = args.output
    is_csv = output_path and output_path.endswith('.csv')
    is_jsonl = output_path and output_path.endswith('.jsonl')

    file_handle = None
    csv_writer = None

    if output_path:
        os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
        
        file_handle = open(output_path, 'w', newline='', encoding='utf-8')
        if is_csv:
            fieldnames = list(TrafficEvent.model_fields.keys())
            csv_writer = csv.DictWriter(file_handle, fieldnames=fieldnames)
            csv_writer.writeheader()

    current_time = datetime.now(timezone.utc) - timedelta(days=1)
    
    events_generated = 0
    start_time = time.time()

    try:
        for _ in range(args.events):
            sensor = random.choice(sensors)
            if args.mode == "batch":
                current_time += timedelta(seconds=random.randint(1, 10))
            else:
                current_time = datetime.now(timezone.utc)

            event = generate_event(sensor, current_time)
            
            if file_handle:
                if is_csv:
                    csv_writer.writerow(event.model_dump())
                elif is_jsonl:
                    file_handle.write(event.model_dump_json() + "\n")
            else:
                if args.mode == "stream":
                    print(event.model_dump_json())

            events_generated += 1

            if args.mode == "stream" and args.interval > 0:
                time.sleep(args.interval)
                
    except KeyboardInterrupt:
        print("\nGeneration interrupted by user.")
    finally:
        if file_handle:
            file_handle.close()
            
    if args.mode == "batch":
        duration = time.time() - start_time
        print(f"Generated {events_generated} events in {duration:.2f} seconds.")

if __name__ == "__main__":
    main()
