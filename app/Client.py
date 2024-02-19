from pymongo import MongoClient

class Client:
    def __init__(self, mongo_url: str, database_name: str):
        self.client = MongoClient(mongo_url, connect=True)
        self.database_name = database_name
    
    def get_config_collection(self):
        """Returns the "config" collection"""
        return self.client[self.database_name].get_collection('config')
    
    def get_todo_collection(self):
        """Returns the "todo" collection"""
        return self.client[self.database_name].get_collection('todo')
