from app.Client import Client, ReturnModel
from app.error_handling import ErrorModel, return_error
from app.ErrorCode import ErrorCode


async def set_todo_to_not_completed(
    client: Client, username: str, id: str
) -> ReturnModel | ErrorModel:
    """
    Set the "completed" flag on a "todo" document to "False"
    """
    collection = client.get_todo_collection()

    result = collection.update_one(
        {"id": id, "user": username, "completed": True},
        {"$set": {"completed": False}},
    )
    if result.modified_count == 1:
        return {"status": "OK", "result": id}
    else:
        # TODO: Is this error because the todo was already completed, or it has not been found, or the user is wrong?
        return return_error(ErrorCode.C02)
