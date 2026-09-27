def run_vehicle_analytics(collection):
    pipeline = [
        {
            "$group": {
                "_id": "$vehicle_type",
                "total_vehicle_count": {"$sum": "$vehicle_count"},
                "average_speed": {"$avg": "$average_speed"},
                "event_count": {"$sum": 1}
            }
        },
        {"$sort": {"total_vehicle_count": -1}}
    ]
    return list(collection.aggregate(pipeline))
