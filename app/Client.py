from pymongo import MongoClient
from pymongo.collection import Collection


class Client:
    def __init__(self, mongo_url: str, database_name: str):
        self.client = MongoClient(mongo_url, connect=True)
        self.database_name = database_name

    def get_config_collection(self) -> Collection:
        """Returns the "config" collection"""
        return self.client[self.database_name].get_collection("config")

    def get_users_collection(self) -> Collection:
        """Returns the "users" collection"""
        return self.client[self.database_name].get_collection("users")

    def get_todo_collection(self) -> Collection:
        """Returns the "todo" collection"""
        return self.client[self.database_name].get_collection("todo")
