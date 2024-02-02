from config.Client import Client
from config.Logger import Logger

TEST_MONGODB_URL = "mongodb://localhost:27017"
TEST_DATABASE_NAME = "toDoApp-tests"

def get_context_for_tests():
    """Create a context to be passed to the application. Please note this is intended for unit tests."""
    logger: Logger = Logger('NOTSET').get_logger()
    client: Client = Client(TEST_MONGODB_URL, TEST_DATABASE_NAME)

    return {"client": client, "logger": logger}

def clear_todo_collection(databaseName = TEST_DATABASE_NAME):
    client: Client = Client(TEST_MONGODB_URL, databaseName)
    client.get_todo_collection().drop()
