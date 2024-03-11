import json
import os
from app.Client import Client
from tests.utils import TEST_DATABASE_NAME, TEST_MONGODB_URL

USERS_MOCKS_RELATIVE_PATH = 'tests/auth/users.json'

def clear_users_collection(database_name = TEST_DATABASE_NAME):
    client: Client = Client(TEST_MONGODB_URL, database_name)
    client.get_users_collection().drop()

def open_mock_file(file_name = USERS_MOCKS_RELATIVE_PATH):
    file_path = os.path.join(os.getcwd(), file_name)
    with open(file_path, 'r') as json_file:
        file_content = json.load(json_file)
        
    return file_content

def insert_documents_in_users_collection(documents, database_name = TEST_DATABASE_NAME):
    client: Client = Client(TEST_MONGODB_URL, database_name)
    client.get_users_collection().insert_many(documents)