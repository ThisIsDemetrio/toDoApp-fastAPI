from app import error_handling
from app.Client import Client

async def set_todo_to_not_completed(client: Client, id: str):
    '''
    Set the "completed" flag on a note to "False"
    '''
    collection = client.get_todo_collection()

    result = collection.update_one({"id":id, "completed": True}, {"$set": {"completed": False}})   
    if result.modified_count == 1:
        return {"status": "OK", "id": id}
    else:
        # TODO: Is this error because the note was already not completed, or it has not been found?
        return error_handling.return_error(error_handling.C02)
