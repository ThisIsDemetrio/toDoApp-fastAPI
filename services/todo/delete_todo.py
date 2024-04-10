from app.error_handling import return_error, ErrorModel
from app.Client import Client, ReturnModel
from app.ErrorCode import ErrorCode


async def delete_todo(client: Client, id: str) -> ReturnModel | ErrorModel:
    '''
    Handle the deletion of a "todo" document
    '''
    collection = client.get_todo_collection()

    result = collection.delete_one({"id": id})
    if result.deleted_count == 1:
        return {"status": "OK", "result": id}
    else:
        return return_error(ErrorCode.A01, id=id)
