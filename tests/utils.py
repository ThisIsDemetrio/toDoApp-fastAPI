from app import error_handling
from app.Client import Client
from app.Logger import Logger
import os
import json
from passlib.context import CryptContext

TEST_MONGODB_URL = "mongodb://localhost:27017"
TEST_DATABASE_NAME = "toDoApp-tests"
TODO_MOCKS_RELATIVE_PATH = 'tests/documents.json'

def get_context_for_tests():
    """Create a context to be passed to the application. Please note this is intended for unit tests only."""
    logger: Logger = Logger('NOTSET').get_logger()
    client: Client = Client(TEST_MONGODB_URL, TEST_DATABASE_NAME)
    pwd_context: CryptContext = CryptContext(schemes=["bcrypt"], deprecated="auto")

    return {
        "client": client, 
        "logger": logger,
        "pwd_context": pwd_context
    }

def get_current_user_for_tests():
    """
    Create an instance of the current user to be passed to the application.
    
    Please note this is intended for unit tests only.
    """
    return {
        "username": "john",
        "email": "john@example.com",
        "disabled": False,
        "hashed_password": "hashed_password"
    }

def open_mock_file(file_name = TODO_MOCKS_RELATIVE_PATH):
    file_path = os.path.join(os.getcwd(), file_name)
    with open(file_path, 'r') as json_file:
        file_content = json.load(json_file)
        
    return file_content

def insert_documents_in_todo_collection(documents, database_name = TEST_DATABASE_NAME):
    client: Client = Client(TEST_MONGODB_URL, database_name)
    client.get_todo_collection().insert_many(documents)

def clear_todo_collection(database_name = TEST_DATABASE_NAME):
    client: Client = Client(TEST_MONGODB_URL, database_name)
    client.get_todo_collection().drop()

def get_todo_document_by_id(document_id, database_name = TEST_DATABASE_NAME):
    client: Client = Client(TEST_MONGODB_URL, database_name)
    return client.get_todo_collection().find_one({"id": document_id})

def assert_ko(error_code, res):
    if error_code not in error_handling.error_codes:
        raise Exception(f'Error code {error_code} does not exist. Verify your test.')
    
    assert res.status_code == 200
    assert res.json()["status"] == "KO"
    assert res.json()["code"] == error_code
