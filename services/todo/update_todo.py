from app import error_handling
from app.Client import Client
from app.ErrorCode import ErrorCode
from models.Todo import ToDoModel

async def update_todo(client: Client, id: str, todo_to_update: ToDoModel):
    '''
    Update the "todo" document with the "id" included in the request.
    Returns a 404 Exception if the document does not exist.
    '''
    collection = client.get_todo_collection()

    result = collection.update_one({"id": id}, {"$set": todo_to_update.model_dump()})
    if result.modified_count == 1:
        return {"status": "OK", "id": id}
    else:
        return error_handling.return_error(ErrorCode.A01, id=id)
