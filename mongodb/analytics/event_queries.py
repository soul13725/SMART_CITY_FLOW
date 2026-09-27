def count_total_events(collection):
    return collection.count_documents({})

def count_events_by_junction(collection, junction_id):
    return collection.count_documents({"junction_id": junction_id})

def get_top_junctions_by_volume(collection, limit=5):
    pipeline = [
        {"$group": {"_id": "$junction_id", "total_volume": {"$sum": "$vehicle_count"}}},
        {"$sort": {"total_volume": -1}},
        {"$limit": limit}
    ]
    return list(collection.aggregate(pipeline))
    
def get_top_sensors_by_volume(collection, limit=5):
    pipeline = [
        {"$group": {"_id": "$sensor_id", "total_volume": {"$sum": "$vehicle_count"}}},
        {"$sort": {"total_volume": -1}},
        {"$limit": limit}
    ]
    return list(collection.aggregate(pipeline))
