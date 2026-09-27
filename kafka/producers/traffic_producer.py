import argparse
import json
import sys
import os
import time
from datetime import datetime, timezone
from confluent_kafka import Producer

# Adjust path for direct execution
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from kafka.config.settings import settings as kafka_settings
from data_generator.schemas.traffic_event import TrafficEvent
from data_generator.generators.traffic_generator import generate_event
from data_generator.generators.location_generator import generate_junctions
from data_generator.generators.sensor_generator import generate_sensors
from data_generator.config.settings import settings as gen_settings

def delivery_report(err, msg):
    """ Called once for each message produced to indicate delivery result. """
    if err is not None:
        print(f"Message delivery failed: {err}")

def produce_from_file(producer, topic, file_path):
    print(f"Reading from JSONL file: {file_path}")
    count = 0
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                if not line.strip(): continue
                
                # Parse to validate
                try:
                    event_data = json.loads(line)
                    event = TrafficEvent(**event_data)
                except Exception as e:
                    print(f"Invalid event in file: {e}")
                    continue

                key = event.sensor_id.encode('utf-8')
                value = event.model_dump_json().encode('utf-8')
                
                producer.produce(topic, key=key, value=value, callback=delivery_report)
                producer.poll(0)
                
                count += 1
                if count % 100 == 0:
                    print(f"Published: {count}")
    except Exception as e:
        print(f"File reading failed: {e}")
        
    producer.flush()
    print(f"Finished. Total published: {count}")
    return count

def produce_live(producer, topic, events_limit, interval):
    print("Starting live generation mode...")
    junctions = generate_junctions(gen_settings.NUM_JUNCTIONS)
    sensors = generate_sensors(gen_settings.NUM_SENSORS, junctions)
    
    count = 0
    try:
        while events_limit == 0 or count < events_limit:
            import random
            sensor = random.choice(sensors)
            current_time = datetime.now(timezone.utc)
            event = generate_event(sensor, current_time)
            
            key = event.sensor_id.encode('utf-8')
            value = event.model_dump_json().encode('utf-8')
            
            producer.produce(topic, key=key, value=value, callback=delivery_report)
            producer.poll(0)
            
            count += 1
            if count % 100 == 0 or interval >= 1.0:
                print(f"Published: {count}")
                
            if interval > 0:
                time.sleep(interval)
                
    except KeyboardInterrupt:
        print("\nLive generation interrupted.")
        
    producer.flush()
    print(f"Finished. Total published: {count}")
    return count

def main():
    parser = argparse.ArgumentParser(description="Smart City Kafka Traffic Producer")
    parser.add_argument("--mode", type=str, choices=["file", "live"], default="file", help="Input mode")
    parser.add_argument("--input", type=str, help="Path to input JSONL file (required for 'file' mode)")
    parser.add_argument("--topic", type=str, default=kafka_settings.KAFKA_TRAFFIC_TOPIC, help="Kafka topic")
    parser.add_argument("--bootstrap-server", type=str, default=kafka_settings.KAFKA_BOOTSTRAP_SERVERS, help="Kafka broker")
    parser.add_argument("--events", type=int, default=0, help="Number of events to generate in live mode (0=infinite)")
    parser.add_argument("--interval", type=float, default=0.0, help="Delay between events in live mode")

    args = parser.parse_args()

    producer_conf = {
        'bootstrap.servers': args.bootstrap_server,
        'client.id': 'smart-city-traffic-producer',
        'acks': 'all',
        'retries': 3
    }
    
    print(f"Connecting to Kafka at {args.bootstrap_server}...")
    try:
        producer = Producer(producer_conf)
        print("Kafka Producer initialized.")
    except Exception as e:
        print(f"Failed to initialize Kafka Producer: {e}")
        sys.exit(1)

    print(f"Target Topic: {args.topic}")
    
    if args.mode == "file":
        if not args.input:
            print("Error: --input file path is required for file mode.")
            sys.exit(1)
        produce_from_file(producer, args.topic, args.input)
    elif args.mode == "live":
        produce_live(producer, args.topic, args.events, args.interval)

if __name__ == "__main__":
    main()
