def run_incident_analytics(collection):
    pipeline = [
        {
            "$group": {
                "_id": "$incident_status",
                "total_vehicle_count": {"$sum": "$vehicle_count"},
                "average_speed": {"$avg": "$average_speed"},
                "event_count": {"$sum": 1},
                "affected_junctions": {"$addToSet": "$junction_id"},
                "affected_sensors": {"$addToSet": "$sensor_id"}
            }
        },
        {
            "$project": {
                "total_vehicle_count": 1,
                "average_speed": 1,
                "event_count": 1,
                "affected_junctions_count": {"$size": "$affected_junctions"},
                "affected_sensors_count": {"$size": "$affected_sensors"}
            }
        }
    ]
    return list(collection.aggregate(pipeline))
