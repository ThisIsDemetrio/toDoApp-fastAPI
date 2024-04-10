from app import error_handling
from app.Client import Client
from app.ErrorCode import ErrorCode


async def delete_todo(client: Client, id: str):
    '''
    Handle the deletion of a "todo" document
    '''
    collection = client.get_todo_collection()

    result = collection.delete_one({"id": id})
    if result.deleted_count == 1:
        return {"status": "OK"}
    else:
        return error_handling.return_error(ErrorCode.A01, id=id)
