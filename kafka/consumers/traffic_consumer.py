import argparse
import json
import sys
import os
from confluent_kafka import Consumer, KafkaException

# Adjust path for direct execution
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from kafka.config.settings import settings as kafka_settings
from data_generator.schemas.traffic_event import TrafficEvent

def main():
    parser = argparse.ArgumentParser(description="Smart City Kafka Traffic Consumer")
    parser.add_argument("--topic", type=str, default=kafka_settings.KAFKA_TRAFFIC_TOPIC, help="Kafka topic")
    parser.add_argument("--bootstrap-server", type=str, default=kafka_settings.KAFKA_BOOTSTRAP_SERVERS, help="Kafka broker")
    parser.add_argument("--group-id", type=str, default=kafka_settings.KAFKA_CONSUMER_GROUP, help="Consumer group ID")
    parser.add_argument("--from-beginning", action="store_true", help="Read from beginning (if no previous offset)")

    args = parser.parse_args()

    consumer_conf = {
        'bootstrap.servers': args.bootstrap_server,
        'group.id': args.group_id,
        'auto.offset.reset': 'earliest' if args.from_beginning else 'latest'
    }

    print(f"Connecting to Kafka at {args.bootstrap_server}...")
    try:
        consumer = Consumer(consumer_conf)
        print("Kafka Consumer initialized.")
    except Exception as e:
        print(f"Failed to initialize Kafka Consumer: {e}")
        sys.exit(1)

    print(f"Subscribing to Topic: {args.topic}")
    consumer.subscribe([args.topic])

    print("Waiting for messages... (Press Ctrl+C to stop)")
    count = 0
    try:
        while True:
            msg = consumer.poll(timeout=1.0)
            if msg is None:
                continue
            if msg.error():
                print(f"Consumer error: {msg.error()}")
                continue

            # Process Message
            try:
                raw_value = msg.value().decode('utf-8')
                event_data = json.loads(raw_value)
                
                # Schema Validation
                event = TrafficEvent(**event_data)
                
                count += 1
                if count % 100 == 1 or count < 5:
                    print(f"Received Event: ID={event.event_id}, Sensor={event.sensor_id}, "
                          f"Junction={event.junction_id}, Type={event.vehicle_type}, "
                          f"Count={event.vehicle_count}, Density={event.traffic_density}")
                
            except json.JSONDecodeError as e:
                print(f"Invalid JSON received: {e}")
            except Exception as e:
                print(f"Schema validation failed: {e}")

    except KeyboardInterrupt:
        print("\nConsumer stopped by user.")
    finally:
        consumer.close()
        print(f"Total valid events consumed: {count}")

if __name__ == "__main__":
    main()
