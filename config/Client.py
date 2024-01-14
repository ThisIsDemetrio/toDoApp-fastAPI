from pymongo import MongoClient
from config.Settings import Settings
from utils import DATABASE_NAME


class Client:
    def __init__(self, settings: Settings):
        self.client = MongoClient(settings.mongo_url, connect=True)
    
    def get_config_collection(self):
        return self.client[DATABASE_NAME].get_collection('config')
    
    def get_todo_collection(self):
        return self.client[DATABASE_NAME].get_collection('todo')