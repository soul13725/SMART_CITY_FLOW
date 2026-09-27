from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError
from mongodb.config.settings import settings

class SmartCityMongoClient:
    def __init__(self):
        self.client = None
        self.db = None
        self.collection = None

    def connect(self):
        self.client = MongoClient(settings.MONGODB_URI, serverSelectionTimeoutMS=2000)
        self.db = self.client[settings.MONGODB_DATABASE]
        self.collection = self.db[settings.MONGODB_COLLECTION]

    def check_connection(self):
        if not self.client:
            self.connect()
        try:
            self.client.admin.command('ping')
            return True
        except (ConnectionFailure, ServerSelectionTimeoutError):
            return False

    def close(self):
        if self.client:
            self.client.close()

db_client = SmartCityMongoClient()
