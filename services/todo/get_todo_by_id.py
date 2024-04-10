from fastapi import HTTPException
from app import error_handling
from app.Client import Client
from app.ErrorCode import ErrorCode

async def get_todo_by_id(client: Client, id: str):
    '''
    Returns the "todo" document with a specific "id" passed in query string.
    Returns a 404 exception if the document is not found.
    '''
    collection = client.get_todo_collection()
    item = collection.find_one({"id": id})
    if item:
        return item
    else:
        return error_handling.return_error(ErrorCode.A01, id=id)
