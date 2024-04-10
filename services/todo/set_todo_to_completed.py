from app import error_handling
from app.Client import Client
from app.ErrorCode import ErrorCode

async def set_todo_to_completed(client: Client, id: str):
    '''
    Set the "completed" flag on a "todo" document to "True"
    '''
    collection = client.get_todo_collection()

    result = collection.update_one({"id":id, "completed": False}, {"$set": {"completed": True}})   
    if result.modified_count == 1:
        return {"status": "OK", "id": id}
    else:
        # TODO: Is this error because the todo was already completed, or it has not been found?
        return error_handling.return_error(ErrorCode.C01)
