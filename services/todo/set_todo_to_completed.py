from app.Client import Client
from app.responses.AlreadyCompletedResponse import AlreadyCompletedResponse
from app.responses.SuccessResponse import SuccessResponse


async def set_todo_to_completed(
    client: Client, username: str, id: str
) -> SuccessResponse | AlreadyCompletedResponse:
    """
    Set the "completed" flag on a "todo" document to "True"
    """
    collection = client.get_todo_collection()

    result = collection.update_one(
        {"id": id, "user": username, "completed": False},
        {"$set": {"completed": True}},
    )
    if result.modified_count == 1:
        return SuccessResponse(result=id)
    else:
        # TODO: Is this error because the todo was already completed, or it has not been found, or the user is wrong?
        return AlreadyCompletedResponse(id=id)
