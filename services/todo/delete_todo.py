from app.Client import Client, ReturnModel
from app.error_handling import ErrorModel, return_error
from app.ErrorCode import ErrorCode


async def delete_todo(
    client: Client, username: str, id: str
) -> ReturnModel | ErrorModel:
    """
    Handle the deletion of a "todo" document
    """
    collection = client.get_todo_collection()

    result = collection.delete_one({"id": id, "user": username})
    if result.deleted_count == 1:
        return {"status": "OK", "result": id}
    else:
        return return_error(ErrorCode.A01, id=id)
