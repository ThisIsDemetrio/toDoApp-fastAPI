from app.Client import Client, ReturnModel
from app.error_handling import ErrorModel, return_error
from app.ErrorCode import ErrorCode


async def get_todo_by_id(
    client: Client, username: str, id: str
) -> ReturnModel | ErrorModel:
    """
    Returns the "todo" document with a specific "id" passed in query string.
    Returns a 404 exception if the document is not found.
    """
    collection = client.get_todo_collection()
    item = collection.find_one({"id": id, "user": username}, {"_id": 0})
    if item:
        return {"status": "OK", "result": item}
    else:
        return return_error(ErrorCode.A01, id=id)
