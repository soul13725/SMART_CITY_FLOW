import argparse
import csv
import sys
import os
import pymongo
from pymongo.errors import BulkWriteError

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from mongodb.client.mongo_client import db_client
from mongodb.schemas.traffic_document import validate_and_parse
from mongodb.config.settings import settings

def setup_indexes(collection):
    collection.create_index("event_id", unique=True)
    collection.create_index("timestamp")
    collection.create_index("sensor_id")
    collection.create_index("junction_id")
    collection.create_index("vehicle_type")
    collection.create_index("traffic_density")
    collection.create_index("weather_condition")
    collection.create_index("incident_status")
    collection.create_index([("junction_id", pymongo.ASCENDING), ("timestamp", pymongo.ASCENDING)])

def insert_batch(batch):
    inserted = 0
    duplicates = 0
    try:
        db_client.collection.insert_many(batch, ordered=False)
        inserted += len(batch)
    except BulkWriteError as bwe:
        for err in bwe.details.get('writeErrors', []):
            if err['code'] == 11000: # Duplicate key
                duplicates += 1
        inserted += (len(batch) - duplicates)
    return inserted, duplicates

def import_csv(file_path):
    records_read = 0
    invalid_records = 0
    duplicates = 0
    inserted = 0
    batch = []
    
    db_client.connect()
    if not db_client.check_connection():
        print("MongoDB connection failed. Aborting import.")
        sys.exit(1)
        
    setup_indexes(db_client.collection)

    with open(file_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            records_read += 1
            doc, err = validate_and_parse(row)
            if not doc:
                invalid_records += 1
                continue
                
            batch.append(doc)
            
            if len(batch) >= settings.MONGODB_BATCH_SIZE:
                ins, dup = insert_batch(batch)
                inserted += ins
                duplicates += dup
                batch = []
                
        if batch:
            ins, dup = insert_batch(batch)
            inserted += ins
            duplicates += dup
            
    db_client.close()
    
    print("=== IMPORT STATISTICS ===")
    print(f"Records read: {records_read}")
    print(f"Inserted: {inserted}")
    print(f"Duplicates: {duplicates}")
    print(f"Invalid: {invalid_records}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    args = parser.parse_args()
    import_csv(args.input)
