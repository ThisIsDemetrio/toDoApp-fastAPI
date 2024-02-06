from config.Client import Client
from config.Logger import Logger

TEST_MONGODB_URL = "mongodb://localhost:27017"
TEST_DATABASE_NAME = "toDoApp-tests"

def get_context_for_tests():
    """Create a context to be passed to the application. Please note this is intended for unit tests."""
    logger: Logger = Logger('NOTSET').get_logger()
    client: Client = Client(TEST_MONGODB_URL, TEST_DATABASE_NAME)

    return {"client": client, "logger": logger}

def insert_documents_in_todo_collection(documents, database_name = TEST_DATABASE_NAME):
    client: Client = Client(TEST_MONGODB_URL, database_name)
    client.get_todo_collection().insert_many(documents)

def clear_todo_collection(database_name = TEST_DATABASE_NAME):
    client: Client = Client(TEST_MONGODB_URL, database_name)
    client.get_todo_collection().drop()

def get_todo_document_by_id(document_id, database_name = TEST_DATABASE_NAME):
    client: Client = Client(TEST_MONGODB_URL, database_name)
    return client.get_todo_collection().find_one({"id": document_id})
