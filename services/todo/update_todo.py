from app.error_handling import return_error, ErrorModel
from app.Client import Client, ReturnModel
from app.ErrorCode import ErrorCode
from models.Todo import ToDoModel


async def update_todo(
    client: Client, id: str, todo_to_update: ToDoModel
) -> ReturnModel | ErrorModel:
    """
    Update the "todo" document with the "id" included in the request.
    Returns a 404 Exception if the document does not exist.
    """
    collection = client.get_todo_collection()

    result = collection.update_one({"id": id}, {"$set": todo_to_update.model_dump()})
    if result.modified_count == 1:
        return {"status": "OK", "result": id}
    else:
        return return_error(ErrorCode.A01, id=id)
