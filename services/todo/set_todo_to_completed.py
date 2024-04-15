from app.error_handling import return_error, ErrorModel
from app.Client import Client, ReturnModel
from app.ErrorCode import ErrorCode


async def set_todo_to_completed(client: Client, id: str) -> ReturnModel | ErrorModel:
    """
    Set the "completed" flag on a "todo" document to "True"
    """
    collection = client.get_todo_collection()

    result = collection.update_one(
        {"id": id, "completed": False}, {"$set": {"completed": True}}
    )
    if result.modified_count == 1:
        return {"status": "OK", "result": id}
    else:
        # TODO: Is this error because the todo was already completed, or it has not been found?
        return return_error(ErrorCode.C01)
