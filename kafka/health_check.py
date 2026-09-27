import sys
import os
from confluent_kafka.admin import AdminClient

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from kafka.config.settings import settings

def main():
    print(f"Checking Kafka connectivity at {settings.KAFKA_BOOTSTRAP_SERVERS}...")
    
    admin = AdminClient({'bootstrap.servers': settings.KAFKA_BOOTSTRAP_SERVERS})
    
    try:
        # Request metadata with a short timeout to check connectivity
        metadata = admin.list_topics(timeout=3.0)
        print("SUCCESS: Connected to Kafka Broker.")
        
        topic = settings.KAFKA_TRAFFIC_TOPIC
        if topic in metadata.topics:
            print(f"SUCCESS: Topic '{topic}' exists. Partitions: {len(metadata.topics[topic].partitions)}")
        else:
            print(f"WARNING: Topic '{topic}' not found on broker.")
            
    except Exception as e:
        print(f"FAILED: Could not connect to Kafka Broker. Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
