import sys
import os
import json

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from mongodb.client.mongo_client import db_client
from mongodb.analytics.event_queries import count_total_events, get_top_junctions_by_volume
from mongodb.analytics.junction_analytics import run_junction_analytics
from mongodb.analytics.sensor_analytics import run_sensor_analytics
from mongodb.analytics.vehicle_analytics import run_vehicle_analytics
from mongodb.analytics.density_analytics import run_density_analytics
from mongodb.analytics.weather_analytics import run_weather_analytics
from mongodb.analytics.incident_analytics import run_incident_analytics

def main():
    db_client.connect()
    if not db_client.check_connection():
        print("MongoDB connection failed. Aborting analytics.")
        sys.exit(1)
        
    coll = db_client.collection
    
    print("=== MONGODB ANALYTICS RUNNER ===")
    
    # Total
    total = count_total_events(coll)
    print(f"Total Unique Events in DB: {total}")
    if total == 0:
        print("No events found. Run import_traffic.py first.")
        sys.exit(0)
        
    print("\n--- Top Junctions by Volume ---")
    top_j = get_top_junctions_by_volume(coll, limit=3)
    for j in top_j:
        print(f"Junction: {j['_id']} | Total Volume: {j['total_volume']}")
        
    # Run full pipelines and optionally export to json
    print("\nRunning Aggregation Pipelines...")
    os.makedirs(os.path.join(os.path.dirname(__file__), '../output'), exist_ok=True)
    
    pipelines = [
        ("junction_analytics", run_junction_analytics),
        ("sensor_analytics", run_sensor_analytics),
        ("vehicle_analytics", run_vehicle_analytics),
        ("density_analytics", run_density_analytics),
        ("weather_analytics", run_weather_analytics),
        ("incident_analytics", run_incident_analytics),
    ]
    
    for name, func in pipelines:
        print(f"Executing: {name} ...")
        res = func(coll)
        out_path = os.path.join(os.path.dirname(__file__), f"../output/{name}.json")
        with open(out_path, 'w', encoding='utf-8') as f:
            json.dump(res, f, indent=2, default=str)
            
    print("\nAll analytics exported to mongodb/output/ successfully.")
    
    db_client.close()

if __name__ == "__main__":
    main()
