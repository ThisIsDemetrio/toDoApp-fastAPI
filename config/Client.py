from pymongo import MongoClient
from config.Settings import Settings

class Client:
    def __init__(self, settings: Settings):
        self.client = MongoClient(settings.mongo_url, connect=True)
        self.database_name = settings.database_name
    
    def get_config_collection(self):
        return self.client[self.database_name].get_collection('config')
    
    def get_todo_collection(self):
        return self.client[self.database_name].get_collection('todo')
