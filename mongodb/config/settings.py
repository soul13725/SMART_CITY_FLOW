import os

class MongoSettings:
    MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
    MONGODB_DATABASE = os.getenv("MONGODB_DATABASE", "smart_city")
    MONGODB_COLLECTION = os.getenv("MONGODB_COLLECTION", "traffic_events")
    MONGODB_BATCH_SIZE = int(os.getenv("MONGODB_BATCH_SIZE", "1000"))
    
settings = MongoSettings()
