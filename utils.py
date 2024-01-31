import uuid

APP_NAME = 'toDoApp'
DATABASE_NAME = 'ToDoApp'

LOG_LEVELS_DICT = {
	'NOTSET': 0,
	'DEBUG': 10,
	'INFO': 20,
	'WARNING': 30,
	'ERROR': 40,
	'CRITICAL': 50
}

def generate_uuid():
    """Generate a uuid4 string (e.g. "b906d035-1a4f-4d45-8886-b09e1990c458")"""
    return str(uuid.uuid4())
