def run_weather_analytics(collection):
    pipeline = [
        {
            "$group": {
                "_id": "$weather_condition",
                "total_vehicle_count": {"$sum": "$vehicle_count"},
                "average_speed": {"$avg": "$average_speed"},
                "average_occupancy": {"$avg": "$occupancy_rate"},
                "event_count": {"$sum": 1}
            }
        }
    ]
    return list(collection.aggregate(pipeline))
